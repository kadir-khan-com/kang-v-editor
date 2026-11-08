"""Layer 4 Executor: FFmpeg renders.

- burn_subtitles: F01 step 4 (subtitles=subs.ass:fontsdir=./fonts)
- make_preview: 10s low-res preview (approval gate)
- audio_to_video: voiceover-only input -> branded background video (Workflow promo)
- reframe_filter / render_format: F05 multi-format (crop/pad per export, uses EDL reframe_x)
"""
from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from .brand import CANVAS
from .runs import run_ffmpeg


def _filter_path(p: str | Path) -> str:
    """Escape a path for use inside an ffmpeg filtergraph option."""
    s = str(Path(p).resolve()).replace("\\", "/")
    return s.replace(":", r"\:").replace("'", r"\'").replace(",", r"\,")


def subtitles_filter(ass_path: str | Path, fonts_dir: str | Path, shaping: str = "complex") -> str:
    """libass burn-in via the `ass` filter with COMPLEX (HarfBuzz) shaping.

    Verified on FFmpeg 7.1: the default `subtitles` filter (auto/simple shaping) breaks
    Devanagari conjuncts (द्वा -> द्‌वा, क्ष -> क्‌ष). `ass` + shaping=complex renders them correctly.
    """
    return (f"ass=filename='{_filter_path(ass_path)}':fontsdir='{_filter_path(fonts_dir)}'"
            f":shaping={shaping}")


def audio_to_video(audio: str | Path, out: str | Path, fmt: str = "9:16", color: str = "#0F172A",
                   fps: int = 30, start: float = 0.0, duration: Optional[float] = None,
                   log: Optional[Path] = None) -> Path:
    """Voiceover/MP3 -> solid branded background video (for subtitle-only promos)."""
    w, h = CANVAS[fmt]
    args: List[str] = []
    if start:
        args += ["-ss", f"{start:.3f}"]
    if duration:
        args += ["-t", f"{duration:.3f}"]
    args += ["-i", str(audio), "-f", "lavfi", "-i", f"color=c=0x{color.lstrip('#')}:s={w}x{h}:r={fps}",
             "-map", "1:v", "-map", "0:a", "-shortest", *(["-t", f"{duration:.3f}"] if duration else []), "-c:v", "libx264", "-preset", "veryfast", "-crf", "23",
             "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", str(out)]
    run_ffmpeg(args, log)
    return Path(out)


def burn_subtitles(video: str | Path, ass_path: str | Path, fonts_dir: str | Path, out: str | Path,
                   start: float = 0.0, duration: Optional[float] = None, scale_h: Optional[int] = None,
                   crf: int = 20, log: Optional[Path] = None) -> Path:
    """Burn ASS subtitles. start/duration slice the source while keeping subtitle sync
    (setpts keeps original timestamps for libass, then resets)."""
    vf = []
    if start:
        vf.append(f"setpts=PTS+{start:.3f}/TB")
    vf.append(subtitles_filter(ass_path, fonts_dir))
    if start:
        vf.append("setpts=PTS-STARTPTS")
    if scale_h:
        vf.append(f"scale=-2:{scale_h}")
    args: List[str] = []
    if start:
        args += ["-ss", f"{start:.3f}"]
    args += ["-i", str(video)]
    if duration:
        args += ["-t", f"{duration:.3f}"]
    # Full-length burn: copy the already-encoded audio. A second AAC generation raised true peak
    # by ~1.9 dB on Dwarika full (-2.0 -> -0.1 dBTP). Slices/previews still re-encode.
    acodec = ["-c:a", "copy"] if not start and not duration else ["-c:a", "aac", "-b:a", "160k"]
    args += ["-vf", ",".join(vf), "-c:v", "libx264", "-preset", "veryfast" if scale_h else "medium",
             "-crf", str(crf), "-pix_fmt", "yuv420p", *acodec, "-movflags", "+faststart", str(out)]
    run_ffmpeg(args, log)
    return Path(out)


def make_preview(video: str | Path, ass_path: str | Path, fonts_dir: str | Path, out: str | Path,
                 start: float = 0.0, seconds: float = 10.0, log: Optional[Path] = None) -> Path:
    """10-second low-res (960 px tall) preview for the approval gate."""
    return burn_subtitles(video, ass_path, fonts_dir, out, start=start, duration=seconds, scale_h=960,
                          crf=28, log=log)


def reframe_filter(src_w: int, src_h: int, fmt: str, reframe_x: float = 0.5) -> str:
    """Crop to target aspect around reframe_x (0..1 of source width), then scale to canvas.
    Taller-than-target sources are cropped vertically (centered)."""
    tw, th = CANVAS[fmt]
    target = tw / th
    src = src_w / src_h
    if abs(src - target) < 1e-3:
        return f"scale={tw}:{th}"
    if src > target:  # too wide -> crop width
        cw = int(round(src_h * target)) // 2 * 2
        x = int(round(reframe_x * src_w - cw / 2))
        x = max(0, min(src_w - cw, x))
        return f"crop={cw}:{src_h}:{x}:0,scale={tw}:{th}"
    ch = int(round(src_w / target)) // 2 * 2
    y = max(0, (src_h - ch) // 2)
    return f"crop={src_w}:{ch}:0:{y},scale={tw}:{th}"


def render_format(video: str | Path, fmt: str, out: str | Path, src_w: int, src_h: int,
                  ass_path: Optional[str | Path] = None, fonts_dir: Optional[str | Path] = None,
                  reframe_x: float = 0.5, crf: int = 20, log: Optional[Path] = None) -> Path:
    vf = reframe_filter(src_w, src_h, fmt, reframe_x) + ",setsar=1"
    if ass_path:
        vf += "," + subtitles_filter(ass_path, fonts_dir)
    run_ffmpeg(["-i", str(video), "-vf", vf, "-c:v", "libx264", "-preset", "medium", "-crf", str(crf),
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(out)], log)
    return Path(out)


def extract_frame(video: str | Path, t: float, out: str | Path, log: Optional[Path] = None) -> Path:
    run_ffmpeg(["-ss", f"{t:.3f}", "-i", str(video), "-frames:v", "1", str(out)], log)
    return Path(out)
