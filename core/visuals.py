"""M3 Workflow G, step 2: approved LOCAL visuals per scene (manual selection, nothing invented).

scenes.json -> visuals.csv template (one row per scene: brief / asset / licence filled by the user)
-> validate against the assets folder -> visuals.json (sha256 per asset) -> Gate "visual_selection"
-> FFmpeg integration preview (selected scenes: visuals + narration + burned captions)
-> Premiere: the same assets as clips on a visual track at scene times (core/premiere.py).

Rules: an asset must exist inside the assets folder, have a non-empty brief and licence, and be an
image or a video. A video shorter than its scene is an error unless fit=loop. No downloads, no AI
generation here; a scene without an asset stays empty (not a placeholder) and is reported.
"""
from __future__ import annotations

import csv
import hashlib
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

SCHEMA = "kang.visuals/1.0"
STILL_EXT = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
VIDEO_EXT = {".mp4", ".mov", ".m4v", ".mkv", ".webm", ".avi", ".mxf"}
FITS = ("cover", "contain", "loop")  # loop = video repeats to fill the scene (cover framing)
COLUMNS = ["scene", "start", "end", "duration_s", "narration", "brief", "asset", "asset_in_s", "fit", "licence", "notes", "shot_start"]
MIN_SHOT_S = 2.0  # a shot shorter than this is a flash, not a visual


def _sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def write_template(plan: Dict[str, Any], out_csv: str | Path) -> Path:
    """One row per scene; brief/asset/licence blank for the user. Narration shown for context only."""
    out = Path(out_csv)
    with open(out, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, COLUMNS)
        w.writeheader()
        for s in plan["scenes"]:
            w.writerow({"scene": s["id"], "start": f"{s['start']:.3f}", "end": f"{s['end']:.3f}",
                        "duration_s": f"{s['end'] - s['start']:.2f}", "narration": s["text"][:220],
                        "brief": "", "asset": "", "asset_in_s": "0", "fit": "cover", "licence": "", "notes": "", "shot_start": ""})
    return out


