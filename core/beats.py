"""Beat layer (0.7.0-dev): a marker + a new shot at every narration point, like a human editor.

words.json + scenes.json -> beats (2.5-7 s, target ~4.5 s) that never cross a scene boundary
-> assignment onto the current visual plan (v9 CSV): every v9 asset stays on the beats inside its own shot,
   further beats of that shot get UNUSED stills from the scene's Commons pool ranking
-> Ken Burns motion on stills (FCP7 Basic Motion keyframes + smooth sub-pixel FFmpeg preview)
-> beat markers in the Premiere sequence.

Design rules adopted (rules only, no code) from louisedesadeleer/b-roll-finder (MIT): one visual per beat,
drop a visual rather than show a wrong one (here: the previous shot continues with motion), land cuts relative
to the word onset (lead -0.2 s or lag +0.25 s), sub-pixel Ken Burns instead of integer zoompan, frame-grid
self-check, manifest of every pick.

Hard rules: no asset twice in a timeline; a new pool pick is 'representative' unless its title names the
same real place as the v9 shot it joins (and that shot is exact); known wrong-place items are rejected
(config/beat_rules.json); text cards / archival shots keep their beats.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import re
import statistics
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = "kang.beats/1.0"
ANCHORS = {"lead": -0.2, "lag": 0.25}
PUNCT = (",", "।", ".", "?", "!", "॥", ";", ":")
NON_PLACE_KEYS = {"sunset", "beach", "sgdhp exhibits", "excavation"}  # kinds, not places -> never 'exact'
PARALLAX_COLUMNS = ["parallax_clip", "parallax_dir", "parallax_status"]
AI_MOTION_COLUMNS = ["ai_motion_clip", "ai_motion_dir", "ai_motion_status", "ai_motion_model"]  # v17 (core/ai_motion.py)
CROP_COLUMNS = ["reuse", "reuse_of", "crop_box"]  # v14 crop reuse (core/crop_reuse.py), written when a row has them
VIDEO_EXT = {".mp4", ".mov", ".webm", ".mkv", ".m4v"}  # stock video clips (v12) sit on the timeline as video  # optional, written when a row has them
BEAT_COLUMNS = ["beat", "scene", "start", "end", "duration_s", "first_word_time", "text", "asset", "source_dir",
                "asset_source", "match", "role", "v9_shot", "licence", "title", "source_page", "motion", "notes"]


def load_rules(path: Optional[str | Path] = None) -> Dict[str, Any]:
    return json.loads(Path(path or ROOT / "config" / "beat_rules.json").read_text(encoding="utf-8"))


def frame_round(t: float, fps: int) -> float:
    return round(round(t * fps) / fps, 6)


def seq_end_of(duration: float, fps: int) -> float:
    return int(duration * fps + 1e-6) / fps


def _strip(w: str) -> str:
    return re.sub(r"[,।.?!॥;:\"'()\-]+", "", w).strip()


# --------------------------------------------------------------------------- segmentation
def boundary_bonus(words: Sequence[Dict[str, Any]], j: int, clause: Iterable[str],
                   bad_start: Iterable[str] = ()) -> Tuple[float, List[str]]:
    """How good it is to start a beat at word j (pause before it, punctuation, clause word); a cut with no
    narration cue costs a little, one in front of a postposition/verb tail ('से', 'है', 'किलोमीटर') costs more."""
    sc, why = 0.0, []
    gap = words[j]["start"] - words[j - 1]["end"] if j > 0 else 0.0
    if gap >= 0.15:
        sc += 1.5 * min(gap, 0.6) / 0.3
        why.append(f"gap{gap:.2f}")
    if j > 0 and words[j - 1]["word"].strip().endswith(PUNCT):
        sc += 2.0
        why.append("punct")
    if _strip(words[j]["word"]) in set(clause):
        sc += 0.7
        why.append("clause")
    if not why:
        sc -= 1.0
    if _strip(words[j]["word"]) in set(bad_start):
        sc -= 2.5
        why.append("bad_start")
    return sc, why


def forced_from_visuals(rows: Sequence[Dict[str, str]], words: Sequence[Dict[str, Any]], tol: float = 0.45) -> Dict[int, str]:
    """v9 shot starts (onset-0.2 by design) -> the word index whose onset they cut on. Text cards keep their beats."""
    out: Dict[int, str] = {}
    by_scene: Dict[str, int] = {}
    for r in rows:
        if not r.get("asset"):
            continue
        by_scene[r["scene"]] = by_scene.get(r["scene"], 0) + 1
        if not r.get("shot_start"):
            continue
        t = float(r["shot_start"]) + 0.2
        j = min(range(len(words)), key=lambda k: abs(words[k]["start"] - t))
        if abs(words[j]["start"] - t) <= tol:
            out[j] = f"{r['scene']}.{by_scene[r['scene']]}"
    return out


def _dp(nodes: List[Tuple[float, float]], mn: float, tg: float, mx: float) -> Optional[List[int]]:
    """nodes: [(time, bonus)], first = span start, last = span end. Returns chosen node indexes or None."""
    n = len(nodes)
    INF = float("inf")
    best, prev = [INF] * n, [-1] * n
    best[0] = 0.0
    for i in range(1, n):
        for j in range(i):
            if best[j] == INF:
                continue
            d = nodes[i][0] - nodes[j][0]
            if d < mn - 1e-6 or d > mx + 1e-6:
                continue
            c = best[j] + ((d - tg) / 1.5) ** 2 - (nodes[i][1] if i < n - 1 else 0.0)
            if c < best[i]:
                best[i], prev[i] = c, j
    if best[-1] == INF:
        return None
    path, i = [], n - 1
    while i >= 0:
        path.append(i)
        i = prev[i]
    return path[::-1]


def segment(words: Sequence[Dict[str, Any]], plan: Dict[str, Any], *, min_s: float = 2.5, target_s: float = 4.5,
            max_s: float = 7.0, anchor: str = "lag", fps: int = 25, forced: Optional[Dict[int, str]] = None,
            rules: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    if anchor not in ANCHORS:
        raise ValueError(f"anchor must be one of {list(ANCHORS)}")
    shift = ANCHORS[anchor]
    rules = rules or load_rules()
    clause = rules.get("clause_words", [])
    bad_start = rules.get("bad_start_words", [])
    forced = forced or {}
    seq_end = seq_end_of(plan["duration"], fps)
    beats: List[Dict[str, Any]] = []
    relaxed: List[str] = []
    scenes = plan["scenes"]
    for si, sc in enumerate(scenes):
        s0 = frame_round(sc["start"], fps)
        s1 = seq_end if si == len(scenes) - 1 else frame_round(sc["end"], fps)
        idx = list(range(sc["first_word"], sc["last_word"] + 1))
        cands: List[Tuple[float, int, float, List[str]]] = []  # (cut, word index, bonus, why)
        for j in idx[1:]:
            cut = frame_round(words[j]["start"] + shift, fps)
            if s0 + 1.0 / fps <= cut <= s1 - 1.0 / fps:
                b, why = boundary_bonus(words, j, clause, bad_start)
                cands.append((cut, j, b, why))
        hard = sorted({(c, j) for c, j, _, _ in cands if j in forced})
        anchors_ = [(s0, idx[0])] + hard + [(s1, None)]
        chosen: List[Tuple[float, int, List[str]]] = [(s0, idx[0], ["scene_start"])]
        for (a, _ja), (b, jb) in zip(anchors_, anchors_[1:]):
            inner = [(c, j, bo, why) for c, j, bo, why in cands if a + 1e-6 < c < b - 1e-6]
            nodes = [(a, 0.0)] + [(c, bo) for c, _, bo, _ in inner] + [(b, 0.0)]
            path = None
            for mn, mx in ((min_s, max_s), (min(min_s, 2.0), max_s), (1.2, max_s * 1.4), (0.4, 1e9)):
                if b - a < mn:
                    path = [0, len(nodes) - 1]
                    break
                path = _dp(nodes, mn, target_s, mx)
                if path:
                    if (mn, mx) != (min_s, max_s):
                        relaxed.append(f"{sc['id']} {a:.2f}-{b:.2f}: bounds relaxed to {mn}-{mx:g}")
                    break
            for k in path[1:-1]:
                c, j, _, why = inner[k - 1]
                chosen.append((c, j, [x for x in why if x != "bad_start"] or ["length"] + (["bad_start"] if "bad_start" in why else [])))
            if jb is not None:
                chosen.append((b, jb, ["forced_v9_cut:" + forced[jb]]))
        starts = [c for c, _, _ in chosen] + [s1]
        for k, (c, j, why) in enumerate(chosen):
            end = starts[k + 1]
            last_j = (chosen[k + 1][1] - 1) if k + 1 < len(chosen) else idx[-1]
            text = " ".join(words[x]["word"] for x in range(j, last_j + 1))
            beats.append({"id": f"{sc['id']}_b{k + 1:02d}", "scene": sc["id"], "start": round(c, 3), "end": round(end, 3),
                          "duration": round(end - c, 3), "first_word": j, "first_word_time": round(words[j]["start"], 3),
                          "last_word": last_j, "text": text, "boundary": why})
    durs = [b["duration"] for b in beats]
    return {"schema": SCHEMA, "anchor": anchor, "shift_s": shift, "fps": fps, "min_s": min_s, "target_s": target_s,
            "max_s": max_s, "duration": plan["duration"], "sequence_end": round(seq_end, 3), "beats": beats,
            "stats": _stats(durs), "relaxed": relaxed, "forced_cuts": len(forced)}


def _stats(durs: Sequence[float]) -> Dict[str, Any]:
    if not durs:
        return {"count": 0}
    return {"count": len(durs), "avg_s": round(sum(durs) / len(durs), 2), "median_s": round(statistics.median(durs), 2),
            "min_s": round(min(durs), 2), "max_s": round(max(durs), 2)}


def check_beats(bp: Dict[str, Any], plan: Dict[str, Any]) -> List[str]:
    """Contiguous, frame-aligned, inside one scene each, ends on the sequence frame end."""
    probs: List[str] = []
    fps = bp["fps"]
    bs = bp["beats"]
    if not bs or abs(bs[0]["start"]) > 1e-6:
        probs.append("first beat must start at 0")
    for a, b in zip(bs, bs[1:]):
        if abs(a["end"] - b["start"]) > 1e-6:
            probs.append(f"gap/overlap {a['id']} -> {b['id']}")
    if bs and abs(bs[-1]["end"] - bp["sequence_end"]) > 1e-6:
        probs.append("last beat must end at the sequence frame end")
    sc = {s["id"]: s for s in plan["scenes"]}
    for b in bs:
        for t in (b["start"], b["end"]):
            if abs(t * fps - round(t * fps)) > 1e-3:
                probs.append(f"{b['id']} not frame-aligned")
        s = sc[b["scene"]]
        if b["start"] < frame_round(s["start"], fps) - 1e-6 or b["end"] > frame_round(s["end"], fps) + 1e-6:
            probs.append(f"{b['id']} crosses its scene boundary")
        if b["duration"] <= 0:
            probs.append(f"{b['id']} empty")
    return probs


def write_beats(bp: Dict[str, Any], prefix: str | Path) -> Tuple[Path, Path]:
    pj, pc = Path(str(prefix) + ".json"), Path(str(prefix) + ".csv")
    pj.parent.mkdir(parents=True, exist_ok=True)
    pj.write_text(json.dumps(bp, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    with open(pc, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["beat", "scene", "start", "end", "duration_s", "first_word_time", "boundary", "text"])
        for b in bp["beats"]:
            w.writerow([b["id"], b["scene"], f"{b['start']:.3f}", f"{b['end']:.3f}", f"{b['duration']:.2f}",
                        f"{b['first_word_time']:.3f}", "+".join(b["boundary"]), b["text"]])
    return pj, pc


# --------------------------------------------------------------------------- places / candidates
def _norm(s: str) -> str:
    from .commons_fetch import _norm as n
    return n(s)


def title_places(title: str, rules: Dict[str, Any]) -> List[str]:
    t = _norm(title.replace("File:", ""))
    return sorted(k for k, al in rules["places"].items() if any(f" {_norm(a).strip()} " in t for a in al))


def rejected(title: str, rules: Dict[str, Any], extra: str = "") -> Optional[str]:
    """Known wrong-place / off-topic items. `extra` = description + categories (Commons), checked too."""
    t = _norm(title + " " + extra)
    for r in rules.get("reject_titles", []):
        if f" {_norm(r['match']).strip()} " in t:
            return r["reason"]
    return rules.get("eye_rejects", {}).get(title)


def match_of(notes: str) -> str:
    m = re.search(r"match:([a-z_]+)", notes or "")
    return m.group(1) if m else "representative"


def pool_candidates(pool_dirs: Sequence[str | Path], plan: Dict[str, Any], top_n: int = 15,
                    min_score: float = 1.0) -> Dict[str, List[Dict[str, Any]]]:
    """Per scene, ranked Commons candidates: deep re-rank of pool.json (same ranker as fetch-pool) when present,
    else pool_ranking.csv. Local files (already downloaded, in CREDITS.json) are attached."""
    from . import commons_fetch as cf
    out: Dict[str, List[Dict[str, Any]]] = {}
    for d in map(Path, pool_dirs):
        local = {}
        cj = d / "CREDITS.json"
        if cj.is_file():
            local = {c["title"]: c for c in json.loads(cj.read_text(encoding="utf-8")) if c.get("title")}
        pj = d / "pool.json"
        if pj.is_file():
            pool = json.loads(pj.read_text(encoding="utf-8"))["files"]
            byt = {c["title"]: c for c in pool}
            rk = cf.rank_pool(plan["scenes"], pool, per_scene=0, min_score=min_score, top_n=top_n)
            rows = [r for r in rk["table"] if r["title"].startswith("File:") and float(r["score"]) >= min_score]
        else:
            rp = d / "pool_ranking.csv"
            if not rp.is_file():
                continue
            with open(rp, encoding="utf-8-sig", newline="") as fh:
                rows = [r for r in csv.DictReader(fh) if r["title"].startswith("File:")]
            byt = {}
        for r in rows:
            c = dict(byt.get(r["title"], {"title": r["title"], "licence": r["licence"], "source_page": r["source_page"]}))
            c.update(score=float(r["score"]), rank=int(r["rank"]), matched=r.get("matched", ""), pool_dir=str(d))
            if r["title"] in local:
                c["local_file"] = str(d / local[r["title"]]["file"])
                c["credit"] = local[r["title"]]
            out.setdefault(r["scene"], []).append(c)
    # global fallback (beat layer): every free-licence still of the pool, for shots whose scene list runs dry;
    # assign() only takes one that shows the SAME real place as the shot (or, for a generic shot, a generic Dwarka view)
    for d in map(Path, pool_dirs):
        pj = d / "pool.json"
        if not pj.is_file():
            continue
        local = {}
        cj = d / "CREDITS.json"
        if cj.is_file():
            local = {c["title"]: c for c in json.loads(cj.read_text(encoding="utf-8")) if c.get("title")}
        for c in json.loads(pj.read_text(encoding="utf-8"))["files"]:
            if cf.licence_family(c["licence"]) not in cf.ALLOWED or cf.SKIP_TITLE.search(c["title"]) \
                    or (c.get("width") or 0) < 1280 or c.get("mime") not in ("image/jpeg", "image/png") \
                    or " dwarka " not in _norm(c["title"] + " " + c.get("description", "")):
                continue
            g = dict(c, score=0.0, rank=999, matched="global", pool_dir=str(d), global_fallback=True)
            if c["title"] in local:
                g["local_file"] = str(d / local[c["title"]]["file"])
            out.setdefault("_global", []).append(g)
    if "_global" in out:
        out["_global"].sort(key=lambda c: c["title"])
    for s in out:
        seen, keep = set(), []
        for c in sorted(out[s], key=lambda c: (-c["score"], c["rank"])):
            if c["title"] not in seen:
                seen.add(c["title"]); keep.append(c)
        out[s] = keep
    return out


# --------------------------------------------------------------------------- assignment
def v9_shots(rows: Sequence[Dict[str, str]], plan: Dict[str, Any]) -> List[Dict[str, Any]]:
    sc = {s["id"]: s for s in plan["scenes"]}
    shots, n = [], {}
    for r in rows:
        if not r.get("asset"):
            continue
        n[r["scene"]] = n.get(r["scene"], 0) + 1
        st = float(r["shot_start"]) if r.get("shot_start") else sc[r["scene"]]["start"]
        shots.append({"shot": f"{r['scene']}.{n[r['scene']]}", "scene": r["scene"], "start": st, "asset": r["asset"],
                      "match": match_of(r.get("notes", "")), "licence": r.get("licence", ""), "brief": r.get("brief", ""),
                      "notes": r.get("notes", "")})
    for a, b in zip(shots, shots[1:]):
        a["end"] = b["start"] if b["scene"] == a["scene"] else sc[a["scene"]]["end"]
    if shots:
        shots[-1]["end"] = sc[shots[-1]["scene"]]["end"]
    return shots


def assign(bp: Dict[str, Any], rows: Sequence[Dict[str, str]], plan: Dict[str, Any], v9_credits: Sequence[Dict[str, Any]],
           cands: Dict[str, List[Dict[str, Any]]], rules: Dict[str, Any], exclude_titles: Iterable[str] = ()) -> Dict[str, Any]:
    """-> {rows (one per beat), picks (new pool candidates used, in order), problems}."""
    shots = v9_shots(rows, plan)
    cred_by_file = {c["file"]: c for c in v9_credits}
    used_titles = {c["title"] for c in v9_credits if c.get("title")} | set(exclude_titles)
    used_assets = set()
    out, picks, problems, rejects = [], [], [], []
    for sh in shots:
        used_assets.add(sh["asset"])
    owner: Dict[str, str] = {}
    for b in bp["beats"]:
        mine = [sh for sh in shots if sh["scene"] == b["scene"]]
        if mine:
            inside = [sh for sh in mine if sh["start"] - 1e-6 <= b["first_word_time"]]
            owner[b["id"]] = (inside[-1] if inside else mine[0])["shot"]
    for sh in shots:
        bs = sorted((b for b in bp["beats"] if owner.get(b["id"]) == sh["shot"]), key=lambda b: b["start"])
        if not bs:
            problems.append(f"{sh['shot']}: no beat inside the shot ({sh['start']:.2f}-{sh['end']:.2f}); v9 asset {sh['asset']} dropped")
            continue
        shot_places = set(title_places(cred_by_file.get(sh["asset"], {}).get("title", sh["asset"]), rules)) | \
            set(title_places(sh["asset"].replace("_", " "), rules))
        hold = sh["match"] in ("text_card", "archival")
        cur = {"asset": sh["asset"], "source_dir": "v9", "asset_source": "v9", "match": sh["match"],
               "licence": sh["licence"], "title": cred_by_file.get(sh["asset"], {}).get("title", ""),
               "source_page": cred_by_file.get(sh["asset"], {}).get("source_page", ""), "notes": sh["notes"]}
        for k, b in enumerate(bs):
            role = "v9_shot"
            if k > 0:
                if hold:
                    role = "card_hold"
                else:
                    pick = None
                    real_shot = shot_places - NON_PLACE_KEYS
                    for c in cands.get(sh["scene"], []) + cands.get("_global", []):
                        if c["title"] in used_titles:
                            continue
                        why = rejected(c["title"], rules, c.get("description", "") + " " + " ".join(c.get("categories") or []))
                        places = set(title_places(c["title"], rules))
                        if not why and not places <= shot_places:
                            why = f"place {sorted(places - shot_places)} not shown by shot {sh['shot']} ({sorted(shot_places) or 'generic'})"
                        if not why and c.get("global_fallback"):
                            if real_shot and not (places & real_shot):
                                why = "global fallback must show the shot's own place"
                            elif not real_shot and shot_places and not places:
                                why = "global fallback: shot shows a kind of view (beach/sunset), candidate generic"
                            elif not shot_places and sh["match"] != "representative":
                                why = "global fallback: generic views only for representative shots"
                        if why:
                            rejects.append({"scene": sh["scene"], "shot": sh["shot"], "title": c["title"], "reason": why})
                            continue
                        pick = c
                        break
                    if pick:
                        used_titles.add(pick["title"])
                        pick["_scene"] = sh["scene"]
                        places = set(title_places(pick["title"], rules))
                        real = places - NON_PLACE_KEYS - set(rules.get("area_keys", []))  # an area (island) is never 'exact'
                        exact = sh["match"] == "exact" and real and real <= shot_places
                        cur = {"asset": pick.get("local_file", ""), "source_dir": pick["pool_dir"], "asset_source": "pool",
                               "match": "exact" if exact else "representative", "licence": pick.get("licence", ""),
                               "title": pick["title"], "source_page": pick.get("source_page", ""),
                               "notes": f"beat layer pool pick for shot {sh['shot']} ("
                                        + ("global same-place fallback" if pick.get("global_fallback") else f"rank {pick['rank']}, score {pick['score']}")
                                        + f"{', places ' + '/'.join(sorted(places)) if places else ', generic Dwarka'}); agent-picked, not human-reviewed",
                               "_cand": pick}
                        picks.append(pick)
                        role = "new_pool"
                    else:
                        role = "continued_with_motion"
            out.append({"beat": b["id"], "scene": b["scene"], "start": b["start"], "end": b["end"],
                        "duration_s": round(b["end"] - b["start"], 3), "first_word_time": b["first_word_time"],
                        "text": b["text"], "role": role, "v9_shot": sh["shot"], **{k_: v for k_, v in cur.items()}})
    covered = {r["beat"] for r in out}
    for b in bp["beats"]:
        if b["id"] not in covered:
            problems.append(f"{b['id']}: no v9 shot covers it")
    out.sort(key=lambda r: r["start"])
    return {"rows": out, "picks": picks, "problems": problems, "rejects": rejects}


def assign_qa(rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """No asset (by file name or Commons title) in two separate shots; roles/labels counted."""
    clips = merge_clips(rows)
    seen, dup = {}, []
    for c in clips:
        # v14: a crop reuse is its own derived file (different framing of a photo already on the timeline); only its
        # file name must be unique - the shared Commons title is the point (crop rules: core/crop_reuse.crop_qa)
        # v18: a cold-open teaser cut ("teaser") is its own derived file too (section of a clip, title overlay)
        keys = (Path(c["asset"]).name,) if c.get("reuse") in ("crop_reuse", "teaser") \
            else (Path(c["asset"]).name, c.get("title"))
        for key in filter(None, keys):
            if key in seen and seen[key] != c["first_beat"]:
                dup.append(key)
            seen[key] = c["first_beat"]
    roles: Dict[str, int] = {}
    for r in rows:
        roles[r["role"]] = roles.get(r["role"], 0) + 1
    labels: Dict[str, int] = {}
    for c in clips:
        labels[c["match"]] = labels.get(c["match"], 0) + 1
    return {"pass": not dup, "duplicates": sorted(set(dup)), "beats": len(rows), "shots": len(clips),
            "crop_reuses": sum(1 for c in clips if c.get("reuse") == "crop_reuse"),
            "unique_assets": len({Path(c["asset"]).name for c in clips}), "roles": roles, "labels_by_shot": labels,
            "shot_stats": _stats([c["end"] - c["start"] for c in clips])}


def merge_clips(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Consecutive beats on the same asset = one clip (a longer shot)."""
    clips: List[Dict[str, Any]] = []
    for r in sorted(rows, key=lambda r: float(r["start"])):
        if clips and clips[-1]["asset"] == r["asset"]:
            clips[-1]["end"] = float(r["end"])
            clips[-1]["beats"].append(r["beat"])
            continue
        clips.append({"asset": r["asset"], "start": float(r["start"]), "end": float(r["end"]), "match": r["match"],
                      "title": r.get("title", ""), "first_beat": r["beat"], "beats": [r["beat"]], "scene": r["scene"],
                      "source_dir": r.get("source_dir", ""), "licence": r.get("licence", ""),
                      "reuse": r.get("reuse", ""), "reuse_of": r.get("reuse_of", ""), "crop_box": r.get("crop_box", "")})
    focus = load_rules().get("focus", {})
    for k, c in enumerate(clips):
        c["motion"] = motion_for(k, c["match"])
        if Path(c["asset"]).name in focus:
            c["motion"]["focus"] = list(focus[Path(c["asset"]).name])
    return clips


