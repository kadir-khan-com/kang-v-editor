"""kang.py fetch-openverse: Openverse (api.openverse.org/v1/images, anonymous, no key) -> assets folder + CREDITS.

Rules (user 2026-11-03): licences by, by-sa, cc0, pdm only (no NC, no ND); min width 1600 (configurable);
creator / source / licence_url recorded; place check: a result whose title or tags name another place (Mathura,
Delhi 'Dwarka sector', DSS Academy, Vrindavan ... config/stock_sources.json wrong_places) is rejected; a result
must also carry a Dwarka-area cue (openverse.require_any). Downloads are de-duplicated against the existing pool
by sha256 AND perceptual hash (dHash), so a Flickr copy of a Commons photo is not added twice.
Default label 'representative'; 'exact' is decided later per beat (same place as the shot), never here.
Anonymous API: page_size <= 20, responses cached 24 h on disk, polite pause between calls.
"""
from __future__ import annotations

import hashlib
import json
import time
import urllib.parse
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence

from . import stock_common as SC

LIC_NAME = {"by": "CC BY", "by-sa": "CC BY-SA", "cc0": "CC0", "pdm": "Public Domain Mark"}
DEFAULT_REQUIRE = ["dwarka", "dwaraka", "dwarika", "dwarkadhish", "dwarkadheesh", "dwarakadheesh", "nageshwar",
                   "nageshvar", "shivrajpur", "gomti", "gomati", "okha", "bhadkeshwar", "rukmini", "beyt", "bet dwarka"]


def query_url(q: str, cfg: Dict[str, Any], page: int = 1) -> str:
    oc = cfg["openverse"]
    params = {"q": q, "license": ",".join(oc.get("licences", LIC_NAME)), "page_size": str(min(20, oc.get("page_size", 20))),
              "page": str(page)}
    if oc.get("size"):
        params["size"] = oc["size"]
    return oc.get("api", "https://api.openverse.org/v1/images/") + "?" + urllib.parse.urlencode(params)


