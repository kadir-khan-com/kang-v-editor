"""v13 commands: `motion-build` (cards + maps into a visuals_beats CSV), `motion-grid`, `motion-preview`.

Priority (per beat): exact > parallax of the same place > MAP / CARD > representative stock > continued_with_motion.
So a card / map may only take a beat whose current visual is NOT exact (representative pool / v9 / stock, an old
static card, or a continued_with_motion hold). Exact shots are never removed (checked, FAIL otherwise).
Every card / map is one MP4 (1920x1080, 25 fps, H.264, no audio) that covers exactly its beats; it is a new
unique asset, so the no-repeat rule holds. Resumable: clips render until the time budget is used.
"""
from __future__ import annotations

import csv
import json
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

from . import beats as B
from . import map_route as M
from . import motion_cards as MC
from .runs import Run, media_summary, write_json

ROOT = Path(__file__).resolve().parent.parent
WORDS = ROOT / "runs" / "2026-10-31_KANG_004" / "words.json"
HWORDS = ROOT / "runs" / "2026-11-01_KANG_001" / "words_hinglish_v1_accepted.json"
VALUE_COLS = ["clip", "type", "phase", "item", "shown_text", "value", "word_ids", "hindi", "hinglish", "word_time", "shown_at",
              "display_lead_s", "lead_s", "status", "note"]
LICENCE = "own work (KANG generated)"


def _rel(p: Path) -> str:
    try:
        return Path(p).resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(Path(p).resolve())


def load_words(words_path=None, hw_path=None):
    w = json.loads(Path(words_path or WORDS).read_text(encoding="utf-8"))
    hw = json.loads(Path(hw_path or HWORDS).read_text(encoding="utf-8"))["words"]
    if len(w) != len(hw):
        raise ValueError("Hindi and Hinglish word lists differ in length")
    return w, hw


def plan_all(spec: Dict[str, Any], rows: Sequence[Dict[str, Any]], words, hw) -> Dict[str, Any]:
    beats = {r["beat"]: r for r in rows}
    plans, problems = [], []
    for c in spec.get("cards", []):
        plans.append(MC.plan_card(c, beats, words, hw, spec["safe_zone"]))
    places = M.load_places()
    for m in spec.get("maps", []):
        plans.append(M.plan_map(m, beats, words, hw, places))
    seen: Dict[str, str] = {}
    for p in plans:
        problems += p["problems"]
        for b in p["beats"]:
            if b in seen:
                problems.append(f"beat {b} used by {seen[b]} and {p['id']}")
            seen[b] = p["id"]
            r = beats[b]
            if r["match"] == "exact" and r["role"] != "continued_with_motion":
                problems.append(f"{p['id']}: beat {b} is an exact shot ({r['asset']}) - exact shots are never replaced")
    return {"plans": plans, "problems": problems}


def integrate(rows: Sequence[Dict[str, Any]], plans: Sequence[Dict[str, Any]], clip_dir: str) -> List[Dict[str, Any]]:
    out = [dict(r) for r in rows]
    by = {r["beat"]: r for r in out}
    for p in plans:
        for k, b in enumerate(p["beats"]):
            r = by[b]
            was = f"{r['asset']} [{r['match']}/{r['role']}]"
            r.update(asset=p["file"], source_dir=clip_dir, asset_source="kang_motion", match=p["type"],
                     role=("motion_" + ("card" if p["type"] == "text_card" else "map")) if k == 0 else "card_hold",
                     licence=LICENCE, title=p["title"], source_page="", parallax_clip="", parallax_dir="", parallax_status="",
                     notes=f"v13 {p['type']} {p['id']} (values read from narration word ids, see card_values.csv); "
                           f"replaced {was}; agent-made, not human-reviewed")
    return out


def _title(p: Dict[str, Any]) -> str:
    if p["type"] == "map":
        names = []
        for s in p["shows"]:
            if s["label"] not in names:
                names.append(s["label"])
        return f"Animated map {p['id'].split('_')[0]}: " + " / ".join(names) + " (Natural Earth public domain; © OpenStreetMap contributors, ODbL)"
    first = next((l["text"] for ph in p["phases"] for l in ph["visible"] if l["role"] in ("title", "big", "text")), p["id"])
    return f"Moving text card {p['id'].split('_')[0]}: {first}"


