"""Combined review video + contact sheet + review CSV for a beats timeline (v17, Dwarika).

Real timeline segments rendered from the visuals_beats CSV the package was built from: video clips (cards, maps,
parallax, stock, YouTube CC, AI motion) are the package files trimmed exactly like the xmeml clipitems (in = 0 at the
clip start); stills use the same Ken Burns renderer as `beats-preview` (core.beats.render_motion_video). Narration
audio + accepted Hinglish captions are burned in; every shot gets a top-left tag (feature + label + beat id).
A 2 s Hinglish title slate precedes each segment. One A/B segment shows the same window cut on LEAD vs LAG beats.

Resumable (one command per step, each fits a 120 s shell limit):
  python scripts/combined_review.py seg  --run RUN K   render segment K (0-based; 'all' = every missing one)
  python scripts/combined_review.py join --run RUN     concat -> out/<name>.mp4, review CSV
  python scripts/combined_review.py sheet --run RUN    contact sheet of every shot of the full timeline
The run is created by `init` (records inputs). UTF-8 everywhere.

v17b: `init --profile v17b` records the profile in the run (review_profile.json; later steps read it), then
  python scripts/combined_review.py reuse --run RUN    copy every segment whose shots (asset, folder, timing) are
                                                       identical to the base review run's; seg renders the rest.
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from core import beats as B  # noqa: E402
from core import beats_package as bpk  # noqa: E402
from core.runs import Run  # noqa: E402

W, H, FPS = 1280, 720, 25
FONT = ROOT / "fonts" / "Mukta-ExtraBold.ttf"
MEDIA = "runs/2026-11-02_KANG_006/premiere_package/media/dwarika.mp3"
VISUALS = "runs/2026-11-04_KANG_027/visuals_beats_v17.csv"
CAPTIONS = "runs/2026-11-01_KANG_001/captions_hinglish_v1_accepted.srt"
BEATS_LEAD = "runs/2026-11-03_KANG_001/beats_lead.json"
BEATS_LAG = "runs/2026-11-03_KANG_002/beats_lag.json"
NAME = "dwarika_v17_combined_review"
REVIEW_CSV = "dwarika_v17_review.csv"
SHEET = "dwarika_v17_review_sheet.jpg"
LABEL = "v17"
BASE_RUN: Optional[str] = None
PROFILES: Dict[str, Dict[str, Any]] = {
    "v17": {"VISUALS": VISUALS, "NAME": NAME, "REVIEW_CSV": REVIEW_CSV, "SHEET": SHEET, "LABEL": "v17", "BASE_RUN": None},
    "v17b": {"VISUALS": "runs/2026-11-05_KANG_001/visuals_beats_v17b.csv", "NAME": "dwarika_v17b_combined_review",
             "REVIEW_CSV": "dwarika_v17b_review_v3.csv", "SHEET": "dwarika_v17b_review_sheet.jpg", "LABEL": "v17b",
             "BASE_RUN": "2026-11-04_KANG_029"},
    "v18": {"VISUALS": "runs/2026-11-07_KANG_008/visuals_beats_v18.csv", "NAME": "dwarika_v18_combined_review",
            "REVIEW_CSV": "dwarika_v18_review.csv", "SHEET": "dwarika_v18_review_sheet.jpg", "LABEL": "v18",
            "BASE_RUN": "2026-11-05_KANG_003",
            "SEG_PATCH": {"S01_opening": {"feature": "cold open teaser + parallax + YouTube CC",
                                          "title": "S01 Cold open: 6.3 s teaser (4 shots + title) + S01",
                                          "look": "Dekhiye: teaser ke 4 shots + title saaf? Narration wahi hai, koi khaali jagah nahi?"}}},
}


def use_profile(name: str) -> None:
    g = globals()
    for k, v in PROFILES[name].items():
        if k == "SEG_PATCH":
            g["SEGMENTS"] = [dict(s, **v.get(s["id"], {})) for s in g["SEGMENTS"]]
            continue
        g[k] = v


def run_profile(run: Run) -> str:
    pf = run.path("review_profile.json")
    return json.loads(pf.read_text(encoding="utf-8"))["profile"] if pf.is_file() else "v17"

# (id, t0, t1, feature, title line, what to look at) - timeline order; AB = lead/lag pair of the same window
SEGMENTS: List[Dict[str, Any]] = [
    {"id": "S01_opening", "t0": 0.00, "t1": 16.60, "feature": "parallax + YouTube CC",
     "title": "S01 Opening: Parallax + YouTube clip (S01_b04)",
     "look": "Dekhiye: parallax smooth hai? YouTube clip mandir ka hi hai?"},
    {"id": "crop_reuse_1", "t0": 160.84, "t1": 170.16, "feature": "crop reuse",
     "title": "Crop reuse #1 (S07_b04)",
     "look": "Dekhiye: same photo ka naya crop alag shot lagta hai?"},
    {"id": "S09_card", "t0": 214.92, "t1": 228.12, "feature": "Ken Burns + card",
     "title": "S09 Auto/rickshaw + card C07",
     "look": "Dekhiye: card ka text bole gaye shabd ke saath aata hai?"},
    {"id": "S10_openverse", "t0": 260.68, "t1": 273.32, "feature": "parallax + Openverse",
     "title": "S10 Bhadkeshwar: Parallax + Openverse photos",
     "look": "Dekhiye: Openverse photos sahi mandir ke hain?"},
    {"id": "S11_stock", "t0": 323.24, "t1": 333.88, "feature": "parallax + Pixabay stock",
     "title": "S11 Beach: Parallax + Pixabay stock",
     "look": "Dekhiye: stock clip (representative) theek lagta hai?"},
    {"id": "M2_map", "t0": 333.88, "t1": 350.24, "feature": "map",
     "title": "M2 Map: Bet Dwarka route",
     "look": "Dekhiye: route aur labels saaf padhne layak hain?"},
    {"id": "AB_lead_lag", "t0": 349.50, "t1": 360.50, "feature": "beat cut A/B", "ab": True,
     "title": "Cut timing A/B: A = LEAD (-0.2 s), B = LAG (+0.25 s)",
     "look": "Dekhiye: kaunsa cut naam ke saath behtar baithta hai, A ya B?"},
    {"id": "S14_gopi_talav_card", "t0": 405.40, "t1": 424.84, "feature": "card",
     "title": "S14 Gopi Talav card (C11)",
     "look": "Dekhiye: har value apne shabd pe aati hai?"},
    {"id": "M4_map", "t0": 424.84, "t1": 441.48, "feature": "map",
     "title": "M4 Map: Gopi Talav se Bet Dwarka (Sudarshan Setu)",
     "look": "Dekhiye: route + Sudarshan Setu label sahi jagah?"},
    {"id": "crop_reuse_2", "t0": 467.00, "t1": 479.76, "feature": "crop reuse",
     "title": "Crop reuse #2 (S15_b08) + parallax + stock",
     "look": "Dekhiye: exhibit crop saaf hai, pehle shot jaisa nahi?"},
    {"id": "S16_ai_motion", "t0": 498.80, "t1": 511.32, "feature": "AI motion (WARN)",
     "title": "AI motion S16_b06 (WARN: sirf 1 clip pass)",
     "look": "Dekhiye: jhanda/aasmaan natural? Patthar hila to nahi?"},
    {"id": "S17_setu_youtube", "t0": 519.32, "t1": 529.36, "feature": "YouTube CC",
     "title": "S17 Sudarshan Setu: YouTube CC clip",
     "look": "Dekhiye: bridge clip exact aur smooth hai?"},
    {"id": "S21_card", "t0": 633.96, "t1": 653.04, "feature": "card",
     "title": "S21 Budget card (C17)",
     "look": "Dekhiye: numbers sahi aur padhne layak hain?"},
    {"id": "S22_outro", "t0": 673.44, "t1": 692.36, "feature": "crop reuse + YouTube CC + stock",
     "title": "S22 Outro: crop reuse #3 + YouTube sunset + stock",
     "look": "Dekhiye: ending smooth hai, koi jhatka nahi?"},
]


def ff(args: List[str], log: Optional[Path] = None) -> None:
    r = subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error"] + args,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if log:
        with open(log, "a", encoding="utf-8") as f:
            f.write(" ".join(args)[:400] + "\n" + r.stderr + "\n")
    if r.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {r.stderr[-1500:]}")


def dur(p: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return float(r.stdout.strip() or 0)


def clips_v17() -> List[Dict[str, Any]]:
    return bpk._clips(B.read_assign_csv(str(ROOT / VISUALS)))


def video_path(c: Dict[str, Any]) -> Optional[str]:
    if c.get("ai_clip"):
        return c["ai_local"]
    if c.get("parallax_clip"):
        return c["parallax_local"]
    if Path(c["asset"]).suffix.lower() in B.VIDEO_EXT:
        return c["path_local"]
    return None


def tag_of(c: Dict[str, Any]) -> str:
    sd, a = (c.get("source_dir") or "").lower(), c["asset"].lower()
    if a.startswith("tsr_"):
        f = "TEASER"
    elif c.get("ai_clip"):
        f = "AI MOTION"
    elif c["match"] == "text_card":
        return "CARD"
    elif c["match"] == "map":
        return "MAP"
    elif c.get("parallax_clip"):
        f = "PARALLAX"
    elif "youtube" in sd or a.startswith("ytc_"):
        f = "YOUTUBE CC"
    elif "pixabay" in sd or "pixabay" in a:
        f = "STOCK (Pixabay)"
    elif c.get("reuse") == "crop_reuse" or a.startswith("cr_"):
        f = "CROP REUSE"
    elif "openverse" in sd:
        f = "OPENVERSE"
    else:
        f = "KEN BURNS"
    return f"{f} | {c['match']}"


def lag_clips(clips: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Same shots, each cut moved to its incoming beat's LAG start (beats_lag.json, +0.25 s anchor). Video clips keep
    their lead-timed content (src_start = lead start), so only the cut point moves (outgoing shot held / extended)."""
    lag = {b["id"]: b for b in json.loads((ROOT / BEATS_LAG).read_text(encoding="utf-8"))["beats"]}
    out = [dict(c) for c in clips]
    for c in out:
        c["src_start"] = c["start"]
        if c["first_beat"] in lag:
            c["start"] = float(lag[c["first_beat"]]["start"])
    for k in range(len(out) - 1):
        out[k]["end"] = out[k + 1]["start"]
    return out