def read_csv(path: str | Path) -> List[Dict[str, str]]:
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return [{k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(fh)]


def asset_kind(p: Path) -> Optional[str]:
    ext = p.suffix.lower()
    return "still" if ext in STILL_EXT else "video" if ext in VIDEO_EXT else None


def validate(rows: Sequence[Dict[str, str]], plan: Dict[str, Any], assets_dir: str | Path,
             probe=None) -> Dict[str, Any]:
    """-> {ok, problems, warnings, visuals: kang.visuals/1.0 dict}. `probe(path)->{duration}` for videos
    (defaults to runs.media_summary). Scene times always come from scenes.json, never from the CSV."""
    if probe is None:
        from .runs import media_summary as probe
    adir = Path(assets_dir).resolve()
    scenes = {s["id"]: s for s in plan["scenes"]}
    problems: List[str] = []
    warnings: List[str] = []
    items: List[Dict[str, Any]] = []
    # Several rows per scene = shots. Row 1 starts at the scene start; each further row needs
    # shot_start (timeline seconds, inside the scene, increasing). A shot ends where the next begins.
    groups: Dict[str, List[Dict[str, str]]] = {}
    for r in rows:
        sid = r.get("scene", "")
        if sid not in scenes:
            problems.append(f"{sid or '?'}: scene not in scenes.json")
            continue
        if r.get("asset"):
            groups.setdefault(sid, []).append(r)
    for sid, grp in groups.items():
        sc = scenes[sid]
        starts: List[float] = []
        bad = False
        for k, r in enumerate(grp):
            if k == 0:
                if r.get("shot_start") and abs(float(r["shot_start"]) - sc["start"]) > 0.002:
                    problems.append(f"{sid}: first shot must start at the scene start ({sc['start']:.3f})")
                    bad = True
                starts.append(sc["start"])
                continue
            try:
                t = float(r.get("shot_start") or "nan")
            except ValueError:
                t = float("nan")
            if t != t:
                problems.append(f"{sid}: shot {k + 1} needs shot_start (seconds on the timeline)")
                bad = True
                break
            if not (starts[-1] + MIN_SHOT_S <= t <= sc["end"] - MIN_SHOT_S):
                problems.append(f"{sid}: shot {k + 1} shot_start {t:.3f} must be >= previous+{MIN_SHOT_S}s and "
                                f"<= scene end-{MIN_SHOT_S}s ({sc['start']:.3f}-{sc['end']:.3f})")
                bad = True
                break
            starts.append(t)
        if bad:
            continue
        ends = starts[1:] + [sc["end"]]
        for k, (r, t0, t1) in enumerate(zip(grp, starts, ends)):
            shot = sid if len(grp) == 1 else f"{sid}.{k + 1}"
            dur = round(t1 - t0, 3)
            p = (adir / r["asset"]).resolve()
            try:
                p.relative_to(adir)
            except ValueError:
                problems.append(f"{shot}: asset outside the assets folder: {r['asset']}")
                continue
            if not p.is_file():
                problems.append(f"{shot}: asset not found: {r['asset']}")
                continue
            kind = asset_kind(p)
            if kind is None:
                problems.append(f"{shot}: unsupported asset type {p.suffix}")
                continue
            if not r.get("brief"):
                problems.append(f"{shot}: brief is empty")
            if not r.get("licence"):
                problems.append(f"{shot}: licence is empty (own / CC-BY ... / licensed - write it)")
            fit = (r.get("fit") or "cover").lower()
            if fit not in FITS:
                problems.append(f"{shot}: fit must be one of {FITS}")
                continue
            try:
                a_in = float(r.get("asset_in_s") or 0)
            except ValueError:
                problems.append(f"{shot}: asset_in_s is not a number")
                continue
            item = {"scene": sid, "shot": shot, "start": t0, "end": t1, "duration": dur, "asset": r["asset"],
                    "kind": kind, "fit": fit, "asset_in": a_in, "brief": r.get("brief", ""),
                    "licence": r.get("licence", ""), "sha256": _sha(p)}
            if kind == "video":
                alen = float(probe(p).get("duration") or 0)
                item["asset_duration"] = round(alen, 3)
                if a_in < 0 or a_in >= alen:
                    problems.append(f"{shot}: asset_in_s {a_in} outside clip (0-{alen:.2f} s)")
                elif alen - a_in < dur - 0.04 and fit != "loop":
                    problems.append(f"{shot}: clip has {alen - a_in:.2f} s from asset_in_s, scene needs {dur:.2f} s "
                                    f"(trim scene, pick a longer clip, or fit=loop)")
            elif fit == "loop":
                problems.append(f"{shot}: fit=loop is for video clips only")
            items.append(item)
    dup = sorted({i["asset"] for i in items if sum(j["asset"] == i["asset"] for j in items) > 1})
    if dup:
        warnings.append(f"asset used in more than one shot: {', '.join(dup[:6])}")
    missing = [s for s in scenes if s not in {i["scene"] for i in items}]
    if missing:
        warnings.append(f"{len(missing)} scene(s) without a visual: {', '.join(missing[:12])}"
                        + (" ..." if len(missing) > 12 else ""))
    visuals = {"schema": SCHEMA, "assets_dir": str(adir), "items": items, "scenes_without_visual": missing}
    return {"ok": not problems, "problems": problems, "warnings": warnings, "visuals": visuals}


def selection_text(visuals: Dict[str, Any]) -> str:
    """What the approver sees at the visual_selection gate."""
    lines = [f"{len(visuals['items'])} scene visual(s); without visual: {len(visuals['scenes_without_visual'])}"]
    for i in visuals["items"]:
        lines.append(f"{i.get('shot', i['scene'])} {i['start']:.1f}-{i['end']:.1f}s {i['kind']} {i['asset']} [{i['fit']}] "
                     f"licence={i['licence']} | {i['brief'][:80]}")
    return "\n".join(lines)


def pick(visuals: Dict[str, Any], plan: Dict[str, Any], scene_ids: Sequence[str]) -> List[Dict[str, Any]]:
    """Selected scenes, in order, contiguous, each with a visual (the preview never shows gaps)."""
    order = [s["id"] for s in plan["scenes"]]
    bad = [s for s in scene_ids if s not in order]
    if bad:
        raise ValueError(f"unknown scene(s): {bad}")
    idx = sorted(order.index(s) for s in scene_ids)
    if idx != list(range(idx[0], idx[-1] + 1)):
        raise ValueError("preview scenes must be contiguous (e.g. S01,S02,S03)")
    sel = [order[k] for k in idx]
    have = {i["scene"] for i in visuals["items"]}
    no = [s for s in sel if s not in have]
    if no:
        raise ValueError(f"scene(s) without an approved visual: {no}")
    return sorted((i for i in visuals["items"] if i["scene"] in sel), key=lambda i: i["start"])


def _vf(fit: str, w: int, h: int, fps: int) -> str:
    if fit == "contain":
        geo = f"scale={w}:{h}:force_original_aspect_ratio=decrease,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black"
    else:
        geo = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
    return f"{geo},setsar=1,fps={fps},format=yuv420p"


def segment_args(item: Dict[str, Any], src: Path, out: Path, dur: float, w: int, h: int, fps: int) -> List[str]:
    """ffmpeg args for one scene segment: exact frame count, same codec params for every segment
    (so the concat demuxer can join them without re-encoding)."""
    nframes = max(1, int(round(dur * fps)))
    if item["kind"] == "still":
        inp = ["-loop", "1", "-framerate", str(fps), "-i", str(src)]
    else:
        inp = (["-stream_loop", "-1"] if item["fit"] == "loop" else []) + ["-ss", f"{item['asset_in']:.3f}", "-i", str(src)]
    return [*inp, "-an", "-vf", _vf(item["fit"], w, h, fps), "-frames:v", str(nframes),
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p",
            "-r", str(fps), "-video_track_timescale", str(fps * 1000), str(out)]
