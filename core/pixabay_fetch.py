"""kang.py fetch-pixabay: Pixabay videos (and images) for GENERIC beats -> assets folder + CREDITS.

Auth: the API key is saved in the user's vault and registered as connect_service 'pixabay' on host pixabay.com.
The request URL carries the placeholder key=__SAVED_KEY__; the egress proxy puts the real key in on the wire.
The key never appears in code, logs, caches or CREDITS (cached URLs keep the placeholder).

Pixabay API terms followed: <= 100 requests / 60 s (sliding-window limiter), responses cached 24 h on disk,
no systematic mass download (only the top few candidates per scene query, after metadata + eye checks), files are
downloaded (never hotlinked). Licence = Pixabay Content License (not Creative Commons), recorded separately;
credit given anyway (user name + page URL).

User rule: Pixabay / generic stock is 'representative' ONLY, never 'exact'. Generic queries only (sea waves, boat,
sky, road / train / auto rickshaw India ...); results naming other places (Kuwait souq, Alibaug Mumbai, ISKCON
Bangalore, Kyoto ...), recognisable landmarks, identifiable-person cues or AI-generated media are rejected.
Videos: prefer the 1920-wide rendition, 4-15 s.
"""
from __future__ import annotations

import hashlib
import json
import time
import urllib.parse
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence

from . import stock_common as SC

LICENCE = "Pixabay Content License"
LICENCE_URL = "https://pixabay.com/service/license-summary/"


def query_url(q: str, cfg: Dict[str, Any], kind: str = "video", page: int = 1) -> str:
    pc = cfg["pixabay"]
    base = pc["api_videos"] if kind == "video" else pc["api_images"]
    params = {"q": q[:100], "per_page": str(max(3, min(200, pc.get("per_page", 20)))), "page": str(page),
              "safesearch": "true" if pc.get("safesearch", True) else "false"}
    if kind == "image":
        params.update(image_type="photo", orientation="horizontal", min_width=str(pc.get("image_min_width", 1600)))
    # key first, exactly as connected: base?key=__SAVED_KEY__&...
    return f"{base}?key={pc.get('key_placeholder', '__SAVED_KEY__')}&" + urllib.parse.urlencode(params)


def parse_hits(data: Dict[str, Any], kind: str = "video") -> List[Dict[str, Any]]:
    out = []
    for h in data.get("hits", []) or []:
        rec = {"id": h.get("id"), "kind": kind, "page_url": h.get("pageURL", ""), "tags": h.get("tags", ""),
               "user": h.get("user", ""), "user_id": h.get("user_id"), "user_url": f"https://pixabay.com/users/{h.get('user_id')}/",
               "ai": bool(h.get("isAiGenerated")), "low_quality": bool(h.get("isLowQuality")),
               "downloads": h.get("downloads", 0), "likes": h.get("likes", 0)}
        if kind == "video":
            vs = h.get("videos") or {}
            big = max((v for v in vs.values() if isinstance(v, dict) and v.get("url")),
                      key=lambda v: (v.get("width") or 0), default={})
            pick = next((vs[k] for k in ("large", "medium") if vs.get(k, {}).get("width", 0) == 1920 and vs[k].get("url")), None)
            pick = pick or next((v for v in sorted(vs.values(), key=lambda v: v.get("width") or 0)
                                 if isinstance(v, dict) and (v.get("width") or 0) >= 1920 and v.get("url")), None)
            rec.update(duration=h.get("duration") or 0, width=(pick or big).get("width") or 0,
                       height=(pick or big).get("height") or 0, url=(pick or {}).get("url", ""),
                       size=(pick or {}).get("size", 0), thumb=(pick or big).get("thumbnail", "") or
                       (vs.get("tiny") or {}).get("thumbnail", ""), max_width=big.get("width") or 0)
        else:
            rec.update(width=h.get("imageWidth") or 0, height=h.get("imageHeight") or 0,
                       url=h.get("largeImageURL", ""), thumb=h.get("webformatURL", ""), duration=None)
        out.append(rec)
    return out


def check(c: Dict[str, Any], cfg: Dict[str, Any]) -> Optional[str]:
    pc = cfg["pixabay"]
    if c.get("ai"):
        return "AI-generated (fake imagery not allowed)"
    if c.get("low_quality"):
        return "flagged low quality"
    why = SC.text_reject(c.get("tags", ""), cfg, people=True, landmarks=True)
    if why:
        return why
    if c["kind"] == "video":
        if not c.get("url") or (c.get("width") or 0) < pc.get("video_min_width", 1920):
            return f"no >= {pc.get('video_min_width', 1920)} px rendition (max {c.get('max_width')})"
        if (c.get("duration") or 0) > pc.get("video_max_duration", 30):
            return f"duration {c.get('duration')} s > {pc.get('video_max_duration', 30)} s"
        if (c.get("duration") or 0) < 3:
            return f"duration {c.get('duration')} s < 3 s"
    else:
        if (c.get("width") or 0) < pc.get("image_min_width", 1600):
            return f"width {c.get('width')} < {pc.get('image_min_width', 1600)}"
    eye = cfg.get("eye_rejects", {}).get(f"pixabay:{c['id']}")
    if eye:
        return "eye check: " + eye
    return None