def render_range(clips: List[Dict[str, Any]], a: float, b: float, wd: Path, tag: str, log: Path) -> tuple:
    """Video-only 1280x720 25 fps of [a,b) + the list of (start, end, tag, beat ids) shown, times relative to a."""
    parts, shown = [], []
    n_a = round(a * FPS)
    for k, c in enumerate(clips):
        sa, sb = max(a, c["start"]), min(b, c["end"])
        n0, n1 = max(round(sa * FPS), n_a), round(sb * FPS)
        if n1 <= n0:
            continue
        part = wd / f"{tag}_p{k:03d}.mp4"
        vp = video_path(c)
        if vp:
            off = n0 / FPS - c.get("src_start", c["start"])
            ff(["-ss", f"{max(0.0, off):.3f}", "-i", vp, "-an", "-vf",
                f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,"
                f"tpad=stop_mode=clone:stop_duration=5", "-frames:v", str(n1 - n0), "-c:v", "libx264",
                "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", str(part)], log)
        else:
            B.render_motion_video([c], lambda c: c["path_local"], n0 / FPS, n1 / FPS, part, w=W, h=H, fps=FPS, crf=18)
        parts.append(part)
        shown.append({"start": (n0 - n_a) / FPS, "end": (n1 - n_a) / FPS, "tag": tag_of(c), "beats": c["beats"],
                      "asset": c["asset"], "first_beat": c["first_beat"]})
    lst = wd / f"{tag}_list.txt"
    lst.write_text("".join(f"file '{p.resolve().as_posix()}'\n" for p in parts), encoding="utf-8")
    vid = wd / f"{tag}_video.mp4"
    ff(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(vid)], log)
    return vid, shown


