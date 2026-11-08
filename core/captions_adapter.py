"""KANG Caption Adapter v0 (Reels).

KANG keeps: reviewed Hinglish words (layer), style presets (presets/reels/*.json), approval gate, QA.
ASS generation: karaoke-subs (github.com/DorXmoon/karaoke-subs, MIT, pip install karaoke-subs) used as-is,
unmodified, through its public API (words_from_dicts, group_words, Style, to_ass). Burn: FFmpeg + libass.
No transcription, no cloud, no publishing. A draft (non-accepted) layer renders only with allow_draft and
every output is then labelled DRAFT.
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parent.parent
PRESET_DIR = ROOT / "presets" / "reels"
FORMATS = {"9:16": (1080, 1920), "1:1": (1080, 1080), "16:9": (1920, 1080)}
# Instagram/YouTube Shorts UI covers roughly the bottom ~20 % and top ~12 % of a 9:16 frame (approximate,
# platform UIs change); captions must stay inside the middle band.
SAFE = {"9:16": (0.12, 0.20), "1:1": (0.06, 0.08), "16:9": (0.05, 0.08)}


def load_preset(name: str) -> Dict[str, Any]:
    p = Path(name) if name.endswith(".json") else PRESET_DIR / f"{name}.json"
    if not p.exists():
        avail = ", ".join(sorted(x.stem for x in PRESET_DIR.glob("*.json")))
        raise ValueError(f"unknown style {name!r}; available: {avail}")
    return json.loads(p.read_text(encoding="utf-8"))


def load_layer(path: str, allow_draft: bool) -> Tuple[Dict[str, Any], bool]:
    doc = json.loads(Path(path).read_text(encoding="utf-8"))
    accepted = doc.get("status") == "accepted_text"
    if not accepted and not allow_draft:
        raise PermissionError(f"layer status is {doc.get('status')!r}, not accepted_text. Finish the Hinglish review "
                              "(apply-hinglish-review) or pass --allow-draft for a labelled DRAFT test render.")
    return doc, accepted


def window_words(entries, start: float, dur: Optional[float]) -> List[Dict[str, Any]]:
    end = start + dur if dur else float("inf")
    out = []
    for e in entries:
        if e["start"] >= start and e["end"] <= end and e["hinglish"].strip():
            out.append({**e, "start": round(e["start"] - start, 3), "end": round(e["end"] - start, 3)})
    return out


def _display(text: str, preset: Dict[str, Any]) -> str:
    t = text.strip()
    t = re.sub(r"[,;]+$", "", t)  # trailing commas look noisy on short lines; full stops stay
    t = t.replace("{", "(").replace("}", ")").replace("\\", "/")  # never let text inject ASS tags
    return t.upper() if preset.get("uppercase") else t


def build_ass(words: List[Dict[str, Any]], preset: Dict[str, Any], fmt: str = "9:16") -> Tuple[str, List[Any]]:
    try:
        from karaoke_subs import Style, group_words, to_ass, words_from_dicts
    except ImportError as exc:  # pragma: no cover
        raise RuntimeError("karaoke-subs not installed: pip install karaoke-subs (MIT)") from exc
    w, h = FORMATS[fmt]
    ks = words_from_dicts([{"word": _display(x["hinglish"], preset), "start": x["start"], "end": x["end"]} for x in words])
    lines = group_words(ks, max_words=preset["max_words"], max_chars=preset["max_chars"],
                        max_gap=preset["max_gap"], max_duration=preset["max_duration"])
    st = Style(font=preset["font"], size=preset["font_size"], base=preset["base_color"],
               highlight=preset["highlight_color"], outline_color=preset["outline_color"],
               outline=preset["outline"], shadow=preset["shadow"], bold=preset["bold"],
               alignment=preset["alignment"], margin_l=preset["margin_h"], margin_r=preset["margin_h"],
               margin_v=preset["margin_v"])
    return to_ass(ks, style=st, play_res=(w, h), lines=lines), lines


def qa(lines, words, preset, fmt: str, accepted: bool) -> Dict[str, Any]:
    """Structural checks only. Visual/playback QA stays with the human."""
    w, h = FORMATS[fmt]
    top, bottom = SAFE[fmt]
    checks = {}
    # vertical: bottom-aligned text sits margin_v above the bottom; middle-aligned is centred
    fs = preset["font_size"]
    if preset["alignment"] in (1, 2, 3):
        y_bottom = h - preset["margin_v"]
        y_top = y_bottom - fs * 1.25 * 2  # allow a wrapped second line
    elif preset["alignment"] in (4, 5, 6):
        y_top, y_bottom = h / 2 - fs * 1.25, h / 2 + fs * 1.25
    else:
        y_top = preset["margin_v"]
        y_bottom = y_top + fs * 1.25 * 2
    checks["safe_zone_vertical"] = "PASS" if (y_top >= h * top and y_bottom <= h * (1 - bottom)) else "FAIL"
    # horizontal: rough width estimate (measured: ~0.55 em per char caps, ~0.42 lower case)
    em = 0.55 if preset.get("uppercase") else 0.42  # calibrated 2026-11-01 on rendered Montserrat Black frames
    avail = w - 2 * preset["margin_h"]
    widest = max((len(" ".join(x.text for x in ln.words)) for ln in lines), default=0)
    est = widest * fs * em
    checks["widest_line_chars"] = widest
    checks["widest_line_est_px"] = round(est)
    checks["fits_one_line_est"] = "PASS" if est <= avail else "WARN"  # libass wraps (WrapStyle 2 = no wrap!)
    # timing: monotonic, no overlaps, readable minimum
    overlaps = sum(1 for a, b in zip(lines, lines[1:]) if b.start < a.end - 0.001)
    short = sum(1 for ln in lines if ln.end - ln.start < 0.25)
    checks["overlapping_events"] = overlaps
    checks["events_under_0_25s"] = short
    checks["timing"] = "PASS" if overlaps == 0 else "FAIL"
    tstat = {}
    for x in words:
        tstat[x.get("timing_status", "?")] = tstat.get(x.get("timing_status", "?"), 0) + 1
    status = "WARN" if (not accepted or "FAIL" in checks.values() or "WARN" in checks.values()
                        or tstat.get("unverified")) else "PASS"
    return {"status": status, "draft": not accepted, "checks": checks, "word_timing_status": tstat,
            "events": len(lines), "words": len(words), "safe_zone_assumed": {"top": top, "bottom": bottom},
            "human_playback_qa": "NOT_TESTED"}


def background_args(visuals_json: str, start: float, dur: float, fmt: str, fps: int, tmp: Path) -> Path:
    """9:16 (or other) background from the approved visuals.json stills/clips for [start, start+dur]."""
    from core.runs import run_ffmpeg
    from core.visuals import segment_args
    v = json.loads(Path(visuals_json).read_text(encoding="utf-8"))
    vj = Path(visuals_json)
    cands = [Path(v["assets_dir"]), ROOT / v["assets_dir"], vj.parent / v["assets_dir"],
             vj.parent / "premiere_package" / "visuals", vj.parent / "visuals"]
    adir = next((c for c in cands if (c / v["items"][0]["asset"]).exists()), None)
    if adir is None:
        raise RuntimeError(f"visual assets not found; tried {[str(c) for c in cands]}")
    w, h = FORMATS[fmt]
    segs = []
    end = start + dur
    for i, it in enumerate(v["items"]):
        s, e = max(it["start"], start), min(it["end"], end)
        if e - s < 1.0 / fps:
            continue
        item = {**it, "fit": "cover" if it["fit"] == "contain" else it["fit"]}
        out = tmp / f"seg_{i:03d}.mp4"
        run_ffmpeg(["-y", *segment_args(item, adir / it["asset"], out, e - s, w, h, fps)])
        segs.append(out)
    if not segs:
        raise RuntimeError("no visuals in that time window")
    lst = tmp / "concat.txt"
    lst.write_text("".join(f"file '{p.name}'\n" for p in segs), encoding="utf-8")
    bg = tmp / "bg.mp4"
    run_ffmpeg(["-y", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(bg)])
    return bg


def make_reel(audio: str, layer: str, *, style: str = "karaoke_yellow", fmt: str = "9:16", start: float = 0.0,
              dur: Optional[float] = 30.0, visuals: Optional[str] = None, allow_draft: bool = False,
              render: bool = True, fps: int = 30, run=None) -> Dict[str, Any]:
    from core.runs import Run, run_ffmpeg
    preset = load_preset(style)
    doc, accepted = load_layer(layer, allow_draft)
    words = window_words(doc["words"], start, dur)
    if not words:
        return {"error": "no words in that window"}
    if preset.get("engine") == "pycaps":
        return _make_reel_pycaps(audio, layer, doc, accepted, words, preset, fmt=fmt, start=start, dur=dur,
                                 visuals=visuals, render=render, fps=fps, run=run)
    ass, lines = build_ass(words, preset, fmt)
    tag = "" if accepted else "DRAFT_"
    run = run or Run()
    run.add_input(layer, "H1")
    run.add_input(audio, "A1")
    out_dir = run.path("reels")
    out_dir.mkdir(exist_ok=True)
    base = f"{tag}reel_{preset['style']}_{fmt.replace(':', 'x')}_{int(start)}s"
    ap = out_dir / f"{base}.ass"
    ap.write_text(ass, encoding="utf-8")
    rep = qa(lines, words, preset, fmt, accepted)
    rep.update({"style": preset, "format": fmt, "window": [start, start + (dur or 0)], "layer": str(layer),
                "layer_status": doc.get("status"), "engine": "karaoke-subs (MIT, unmodified)",
                "approval": "pending (render is a preview; nothing published)"})
    run.add_output(ap, "reel_ass")
    vp = None
    if render:
        if not visuals:
            return {"error": "render needs --visuals visuals.json (background); or use --no-render"}
        tmp = out_dir / f"_{base}_tmp"
        tmp.mkdir(exist_ok=True)
        try:
            bg = background_args(visuals, start, dur or 30.0, fmt, fps, tmp)
            vp = out_dir / f"{base}.mp4"
            fonts = (ROOT / "fonts").as_posix().replace(":", r"\:")
            assf = ap.as_posix().replace(":", r"\:")
            run_ffmpeg(["-y", "-i", str(bg), "-ss", f"{start:.3f}", "-t", f"{dur or 30.0:.3f}", "-i", audio,
                        "-map", "0:v", "-map", "1:a", "-vf", f"ass='{assf}':fontsdir='{fonts}'",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "160k", "-shortest", str(vp)])
            run.add_output(vp, "reel_mp4")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    qp = out_dir / f"{base}_qa_report.json"
    qp.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    run.add_output(qp, "reel_qa")
    run.log_step("reel", style=preset["style"], fmt=fmt, start=start, dur=dur, draft=not accepted, status=rep["status"])
    run.set_status("reel_preview_ready_awaiting_review")
    return {"run_id": run.run_id, "status": rep["status"], "draft": not accepted, "events": rep["events"],
            "checks": rep["checks"], "files": {"ass": str(ap), "mp4": str(vp) if vp else None, "qa": str(qp)}}


def _make_reel_pycaps(audio, layer, doc, accepted, words, preset, *, fmt, start, dur, visuals, render, fps, run):
    """Optional animated engine (pycaps, MIT). Burned MP4 only; same draft gate, run folder, manifest and QA file."""
    from core.runs import Run, run_ffmpeg
    from core import pycaps_engine as pe
    if fmt != "9:16":
        return {"error": "pycaps presets are calibrated for 9:16 only"}
    tag = "" if accepted else "DRAFT_"
    run = run or Run()
    run.add_input(layer, "H1")
    run.add_input(audio, "A1")
    out_dir = run.path("reels")
    out_dir.mkdir(exist_ok=True)
    base = f"{tag}reel_{preset['style']}_{fmt.replace(':', 'x')}_{int(start)}s"
    tj = out_dir / f"{base}_transcript_whisper.json"
    tj.write_text(json.dumps(pe.to_whisper_json(words), ensure_ascii=False, indent=1), encoding="utf-8")
    run.add_output(tj, "reel_transcript")
    tdir = out_dir / f"{base}_pycaps_template"
    tjson = pe.stage_template(preset, tdir)
    rep = pe.qa_pycaps(words, preset, accepted)
    rep.update({"style": preset, "format": fmt, "window": [start, start + (dur or 0)], "layer": str(layer),
                "layer_status": doc.get("status"), "engine": "pycaps (francozanardi, MIT) PictexSubtitleRenderer",
                "approval": "pending (render is a preview; nothing published)"})
    vp = None
    if render:
        if not visuals:
            return {"error": "render needs --visuals visuals.json (background); or use --no-render"}
        tmp = out_dir / f"_{base}_tmp"
        tmp.mkdir(exist_ok=True)
        try:
            bg = background_args(visuals, start, dur or 30.0, fmt, fps, tmp)
            clip = tmp / "input.mp4"
            run_ffmpeg(["-y", "-i", str(bg), "-ss", f"{start:.3f}", "-t", f"{dur or 30.0:.3f}", "-i", audio,
                        "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest",
                        str(clip)])
            vp = out_dir / f"{base}.mp4"
            pe.render(clip, tj, tjson, vp)
            run.add_output(vp, "reel_mp4")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    qp = out_dir / f"{base}_qa_report.json"
    qp.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    run.add_output(qp, "reel_qa")
    run.log_step("reel", style=preset["style"], engine="pycaps", fmt=fmt, start=start, dur=dur, draft=not accepted,
                 status=rep["status"])
    run.set_status("reel_preview_ready_awaiting_review")
    return {"run_id": run.run_id, "status": rep["status"], "draft": not accepted, "checks": rep["checks"],
            "files": {"transcript": str(tj), "template": str(tjson), "mp4": str(vp) if vp else None, "qa": str(qp)}}
