"""F04 Audio cleanup + loudness.

highpass ~80Hz -> denoise (arnndn if a model file is given, else afftdn) -> light EQ
-> loudnorm two-pass to -14 LUFS / -1.5 dBTP. Before/after measured with ebur128.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, Optional

from .runs import run_ffmpeg


def _ff(args) -> str:
    res = subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", *args], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        raise RuntimeError(res.stderr[-1500:])
    return res.stderr


def measure_loudness(media: str | Path) -> Dict[str, float]:
    """Integrated LUFS, LRA and true peak (dBTP) via ebur128."""
    log = _ff(["-i", str(media), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"])
    summary = log[log.rfind("Summary:"):]
    def grab(pat):
        m = re.search(pat, summary, re.S)
        return float(m.group(1)) if m else float("nan")
    return {
        "integrated_lufs": grab(r"I:\s*(-?[\d.]+|-inf)\s*LUFS"),
        "lra_lu": grab(r"LRA:\s*(-?[\d.]+)\s*LU"),
        "true_peak_dbtp": grab(r"True peak:\s*Peak:\s*(-?[\d.]+|-inf)\s*dBFS"),
    }


def cleanup_chain(denoise: bool = True, rnnoise_model: Optional[str] = None) -> str:
    chain = ["highpass=f=80"]
    if denoise:
        if rnnoise_model and Path(rnnoise_model).is_file():
            chain.append(f"arnndn=m='{Path(rnnoise_model).resolve()}'")
        else:
            chain.append("afftdn=nr=10:nf=-40")  # gentle: avoids 'underwater' voice
    chain.append("equalizer=f=250:t=q:w=1:g=-2")   # reduce mud
    chain.append("equalizer=f=3500:t=q:w=1.2:g=2")  # presence
    return ",".join(chain)


def loudnorm_two_pass(media: str | Path, out: str | Path, target_lufs: float = -14.0, true_peak: float = -1.5,
                      lra: float = 11.0, pre_filter: Optional[str] = None, video_copy: bool = False,
                      log: Optional[Path] = None) -> Dict[str, Any]:
    pre = (pre_filter + ",") if pre_filter else ""
    first = _ff(["-i", str(media), "-vn", "-af",
                 f"{pre}loudnorm=I={target_lufs}:TP={true_peak}:LRA={lra}:print_format=json", "-f", "null", "-"])
    js = json.loads(first[first.rfind("{"): first.rfind("}") + 1])
    second = (f"{pre}loudnorm=I={target_lufs}:TP={true_peak}:LRA={lra}:"
              f"measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:"
              f"measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true,"
              f"aresample=48000")
    args = ["-i", str(media), "-af", second]
    out_s = str(out)
    if video_copy:
        args += ["-c:v", "copy", "-c:a", "aac", "-b:a", "192k"]
    elif out_s.endswith(".wav"):
        args += ["-vn", "-c:a", "pcm_s16le"]
    elif out_s.endswith((".m4a", ".mp4")):
        args += ["-vn", "-c:a", "aac", "-b:a", "192k"]
    else:
        args += ["-vn"]
    run_ffmpeg(args + [out_s], log)
    return {"pass1": js}


def clean_audio(media: str | Path, out: str | Path, target_lufs: float = -14.0, true_peak: float = -1.5,
                denoise: bool = True, rnnoise_model: Optional[str] = None, video_copy: bool = False,
                log: Optional[Path] = None) -> Dict[str, Any]:
    before = measure_loudness(media)
    chain = cleanup_chain(denoise, rnnoise_model)
    info = loudnorm_two_pass(media, out, target_lufs, true_peak, pre_filter=chain, video_copy=video_copy, log=log)
    after = measure_loudness(out)
    correction = []
    for _ in range(3):
        delta = target_lufs - after["integrated_lufs"]
        if not (abs(delta) > 0.3 or after["true_peak_dbtp"] > true_peak + 0.1):
            break
        # loudnorm falls back to dynamic mode when linear gain would clip (e.g. a source
        # already peaking at 0 dBTP) and then undershoots. Corrective pass: exact gain +
        # true-peak-safe limiter (limit 0.5 dB under the TP target, 4x oversampled).
        tmp = Path(out).with_name(Path(out).stem + "_pass2" + Path(out).suffix)
        Path(out).replace(tmp)
        limit = 10 ** ((true_peak - 0.5) / 20)
        af = (f"aresample=192000,volume={delta:.2f}dB,"
              f"alimiter=limit={limit:.4f}:attack=5:release=50:level=disabled,aresample=48000")
        args = ["-i", str(tmp), "-af", af]
        if video_copy:
            args += ["-c:v", "copy", "-c:a", "aac", "-b:a", "192k"]
        elif str(out).endswith(".wav"):
            args += ["-c:a", "pcm_s16le"]
        run_ffmpeg(args + [str(out)], log)
        tmp.unlink(missing_ok=True)
        correction.append({"gain_db": round(delta, 2), "limiter_linear": round(limit, 4)})
        after = measure_loudness(out)
    ok = abs(after["integrated_lufs"] - target_lufs) <= 1.0 and after["true_peak_dbtp"] <= true_peak + 0.3
    return {"chain": chain, "target_lufs": target_lufs, "target_true_peak": true_peak,
            "before": before, "after": after, "correction": correction, "pass": bool(ok), "loudnorm_pass1": info["pass1"],
            "note": "Human A/B listen still required (over-denoise check)."}


def ensure_final_true_peak(video: str | Path, limit_db: float = -1.5, log: Optional[Path] = None,
                           max_passes: int = 3) -> Dict[str, Any]:
    """Measure the DELIVERED file; if AAC overshoot pushed true peak over limit_db, re-limit the
    audio only (video stream copied) with growing margin. Kaggle's FFmpeg 6.1 AAC added +1.6 dB
    on Dwarika full (-3.0 -> -1.4 dBTP), local FFmpeg ~+0.9 dB, so headroom alone is not enough."""
    video = Path(video)
    m = measure_loudness(video)
    passes = []
    for k in range(max_passes):
        if m["true_peak_dbtp"] <= limit_db:
            break
        excess = m["true_peak_dbtp"] - limit_db
        lim = 10 ** ((limit_db - 1.0 - excess - 0.5 * k) / 20)
        tmp = video.with_name(video.stem + "_tpfix" + video.suffix)
        af = f"aresample=192000,alimiter=limit={lim:.4f}:attack=5:release=50:level=disabled,aresample=48000"
        run_ffmpeg(["-i", str(video), "-map", "0", "-c:v", "copy", "-af", af, "-c:a", "aac", "-b:a", "160k",
                    "-movflags", "+faststart", str(tmp)], log)
        tmp.replace(video)
        m = measure_loudness(video)
        passes.append({"limiter_linear": round(lim, 4), "true_peak_after": m["true_peak_dbtp"]})
    return {"measured": m, "passes": passes, "pass": m["true_peak_dbtp"] <= limit_db}