def esc(p: Path) -> str:
    return p.resolve().as_posix().replace(":", r"\:").replace("'", r"\'")


def finish_segment(vid: Path, shown: List[Dict[str, Any]], a: float, b: float, out: Path, wd: Path, tag: str,
                   log: Path, banner: Optional[str] = None) -> None:
    """Tags + burned captions + narration audio."""
    srt = wd / f"{tag}.srt"
    srt.write_text(B.shift_srt((ROOT / CAPTIONS).read_text(encoding="utf-8-sig"), a, b), encoding="utf-8")
    filt = []
    for k, s in enumerate(shown):
        tf = wd / f"{tag}_tag{k:02d}.txt"
        bid = s["beats"][0] + (f"-{s['beats'][-1].split('_')[-1]}" if len(s["beats"]) > 1 else "")
        tf.write_text(f"{s['tag']}  {bid}", encoding="utf-8")
        filt.append(f"drawtext=fontfile='{esc(FONT)}':textfile='{esc(tf)}':x=14:y=12:fontsize=24:fontcolor=white:"
                    f"box=1:boxcolor=black@0.62:boxborderw=8:enable='between(t,{s['start']:.3f},{s['end'] - 0.001:.3f})'")
    if banner:
        bf = wd / f"{tag}_banner.txt"
        bf.write_text(banner, encoding="utf-8")
        filt.append(f"drawtext=fontfile='{esc(FONT)}':textfile='{esc(bf)}':x=(w-tw)/2:y=62:fontsize=34:"
                    f"fontcolor=yellow:box=1:boxcolor=black@0.7:boxborderw=10")
    filt.append(f"subtitles=filename='{esc(srt)}':fontsdir='{esc(ROOT / 'fonts')}':force_style='FontName=Mukta "
                f"ExtraBold,FontSize=22,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,"
                f"Shadow=0,MarginV=22'")
    d = b - a
    ff(["-i", str(vid), "-ss", f"{a:.3f}", "-t", f"{d:.3f}", "-i", str(ROOT / MEDIA), "-map", "0:v", "-map", "1:a",
        "-vf", ",".join(filt), "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p",
        "-r", str(FPS), "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2", "-t", f"{d:.3f}", str(out)], log)