def rank(cands: List[Dict[str, Any]], cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
    lo, hi = cfg["pixabay"].get("video_pref_duration", [4, 15])

    def key(c):
        d = c.get("duration") or 0
        off = 0 if lo <= d <= hi else (lo - d if d < lo else d - hi)
        return (off, -(c.get("downloads") or 0))
    return sorted(cands, key=key)


class Client:
    """Rate-limited (<= n / 60 s), cached (24 h) API client. Records HTTP status per request."""

    def __init__(self, cfg: Dict[str, Any], cache_dir: str | Path, get: Optional[Callable[[str], bytes]] = None,
                 limiter: Optional[SC.RateLimiter] = None):
        pc = cfg["pixabay"]
        self.cfg = cfg
        self.get = get or (lambda u: SC.http_get(u, retries=1))
        self.cache = SC.JsonCache(cache_dir, pc.get("cache_ttl_s", 86400))
        self.limiter = limiter or SC.RateLimiter(int(pc.get("max_requests_per_60s", 100)) - 5, 60.0)
        self.requests = 0
        self.http: List[Any] = []

    def search(self, q: str, kind: str = "video") -> Dict[str, Any]:
        url = query_url(q, self.cfg, kind)
        data = self.cache.get(url)
        if data is not None:
            self.http.append("cache")
            return {"ok": True, "http": "cache", "hits": parse_hits(data, kind), "total": data.get("totalHits")}
        self.limiter.wait()
        self.requests += 1
        try:
            raw = self.get(url)
        except Exception as exc:
            code = getattr(exc, "code", None) or type(exc).__name__
            self.http.append(code)
            return {"ok": False, "http": code, "hits": [], "error": str(exc)[:160]}
        try:
            data = json.loads(raw.decode("utf-8"))
        except Exception:
            self.http.append("non_json")
            return {"ok": False, "http": "non_json", "hits": [], "error": raw[:160].decode("utf-8", "replace")}
        self.http.append(200)
        self.cache.put(url, data)
        return {"ok": True, "http": 200, "hits": parse_hits(data, kind), "total": data.get("totalHits")}


def verify_auth(cfg: Optional[Dict[str, Any]] = None, get: Optional[Callable[[str], bytes]] = None,
                kind: str = "video") -> Dict[str, Any]:
    """ONE uncached request; reports the HTTP status (200 = auth works). Never prints the key."""
    cfg = cfg or SC.load_cfg()
    get = get or (lambda u: SC.http_get(u, retries=0))
    url = query_url("sea waves", cfg, kind)
    try:
        data = json.loads(get(url).decode("utf-8"))
        return {"kind": kind, "http": 200, "auth": "PASS", "total_hits": data.get("totalHits")}
    except Exception as exc:
        code = getattr(exc, "code", None)
        body = ""
        try:
            body = exc.read().decode("utf-8", "replace")[:160]  # type: ignore[attr-defined]
        except Exception:
            pass
        return {"kind": kind, "http": code or type(exc).__name__, "auth": "FAIL", "detail": body or str(exc)[:160]}


def _write_credits(out: Path, credits: List[Dict[str, Any]]) -> None:
    (out / "CREDITS.json").write_text(json.dumps(credits, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    lines = [f"Pixabay credits. Licence: {LICENCE} ({LICENCE_URL}) - NOT Creative Commons; credit given anyway.",
             "Label: representative (generic stock, never the narrated place)."]
    for c in credits:
        lines.append(f"{c['file']}: Pixabay {c['kind']} {c['pixabay_id']} by {c['author']} ({c['author_url']}), "
                     f"{c['licence']}, {c['source_page']} [tags: {c['tags']}]")
    (out / "CREDITS.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def fetch(queries: Sequence[Dict[str, Any]], out_dir: str | Path, *, cfg: Optional[Dict[str, Any]] = None,
          get: Optional[Callable[[str], bytes]] = None, download_get: Optional[Callable[[str], bytes]] = None,
          per_query: Optional[int] = None, thumbs_only: bool = False, pool_dirs: Sequence[str | Path] = (),
          client: Optional[Client] = None, max_errors: int = 4) -> Dict[str, Any]:
    """queries: [{theme, query, kind video|image}]. thumbs_only: list candidates + save thumbnails for the eye
    check (no media download). Otherwise downloads the top `per_query` passing candidates per query."""
    cfg = cfg or SC.load_cfg()
    pc = cfg["pixabay"]
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    cl = client or Client(cfg, out / "_cache" / "pixabay", get=get)
    dget = download_get or (lambda u: SC.http_get(u, retries=2, timeout=180, direct="cdn.pixabay.com" in u))
    want = per_query or pc.get("download_per_query", 3)
    cj = out / "CREDITS.json"
    credits: List[Dict[str, Any]] = json.loads(cj.read_text(encoding="utf-8")) if cj.exists() else []
    have = {(c["kind"], c["pixabay_id"]) for c in credits}
    shas = SC.pool_shas(pool_dirs)
    shas.update({c["sha256"]: c["file"] for c in credits if c.get("sha256")})
    seen: set = set(have)
    rejected, cands_out, got, errors, report = [], [], [], [], []
    for q in queries:
        kind = q.get("kind", "video")
        r = cl.search(q["query"], kind)
        if not r["ok"]:
            report.append({"theme": q.get("theme"), "query": q["query"], "kind": kind, "http": r["http"], "error": r.get("error")})
            errors.append({"query": q["query"], "http": r["http"], "error": r.get("error")})
            if len(errors) >= max_errors:
                break
            continue
        keep = []
        for c in r["hits"]:
            if (kind, c["id"]) in seen and (kind, c["id"]) not in have:
                continue  # same hit from another query of this run
            why = check(c, cfg)
            if why:
                rejected.append({"pixabay_id": c["id"], "kind": kind, "query": q["query"], "theme": q.get("theme"),
                                 "tags": c["tags"], "page_url": c["page_url"], "reason": why, "stage": "metadata"})
                continue
            keep.append(c)
        keep = rank(keep, cfg)
        n = 0
        need_ok = (not thumbs_only) and pc.get("require_eye_ok")
        if need_ok:  # download only what the agent already looked at (thumbnail sheet)
            keep = [c for c in keep if f"pixabay:{c['id']}" in cfg.get("eye_ok", {})]
        for c in keep:
            if n >= want:
                break
            if (kind, c["id"]) in seen:
                if (kind, c["id"]) in have:
                    n += 1
                continue
            seen.add((kind, c["id"]))
            n += 1
            row = {"pixabay_id": c["id"], "kind": kind, "theme": q.get("theme"), "query": q["query"], "tags": c["tags"],
                   "duration": c.get("duration"), "width": c.get("width"), "page_url": c["page_url"], "user": c["user"],
                   "thumb": c.get("thumb"), "size": c.get("size")}
            if thumbs_only:
                if c.get("thumb"):
                    tdir = out / "_thumbs"
                    tdir.mkdir(exist_ok=True)
                    tp = tdir / f"{kind}_{c['id']}.jpg"
                    if not tp.is_file():
                        try:
                            tp.write_bytes(dget(c["thumb"]))
                        except Exception as exc:
                            errors.append({"pixabay_id": c["id"], "thumb_error": str(exc)[:120]})
                    row["thumb_file"] = str(tp)
                cands_out.append(row)
                continue
            try:
                data = dget(c["url"])
            except Exception as exc:
                errors.append({"pixabay_id": c["id"], "error": str(getattr(exc, "code", exc))[:120]})
                n -= 1
                if len(errors) >= max_errors:
                    break
                continue
            sha = hashlib.sha256(data).hexdigest()
            if sha in shas:
                rejected.append({**row, "reason": f"same bytes as {shas[sha]}", "stage": "sha256"})
                n -= 1
                continue
            ext = ".mp4" if kind == "video" else ".jpg"
            name = f"PXB_{'V' if kind == 'video' else 'I'}_{c['id']}_{SC.slug(c['tags'], 30)}{ext}"
            (out / name).write_bytes(data)
            shas[sha] = name
            rec = {"file": name, "source": "pixabay", "kind": kind, "pixabay_id": c["id"], "theme": q.get("theme"),
                   "query": q["query"], "title": f"Pixabay {kind} {c['id']}: {c['tags']}", "tags": c["tags"],
                   "author": c["user"], "author_url": c["user_url"], "licence": LICENCE, "licence_url": LICENCE_URL,
                   "licence_family": "PIXABAY_CL", "source_page": c["page_url"], "duration": c.get("duration"),
                   "width": c.get("width"), "height": c.get("height"), "sha256": sha, "label": "representative",
                   "rights_status": "recorded_not_cleared",
                   "licence_note": "Pixabay Content License: free use incl. commercial; no sale/redistribution as-is; "
                                   "do not imply endorsement by depicted people/brands. Not CC."}
            credits.append(rec)
            have.add((kind, c["id"]))
            got.append(rec)
            _write_credits(out, credits)
        report.append({"theme": q.get("theme"), "query": q["query"], "kind": kind, "http": r["http"],
                       "total_hits": r.get("total"), "returned": len(r["hits"]), "passed_filters": len(keep), "taken": n})
    if credits:
        _write_credits(out, credits)
    (out / "rejected.json").write_text(json.dumps(rejected, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    if thumbs_only:
        (out / "candidates.json").write_text(json.dumps(cands_out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    (out / "fetch_report.json").write_text(json.dumps({"queries": report, "errors": errors, "api_requests": cl.requests,
                                                      "cache_hits": cl.cache.hits, "rate_wait_s": round(cl.limiter.waited, 2)},
                                                     ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    status = "FAIL" if report and all(x.get("http") not in (200, "cache") for x in report) else ("WARN" if errors else "PASS")
    return {"status": status, "fetched": len(got), "candidates": len(cands_out), "rejected": len(rejected),
            "errors": errors, "api_requests": cl.requests, "cache_hits": cl.cache.hits, "queries": report,
            "out": str(out), "credits": len(credits)}