def qa_plans(plans: Sequence[Dict[str, Any]], safe: Dict[str, int]) -> Dict[str, Any]:
    """Safe zone (nothing below the caption line), inside the frame, label overlaps (WARN), clip lengths."""
    fails, warns = [], []
    rend = M.MapRenderer(M.load_map_data())
    for p in plans:
        boxes = MC.card_boxes(p) if p["type"] == "text_card" else M.map_boxes(p, rend)
        if p["type"] == "map":  # v13b: label margin (5 %) + pixel check that nothing is drawn below the caption line
            fails += [f"{p['id']}: {x}" for x in M.label_box_problems(boxes)]
            fails += M.safe_zone_problems(p, rend)
        for t, (x0, y0, x1, y1) in boxes:
            if t.split(":")[-1].startswith("route"):
                continue  # route extents may leave the frame; their pixels are checked by safe_zone_problems
            if y1 > safe["bottom_px"] or x0 < 0 or x1 > 1920 or y0 < 0:
                fails.append(f"{p['id']}: '{t}' box {x0},{y0},{x1},{y1} outside safe zone (bottom {safe['bottom_px']})")
            if p["type"] == "text_card" and x1 > safe["right_px"]:
                fails.append(f"{p['id']}: '{t}' runs past {safe['right_px']} px")
        if p["type"] == "map":
            for tag in sorted({t.split(":", 1)[0] for t, _ in boxes}):  # one sample time at a time
                bx = [(t, b) for t, b in boxes if t.split(":", 1)[0] == tag]
                bx = [x for x in bx if not x[0].split(":", 1)[1].startswith("route")]
                for i in range(len(bx)):
                    for j in range(i + 1, len(bx)):
                        a, b = bx[i][1], bx[j][1]
                        if a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]:
                            warns.append(f"{p['id']}: labels overlap {bx[i][0]} / {bx[j][0]}")
    return {"fail": fails, "warn": warns}


