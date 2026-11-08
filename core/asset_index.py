"""Asset Brain v0 - Phase 1 (ingest + tag search). Local only, no models, no network.

ingest(assets_dir) scans images/videos, merges licence/source from CREDITS.json (if present) and the
brief column of any visuals CSV given, and writes <assets_dir>/index.json (schema kang.assets/1.0).
Tags come from file names, titles and briefs (deterministic). embedding_ref stays null until the
CLIP phase. search(index, query) = plain tag/text match, scored by matched terms; hints only.
Nothing here selects an asset for a video: selection stays a human approval (visual_selection gate).
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

SCHEMA = "kang.assets/1.0"
IMG = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
VID = {".mp4", ".mov", ".mkv", ".webm", ".m4v"}
STOP = {"the", "and", "at", "of", "on", "in", "to", "a", "an", "with", "jpg", "jpeg", "png", "file", "representative",
        "represen", "representa", "s", "ki", "ka", "ke"}
# small alias table so Hindi/Hinglish queries hit English tags (extend in config later)
ALIASES = {"मंदिर": "temple", "mandir": "temple", "घाट": "ghat", "समुद्र": "sea", "samudra": "sea",
           "सूर्यास्त": "sunset", "द्वारका": "dwarka", "द्वारिका": "dwarka", "dwarika": "dwarka",
           "नागेश्वर": "nageshwar", "बेट": "bet", "गोमती": "gomti", "रेलवे": "railway", "स्टेशन": "station",
           "ट्रेन": "train", "नाव": "boat", "boats": "boat", "पुल": "bridge", "सुदामा": "sudama",
           "हनुमान": "hanuman", "शिव": "shiva", "mahadev": "shiva", "महादेव": "shiva", "lighthouse": "lighthouse",
           "रुक्मिणी": "rukmini", "rukmani": "rukmini", "गोपी": "gopi", "तालाब": "talav", "talab": "talav",
           "बीच": "beach", "ऑटो": "auto", "rickshaw": "auto", "rickshaws": "auto",
           # Commons spelling variants (fetch v3): one tag per place
           "dwaraka": "dwarka", "dwarakadhish": "dwarkadhish", "dwarkadheesh": "dwarkadhish",
           "dwarakadheesh": "dwarkadhish", "gomati": "gomti", "nageshvar": "nageshwar", "nageshvara": "nageshwar",
           "nageswar": "nageshwar", "jyotirling": "jyotirlinga"}


def _load_config_aliases() -> None:
    cfg = Path(__file__).resolve().parent.parent / "config" / "asset_aliases.json"
    if cfg.is_file():
        for k, v in json.loads(cfg.read_text(encoding="utf-8")).get("aliases", {}).items():
            ALIASES.setdefault(k.lower(), v)


_load_config_aliases()


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def terms(text: str) -> List[str]:
    out = []
    for t in re.split(r"[^\w\u0900-\u0963\u0966-\u097F]+|_", (text or "").lower()):
        if not t or t.isdigit() or re.fullmatch(r"s\d+", t):  # drop scene ids like s13 from file names
            continue
        t = ALIASES.get(t, t)
        if t not in STOP and len(t) > 1:
            out.append(t)
    return out


def licence_family(lic: str) -> Dict[str, Any]:
    l = (lic or "").upper()
    if "PIXABAY" in l:  # Pixabay Content License: not Creative Commons, recorded separately; credit given anyway
        return {"family": "PIXABAY_CL", "sharealike": False, "attribution_required": False, "commercial_ok": True,
                "is_cc": False, "note": "Pixabay Content License (no resale as-is; no endorsement implied)"}
    if "PUBLIC DOMAIN MARK" in l or l.strip() == "PDM":
        return {"family": "PD", "sharealike": False, "attribution_required": False, "commercial_ok": True}
    fam = ("CC BY-SA" if "BY-SA" in l else "CC BY-NC" if "NC" in l else "CC BY" if "CC BY" in l else
           "CC0" if "CC0" in l else "PD" if "PUBLIC DOMAIN" in l or l.strip() == "PD" else ("UNKNOWN" if not l else "OTHER"))
    return {"family": fam, "sharealike": fam == "CC BY-SA", "attribution_required": fam in ("CC BY-SA", "CC BY", "CC BY-NC"),
            "commercial_ok": None if fam in ("UNKNOWN", "OTHER") else fam != "CC BY-NC"}


def _dims(p: Path) -> Dict[str, Any]:
    if p.suffix.lower() in IMG:
        from PIL import Image
        with Image.open(p) as im:
            return {"width": im.width, "height": im.height, "duration": None}
    from .runs import media_summary
    m = media_summary(p)
    return {"width": m.get("width"), "height": m.get("height"), "duration": m.get("duration")}


def ingest(assets_dir: str | Path, briefs_csv: Sequence[str | Path] = (), out: Optional[str | Path] = None) -> Dict[str, Any]:
    adir = Path(assets_dir).resolve()
    if not adir.is_dir():
        return {"ok": False, "problems": [f"not a folder: {adir}"]}
    credits: Dict[str, Dict[str, Any]] = {}
    cj = adir / "CREDITS.json"
    if cj.is_file():
        data = json.loads(cj.read_text(encoding="utf-8"))
        for c in (data if isinstance(data, list) else data.get("items", [])):
            credits[c.get("file", "")] = c
    briefs: Dict[str, List[str]] = {}
    for b in briefs_csv:
        with open(b, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f):
                if r.get("asset"):
                    briefs.setdefault(Path(r["asset"]).name, []).append(r.get("brief", ""))
    items, problems, warnings = [], [], []
    for p in sorted(adir.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in IMG | VID:
            continue
        rel = p.relative_to(adir).as_posix()
        c = credits.get(p.name, {})
        sha = _sha(p)
        if c.get("sha256") and c["sha256"] != sha:
            problems.append(f"{rel}: sha256 differs from CREDITS.json (file changed after crediting)")
        try:
            dims = _dims(p)
        except Exception as e:  # unreadable media is a problem, not a crash
            problems.append(f"{rel}: cannot read ({e})")
            continue
        desc = "; ".join(x for x in briefs.get(p.name, []) if x)
        title = re.sub(r"^File:|\.\w+$", "", c.get("title", ""))
        tags = sorted(set(terms(Path(p.name).stem) + terms(title) + terms(desc)))
        lic = c.get("licence", "")
        if not lic:
            warnings.append(f"{rel}: no licence recorded")
        items.append({"asset_id": sha[:12], "path": rel, "type": "image" if p.suffix.lower() in IMG else "video",
                      **dims, "sha256": sha, "tags": tags, "description": desc or title,
                      "title": title, "author": c.get("author"), "source_url": c.get("source_page"),
                      "licence": lic or None, "licence_url": c.get("licence_url"), "licence_info": licence_family(lic),
                      "modified": c.get("modified"), "embedding_ref": None,
                      "rights_status": "recorded_not_cleared" if lic else "unknown",
                      "fetched_for_scene": c.get("scene") or None,
                      "source": c.get("source") or ("commons" if "commons.wikimedia" in (c.get("source_page") or "") else None),
                      "label": c.get("label"), "dhash": c.get("dhash"),
                      **({"theme": c["theme"]} if c.get("theme") else {}),
                      **({"source_tags": c["tags"]} if c.get("tags") else {})})
    ids = [i["asset_id"] for i in items]
    if len(ids) != len(set(ids)):
        warnings.append("duplicate files (same sha256) in library")
    missing = sorted(set(credits) - {Path(i["path"]).name for i in items})
    if missing:
        warnings.append(f"CREDITS.json lists {len(missing)} file(s) not found: {', '.join(missing[:6])}")
    fams: Dict[str, int] = {}
    for i in items:
        fams[i["licence_info"]["family"]] = fams.get(i["licence_info"]["family"], 0) + 1
    index = {"schema": SCHEMA, "assets_dir": adir.name, "count": len(items), "licence_summary": fams,
             "rights_note": "licence recorded per asset; clearance is a separate gate before publishing", "items": items}
    outp = Path(out) if out else adir / "index.json"
    outp.write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return {"ok": not problems, "problems": problems, "warnings": warnings, "index": str(outp), "count": len(items),
            "licence_summary": fams}


def search(index: Dict[str, Any], query: str, top: int = 3, exclude_sharealike: bool = False) -> List[Dict[str, Any]]:
    q = terms(query)
    if not q:
        return []
    res = []
    for it in index.get("items", []):
        if exclude_sharealike and it.get("licence_info", {}).get("sharealike"):
            continue
        tags = set(it.get("tags", []))
        hit = [t for t in q if t in tags]
        if hit:
            res.append({"asset_id": it["asset_id"], "path": it["path"], "score": round(len(set(hit)) / len(set(q)), 3),
                        "matched": sorted(set(hit)), "licence": it.get("licence")})
    res.sort(key=lambda r: (-r["score"], r["path"]))
    return res[:top]


def contact_sheet(index_path: str | Path, out: str | Path) -> Dict[str, Any]:
    """Labelled thumbnail grid (asset_id + licence family) via ImageMagick montage."""
    import subprocess
    ip = Path(index_path)
    idx = json.loads(ip.read_text(encoding="utf-8"))
    adir = ip.parent if (ip.parent / idx["items"][0]["path"]).exists() else Path(idx["assets_dir"])
    args = ["montage"]
    for it in idx["items"]:
        if it["type"] != "image":
            continue
        args += ["-label", f"{it['asset_id'][:8]} {it['licence_info']['family']}\n{Path(it['path']).stem[:28]}",
                 str(adir / it["path"])]
    args += ["-tile", "8x", "-geometry", "240x135+4+4", "-pointsize", "10", str(out)]
    r = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    return {"ok": r.returncode == 0 and Path(out).is_file(), "out": str(out), "stderr": r.stderr[-400:]}


MASTER_SCHEMA = "kang.asset_index/1.0"


def build_master_index(dirs: Sequence[str | Path], out: str | Path, root: Optional[str | Path] = None) -> Dict[str, Any]:
    """ONE asset index over several asset folders (Commons, Openverse, Pixabay, own): re-ingests each folder,
    merges items with folder-relative paths, flags duplicates (same sha256 across folders) and keeps per-source,
    per-licence-family and per-label counts. Per-folder indexes go next to the master (folders are read-only here)."""
    root = Path(root) if root else Path(__file__).resolve().parent.parent
    items, problems, warnings = [], [], []
    seen: Dict[str, str] = {}
    dups = []
    sub = Path(out).parent / "_folder_index"
    sub.mkdir(parents=True, exist_ok=True)
    for d in map(Path, dirs):
        r = ingest(d, out=sub / f"{d.name}.json")  # existing folders are only read, never written
        problems += [f"{d.name}: {p}" for p in r.get("problems", [])]
        warnings += [f"{d.name}: {w}" for w in r.get("warnings", [])]
        if not r.get("ok") and not Path(r.get("index", "")).is_file():
            continue
        idx = json.loads(Path(r["index"]).read_text(encoding="utf-8"))
        try:
            rel = d.resolve().relative_to(root.resolve()).as_posix()
        except ValueError:
            rel = str(d.resolve())
        for it in idx["items"]:
            it = dict(it, folder=rel)
            if not it.get("source"):
                it["source"] = "own_or_card" if not it.get("licence") else "unknown"
            if it["sha256"] in seen:
                dups.append(f"{rel}/{it['path']} = {seen[it['sha256']]}")
            seen.setdefault(it["sha256"], f"{rel}/{it['path']}")
            items.append(it)
    def count(key):
        out_: Dict[str, int] = {}
        for i in items:
            k = key(i) or "none"
            out_[k] = out_.get(k, 0) + 1
        return out_
    index = {"schema": MASTER_SCHEMA, "folders": [str(Path(d)) for d in dirs], "count": len(items),
             "by_source": count(lambda i: i.get("source")), "by_type": count(lambda i: i.get("type")),
             "licence_summary": count(lambda i: i["licence_info"]["family"]), "by_label": count(lambda i: i.get("label")),
             "duplicates_sha256": dups,
             "rights_note": "licence recorded per asset; clearance is a separate gate before publishing. "
                            "Pixabay Content License is not CC and is listed as PIXABAY_CL.", "items": items}
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(index, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return {"ok": not problems, "index": str(out), "count": len(items), "by_source": index["by_source"],
            "licence_summary": index["licence_summary"], "duplicates_sha256": dups, "problems": problems,
            "warnings": warnings[:20]}
