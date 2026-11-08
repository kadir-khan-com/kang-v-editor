"""Asset Brain v0 - Phase 2: rule-based scene -> asset suggestions (hints only).

match(): scene narration (from words.json, else scenes.json text) -> terms (Hindi/English aliases)
-> IDF-weighted overlap with index.json tags -> top-N candidates per scene, with a reason.
Repetition control: an asset already suggested as #1 for an earlier scene is penalised (strongly
within the last `recent` scenes), and the #1 picks are kept unique when an alternative exists.
Nothing is selected here: approval_status stays "awaiting_user" until the user marks choices in
broll_suggestions.csv and runs approve(), which writes a visuals.csv for the existing `visuals`
command (whose own visual_selection gate still applies).
"""
from __future__ import annotations

import csv
import json
import math
from collections import Counter
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import asset_index as ai

SCHEMA = "kang.broll_suggestions/1.0"
CHOOSE_YES = {"1", "x", "y", "yes", "haan", "ha", "✓"}


def _scene_text(sc: Dict[str, Any], words: Optional[List[Dict[str, Any]]]) -> str:
    if words is not None and "first_word" in sc and "last_word" in sc:
        return " ".join(str(w.get("word", "")).strip() for w in words[sc["first_word"]:sc["last_word"] + 1])
    return sc.get("text", "")


PROFILES_PATH = Path(__file__).resolve().parents[1] / "config" / "scene_profiles.json"


def load_profiles(path: Optional[str | Path] = None) -> Dict[str, Any]:
    p = Path(path) if path else PROFILES_PATH
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {"entities": [], "profiles": []}