def build_cmd(assign_csv: str, out: str, *, spec_path: Optional[str] = None, run_id: Optional[str] = None,
              budget_s: float = 95.0, only: Sequence[str] = ()) -> Dict[str, Any]:
    t_start = time.time()
    run = Run(run_id) if run_id else Run()
    spec_p = Path(spec_path) if spec_path else MC.SPEC
    if not run_id:
        for p, k in ((assign_csv, "VISUALS_BEATS"), (str(spec_p), "MOTION_SPEC"), (str(WORDS), "W1"), (str(HWORDS), "W_HINGLISH"),
                     (str(M.MAP_DATA), "MAP_DATA_NE"), (str(M.FINE_DATA), "MAP_DATA_OSM"), (str(M.PLACES), "MAP_PLACES")):
            run.add_input(p, k)
    spec = MC.load_spec(spec_p)
    words, hw = load_words()
    rows = B.read_assign_csv(assign_csv)
    pa = plan_all(spec, rows, words, hw)
    plans = pa["plans"]
    clip_dir = run.path("motion_clips")
    clip_dir.mkdir(exist_ok=True)
    for p in plans:
        p["file"] = f"{'MAP' if p['type'] == 'map' else 'CARD'}_{p['id']}.mp4"
        p["title"] = _title(p)
    vrows = [r for p in plans for r in p["rows"]]
    with open(run.path("card_values.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, VALUE_COLS)
        w.writeheader()
        for r in vrows:
            w.writerow({k: r.get(k, "") for k in VALUE_COLS})
    qa = qa_plans(plans, spec["safe_zone"])
    hard = pa["problems"] + qa["fail"] + lead_fails(vrows)
    if hard:
        run.set_status("qa_failed")
        write_json(run.path("motion_plan_problems.json"), {"problems": hard, "warn": qa["warn"]})
        return {"run_id": run.run_id, "status": "qa_failed", "problems": hard, "warn": qa["warn"], "qa": {"pass": False}}
    data = M.load_map_data()
    pending, done = [], []
    for p in plans:
        dst = clip_dir / p["file"]
        mark = clip_dir / (p["file"] + ".json")
        if dst.is_file() and mark.is_file():
            done.append(p["id"])
            continue
        if (only and p["id"] not in only) or time.time() - t_start > budget_s:
            pending.append(p["id"])
            continue
        tmp = dst.with_suffix(".tmp.mp4")
        t0 = time.time()
        res = MC.render_card(p, tmp) if p["type"] == "text_card" else M.render_map(p, tmp, data)
        tmp.replace(dst)
        info = media_summary(dst)
        write_json(mark, {**res, "need_frames": p["frames"], "render_s": round(time.time() - t0, 1),
                          "duration": info.get("duration"), "has_audio": info.get("has_audio"),
                          "width": info.get("width"), "height": info.get("height")})
        done.append(p["id"])
    if pending:
        run.set_status("partial")
        return {"run_id": run.run_id, "status": "partial", "rendered": len(done), "pending": pending,
                "next": f"run again with --run {run.run_id}", "qa": {"pass": False}}
    # all clips rendered: integrate + checks
    new = integrate(rows, plans, _rel(clip_dir))
    credits, clip_checks = [], []
    for p in plans:
        mk = json.loads((clip_dir / (p["file"] + ".json")).read_text(encoding="utf-8"))
        clip_checks.append({"clip": p["file"], "frames": mk["frames"], "need": p["frames"], "has_audio": mk["has_audio"],
                            "size": f"{mk['width']}x{mk['height']}", "seconds": round(p["end"] - p["start"], 2)})
        credits.append(credit_rec(p, clip_dir))
    write_json(clip_dir / "CREDITS.json", credits)
    qa_a = B.assign_qa(new)
    bad_len = [c["clip"] for c in clip_checks if c["frames"] != c["need"] or c["has_audio"] or c["size"] != "1920x1080"]
    missing = [r["beat"] for r in new if not (ROOT / r["source_dir"] / r["asset"]).is_file()]
    probs = ([f"duplicates {qa_a['duplicates']}"] if qa_a["duplicates"] else []) + ([f"clip length/audio/size {bad_len}"] if bad_len else []) + \
        ([f"missing files {missing[:5]}"] if missing else [])
    before = {Path(r["asset"]).name for r in rows}
    after = {Path(r["asset"]).name for r in new}
    removed = sorted(before - after)
    op = B.write_assign_csv(new, run.path(Path(out).name))
    summ = op.with_suffix(".json")
    clips = B.merge_clips(new)
    longest = max(clips, key=lambda c: c["end"] - c["start"])
    write_json(summ, {"schema": "kang.motion_build/1.0", "assign_csv": assign_csv, "spec": _rel(spec_p),
                      "priority": "exact > parallax same place > map/card > representative stock > continued_with_motion",
                      "clips": clip_checks, "removed_assets": removed, "qa": qa_a, "problems": probs, "warn": qa["warn"],
                      "value_rows": len(vrows), "value_status": _count(vrows),
                      "longest_shot": {"first_beat": longest["first_beat"], "asset": longest["asset"],
                                       "seconds": round(longest["end"] - longest["start"], 2), "match": longest["match"]},
                      "selected_by": "agent_under_user_delegation", "human_reviewed": False})
    run.add_output(op, "visuals_beats_csv")
    run.add_output(summ, "visuals_beats_summary")
    run.add_output(run.path("card_values.csv"), "card_values_csv")
    run.add_output(clip_dir / "CREDITS.json", "motion_credits")
    for p in plans:
        run.add_output(clip_dir / p["file"], "motion_clip")
    run.log_step("motion_build", clips=len(plans), labels=qa_a["labels_by_shot"], removed=len(removed))
    run.set_status("qa_failed" if probs else "done")
    return {"run_id": run.run_id, "csv": str(op), "summary": str(summ), "clips": clip_checks, "removed_assets": removed,
            "labels": qa_a["labels_by_shot"], "roles": qa_a["roles"], "longest": longest["end"] - longest["start"],
            "warn": qa["warn"], "value_status": _count(vrows), "qa": {"pass": not probs, **qa_a}, "problems": probs}


def lead_fails(vrows) -> List[str]:
    """v13b: card_values rows with lead_s > 0.25 s (value / label shown before it is spoken)."""
    return [f"{r['clip']}: '{r['shown_text']}' value {r['value']} lead {r['lead_s']} s > {M.MAX_LEAD_S} s"
            for r in vrows if r.get("status") == "FAIL" and r.get("lead_s") not in ("", None)]


def write_values_csv(path, vrows) -> None:
    with open(path, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, VALUE_COLS)
        w.writeheader()
        for r in vrows:
            w.writerow({k: r.get(k, "") for k in VALUE_COLS})


def changed_clips(plans, old_values_csv) -> List[str]:
    """Clips whose value rows (shown text / time / status) differ from an earlier card_values.csv."""
    old: Dict[str, list] = {}
    with open(old_values_csv, encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            old.setdefault(r["clip"], []).append((r["item"], r["shown_text"], r["value"], f"{float(r['shown_at']):.3f}", r["status"]))
    out = []
    for p in plans:
        new = [(r["item"], r["shown_text"], str(r["value"]), f"{float(r['shown_at']):.3f}", r["status"]) for r in p["rows"]]
        if new != old.get(p["id"]):
            out.append(p["id"])
    return out


def credit_rec(p: Dict[str, Any], clip_dir: Path, note_extra: str = "") -> Dict[str, Any]:
    rec = {"scene": p["beats"][0].split("_")[0], "file": p["file"], "title": p["title"], "author": "KANG", "licence": LICENCE,
           "licence_family": "own", "source_folder": _rel(clip_dir), "used_on_beats": p["beats"], "match": p["type"],
           "note": "Own work: KANG-rendered motion graphic (numpy/Pillow/OpenCV + FFmpeg); fonts Mukta / Montserrat (SIL OFL 1.1). "
                   "Every number / time / name read from the narration words (card_values.csv)." + note_extra}
    if p["type"] == "map":
        rec["data_credits"] = ["Natural Earth 1:10m land + admin lines (public domain)",
                               "© OpenStreetMap contributors (ODbL 1.0): Devbhumi Dwaraka / Jamnagar district coast polygons, Gopi Talav point",
                               "Wikidata coordinates (CC0)"]
        rec["source_page"] = "https://www.openstreetmap.org/copyright"
    if p.get("replaces_card"):
        rec["replaces"] = p["replaces_card"] + " (static v9 card; original file untouched)"
    return rec


def value_display_problems(plans) -> List[str]:
    """v17b FAIL list: frame-by-frame (render plan) - any shown number differing from its final value, a km badge not
    final, a place label not fully visible at its spoken word."""
    out: List[str] = []
    for p in plans:
        out += (MC.displayed_value_problems(p) if p["type"] == "text_card" else M.displayed_value_problems(p))
    return out


def fix_build_cmd(base_run: str, out_name: str, *, force: Sequence[str] = (), run_id: Optional[str] = None,
                  budget_s: float = 95.0, base_csv: Optional[str] = None, base_values: Optional[str] = None) -> Dict[str, Any]:
    """v13b: re-plan every card / map with the current code + spec, re-render ONLY the clips that changed
    (value rows differ from the base run's card_values.csv, beats changed, or listed in --force) into a new run;
    the other beats keep pointing at the base run's clips. Writes <out_name> (copy of the base CSV) + card_values.csv."""
    t_start = time.time()
    bd = ROOT / "runs" / base_run
    base_csv = Path(base_csv) if base_csv else bd / "visuals_beats_v13.csv"  # v17b: any visuals CSV (e.g. v17) as base
    base_values = Path(base_values) if base_values else bd / "card_values.csv"
    run = Run(run_id) if run_id else Run()
    if not run_id:
        for pth, k in ((str(base_csv), "VISUALS_BEATS_BASE"), (str(base_values), "CARD_VALUES_BASE"), (str(MC.SPEC), "MOTION_SPEC"),
                       (str(WORDS), "W1"), (str(HWORDS), "W_HINGLISH"), (str(M.MAP_DATA), "MAP_DATA_NE"), (str(M.FINE_DATA), "MAP_DATA_OSM"),
                       (str(M.PLACES), "MAP_PLACES")):
            run.add_input(pth, k)
    spec = MC.load_spec()
    words, hw = load_words()
    rows = B.read_assign_csv(str(base_csv))
    by = {r["beat"]: r for r in rows}
    pa = plan_all(spec, rows, words, hw)
    plans = pa["plans"]
    clip_dir = run.path("motion_clips")
    clip_dir.mkdir(exist_ok=True)
    affected = set(changed_clips(plans, base_values)) | set(force)
    for p in plans:
        p["file"] = f"{'MAP' if p['type'] == 'map' else 'CARD'}_{p['id']}.mp4"
        p["title"] = _title(p)
        if any(by[b]["asset"] != p["file"] for b in p["beats"]):
            affected.add(p["id"])
    vrows = [r for p in plans for r in p["rows"]]
    write_values_csv(run.path("card_values.csv"), vrows)
    qa_mark = run.path("motion_plan_qa.json")
    if qa_mark.is_file():  # resumed run: the plan QA (renders check frames, ~30 s) already passed
        qa = json.loads(qa_mark.read_text(encoding="utf-8"))
    else:
        qa = qa_plans(plans, spec["safe_zone"])
        qa["value_display_fail"] = value_display_problems(plans)
    hard = pa["problems"] + qa["fail"] + qa.get("value_display_fail", []) + lead_fails(vrows)
    if hard:
        run.set_status("qa_failed")
        write_json(run.path("motion_plan_problems.json"), {"problems": hard, "warn": qa["warn"]})
        return {"run_id": run.run_id, "status": "qa_failed", "problems": hard, "warn": qa["warn"]}
    write_json(qa_mark, qa)
    data = M.load_map_data()
    pending = []
    for p in plans:
        if p["id"] not in affected:
            continue
        dst, mark = clip_dir / p["file"], clip_dir / (p["file"] + ".json")
        if dst.is_file() and mark.is_file():
            continue
        if time.time() - t_start > budget_s:
            pending.append(p["id"])
            continue
        tmp = dst.with_suffix(".tmp.mp4")
        t0 = time.time()
        res = MC.render_card(p, tmp) if p["type"] == "text_card" else M.render_map(p, tmp, data)
        tmp.replace(dst)
        info = media_summary(dst)
        write_json(mark, {**res, "need_frames": p["frames"], "render_s": round(time.time() - t0, 1), "duration": info.get("duration"),
                          "has_audio": info.get("has_audio"), "width": info.get("width"), "height": info.get("height")})
    if pending:
        run.set_status("partial")
        return {"run_id": run.run_id, "status": "partial", "pending": pending, "next": f"run again with --run {run.run_id}"}
    re_plans = [p for p in plans if p["id"] in affected]
    write_json(clip_dir / "CREDITS.json", [credit_rec(p, clip_dir, " v17b fix re-render: values shown final (no count-up), "
                                                       "labels full opacity at their word, route chips beside their route.")
                                           for p in re_plans])  # v17b: the package reads credits per source folder
    run.add_output(clip_dir / "CREDITS.json", "motion_credits")
    new = integrate(rows, re_plans, _rel(clip_dir))
    checks = []
    for p in re_plans:
        mk = json.loads((clip_dir / (p["file"] + ".json")).read_text(encoding="utf-8"))
        checks.append({"clip": p["file"], "frames": mk["frames"], "need": p["frames"], "has_audio": mk["has_audio"],
                       "size": f"{mk['width']}x{mk['height']}", "seconds": round(p["end"] - p["start"], 2)})
    bad_len = [c["clip"] for c in checks if c["frames"] != c["need"] or c["has_audio"] or c["size"] != "1920x1080"]
    missing = [r["beat"] for r in new if not (ROOT / r["source_dir"] / r["asset"]).is_file()]
    qa_a = B.assign_qa(new)
    removed = sorted({Path(r["asset"]).name for r in rows} - {Path(r["asset"]).name for r in new})
    op = B.write_assign_csv(new, run.path(out_name))
    probs = ([f"duplicates {qa_a['duplicates']}"] if qa_a["duplicates"] else []) + ([f"clip length/audio/size {bad_len}"] if bad_len else []) + \
        ([f"missing files {missing[:5]}"] if missing else [])
    write_json(op.with_suffix(".json"), {"schema": "kang.motion_fix/1.0", "base_csv": _rel(base_csv), "spec": _rel(MC.SPEC),
                                         "re_rendered": sorted(affected), "kept_from_base": sorted(p["id"] for p in plans if p["id"] not in affected),
                                         "clips": checks, "removed_assets": removed, "qa": qa_a, "problems": probs, "warn": qa["warn"],
                                         "value_status": _count(vrows), "human_reviewed": False})
    run.add_output(op, "visuals_beats_csv")
    run.add_output(op.with_suffix(".json"), "visuals_beats_summary")
    run.add_output(run.path("card_values.csv"), "card_values_csv")
    for p in re_plans:
        run.add_output(clip_dir / p["file"], "motion_clip")
    run.log_step("motion_fix_build", re_rendered=sorted(affected), removed=removed)
    run.set_status("qa_failed" if probs else "done")
    return {"run_id": run.run_id, "status": "qa_failed" if probs else "done", "csv": str(op), "re_rendered": sorted(affected),
            "removed_assets": removed, "value_status": _count(vrows), "warn": qa["warn"], "problems": probs, "clips": checks}


def _count(vrows):
    out: Dict[str, int] = {}
    for r in vrows:
        out[r["status"]] = out.get(r["status"], 0) + 1
    return out


# --------------------------------------------------------------------------- grid + preview
def motion_plans_from_run(run_dir: Path):
    spec = MC.load_spec()
    words, hw = load_words()
    rows = B.read_assign_csv(json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))["inputs"][0]["path"])
    pa = plan_all(spec, rows, words, hw)
    for p in pa["plans"]:
        p["file"] = f"{'MAP' if p['type'] == 'map' else 'CARD'}_{p['id']}.mp4"
    return pa["plans"]


def grid_cmd(build_run: str, out: str, cols: int = 4) -> Dict[str, Any]:
    """One tile per phase of every card / map, taken from the RENDERED clip (end of phase), with id + label."""
    from PIL import Image, ImageDraw, ImageFont
    rd = ROOT / "runs" / build_run
    plans = motion_plans_from_run(rd)
    run = Run()
    run.add_input(str(rd / "visuals_beats_v13.csv") if (rd / "visuals_beats_v13.csv").is_file() else str(rd / "manifest.json"), "BUILD")
    tmp = Path(tempfile.mkdtemp(prefix="kang_mgrid_"))
    tiles = []
    for p in plans:
        times = MC.phase_sample_times(p) if p["type"] == "text_card" else M.phase_sample_times(p)
        for k, T in enumerate(times):
            fp = tmp / f"{p['id']}_{k}.jpg"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{T - p['start']:.3f}", "-i", str(rd / "motion_clips" / p["file"]),
                            "-frames:v", "1", "-vf", "scale=480:270", str(fp)], check=True)
            tiles.append((Image.open(fp).convert("RGB"), f"{p['id']} p{k + 1}/{len(times)}",
                          f"{p['type']} {p['beats'][0]}..{p['beats'][-1]} {p['start']:.1f}-{p['end']:.1f}s"))
    font = ImageFont.truetype(str(ROOT / "fonts" / "Mukta-ExtraBold.ttf"), 15)
    tw, th = 480, 270 + 42
    rows_n = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows_n * th), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    for k, (im, a, b) in enumerate(tiles):
        x, y = (k % cols) * tw, (k // cols) * th
        sheet.paste(im, (x, y))
        d.line([(x, y + int(270 * 800 / 1080)), (x + tw, y + int(270 * 800 / 1080))], fill=(220, 60, 60), width=1)  # caption line
        d.text((x + 4, y + 272), a, fill=(255, 220, 90), font=font)
        d.text((x + 4, y + 291), b, fill=(220, 220, 220), font=font)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=88)
    shutil.copy2(out, run.path(Path(out).name))
    run.add_output(run.path(Path(out).name), "motion_grid")
    run.log_step("motion_grid", tiles=len(tiles))
    run.set_status("done")
    return {"run_id": run.run_id, "grid": out, "tiles": len(tiles)}


