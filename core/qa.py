"""Layer 5 QA: automatic checks from roadmap Section 9.

Each check returns {"name", "pass", "detail"}; qa_report() aggregates them.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .runs import media_summary, run_ffmpeg
from .subtitles import ass_events, ass_word_onsets

# Conjunct / matra test sentences (F01 glyph test): Dwarka, Kshatriya, Shri, etc.
GLYPH_TEST_SENTENCES = [
    "द्वारिका क्षत्रिय श्री",
    "ज्ञान त्र्यंबकेश्वर कृष्ण",
    "हृदय श्रृंगार द्वारिकाधीश",
    "रुक्मिणी दर्शन प्रसाद",
]


def _res(name: str, ok: bool, **detail: Any) -> Dict[str, Any]:
    return {"name": name, "pass": bool(ok), "detail": detail}


def check_export(path: str | Path, expected_dur: Optional[float] = None, size: Optional[Tuple[int, int]] = None,
                 fps: float = 30.0, tol_frames: float = 1.0) -> Dict[str, Any]:
    """ffprobe clean, resolution exact, duration within +/- tol frames of expectation."""
    try:
        m = media_summary(path)
    except Exception as exc:
        return _res("export_integrity", False, error=str(exc))
    ok = m.get("has_video", False)
    d: Dict[str, Any] = {"duration": m["duration"], "width": m.get("width"), "height": m.get("height")}
    if size:
        ok &= (m.get("width"), m.get("height")) == tuple(size)
    if expected_dur is not None:
        tol = tol_frames / fps + 0.025  # + AAC frame padding allowance
        d["expected"] = expected_dur
        d["delta"] = round(m["duration"] - expected_dur, 4)
        ok &= abs(m["duration"] - expected_dur) <= tol
    return _res("export_integrity", ok, **d)


def check_sync(ass_text: str, words: List[Dict[str, Any]], tol_ms: float = 100.0) -> Dict[str, Any]:
    """Option A: every karaoke word onset vs words.json start (+/- tol_ms)."""
    onsets = ass_word_onsets(ass_text)
    if len(onsets) != len(words):
        return _res("subtitle_sync", False, error="word count mismatch", ass=len(onsets), words=len(words))
    deltas = [abs(t - w["start"]) * 1000 for (_, t), w in zip(onsets, words)]
    worst = max(deltas) if deltas else 0.0
    return _res("subtitle_sync", worst <= tol_ms, worst_ms=round(worst, 1), tol_ms=tol_ms, words=len(words))


def check_no_overlap(ass_text: str) -> Dict[str, Any]:
    ev = sorted(ass_events(ass_text))
    bad = [(a, b) for a, b in zip(ev, ev[1:]) if a[1] > b[0] + 1e-6]
    return _res("no_overlap", not bad, overlaps=len(bad))


def check_glyphs(font_path: str | Path, texts: List[str]) -> Dict[str, Any]:
    from .brand import missing_glyphs
    miss = sorted({c for t in texts for c in missing_glyphs(font_path, t)})
    return _res("glyph_coverage", not miss, missing=[f"U+{ord(c):04X}" for c in miss])


def text_bbox(png: str | Path, threshold: int = 40, bg: Tuple[int, int, int] = (0, 0, 0)) -> Optional[Tuple[int, int, int, int]]:
    """Bounding box of pixels that differ from a flat background."""
    import numpy as np
    from PIL import Image
    a = np.asarray(Image.open(png).convert("RGB")).astype(int)
    diff = np.abs(a - np.array(bg)).sum(-1) > threshold
    ys, xs = np.nonzero(diff)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def check_safe_zone(png: str | Path, canvas: Tuple[int, int], margin_lr: int, bottom_px: int,
                    bg: Tuple[int, int, int] = (0, 0, 0)) -> Dict[str, Any]:
    """Subtitle pixels must stay inside: x in [margin, W-margin], bottom edge <= H - bottom_px."""
    box = text_bbox(png, bg=bg)
    if box is None:
        return _res("safe_zone", False, error="no subtitle pixels found")
    W, H = canvas
    x0, y0, x1, y1 = box
    ok = x0 >= margin_lr - 2 and x1 <= W - margin_lr + 2 and y1 <= H - bottom_px + 4
    return _res("safe_zone", ok, bbox=box, limits={"x_min": margin_lr, "x_max": W - margin_lr, "y_max": H - bottom_px})


def check_contrast(fg: str, bg: str, target: float = 7.0, hard_fail: float = 4.5) -> Dict[str, Any]:
    from .style import contrast_ratio
    r = contrast_ratio(fg, bg)
    return _res("contrast", r >= hard_fail, ratio=r, target=target, meets_target=r >= target, hard_fail_below=hard_fail)


def render_ass_on_black(ass_path: str | Path, fonts_dir: str | Path, canvas: Tuple[int, int], t: float,
                        out_png: str | Path, log: Optional[Path] = None, shaping: str = "complex") -> Path:
    """Render a single subtitle frame on pure black (for bbox + glyph human check)."""
    from .render import subtitles_filter
    W, H = canvas
    run_ffmpeg(["-f", "lavfi", "-i", f"color=c=black:s={W}x{H}:r=30:d={t + 0.5:.3f}",
                "-vf", subtitles_filter(ass_path, fonts_dir, shaping) + f",trim=start={t:.3f},setpts=PTS-STARTPTS",
                "-frames:v", "1", str(out_png)], log)
    return Path(out_png)


def qa_report(checks: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {"pass": all(c["pass"] for c in checks), "checks": checks,
            "failed": [c["name"] for c in checks if not c["pass"]]}


def check_shaping(ass_path: str | Path, fonts_dir: str | Path, canvas: Tuple[int, int], t: float,
                  work_dir: str | Path) -> Dict[str, Any]:
    """Automatic broken-glyph detector: render the same frame with complex and with simple
    shaping. Correct conjunct shaping is visibly narrower than the broken (halant-visible)
    simple rendering. Pipeline must use complex and the widths must differ."""
    wd = Path(work_dir)
    good = render_ass_on_black(ass_path, fonts_dir, canvas, t, wd / "shaping_complex.png", shaping="complex")
    bad = render_ass_on_black(ass_path, fonts_dir, canvas, t, wd / "shaping_simple.png", shaping="simple")
    bg, bb = text_bbox(good), text_bbox(bad)
    if not bg or not bb:
        return _res("hindi_shaping", False, error="no text rendered")
    wg, wb = bg[2] - bg[0], bb[2] - bb[0]
    return _res("hindi_shaping", wg < wb * 0.97, complex_width=wg, simple_width=wb, frame=str(good))