def slate(seg: Dict[str, Any], out: Path, wd: Path, log: Path, num: int) -> None:
    t1, t2 = wd / f"slate{num:02d}_1.txt", wd / f"slate{num:02d}_2.txt"
    t1.write_text(f"{num}. {seg['title']}", encoding="utf-8")
    t2.write_text(seg["look"], encoding="utf-8")
    vf = (f"drawtext=fontfile='{esc(FONT)}':textfile='{esc(t1)}':x=(w-tw)/2:y=h/2-60:fontsize=40:fontcolor=white,"
          f"drawtext=fontfile='{esc(FONT)}':textfile='{esc(t2)}':x=(w-tw)/2:y=h/2+10:fontsize=30:fontcolor=0xFFD24A")
    ff(["-f", "lavfi", "-i", f"color=c=0x141414:s={W}x{H}:r={FPS}:d=2", "-f", "lavfi", "-i",
        "anullsrc=r=48000:cl=stereo", "-vf", vf, "-t", "2", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22",
        "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2",
        str(out)], log)


def seg_cmd(run_id: str, which: str) -> Dict[str, Any]:
    run = Run(run_id)
    wd = run.path("review_parts")
    wd.mkdir(exist_ok=True)
    log = run.path("ffmpeg_review.log")
    clips = clips_v17()
    idx = range(len(SEGMENTS)) if which == "all" else [int(which)]
    done = []
    for k in idx:
        seg = SEGMENTS[k]
        out = wd / f"seg{k:02d}.mp4"
        meta = wd / f"seg{k:02d}.json"
        if out.exists() and meta.exists():
            continue
        slate(seg, wd / f"seg{k:02d}_slate.mp4", wd, log, k + 1)
        a, b = seg["t0"], seg["t1"]
        if seg.get("ab"):
            info = {"parts": []}
            for lab, cl, ban in (("A", clips, f"A: LEAD cut (-0.2 s, {LABEL} timeline)"),
                                 ("B", lag_clips(clips), "B: LAG cut (+0.25 s, beats_lag)")):
                vid, shown = render_range(cl, a, b, wd, f"seg{k:02d}{lab}", log)
                for s in shown:
                    s["tag"] = f"BEAT CUT {lab} | " + s["tag"]
                o = wd / f"seg{k:02d}{lab}.mp4"
                finish_segment(vid, shown, a, b, o, wd, f"seg{k:02d}{lab}", log, banner=ban)
                info["parts"].append({"label": lab, "file": o.name, "shown": shown, "duration": dur(o)})
            lst = wd / f"seg{k:02d}_ab.txt"
            lst.write_text("".join(f"file '{(wd / p['file']).resolve().as_posix()}'\n" for p in info["parts"]),
                           encoding="utf-8")
            ff(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out)], log)
        else:
            vid, shown = render_range(clips, a, b, wd, f"seg{k:02d}", log)
            finish_segment(vid, shown, a, b, out, wd, f"seg{k:02d}", log)
            info = {"parts": [{"label": "", "file": out.name, "shown": shown, "duration": dur(out)}]}
        info.update(seg=seg, duration=dur(out), slate_duration=dur(wd / f"seg{k:02d}_slate.mp4"))
        meta.write_text(json.dumps(info, ensure_ascii=False, indent=1), encoding="utf-8")
        done.append({"seg": k, "id": seg["id"], "duration": info["duration"]})
    return {"run_id": run.run_id, "rendered": done}