def preview_cmd(build_run: str, media: str, captions: str, out: str, *, run_id: Optional[str] = None,
                budget_s: float = 90.0, w: int = 1280) -> Dict[str, Any]:
    """Only the card / map beats back to back (timeline order), narration audio of each range, Hinglish captions burned."""
    from .render import _filter_path
    t_start = time.time()
    rd = ROOT / "runs" / build_run
    plans = sorted(motion_plans_from_run(rd), key=lambda p: p["start"])
    run = Run(run_id) if run_id else Run()
    if not run_id:
        run.add_input(media, "A1")
        run.add_input(captions, "CAPTIONS")
        run.add_input(str(rd / "visuals_beats_v13.csv"), "VISUALS_BEATS_V13")
    parts = run.path("preview_parts")
    parts.mkdir(exist_ok=True)
    srt_all = Path(captions).read_text(encoding="utf-8-sig")
    fonts = ROOT / "fonts"
    for k, p in enumerate(plans):
        part = parts / f"part_{k:02d}.mp4"
        if part.is_file() and part.stat().st_size > 0:
            continue
        if time.time() - t_start > budget_s:
            run.set_status("preview_partial")
            return {"run_id": run.run_id, "status": "partial", "done": k, "of": len(plans), "next": f"--run {run.run_id}"}
        dur = round(p["end"] * 25) / 25 - round(p["start"] * 25) / 25
        srt = parts / f"part_{k:02d}.srt"
        srt.write_text(B.shift_srt(srt_all, p["start"], p["end"]), encoding="utf-8")
        tag = f"{p['id']}  {p['start']:.1f}s".replace(":", "\\:")
        vf = (f"scale={w}:-2:flags=lanczos,subtitles=filename='{_filter_path(srt)}':fontsdir='{_filter_path(fonts)}'"
              f":force_style='FontName=Mukta ExtraBold,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
              f"BorderStyle=1,Outline=2,Shadow=0,MarginV=22',"
              f"drawtext=fontfile='{_filter_path(fonts / 'Mukta-ExtraBold.ttf')}':text='{tag}':x=10:y=8:fontsize=16:"
              f"fontcolor=white@0.85:box=1:boxcolor=black@0.45:boxborderw=4")
        tmp = part.with_suffix(".tmp.mp4")
        r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(rd / "motion_clips" / p["file"]), "-ss", f"{p['start']:.3f}",
                            "-t", f"{dur:.3f}", "-i", media, "-map", "0:v", "-map", "1:a", "-vf", vf, "-c:v", "libx264",
                            "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", "-r", "25", "-c:a", "aac", "-b:a", "128k",
                            "-ar", "48000", "-ac", "2", "-t", f"{dur:.3f}", str(tmp)], capture_output=True, text=True, encoding="utf-8",
                           errors="replace")
        if r.returncode != 0:
            raise RuntimeError(r.stderr[-400:])
        tmp.replace(part)
    lst = parts / "concat.txt"
    lst.write_text("".join(f"file '{(parts / f'part_{k:02d}.mp4').resolve().as_posix()}'\n" for k in range(len(plans))), encoding="utf-8")
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy",
                    "-movflags", "+faststart", out], check=True)
    shutil.copy2(out, run.path(Path(out).name))
    pm = media_summary(out)
    want = sum(round(p["end"] * 25) / 25 - round(p["start"] * 25) / 25 for p in plans)
    ok = abs(pm["duration"] - want) < 0.5 and pm["has_audio"] and pm.get("width") == w
    run.add_output(run.path(Path(out).name), "motion_preview")
    run.log_step("motion_preview", clips=len(plans), seconds=round(pm["duration"], 2))
    run.set_status("done" if ok else "qa_failed")
    return {"run_id": run.run_id, "status": "done", "preview": out, "duration": round(pm["duration"], 2), "expected": round(want, 2),
            "width": pm.get("width"), "qa": {"pass": ok}}