def _profile_for(text: str, pos: int, last: int, profiles: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    for pr in profiles:  # position (first/last scene) wins over keywords
        where = pr.get("position")
        if (where == "first" and pos == 0) or (where == "last" and pos == last):
            return pr
    for pr in profiles:  # then keywords, in file order
        if any(k in text for k in pr.get("any", [])):
            return pr
    return None


def match(scenes: Dict[str, Any], index: Dict[str, Any], words: Optional[List[Dict[str, Any]]] = None,
          top: int = 3, recent: int = 3, exclude_sharealike: bool = False,
          profiles: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    cfg = profiles if profiles is not None else load_profiles()
    entities = set(cfg.get("entities", []))
    sec_f, prof_w = cfg.get("secondary_entity_factor", 0.55), cfg.get("profile_weight", 0.6)
    items = [i for i in index.get("items", [])
             if not (exclude_sharealike and i.get("licence_info", {}).get("sharealike"))]
    n = max(1, len(items))
    df = Counter(t for i in items for t in set(i.get("tags", [])))
    idf = {t: math.log((n + 1) / (c + 0.5)) for t, c in df.items()}
    first_pick: Dict[str, int] = {}  # asset_id -> scene position where it was #1
    out = []
    all_sc = scenes.get("scenes", [])

    def _rank(tf: Counter, pos: int, weight: float = 1.0, tag: str = "", scene_id: str = "") -> List[Dict[str, Any]]:
        toks = [t for t in tf if t in df]
        ents = {t: tf[t] for t in toks if t in entities}
        primary = max(ents, key=lambda e: (ents[e], idf.get(e, 0.0))) if len(ents) > 1 else None
        scored = []
        for it in items:
            tags = set(it.get("tags", []))
            hit = [t for t in tf if t in tags]
            if not hit:
                continue
            s = weight * sum(idf.get(t, 0.0) * (1 + math.log(tf[t])) for t in hit)
            why = [tag] if tag else []
            a_ents = tags & set(ents)
            if primary and a_ents and primary not in a_ents:
                s *= sec_f
                why.append(f"minor mention ({', '.join(sorted(a_ents))}); scene is mainly {primary}")
            if scene_id and it.get("fetched_for_scene") == scene_id:  # fetch-pool already ranked it for this scene
                s *= 1.5
                why.append(f"fetched for {scene_id}")
            if it["asset_id"] in first_pick:
                gap = pos - first_pick[it["asset_id"]]
                s *= 0.3 if gap <= recent else 0.7
                why.append(f"already #1 in a scene {gap} back")
            top_terms = sorted(hit, key=lambda t: -idf.get(t, 0.0) * tf[t])[:4]
            reason = "matched: " + ", ".join(f"{t}×{tf[t]}" if tf[t] > 1 else t for t in top_terms)
            specific = [t for t in hit if df[t] <= 0.25 * n]  # not a library-wide tag like dwarka/temple
            scored.append({"asset_id": it["asset_id"], "path": it["path"], "raw_score": round(s, 3), "specific": bool(specific),
                           "matched_tags": top_terms, "fallback": False,
                           "reason": "; ".join([reason] + why), "licence": it.get("licence"),
                           "sharealike": it.get("licence_info", {}).get("sharealike")})
        scored.sort(key=lambda c: (-c["raw_score"], c["path"]))
        return scored

    for pos, sc in enumerate(all_sc):
        text = _scene_text(sc, words)
        tf = Counter(ai.terms(text))
        scored = _rank(tf, pos, scene_id=sc.get("id", ""))
        profile = None
        if not (scored and scored[0]["specific"]):  # no specific match -> scene profile (intro/outro/...)
            profile = _profile_for(text, pos, len(all_sc) - 1, cfg.get("profiles", []))
            if profile:
                ptf = Counter(tf)
                for t in profile["prefer"]:
                    ptf[t] += 1
                pscored = _rank(ptf, pos, prof_w if scored else 1.0, f"profile:{profile['name']}", scene_id=sc.get("id", ""))
                seen = {c["asset_id"] for c in pscored}
                scored = pscored + [c for c in scored if c["asset_id"] not in seen]
        cands = scored[:top]
        n_matched = len(cands)
        if len(cands) < top:  # fill with clearly-labelled fallback shots so the editor still has A/B/C
            have = {c["asset_id"] for c in cands}
            pool = sorted((i for i in items if i["asset_id"] not in have),
                          key=lambda i: (i["asset_id"] in first_pick, i["path"]))
            for it in pool[:top - len(cands)]:
                cands.append({"asset_id": it["asset_id"], "path": it["path"], "raw_score": 0.0, "specific": False,
                              "matched_tags": [], "fallback": True,
                              "reason": "fallback: no keyword match in this scene; general library shot",
                              "licence": it.get("licence"), "sharealike": it.get("licence_info", {}).get("sharealike")})
        if n_matched:
            first_pick.setdefault(cands[0]["asset_id"], pos)
        out.append({"scene": sc["id"], "scene_id": sc["id"], "start": sc["start"], "end": sc["end"],
                    "query_terms": [t for t, _ in tf.most_common(12) if t in df],
                    "candidates": cands, "approval_status": "awaiting_user",
                    "matched_candidates": n_matched, "profile": profile["name"] if profile else None,
                    "confidence": ("profile" if profile else "high") if n_matched and cands[0]["specific"] and not profile
                                  else ("profile" if profile and n_matched else ("low" if n_matched else "none")),
                    "needs_manual": bool(profile) or n_matched < top or not (n_matched and cands[0]["specific"])})
    peak = max((c["raw_score"] for s_ in out for c in s_["candidates"]), default=0.0) or 1.0
    for s_ in out:  # score = 0..1, relative to the strongest match in this run (comparable across scenes)
        for c in s_["candidates"]:
            c["score"] = round(c["raw_score"] / peak, 3)
            c.pop("specific", None)
    return {"schema": SCHEMA, "index_count": len(items), "top": top, "scenes": out,
            "note": "rule-based tag match; hints only, nothing selected"}


def qa(sugg: Dict[str, Any], expected_scenes: Optional[List[str]] = None, top: int = 3) -> Dict[str, Any]:
    """Structural acceptance checks for a suggestions file (says nothing about visual relevance)."""
    sc = sugg.get("scenes", [])
    ids = [s["scene_id"] for s in sc]
    exp = expected_scenes or ids
    cands = [c for s in sc for c in s["candidates"]]
    dup = [s["scene_id"] for s in sc if len({c["asset_id"] for c in s["candidates"]}) != len(s["candidates"])]
    fields = ("asset_id", "path", "score", "matched_tags", "reason")
    scores = sorted(c["score"] for c in cands if not c.get("fallback"))
    q = lambda f: scores[min(len(scores) - 1, int(f * len(scores)))] if scores else None
    checks = {
        "coverage": f"{len(set(ids) & set(exp))}/{len(exp)}",
        "missing_scenes": sorted(set(exp) - set(ids)),
        "scenes_with_3": f"{sum(len(s['candidates']) == top for s in sc)}/{len(sc)}",
        "keyword_matched_candidates": f"{sum(not c.get('fallback') for c in cands)}/{len(cands)}",
        "fallback_candidates": [f"{s['scene_id']}:{c['path']}" for s in sc for c in s["candidates"] if c.get("fallback")],
        "duplicate_in_scene": dup,
        "fields_complete": f"{sum(all(f in c and c[f] not in (None, '') or f == 'matched_tags' for f in fields) for c in cands)}/{len(cands)}",
        "reason_present": f"{sum(bool(c.get('reason')) for c in cands)}/{len(cands)}",
        "approval_awaiting_user": f"{sum(s.get('approval_status') == 'awaiting_user' for s in sc)}/{len(sc)}",
        "confidence": {k: sum(s.get("confidence") == k for s in sc) for k in ("high", "profile", "low", "none")},
        "score_matched": {"min": q(0), "p25": q(.25), "median": q(.5), "p75": q(.75), "max": q(.999)},
        "auto_selected": False,
    }
    ok = (not checks["missing_scenes"] and not dup and checks["scenes_with_3"] == f"{len(sc)}/{len(sc)}"
          and checks["reason_present"] == f"{len(cands)}/{len(cands)}"
          and checks["approval_awaiting_user"] == f"{len(sc)}/{len(sc)}")
    return {"structure": "PASS" if ok else "FAIL", "content_review": "PENDING (user spot-check)", **checks}


LETTERS = "ABCDEFGH"


def choices_from_spec(sugg: Dict[str, Any], spec: str) -> Dict[str, List[str]]:
    """'S01=A,S02=AB,S22=skip' -> {scene: [asset paths]}."""
    by = {s["scene_id"]: s for s in sugg["scenes"]}
    out: Dict[str, List[str]] = {}
    for part in filter(None, (x.strip() for x in spec.split(","))):
        sid, _, pick = part.partition("=")
        sid, pick = sid.strip(), pick.strip().upper()
        if sid not in by:
            raise ValueError(f"{sid}: unknown scene")
        if pick in ("", "SKIP", "-"):
            continue
        cs = by[sid]["candidates"]
        for ch in pick:
            k = LETTERS.find(ch)
            if k < 0 or k >= len(cs):
                raise ValueError(f"{sid}: no option {ch}")
            out.setdefault(sid, []).append(cs[k]["path"])
    return out


def interactive_choices(sugg: Dict[str, Any], ask=input, show=print) -> Dict[str, List[str]]:
    out: Dict[str, List[str]] = {}
    for s in sugg["scenes"]:
        show(f"\n{s['scene_id']}  {s['start']:.1f}-{s['end']:.1f}s  confidence={s.get('confidence')}")
        for k, c in enumerate(s["candidates"]):
            show(f"  {LETTERS[k]}) {Path(c['path']).name}  score={c['score']}  [{c['reason']}]")
        while True:
            a = ask(f"{s['scene_id']}: choose A/B/C (several = AB, blank = skip): ").strip().upper()
            try:
                got = choices_from_spec(sugg, f"{s['scene_id']}={a or 'skip'}")
                break
            except ValueError as e:
                show(f"  {e}")
        out.update(got)
    return out


def write_csv(sugg: Dict[str, Any], path: str | Path) -> None:
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f)
        w.writerow(["scene", "start", "end", "confidence", "rank", "option", "asset", "score", "matched_tags", "reason", "licence", "choose"])
        for s in sugg["scenes"]:
            if not s["candidates"]:
                w.writerow([s["scene_id"], s["start"], s["end"], "none", "", "", "", "", "", "no match - pick manually", "", ""])
            for k, c in enumerate(s["candidates"], 1):
                w.writerow([s["scene_id"], s["start"], s["end"], s["confidence"], k, LETTERS[k - 1], c["path"], c["score"],
                            " ".join(c.get("matched_tags") or []), c["reason"],
                            c["licence"] or "", ""])


def hit_at_k(sugg: Dict[str, Any], chosen: Dict[str, set]) -> Dict[str, Any]:
    """Share of scenes where any asset the editor actually used is in the top-k suggestions."""
    rows, hits = [], 0
    for s in sugg["scenes"]:
        want = chosen.get(s["scene_id"], set())
        got = {Path(c["path"]).name for c in s["candidates"]}
        ok = bool(want & got)
        hits += ok
        rows.append({"scene": s["scene_id"], "hit": ok, "overlap": len(want & got), "used": len(want),
                     "confidence": s.get("confidence")})
    hi = [r for r in rows if r["confidence"] == "high"]
    return {"scenes": len(rows), "hits": hits, "hit_rate": round(hits / max(1, len(rows)), 3),
            "high_conf_scenes": len(hi), "high_conf_hits": sum(r["hit"] for r in hi), "rows": rows}


def picks_from_csv(sugg_csv: str | Path) -> Dict[str, List[str]]:
    picks: Dict[str, List[str]] = {}
    with open(sugg_csv, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f):
            if (r.get("choose") or "").strip().lower() in CHOOSE_YES and r.get("asset"):
                picks.setdefault(r["scene"], []).append(r["asset"])
    return picks


def approve(sugg_csv: str | Path | None, index: Dict[str, Any], out_csv: str | Path, scenes: Dict[str, Any],
            allow_missing: bool = False, picks: Optional[Dict[str, List[str]]] = None) -> Dict[str, Any]:
    """User choices (CSV choose=1/x/yes, or a picks dict) -> visuals.csv; several in a scene = equal shots."""
    from .visuals import COLUMNS, MIN_SHOT_S
    by_path = {i["path"]: i for i in index.get("items", [])}
    picks = picks if picks is not None else picks_from_csv(sugg_csv)
    problems, rows = [], []
    for sc in scenes.get("scenes", []):
        sel = picks.get(sc["id"], [])
        if not sel:
            if not allow_missing:
                problems.append(f"{sc['id']}: nothing chosen")
            continue
        dur = sc["end"] - sc["start"]
        if dur / len(sel) < MIN_SHOT_S:
            problems.append(f"{sc['id']}: {len(sel)} shots in {dur:.2f}s is under {MIN_SHOT_S}s each")
            continue
        for k, a in enumerate(sel):
            it = by_path.get(a)
            if not it:
                problems.append(f"{sc['id']}: {a} not in index")
                continue
            if not it.get("licence"):
                problems.append(f"{sc['id']}: {a} has no licence recorded")
            rows.append({"scene": sc["id"], "start": f"{sc['start']:.3f}", "end": f"{sc['end']:.3f}",
                         "duration_s": f"{dur:.2f}", "narration": sc.get("text", "")[:200],
                         "brief": it.get("description") or it.get("title") or Path(a).stem.replace("_", " "), "asset": a, "asset_in_s": "0",
                         "fit": "cover", "licence": f"{it.get('licence') or ''} - {it.get('author') or ''}".strip(" -"),
                         "notes": "chosen from broll_suggestions (user)",
                         "shot_start": "" if k == 0 else f"{sc['start'] + dur * k / len(sel):.3f}"})
    if problems:
        return {"ok": False, "problems": problems}
    with open(out_csv, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    return {"ok": True, "visuals_csv": str(out_csv), "shots": len(rows), "scenes": len({r['scene'] for r in rows})}


def review_sheet(sugg: Dict[str, Any], assets_dir: str | Path, scenes: Dict[str, Any], out: str | Path,
                 scene_ids: Optional[List[str]] = None, font: Optional[str] = None) -> str:
    """One row per scene: narration excerpt + A/B/C thumbnails, for the human spot-check."""
    from PIL import Image, ImageDraw, ImageFont
    text = {s["id"]: s.get("text", "") for s in scenes.get("scenes", [])}
    rows = [s for s in sugg["scenes"] if not scene_ids or s["scene_id"] in scene_ids]
    tw, th, lw, pad = 320, 180, 420, 12
    W, H = lw + 3 * (tw + pad) + pad, len(rows) * (th + 44) + pad
    img = Image.new("RGB", (W, H), (24, 24, 28))
    d = ImageDraw.Draw(img)
    def _font(path, size):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            return ImageFont.load_default()
    dev = font or str(Path(__file__).resolve().parents[1] / "fonts" / "NotoSansDevanagari-Bold.ttf")
    lat = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    f, fs, fd = _font(lat, 17), _font(lat, 14), _font(dev, 15)
    is_dev = lambda w_: any("\u0900" <= ch <= "\u097f" for ch in w_)
    for r, s in enumerate(rows):
        y = pad + r * (th + 44)
        d.text((pad, y), f"{s['scene_id']}  {s['start']:.0f}-{s['end']:.0f}s  [{s.get('confidence')}]", fill=(255, 210, 90), font=f)
        x0, ly = pad, y + 28
        for w_ in text.get(s["scene_id"], "").split()[:45]:  # per-word font: Devanagari vs Latin
            fw = fd if is_dev(w_) else fs
            wl = d.textlength(w_ + " ", font=fw)
            if x0 + wl > lw - pad:
                x0, ly = pad, ly + 21
                if ly > y + th:
                    break
            d.text((x0, ly), w_, fill=(220, 220, 220), font=fw)
            x0 += wl
        for k, c in enumerate(s["candidates"]):
            x = lw + k * (tw + pad)
            try:
                im = Image.open(Path(assets_dir) / c["path"]).convert("RGB")
                im.thumbnail((tw, th))
                img.paste(im, (x + (tw - im.width) // 2, y + (th - im.height) // 2))
            except OSError:
                d.rectangle([x, y, x + tw, y + th], outline=(200, 60, 60))
            tag = f"{LETTERS[k]}  {c['score']:.2f}  " + (" ".join(c.get("matched_tags") or []) or "FALLBACK")
            d.rectangle([x, y + th, x + tw, y + th + 24], fill=(0, 0, 0))
            d.text((x + 4, y + th + 3), tag[:36], fill=(255, 120, 120) if c.get("fallback") else (140, 230, 140), font=fs)
    img.save(out, quality=88)
    return str(out)