def tc(x: float) -> str:
    return f"{int(x // 60):02d}:{x % 60:05.2f}"


def join_cmd(run_id: str) -> Dict[str, Any]:
    run = Run(run_id)
    wd = run.path("review_parts")
    log = run.path("ffmpeg_review.log")
    files, rows, segs, t = [], [], [], 0.0
    for k, seg in enumerate(SEGMENTS):
        meta = json.loads((wd / f"seg{k:02d}.json").read_text(encoding="utf-8"))
        files += [wd / f"seg{k:02d}_slate.mp4", wd / f"seg{k:02d}.mp4"]
        t_slate = t
        t += meta["slate_duration"]
        segs.append({"n": k + 1, "id": seg["id"], "slate_at": round(t_slate, 2), "start": round(t, 2),
                     "end": round(t + meta["duration"], 2), "timeline": f"{seg['t0']:.2f}-{seg['t1']:.2f}",
                     "feature": seg["feature"]})
        pt = t
        for part in meta["parts"]:
            for s in part["shown"]:
                ftag = re.sub(r"^BEAT CUT [AB] \| ", "", s["tag"])  # A/B part is in the segment column
                rows.append({"segment": f"{k + 1:02d} {seg['id']}" + (f" ({part['label']})" if part["label"] else ""),
                             "review_tc_start": tc(pt + s["start"]), "review_tc_end": tc(pt + s["end"]),
                             "timeline_start_s": f"{seg['t0'] + s['start']:.2f}",
                             "timeline_end_s": f"{seg['t0'] + s['end']:.2f}",
                             "beat_ids": " ".join(s["beats"]), "feature": ftag.split(" | ")[-2] if " | " in ftag else ftag,
                             "label": ftag.split(" | ")[-1] if " | " in ftag else ftag.lower().replace("card", "text_card"),
                             "asset": s["asset"], "what_to_check": seg["look"].replace("Dekhiye: ", ""),
                             "user_verdict (ok/fix)": "", "notes": ""})
            pt += part["duration"]
        t += meta["duration"]
    lst = wd / "join.txt"
    lst.write_text("".join(f"file '{p.resolve().as_posix()}'\n" for p in files), encoding="utf-8")
    out = ROOT / "out" / f"{NAME}.mp4"
    tmp = run.path(f"{NAME}.mp4")
    import tempfile
    local = Path(tempfile.mkdtemp(prefix="kang_review_")) / f"{NAME}.mp4"  # +faststart rewrite fails on the workspace FS
    ff(["-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", "-movflags", "+faststart", str(local)], log)
    shutil.copy2(local, tmp)
    shutil.move(str(local), out)
    csv_p = ROOT / "out" / REVIEW_CSV
    with open(run.path(REVIEW_CSV), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    shutil.copy2(run.path(REVIEW_CSV), csv_p)
    (run.path("review_segments.json")).write_text(json.dumps(segs, ensure_ascii=False, indent=1), encoding="utf-8")
    run.add_output(tmp, "combined_review_video")
    run.add_output(run.path(REVIEW_CSV), "review_csv")
    run.add_output(run.path("review_segments.json"), "review_segments")
    d = dur(out)
    run.log_step("combined_review_join", segments=len(segs), shots_tagged=len(rows), duration=round(d, 2),
                 expected=round(t, 2), out=str(out.relative_to(ROOT)))
    return {"run_id": run.run_id, "out": str(out), "duration": round(d, 2), "expected": round(t, 2),
            "size": out.stat().st_size, "segments": segs, "csv": str(csv_p), "csv_rows": len(rows)}


def sheet_cmd(run_id: str, cols: int = 12) -> Dict[str, Any]:
    from PIL import Image, ImageDraw, ImageFont
    run = Run(run_id)
    wd = run.path("sheet_frames")
    wd.mkdir(exist_ok=True)
    clips = clips_v17()
    tw, th, lh = 256, 144, 40
    tiles = []
    for k, c in enumerate(clips):
        fp = wd / f"f{k:03d}.jpg"
        if not fp.exists():
            mid = (c["start"] + c["end"]) / 2
            vp = video_path(c)
            if vp:
                ff(["-ss", f"{max(0.0, mid - c['start']):.3f}", "-i", vp, "-frames:v", "1", "-update", "1", "-vf",
                    f"scale={tw}:{th}:force_original_aspect_ratio=increase,crop={tw}:{th}", str(fp)])
            else:
                src = B._cover_source(c["path_local"], 640, 360, c["motion"]["smax"])
                B.frame_at(src, c["motion"], 0.5, 640, 360).resize((tw, th)).save(fp, quality=88)
        tiles.append((Image.open(fp).convert("RGB"), c))
    font = ImageFont.truetype(str(FONT), 15)
    font_s = ImageFont.truetype(str(FONT), 13)
    head = 50
    n_rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, head + n_rows * (th + lh)), (18, 18, 18))
    d = ImageDraw.Draw(sheet)
    d.text((10, 10), f"KANG {LABEL} Dwarika - {len(tiles)} shots (one frame per shot, mid-shot; captions not burned) - "
                     f"{VISUALS}", fill=(255, 255, 255), font=ImageFont.truetype(str(FONT), 22))
    colors = {"AI MOTION": (255, 90, 90), "PARALLAX": (120, 200, 255), "YOUTUBE CC": (255, 80, 80),
              "STOCK (Pixabay)": (120, 230, 120), "CROP REUSE": (255, 170, 60), "OPENVERSE": (200, 140, 255),
              "CARD": (255, 220, 80), "MAP": (80, 220, 200), "KEN BURNS": (210, 210, 210), "TEASER": (255, 120, 220)}
    for k, (im, c) in enumerate(tiles):
        x, y = (k % cols) * tw, head + (k // cols) * (th + lh)
        sheet.paste(im, (x, y))
        tag = tag_of(c)
        feat = tag.split(" | ")[0]
        bid = c["first_beat"] + (f"-{c['beats'][-1].split('_')[-1]}" if len(c["beats"]) > 1 else "")
        d.text((x + 4, y + th + 2), f"{bid}  {c['start']:.1f}s", fill=(255, 255, 255), font=font)
        d.text((x + 4, y + th + 20), tag, fill=colors.get(feat, (220, 220, 220)), font=font_s)
    out = ROOT / "out" / SHEET
    sheet.save(run.path(SHEET), quality=86)
    shutil.copy2(run.path(SHEET), out)
    run.add_output(run.path(SHEET), "review_sheet")
    counts: Dict[str, int] = {}
    for _, c in tiles:
        f = tag_of(c).split(" | ")[0]
        counts[f] = counts.get(f, 0) + 1
    run.log_step("review_sheet", shots=len(tiles), features=counts)
    return {"run_id": run.run_id, "sheet": str(out), "shots": len(tiles), "features": counts, "size": sheet.size}


def seg_signature(clips: List[Dict[str, Any]], a: float, b: float) -> List[tuple]:
    """What a segment shows: every clip overlapping [a, b) with its file, folder and timing (A/B uses the same clips)."""
    # v18: the still move (desk_motion may swap zoom in/out) is part of what a segment shows
    return [(c["asset"], c.get("source_dir", ""), c.get("parallax_clip", ""), c.get("ai_clip", ""), round(c["start"], 3),
             round(c["end"], 3), c.get("motion", {}).get("type", "")) for c in clips if c["end"] > a and c["start"] < b]


def reuse_cmd(run_id: str) -> Dict[str, Any]:
    """v17b: copy segments whose shots are identical in the base review run's timeline (slate + segment + meta)."""
    run = Run(run_id)
    if not BASE_RUN:
        raise SystemExit("profile has no BASE_RUN")
    base = Run(BASE_RUN)
    bm = json.loads(base.path("manifest.json").read_text(encoding="utf-8"))
    base_vis = next(i["path"] for i in bm["inputs"] if i.get("id") == "VISUALS_BEATS")
    old = bpk._clips(B.read_assign_csv(str(base_vis)))
    new = clips_v17()
    wd, bwd = run.path("review_parts"), base.path("review_parts")
    wd.mkdir(exist_ok=True)
    reused, todo = [], []
    for k, seg in enumerate(SEGMENTS):
        if seg_signature(old, seg["t0"], seg["t1"]) == seg_signature(new, seg["t0"], seg["t1"]) and (bwd / f"seg{k:02d}.json").is_file():
            for n in (f"seg{k:02d}.mp4", f"seg{k:02d}_slate.mp4", f"seg{k:02d}.json"):
                shutil.copy2(bwd / n, wd / n)
            reused.append(k)
        else:
            todo.append(k)
    run.log_step("combined_review_reuse", base_run=BASE_RUN, reused=[SEGMENTS[k]["id"] for k in reused],
                 to_render=[SEGMENTS[k]["id"] for k in todo])
    return {"run_id": run.run_id, "reused": reused, "to_render": todo}


def init_cmd(profile: str = "v17") -> Dict[str, Any]:
    run = Run()
    run.path("review_profile.json").write_text(json.dumps({"profile": profile, **PROFILES[profile]}, ensure_ascii=False,
                                                          indent=1), encoding="utf-8")
    for p, k in ((MEDIA, "A1"), (VISUALS, "VISUALS_BEATS"), (CAPTIONS, "CAPTIONS"), (BEATS_LEAD, "BEATS_LEAD"),
                 (BEATS_LAG, "BEATS_LAG")):
        run.add_input(str(ROOT / p), k)
    run.log_step("combined_review_init", profile=profile, segments=[s["id"] for s in SEGMENTS])
    return {"run_id": run.run_id}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("cmd", choices=["init", "seg", "join", "sheet", "reuse"])
    ap.add_argument("which", nargs="?", default="all")
    ap.add_argument("--run")
    ap.add_argument("--profile", default="v17", choices=sorted(PROFILES))
    a = ap.parse_args()
    if a.cmd == "init":
        use_profile(a.profile)
        r = init_cmd(a.profile)
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return 0
    use_profile(run_profile(Run(a.run)))
    if a.cmd == "reuse":
        r = reuse_cmd(a.run)
    elif a.cmd == "seg":
        r = seg_cmd(a.run, a.which)
    elif a.cmd == "join":
        r = join_cmd(a.run)
    else:
        r = sheet_cmd(a.run)
    print(json.dumps(r, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