def parse_results(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    out = []
    for r in data.get("results", []) or []:
        lic = (r.get("license") or "").lower()
        ver = r.get("license_version") or ""
        out.append({"id": r.get("id"), "title": r.get("title") or "", "creator": r.get("creator") or "",
                    "creator_url": r.get("creator_url") or "", "license": lic, "license_version": ver,
                    "licence": (LIC_NAME.get(lic, lic.upper()) + (f" {ver}" if ver and lic not in ("pdm", "cc0") else "")).strip(),
                    "licence_url": r.get("license_url") or "", "source": r.get("source") or "",
                    "provider": r.get("provider") or "", "source_page": r.get("foreign_landing_url") or "",
                    "url": r.get("url") or "", "width": r.get("width") or 0, "height": r.get("height") or 0,
                    "filetype": (r.get("filetype") or "").lower(), "mature": bool(r.get("mature")),
                    "tags": [t.get("name", "") for t in (r.get("tags") or []) if isinstance(t, dict)],
                    "attribution": r.get("attribution") or "", "detail_url": r.get("detail_url") or ""})
    return out


def check(c: Dict[str, Any], cfg: Dict[str, Any]) -> Optional[str]:
    """None = keep; else the reject reason (licence, size, mature, wrong place, no Dwarka cue, eye reject)."""
    oc = cfg["openverse"]
    if c["license"] not in oc.get("licences", list(LIC_NAME)):
        return f"licence {c['license'] or 'unknown'} not in by/by-sa/cc0/pdm"
    if (c.get("width") or 0) < oc.get("min_width", 1600):
        return f"width {c.get('width')} < {oc.get('min_width', 1600)}"
    if c.get("mature"):
        return "mature flag"
    if c.get("filetype") and c["filetype"] not in ("jpg", "jpeg", "png"):
        return f"filetype {c['filetype']}"
    text = c["title"] + " " + " ".join(c.get("tags", []))
    why = SC.text_reject(text, cfg, people=True, landmarks=True)
    if why:
        return why
    if not SC.find_terms(text, oc.get("require_any", DEFAULT_REQUIRE)):
        return "no Dwarka-area cue in title/tags"
    eye = cfg.get("eye_rejects", {}).get(f"openverse:{c['id']}")
    if eye:
        return "eye check: " + eye
    return None


def download_url(c: Dict[str, Any], cfg: Dict[str, Any]) -> str:
    """Wikimedia originals are throttled: take the standard 1920 px thumbnail when the original is wider."""
    import re
    tw = cfg["openverse"].get("wikimedia_thumb_width", 1920)
    u = c["url"]
    m = re.match(r"(https://upload\.wikimedia\.org/wikipedia/commons)/(\w/\w\w)/([^/?]+)$", u)
    if m and (c.get("width") or 0) > tw and "/thumb/" not in u:
        base, h, name = m.groups()
        return f"{base}/thumb/{h}/{name}/{tw}px-{name}"
    return u


def load_seeds(seed_dir: Optional[str | Path]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    if seed_dir and Path(seed_dir).is_dir():
        for p in sorted(Path(seed_dir).glob("openverse_*.json")):
            d = json.loads(p.read_text(encoding="utf-8"))
            out[d["query"]] = d["data"]
    return out


def search(q: str, cfg: Dict[str, Any], get: Callable[[str], bytes], cache: SC.JsonCache,
           pause: Callable[[], None] = lambda: None, pages: int = 1,
           seeds: Optional[Dict[str, Dict[str, Any]]] = None) -> Dict[str, Any]:
    res: List[Dict[str, Any]] = []
    status: List[Any] = []
    total = None
    for page in range(1, pages + 1):
        url = query_url(q, cfg, page)
        data = cache.get(url)
        if data is None:
            try:
                raw = get(url)
                data = json.loads(raw.decode("utf-8"))
                status.append(200)
            except Exception as exc:  # HTTP error or Cloudflare HTML page
                status.append(getattr(exc, "code", None) or type(exc).__name__)
                if seeds and q in seeds and page == 1:
                    data = seeds[q]
                    status.append("seed_webfetch")
                else:
                    break
            if status[-1] == 200:  # seeds are never cached (provenance stays visible on every run)
                cache.put(url, data)
            pause()
        else:
            status.append("cache")
        total = data.get("result_count", total)
        res += parse_results(data)
        if page >= int(data.get("page_count") or 1):
            break
    return {"query": q, "results": res, "result_count": total, "http": status}


def _write_credits(out: Path, credits: List[Dict[str, Any]]) -> None:
    (out / "CREDITS.json").write_text(json.dumps(credits, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    lines = ["Openverse credits (rights recorded, NOT cleared). Licence filter: CC BY, CC BY-SA, CC0, PDM only."]
    for c in credits:
        lines.append(f"{c['file']}: \"{c['title']}\" by {c.get('author') or 'unknown'}"
                     f"{(' (' + c['author_url'] + ')') if c.get('author_url') else ''}, {c['licence']}"
                     f" ({c.get('licence_url', '')}), source {c.get('provider', '')}: {c['source_page']}"
                     f" [via Openverse {c['openverse_id']}] [{c.get('label', 'representative')}]")
    (out / "CREDITS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def fetch(queries: Sequence[Dict[str, Any]], out_dir: str | Path, *, cfg: Optional[Dict[str, Any]] = None,
          get: Optional[Callable[[str], bytes]] = None, pool_dirs: Sequence[str | Path] = (),
          dry_run: bool = False, pause_s: Optional[float] = None, max_errors: int = 4,
          sleep: Callable[[float], None] = time.sleep, hash_cache: Optional[str | Path] = None,
          seed_dir: Optional[str | Path] = None, known_titles: Sequence[str] = ()) -> Dict[str, Any]:
    cfg = cfg or SC.load_cfg()
    oc = cfg["openverse"]
    get = get or SC.http_get
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    cache = SC.JsonCache(out / "_cache" / "openverse", oc.get("cache_ttl_s", 86400))
    ps = oc.get("pause_s", 3.0) if pause_s is None else pause_s
    pause = (lambda: sleep(ps)) if ps else (lambda: None)
    cj = out / "CREDITS.json"
    credits: List[Dict[str, Any]] = json.loads(cj.read_text(encoding="utf-8")) if cj.exists() else []
    seen_ids = {c.get("openverse_id") for c in credits}
    shas = SC.pool_shas(pool_dirs)
    shas.update({c["sha256"]: f"{out.name}/{c['file']}" for c in credits if c.get("sha256")})
    hashes = SC.pool_hashes(pool_dirs, hash_cache) if pool_dirs else {}
    hashes.update({f"{out.name}/{c['file']}": int(c["dhash"], 16) for c in credits if c.get("dhash")})
    min_w = oc.get("min_width", 1600)
    known = {SC.norm_text(t.replace("File:", "").rsplit(".", 1)[0]) for t in known_titles if t}
    report: List[Dict[str, Any]] = []
    rejected: List[Dict[str, Any]] = []
    got: List[Dict[str, Any]] = []
    errors: List[Dict[str, Any]] = []
    http: Dict[str, Any] = {}
    for q in queries:
        scene, query, want = q.get("scene", ""), q["query"], int(q.get("count", 3))
        sr = search(query, cfg, get, cache, pause, seeds=load_seeds(seed_dir if seed_dir is not None else out / "_seed"))
        http[query] = sr["http"]
        n_keep = 0
        n = 0
        for c in sr["results"]:
            if c["id"] in seen_ids:
                continue
            why = check(c, cfg)
            if why:
                rejected.append({"scene": scene, "query": query, "openverse_id": c["id"], "title": c["title"],
                                 "source_page": c["source_page"], "reason": why, "stage": "metadata"})
                continue
            if c.get("source") == "wikimedia" and SC.norm_text(c["title"]) in known:
                rejected.append({"scene": scene, "query": query, "openverse_id": c["id"], "title": c["title"],
                                 "source_page": c["source_page"], "reason": "same Commons file already in the KANG pool",
                                 "stage": "title"})
                continue
            n_keep += 1
            if n >= want:
                continue
            seen_ids.add(c["id"])
            if dry_run:
                got.append({"scene": scene, "title": c["title"], "openverse_id": c["id"]})
                n += 1
                continue
            try:
                data = get(download_url(c, cfg))
                pause()
            except Exception as exc:
                errors.append({"openverse_id": c["id"], "url": c["url"], "error": str(getattr(exc, "code", exc))[:120]})
                if len(errors) >= max_errors:
                    break
                continue
            sha = hashlib.sha256(data).hexdigest()
            if sha in shas:
                rejected.append({"scene": scene, "query": query, "openverse_id": c["id"], "title": c["title"],
                                 "source_page": c["source_page"], "reason": f"same bytes as {shas[sha]}", "stage": "sha256"})
                continue
            import io
            from PIL import Image
            try:
                im = Image.open(io.BytesIO(data))
                im.load()
            except Exception as exc:
                rejected.append({"scene": scene, "query": query, "openverse_id": c["id"], "title": c["title"],
                                 "source_page": c["source_page"], "reason": f"not an image ({exc})"[:120], "stage": "download"})
                continue
            if im.width < min_w:
                rejected.append({"scene": scene, "query": query, "openverse_id": c["id"], "title": c["title"],
                                 "source_page": c["source_page"], "reason": f"downloaded width {im.width} < {min_w}",
                                 "stage": "download"})
                continue
            h = SC.dhash_image(im)
            dup = SC.near_duplicate(h, hashes)
            if dup:
                rejected.append({"scene": scene, "query": query, "openverse_id": c["id"], "title": c["title"],
                                 "source_page": c["source_page"], "reason": f"near-duplicate of {dup}", "stage": "dhash"})
                continue
            n += 1
            ext = ".png" if (im.format or "").upper() == "PNG" else ".jpg"
            name = f"OV_{scene + '_' if scene else ''}{len(credits) + 1:03d}_{SC.slug(c['title'])}{ext}"
            (out / name).write_bytes(data)
            rec = {"file": name, "source": "openverse", "openverse_id": c["id"], "scene": scene, "query": query,
                   "title": c["title"], "author": c["creator"], "author_url": c["creator_url"], "licence": c["licence"],
                   "licence_code": c["license"], "licence_url": c["licence_url"], "provider": c["source"] or c["provider"],
                   "source_page": c["source_page"], "downloaded": c["url"], "tags": c["tags"][:30],
                   "width": im.width, "height": im.height, "sha256": sha, "dhash": f"{h:016x}",
                   "label": "representative", "rights_status": "recorded_not_cleared",
                   "attribution": c.get("attribution", "")}
            credits.append(rec)
            shas[sha] = f"{out.name}/{name}"
            hashes[f"{out.name}/{name}"] = h
            got.append(rec)
            _write_credits(out, credits)
        report.append({"scene": scene, "query": query, "result_count": sr["result_count"], "returned": len(sr["results"]),
                       "passed_filters": n_keep, "downloaded": n, "http": sr["http"]})
        if len(errors) >= max_errors:
            break
    if credits and not dry_run:
        _write_credits(out, credits)
    (out / "rejected.json").write_text(json.dumps(rejected, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (out / "fetch_report.json").write_text(json.dumps({"queries": report, "errors": errors, "cache_hits": cache.hits,
                                                      "cache_misses": cache.misses}, ensure_ascii=False, indent=1) + "\n",
                                           encoding="utf-8")
    blocked = [q for q, st in http.items() if st and st[-1] not in (200, "cache", "seed_webfetch")]
    seeded = [q for q, st in http.items() if "seed_webfetch" in st]
    status = "FAIL" if (blocked and len(blocked) == len(http)) else ("WARN" if (blocked or errors or seeded) else "PASS")
    reasons: Dict[str, int] = {}
    for r in rejected:
        k = r["reason"].split(":")[0].split(" ")[0] if not r["reason"].startswith("wrong place") else "wrong place"
        reasons[k] = reasons.get(k, 0) + 1
    return {"status": status, "fetched": len(got), "rejected": len(rejected), "reject_reasons": reasons,
            "errors": errors, "http": http, "blocked_queries": blocked, "seeded_queries": seeded, "out": str(out), "queries": report,
            "credits": len(credits)}
