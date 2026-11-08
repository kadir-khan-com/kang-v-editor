"""Optional animated caption engine: pycaps (github.com/francozanardi/pycaps, MIT) via PictexSubtitleRenderer.

KANG never requires it: imported lazily only for presets with "engine": "pycaps". Our layer is passed as an
external transcript (no Whisper, no AI tagging, no sound effects). Output is a burned-in MP4 only (no ASS),
so Premiere editing stays with the karaoke-subs ASS presets.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parent.parent
PYCAPS_INSTALL = ("pip install https://github.com/francozanardi/pycaps/archive/"
                  "e2d36edfa08e3307d65b15bb20f17399dc2c9b40.zip html2pic")


def to_whisper_json(words: List[Dict[str, Any]], max_words: int = 12) -> Dict[str, Any]:
    """Window words (already shifted to 0) -> whisper_json; one segment per sentence or max_words."""
    segs, cur = [], []
    for w in words:
        cur.append(w)
        if w["hinglish"].rstrip()[-1:] in ".?!" or len(cur) >= max_words:
            segs.append(cur)
            cur = []
    if cur:
        segs.append(cur)
    return {"language": "hi", "segments": [
        {"start": s[0]["start"], "end": s[-1]["end"], "text": " ".join(x["hinglish"].strip() for x in s),
         "words": [{"word": " " + x["hinglish"].strip(), "start": x["start"], "end": x["end"]} for x in s]}
        for s in segs]}


def stage_template(preset: Dict[str, Any], dest: Path) -> Path:
    """Copy the template + font into dest so the run is self-contained and reproducible."""
    src = ROOT / preset["template_dir"]
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)
    res = dest / "resources"
    res.mkdir(exist_ok=True)
    shutil.copy2(ROOT / preset["font_file"], res / Path(preset["font_file"]).name)
    cfg = json.loads((dest / "pycaps.template.json").read_text(encoding="utf-8"))
    banned = [k for k in ("sound_effects", "tagger_rules", "whisper") if cfg.get(k)]
    if banned:
        raise ValueError(f"template must not use {banned} (no audio changes, no AI/cloud, no Whisper)")
    return dest / "pycaps.template.json"


def qa_pycaps(words, preset, accepted: bool) -> Dict[str, Any]:
    from core.captions_adapter import SAFE
    top, bottom = SAFE["9:16"]
    checks = {}
    tb = preset["text_bottom_ratio"]
    checks["safe_zone_vertical_config"] = "PASS" if tb <= 1 - bottom else "FAIL"
    checks["max_width_ratio_config"] = "PASS" if preset["max_width_ratio"] <= 0.85 else "WARN"
    starts = [w["start"] for w in words]
    checks["timing"] = "PASS" if starts == sorted(starts) and all(w["end"] >= w["start"] for w in words) else "FAIL"
    tstat: Dict[str, int] = {}
    for x in words:
        tstat[x.get("timing_status", "?")] = tstat.get(x.get("timing_status", "?"), 0) + 1
    status = "WARN" if (not accepted or "FAIL" in checks.values() or "WARN" in checks.values()
                        or tstat.get("unverified")) else "PASS"
    return {"status": status, "draft": not accepted, "checks": checks, "word_timing_status": tstat,
            "words": len(words), "safe_zone_assumed": {"top": top, "bottom": bottom},
            "note": "layout checked from template config only; pixel/playback QA is human",
            "human_playback_qa": "NOT_TESTED"}


def render(clip: Path, transcript: Path, template_json: Path, out: Path) -> None:
    try:
        from pycaps import JsonConfigLoader, PictexSubtitleRenderer
    except ImportError as exc:  # optional engine
        raise RuntimeError(f"pycaps engine not installed ({exc}). Install: {PYCAPS_INSTALL}") from exc
    builder = JsonConfigLoader(str(template_json)).load(False)
    builder.with_input_video(str(clip))
    builder.with_custom_subtitle_renderer(PictexSubtitleRenderer())
    builder.with_transcription_file(str(transcript), "whisper_json")
    builder.with_output_video(str(out))
    builder.build().run()
