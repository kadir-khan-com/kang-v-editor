"""kang.py fetch: Wikimedia Commons stills + licence metadata -> assets folder + CREDITS.json/.txt (ingest-ready).

Rules: only free licences (CC0, PD, CC BY, CC BY-SA; BY-SA skippable). NC/ND/unknown/fair-use are skipped and listed.
Nothing is approved: fetched files are candidates; rights_status stays recorded_not_cleared (ingest sets it).
Polite client: descriptive User-Agent, 1 request/s, backoff on 429/503, thumbnails (<= 1920 px) not originals.
"""
from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import time
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

API = "https://commons.wikimedia.org/w/api.php"
UA = "KANG-asset-fetch/0.6 (personal video editing tool; Wikimedia API etiquette followed)"
ALLOWED = ("CC0", "PD", "CC BY", "CC BY-SA")
SKIP_TITLE = re.compile(r"(\b3D\b|stereo|anaglyph|stereoscop)", re.I)


def _clean(s: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def licence_family(short: str) -> str:
    l = (short or "").upper().replace("-", " ").replace("_", " ")
    if not l:
        return "UNKNOWN"
    if "NC" in l.split() or "NONCOMMERCIAL" in l or "ND" in l.split() or "NODERIVS" in l:
        return "RESTRICTED"
    if "BY SA" in l:
        return "CC BY-SA"
    if "CC BY" in l:
        return "CC BY"
    if "CC0" in l or "CC ZERO" in l:
        return "CC0"
    if "PUBLIC DOMAIN" in l or l.startswith("PD"):
        return "PD"
    return "OTHER"


def http_get(url: str, *, retries: int = 4, pause: float = 2.0, timeout: float = 30.0) -> bytes:
    delay = 5.0
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                data = r.read()
            time.sleep(pause)
            return data
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < retries:
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise RuntimeError("unreachable")


def search(query: str, limit: int, get: Callable[[str], bytes] = http_get, width: int = 1920) -> List[Dict[str, Any]]:
    params = {"action": "query", "generator": "search", "gsrsearch": f"{query} filetype:bitmap",
              "gsrnamespace": "6", "gsrlimit": str(max(limit * 4, 8)), "prop": "imageinfo",
              "iiprop": "url|size|mime|extmetadata|sha1", "iiurlwidth": str(width), "format": "json",
              "formatversion": "2"}
    data = json.loads(get(API + "?" + urllib.parse.urlencode(params)).decode("utf-8"))
    if "error" in data or "query" not in data:
        return []
    return _parse_pages(data["query"]["pages"])


def _parse_pages(pages_in: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    pages = sorted(pages_in, key=lambda p: p.get("index", 0))
    out = []
    for p in pages:
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata", {})
        short = _clean(em.get("LicenseShortName", {}).get("value", ""))
        out.append({"title": p["title"], "width": ii.get("width"), "height": ii.get("height"), "mime": ii.get("mime"),
                    "sha1": ii.get("sha1"), "thumb": ii.get("thumburl") or ii.get("url"),
                    "source_page": ii.get("descriptionurl"), "licence": short,
                    "licence_url": _clean(em.get("LicenseUrl", {}).get("value", "")),
                    "author": _clean(em.get("Artist", {}).get("value", ""))[:200],
                    "description": _clean(em.get("ImageDescription", {}).get("value", ""))[:300],
                    "categories": _clean(em.get("Categories", {}).get("value", "")).split("|")[:12]})
    return out


# ---------------- category pool mode (idea: CommonsLens / WikiSemanticImgSearch category paths) ----------------
def pool_search(expr: str, max_items: int = 800, get: Callable[[str], bytes] = http_get, width: int = 1920,
                page_size: int = 50) -> List[Dict[str, Any]]:
    """All files for a Commons search expression, e.g. 'deepcat:"Dwarka"' or 'incategory:"Bet_Dwarka"'. Paged."""
    out: List[Dict[str, Any]] = []
    offset = 0
    while len(out) < max_items:
        params = {"action": "query", "generator": "search", "gsrsearch": f"{expr} filetype:bitmap", "gsrnamespace": "6",
                  "gsrlimit": str(page_size), "gsroffset": str(offset), "prop": "imageinfo",
                  "iiprop": "url|size|mime|extmetadata|sha1", "iiurlwidth": str(width), "format": "json",
                  "formatversion": "2"}
        data = json.loads(get(API + "?" + urllib.parse.urlencode(params)).decode("utf-8"))
        if "error" in data or "query" not in data:
            break
        out += _parse_pages(data["query"]["pages"])
        nxt = (data.get("continue") or {}).get("gsroffset")
        if nxt is None:
            break
        offset = int(nxt)
    return out[:max_items]


_NORM = [(r"dwaraka", "dwarka"), (r"dwarika", "dwarka"), (r"dwarakadhish", "dwarkadhish"), (r"dwarakadheesh", "dwarkadhish"),
         (r"dwarkadheesh", "dwarkadhish"), (r"gomati", "gomti"), (r"nageshvara?", "nageshwar"), (r"rukmani", "rukmini"),
         (r"[_\-]", " ")]
GENERIC = {"dwarka", "gujarat", "temple", "india", "krishna", "shri krishna"}


def _norm(s: str) -> str:
    s = s.lower()
    for a, b in _NORM:
        s = re.sub(a, b, s)
    return " " + re.sub(r"[^a-z0-9 ]+", " ", s) + " "


def scene_terms(text: str) -> List[str]:
    """Roman search terms for a scene: whole named phrases (hinglish_names) + asset_aliases tags. Phrases stay whole."""
    root = Path(__file__).resolve().parent.parent
    aliases = json.loads((root / "config" / "asset_aliases.json").read_text(encoding="utf-8"))["aliases"]
    names = json.loads((root / "config" / "hinglish_names.json").read_text(encoding="utf-8"))
    terms: List[str] = []
    for hi, ro in list(names.get("phrases", {}).items()) + list(names.get("names", {}).items()):
        if hi in text and ro.lower() not in terms:
            terms.append(ro.lower())
    for t in re.findall(r"[\w\u0900-\u097F]+", text):
        tag = aliases.get(t) or aliases.get(t.lower())
        if tag and tag.lower() not in terms:
            terms.append(tag.lower())
    return [_norm(t).strip() for t in terms]


def score_candidate(terms: List[str], c: Dict[str, Any]) -> (float, List[str]):
    title = _norm(c.get("title", ""))
    rest = _norm(" ".join([c.get("description", "")] + list(c.get("categories") or [])))
    sc, hit = 0.0, []
    for t in terms:
        w = 0.3 if t in GENERIC else (3.0 if " " in t else 1.0)
        if f" {t} " in title:
            sc += 2 * w; hit.append(t)
        elif f" {t} " in rest:
            sc += w; hit.append(t)
    return round(sc, 2), hit


def rank_pool(scenes: List[Dict[str, Any]], pool: List[Dict[str, Any]], per_scene: int = 2, min_score: float = 1.0,
              no_sharealike: bool = False, min_width: int = 1280, top_n: int = 5) -> Dict[str, Any]:
    """Greedy, scene order: each scene gets its best unused free-licence candidates scoring >= min_score."""
    allowed = [a for a in ALLOWED if not (no_sharealike and a == "CC BY-SA")]
    ok = [c for c in pool if licence_family(c["licence"]) in allowed and not SKIP_TITLE.search(c["title"])
          and (c.get("width") or 0) >= min_width and c.get("mime") in ("image/jpeg", "image/png")]
    used: set = set()
    picks: Dict[str, List[Dict[str, Any]]] = {}
    table: List[Dict[str, Any]] = []
    for s in scenes:
        terms = scene_terms(s.get("text", ""))
        scored = sorted(((score_candidate(terms, c), c) for c in ok), key=lambda x: -x[0][0])
        chosen = []
        for (sc, hit), c in scored:
            if sc < min_score:
                break
            if c["title"] in used:
                continue
            if len(chosen) < per_scene:
                chosen.append(c); used.add(c["title"])
            if len(chosen) >= per_scene:
                break
        picks[s["id"]] = chosen
        for r, ((sc, hit), c) in enumerate(scored[:top_n], 1):
            table.append({"scene": s["id"], "rank": r, "score": sc, "matched": " + ".join(hit),
                          "picked": "yes" if c in chosen else "", "title": c["title"], "licence": c["licence"],
                          "source_page": c["source_page"]})
        if not scored or scored[0][0][0] < min_score:
            table.append({"scene": s["id"], "rank": 0, "score": scored[0][0][0] if scored else 0, "matched": "",
                          "picked": "", "title": "(no candidate >= min_score: talk scene -> profile fallback)",
                          "licence": "", "source_page": ""})
    return {"picks": picks, "table": table, "pool_free": len(ok), "pool_total": len(pool),
            "terms": {s["id"]: scene_terms(s.get("text", "")) for s in scenes}}


def fetch_pool(scenes_path: str, out_dir: str, expr: str, *, per_scene: int = 2, max_pool: int = 800,
               min_score: float = 1.0, no_sharealike: bool = False, min_width: int = 1280, dry_run: bool = False,
               get: Callable[[str], bytes] = http_get, pool_cache: Optional[str] = None) -> Dict[str, Any]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    cache = Path(pool_cache) if pool_cache else out / "pool.json"
    if cache.exists():
        pool = json.loads(cache.read_text(encoding="utf-8"))["files"]
    else:
        pool, seen = [], set()
        for e in [x.strip() for x in expr.split(";") if x.strip()]:  # several pools: 'deepcat:"Dwarka";incategory:"Bet_Dwarka"'
            for c in pool_search(e, max_items=max_pool, get=get):
                if c["title"] not in seen:
                    seen.add(c["title"]); pool.append(c)
        cache.write_text(json.dumps({"expr": expr, "count": len(pool), "files": pool}, ensure_ascii=False, indent=1),
                         encoding="utf-8")
    scenes = json.loads(Path(scenes_path).read_text(encoding="utf-8"))["scenes"]
    rk = rank_pool(scenes, pool, per_scene=per_scene, min_score=min_score, no_sharealike=no_sharealike,
                   min_width=min_width)
    with open(out / "pool_ranking.csv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rk["table"][0].keys()) if rk["table"] else ["scene"])
        w.writeheader(); w.writerows(rk["table"])
    queries = [{"scene": sid, "query": f"pool:{expr}", "count": str(per_scene), "_cands": cs}
               for sid, cs in rk["picks"].items() if cs]
    r = fetch(queries, out_dir, per_query=per_scene, no_sharealike=no_sharealike, min_width=min_width,
              dry_run=dry_run, get=get)
    r.update({"mode": "category_pool", "pool_expr": expr, "pool_total": rk["pool_total"], "pool_free_licence": rk["pool_free"],
              "scenes_without_pick": [sid for sid, cs in rk["picks"].items() if not cs],
              "ranking_csv": str(out / "pool_ranking.csv"), "pool_cache": str(cache)})
    r["status"] = "FAIL" if not r["ok"] else ("WARN" if (r["scenes_without_pick"] or r["download_errors"]) else "PASS")
    return r


def standard_thumb(url: str, width: Optional[int]) -> str:
    """Wikimedia throttles original-file downloads (429) and asks for standard thumbnail sizes.
    When imageinfo returned the unscaled original (file narrower than 1920), use the 1280px thumbnail instead."""
    if not url or "/thumb/" in url or not (width and width > 1280):
        return url
    m = re.match(r"(https://upload\.wikimedia\.org/wikipedia/commons)/(\w/\w\w)/([^?]+)", url)
    if not m:
        return url
    base, h, name = m.groups()
    return f"{base}/thumb/{h}/{name}/1280px-{name}"


def _slug(s: str, n: int = 36) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:n] or "img"


def read_queries(path: str) -> List[Dict[str, str]]:
    """CSV columns: scene,query[,count] — one row per query; empty query rows are skipped."""
    with open(path, encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f) if (r.get("query") or "").strip()]


def plan_queries(scenes_path: str, out_csv: str, place: str = "") -> Dict[str, Any]:
    """Draft scene->query CSV from config/asset_aliases.json tags found in each scene text. User edits it."""
    root = Path(__file__).resolve().parent.parent
    aliases = json.loads((root / "config" / "asset_aliases.json").read_text(encoding="utf-8"))["aliases"]
    ents = set(json.loads((root / "config" / "scene_profiles.json").read_text(encoding="utf-8"))["entities"])
    sc = json.loads(Path(scenes_path).read_text(encoding="utf-8"))["scenes"]
    rows = []
    for s in sc:
        toks = re.findall(r"[\w\u0900-\u097F]+", s.get("text", ""))
        tags: List[str] = []
        for t in toks:
            tag = aliases.get(t) or aliases.get(t.lower())
            if tag and tag not in tags:
                tags.append(tag)
        main = [t for t in tags if t in ents][:2]
        rest = [t for t in tags if t not in ents][:2]
        place_toks = {t.lower() for t in place.split()}
        tags_q = [t for t in main + rest if t.lower() not in place_toks][:2]  # Commons ANDs words: keep short
        q = " ".join(([place] if place else []) + tags_q).strip()
        rows.append({"scene": s["id"], "query": q, "count": "3", "scene_title": s.get("title", "")[:60]})
    with open(out_csv, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["scene", "query", "count", "scene_title"])
        w.writeheader()
        w.writerows(rows)
    return {"ok": True, "csv": out_csv, "scenes": len(rows), "empty": sum(1 for r in rows if not r["query"])}


def _write_credits(out: Path, credits: List[Dict[str, Any]]) -> None:
    (out / "CREDITS.json").write_text(json.dumps(credits, ensure_ascii=False, indent=1), encoding="utf-8")
    lines = [f"{c['file']}: \"{c['title'].replace('File:', '')}\" by {c['author'] or 'unknown'}, {c['licence']}"
             f" ({c['licence_url']}), {c['source_page']}" for c in credits]
    (out / "CREDITS.txt").write_text("Wikimedia Commons credits (rights recorded, NOT cleared)\n" + "\n".join(lines) + "\n",
                                     encoding="utf-8")


def fetch(queries: List[Dict[str, str]], out_dir: str, *, per_query: int = 3, no_sharealike: bool = False,
          min_width: int = 1280, dry_run: bool = False, get: Callable[[str], bytes] = http_get,
          max_errors: int = 5) -> Dict[str, Any]:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    cj = out / "CREDITS.json"
    credits: List[Dict[str, Any]] = json.loads(cj.read_text(encoding="utf-8")) if cj.exists() else []
    seen_titles = {c.get("title") for c in credits}
    seen_sha = {c.get("sha256") for c in credits}
    skipped: List[Dict[str, str]] = []
    got: List[Dict[str, Any]] = []
    allowed = [a for a in ALLOWED if not (no_sharealike and a == "CC BY-SA")]
    errors: List[Dict[str, str]] = []
    aborted = False
    for q in queries:
        want = int(q.get("count") or per_query)
        scene, query = (q.get("scene") or "").strip(), q["query"].strip()
        n = 0
        words = query.split()
        variants = [" ".join(words[:k]) for k in range(len(words), 0, -1)]  # broaden if too narrow
        cands: List[Dict[str, Any]] = list(q.get("_cands") or [])
        used = query
        for v in ([] if cands else variants):
            cands = search(v, want, get=get)
            if cands:
                used = v
                break
        for c in cands:
            if n >= want:
                break
            fam = licence_family(c["licence"])
            if c["title"] in seen_titles:
                continue
            if SKIP_TITLE.search(c["title"]):
                skipped.append({"scene": scene, "title": c["title"], "reason": "3D/stereo/anaglyph"})
                continue
            if fam not in allowed:
                skipped.append({"scene": scene, "title": c["title"], "reason": f"licence {c['licence'] or 'unknown'}"})
                continue
            if (c.get("width") or 0) < min_width or c.get("mime") not in ("image/jpeg", "image/png"):
                skipped.append({"scene": scene, "title": c["title"], "reason": f"size/mime {c.get('width')} {c.get('mime')}"})
                continue
            n += 1
            seen_titles.add(c["title"])
            ext = ".png" if c["mime"] == "image/png" else ".jpg"
            name = f"{scene + '_' if scene else ''}{n}_{_slug(Path(c['title']).stem.replace('File:', ''))}{ext}"
            rec = {"scene": scene, "query": query, "query_used": used, "file": name, "title": c["title"], "author": c["author"],
                   "licence": c["licence"], "licence_family": fam, "licence_url": c["licence_url"],
                   "source_page": c["source_page"], "downloaded": c["thumb"], "description": c["description"],
                   "categories": c["categories"], "rights_status": "recorded_not_cleared"}
            if not dry_run:
                try:
                    data = get(standard_thumb(c["thumb"], c.get("width")))
                except Exception as exc:  # keep going; record it (429 = Wikimedia throttling this IP)
                    n -= 1
                    errors.append({"scene": scene, "title": c["title"], "error": str(exc)[:160]})
                    if len(errors) >= max_errors:
                        aborted = True
                        break
                    continue
                sha = hashlib.sha256(data).hexdigest()
                if sha in seen_sha:
                    n -= 1
                    continue
                (out / name).write_bytes(data)
                rec["sha256"] = sha
                seen_sha.add(sha)
                credits.append(rec)
                _write_credits(out, credits)  # incremental: a crash never leaves files without credits
            got.append(rec)
        if aborted:
            break
    if not dry_run:
        _write_credits(out, credits)
    fams: Dict[str, int] = {}
    for g in got:
        fams[g["licence_family"]] = fams.get(g["licence_family"], 0) + 1
    no_hit = [q.get("scene") or q["query"] for q in queries
              if not any(g["query"] == q["query"].strip() and g["scene"] == (q.get("scene") or "").strip() for g in got)]
    return {"ok": not aborted, "status": "FAIL" if aborted else ("WARN" if (no_hit or errors) else "PASS"),
            "aborted_after_errors": aborted, "download_errors": errors, "fetched": len(got), "dry_run": dry_run,
            "licence_families": fams, "skipped": len(skipped), "skipped_detail": skipped[:40],
            "queries_without_result": no_hit, "out": str(out),
            "next": f"python kang.py ingest {out} --sheet {out}/contact_sheet.jpg  (then match / approve-broll)"}