def motion_for(k: int, match: str) -> Dict[str, Any]:
    """Alternating zoom in / out with a slight centre drift tied to the zoom (never reveals an edge).
    Text cards and archival-labelled stills move less and do not drift (label stays inside the frame)."""
    zmax = {"text_card": 1.03, "archival": 1.02}.get(match, 1.08)
    zin = k % 2 == 0
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1)]
    dx, dy = dirs[(k // 2) % len(dirs)]
    drift = 0.0 if match in ("text_card", "archival") else 0.015
    return {"type": "zoom_in" if zin else "zoom_out", "s0": 1.0 if zin else zmax, "s1": zmax if zin else 1.0,
            "smax": zmax, "dx": dx * drift, "dy": dy * drift}


def focus_offset(iw: int, ih: int, w: int, h: int, s: float, fx: float, fy: float) -> Tuple[float, float]:
    """Frame offset (fraction of the output frame) that moves the view centre towards image point (fx, fy),
    clamped so no edge shows at zoom s (cover-fit * s)."""
    k = max(w / iw, h / ih) * s
    sx, sy = (k * iw - w) / 2, (k * ih - h) / 2  # slack in output px
    ox = max(-sx, min(sx, -(fx - 0.5) * k * iw))
    oy = max(-sy, min(sy, -(fy - 0.5) * k * ih))
    return ox / w, oy / h


def motion_at(m: Dict[str, Any], p: float) -> Tuple[float, float, float]:
    """(scale, offset_x, offset_y) at progress p in [0,1]; offsets are fractions of the frame size."""
    p = min(1.0, max(0.0, p))
    s = m["s0"] + (m["s1"] - m["s0"]) * p
    f = (s - 1.0) / (m["smax"] - 1.0) if m["smax"] > 1.0 else 0.0
    return s, m["dx"] * f, m["dy"] * f


def write_assign_csv(rows: Sequence[Dict[str, Any]], out: str | Path) -> Path:
    clips = merge_clips(rows)
    mot = {b: c["motion"]["type"] for c in clips for b in c["beats"]}
    p = Path(out)
    p.parent.mkdir(parents=True, exist_ok=True)
    cols = BEAT_COLUMNS + (PARALLAX_COLUMNS if any(r.get("parallax_clip") for r in rows) else []) + \
        (CROP_COLUMNS if any(r.get("reuse") for r in rows) else []) + \
        (AI_MOTION_COLUMNS if any(r.get("ai_motion_clip") for r in rows) else [])
    with open(p, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({**r, "start": f"{float(r['start']):.3f}", "end": f"{float(r['end']):.3f}",
                        "duration_s": f"{float(r['end']) - float(r['start']):.2f}",
                        "first_word_time": f"{float(r['first_word_time']):.3f}",
                        "motion": "ai_animated" if r.get("ai_motion_clip") else
                        "parallax_2_5d" if r.get("parallax_clip") else
                        ("video_clip" if Path(r["asset"]).suffix.lower() in VIDEO_EXT else mot.get(r["beat"], ""))})
    return p


def read_assign_csv(path: str | Path) -> List[Dict[str, Any]]:
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rows = [dict(r) for r in csv.DictReader(fh)]
    for r in rows:
        for k in ("start", "end", "first_word_time"):
            r[k] = float(r[k])
    return rows


# --------------------------------------------------------------------------- downloads
def _slug(s: str, n: int = 40) -> str:
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:n] or "img"


def download_picks(picks: Sequence[Dict[str, Any]], out_dir: str | Path, get=None) -> Dict[str, Any]:
    """Download pool picks that are not local yet into out_dir (free licences only, standard thumbnails),
    unique names B10_<scene>_<nn>_<slug>, CREDITS.json/.txt appended. Returns {title: local path, errors}."""
    from . import commons_fetch as cf
    get = get or cf.http_get
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    cj = out / "CREDITS.json"
    credits = json.loads(cj.read_text(encoding="utf-8")) if cj.exists() else []
    have = {c["title"]: c for c in credits}
    shas = {c.get("sha256") for c in credits}
    got, errors = {}, []
    n = len(credits)
    for c in picks:
        if c.get("local_file"):
            got[c["title"]] = c["local_file"]
            continue
        if c["title"] in have:
            got[c["title"]] = str(out / have[c["title"]]["file"])
            continue
        if cf.licence_family(c.get("licence", "")) not in cf.ALLOWED or cf.SKIP_TITLE.search(c["title"]):
            errors.append({"title": c["title"], "error": "licence/3D filter"})
            continue
        try:
            data = get(cf.standard_thumb(c["thumb"], c.get("width")))
        except Exception as exc:  # pragma: no cover - network
            errors.append({"title": c["title"], "error": str(exc)[:160]})
            if len(errors) >= 6:
                break
            continue
        sha = hashlib.sha256(data).hexdigest()
        if sha in shas:
            errors.append({"title": c["title"], "error": "same bytes as an earlier download"})
            continue
        n += 1
        scene = c.get("_scene", "SXX")
        ext = ".png" if c.get("mime") == "image/png" else ".jpg"
        name = f"B10_{scene}_{n:03d}_{_slug(c['title'].replace('File:', ''))}{ext}"
        (out / name).write_bytes(data)
        shas.add(sha)
        rec = {"scene": scene, "query": "pool (beat layer v10)", "file": name, "title": c["title"], "author": c.get("author", ""),
               "licence": c.get("licence", ""), "licence_family": cf.licence_family(c.get("licence", "")),
               "licence_url": c.get("licence_url", ""), "source_page": c.get("source_page", ""), "downloaded": c.get("thumb", ""),
               "description": c.get("description", ""), "categories": c.get("categories", []),
               "rights_status": "recorded_not_cleared", "sha256": sha, "source_folder": out.name}
        credits.append(rec)
        have[c["title"]] = rec
        got[c["title"]] = str(out / name)
        cf._write_credits(out, credits)
    if credits:
        cf._write_credits(out, credits)
    return {"files": got, "errors": errors, "credits": len(credits)}


# --------------------------------------------------------------------------- preview (smooth sub-pixel motion)
def _cover_source(path: str | Path, w: int, h: int, smax: float):
    from PIL import Image
    im = Image.open(path).convert("RGB")
    k = max(w / im.width, h / im.height) * smax * 1.25  # pre-scale once; per-frame transform stays sub-pixel
    if k < 1.0:
        im = im.resize((max(1, round(im.width * k)), max(1, round(im.height * k))), Image.LANCZOS)
    return im


def frame_at(src, m: Dict[str, Any], p: float, w: int, h: int):
    """One output frame: affine (float) mapping output -> source, bilinear; no integer stepping."""
    from PIL import Image
    s, ox, oy = motion_at(m, p)
    if m.get("focus"):  # off-centre subject: no drift, the zoom closes in on the subject instead
        ox, oy = focus_offset(src.width, src.height, w, h, s, *m["focus"])
    k = max(w / src.width, h / src.height) * s
    cx = src.width / 2 - ox * w / k
    cy = src.height / 2 - oy * h / k
    a = 1.0 / k
    return src.transform((w, h), Image.AFFINE, (a, 0.0, cx - (w / 2) * a, 0.0, a, cy - (h / 2) * a),
                         resample=Image.BILINEAR)


def render_motion_video(clips: Sequence[Dict[str, Any]], resolve, t0: float, t1: float, out: str | Path,
                        w: int = 1280, h: int = 720, fps: int = 25, crf: int = 26) -> Path:
    """Video-only H.264 of [t0,t1) built frame by frame (PIL affine -> ffmpeg rawvideo pipe)."""
    import subprocess
    out = Path(out)
    n0, n1 = round(t0 * fps), round(t1 * fps)
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
                             "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf),
                             "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    cache: Dict[str, Any] = {}
    try:
        for n in range(n0, n1):
            t = (n + 0.5) / fps
            c = next((c for c in clips if c["start"] - 1e-9 <= t < c["end"]), clips[-1])
            key = c["asset"]
            if key not in cache:
                cache.clear()
                cache[key] = _cover_source(resolve(c), w, h, c["motion"]["smax"])
            p = (t - c["start"]) / max(1e-6, c["end"] - c["start"])
            proc.stdin.write(frame_at(cache[key], c["motion"], p, w, h).tobytes())
    finally:
        proc.stdin.close()
        rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"ffmpeg rawvideo encode failed ({rc})")
    return out


def shift_srt(srt_text: str, t0: float, t1: float) -> str:
    """Cues overlapping [t0,t1) re-timed to start at 0 (clipped)."""
    def ts(x: str) -> float:
        hh, mm, rest = x.strip().split(":")
        s, ms = rest.split(",")
        return int(hh) * 3600 + int(mm) * 60 + int(s) + int(ms) / 1000

    def fm(x: float) -> str:
        x = max(0.0, x)
        ms = int(round(x * 1000))
        return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
    out, n = [], 0
    for block in re.split(r"\n\s*\n", srt_text.replace("\r\n", "\n").strip()):
        lines = block.split("\n")
        tl = next((i for i, l in enumerate(lines) if "-->" in l), None)
        if tl is None:
            continue
        a, b = (ts(x) for x in lines[tl].split("-->"))
        if b <= t0 or a >= t1:
            continue
        n += 1
        out.append(f"{n}\n{fm(max(a, t0) - t0)} --> {fm(min(b, t1) - t0)}\n" + "\n".join(lines[tl + 1:]))
    return "\n\n".join(out) + "\n"


def jitter_metric(frames: Sequence[Any]) -> Dict[str, float]:
    """Mean abs frame-to-frame luma difference; integer-stepped zoom shows up as a spiky series (high max/median)."""
    import numpy as np
    arr = [np.asarray(f.convert("L"), dtype=np.float32) for f in frames]
    d = [float(np.abs(a - b).mean()) for a, b in zip(arr, arr[1:])]
    if not d:
        return {"median": 0.0, "max": 0.0, "ratio": 0.0}
    med = statistics.median(d)
    return {"median": round(med, 3), "max": round(max(d), 3), "ratio": round(max(d) / med, 2) if med else 0.0}
