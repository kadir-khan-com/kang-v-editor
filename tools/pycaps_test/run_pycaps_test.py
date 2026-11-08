"""A/B test: pycaps (github.com/francozanardi/pycaps, MIT) vs KANG reels (karaoke-subs) on the same window.

Test-only. Uses our Hinglish layer as an external transcript (no Whisper), the approved visuals as background.
Output: out/pycaps_test/pycaps_<template>.mp4 (+ the input clip). Nothing is published or approved.

PC setup (once):  pip uninstall -y pycaps  (PyPI "pycaps" 0.2.0 is an unrelated Linux-capabilities lib!)
                  pip install https://github.com/francozanardi/pycaps/archive/e2d36edfa08e3307d65b15bb20f17399dc2c9b40.zip html2pic
Run:  python tools/pycaps_test/run_pycaps_test.py runs/2026-11-01_KANG_001/words_hinglish_v1.json ^
          samples/dwarika.mp3 runs/2026-10-31_KANG_008/visuals.json --start 160 --dur 30
"""
import argparse
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from core.captions_adapter import background_args, window_words  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("layer"); ap.add_argument("audio"); ap.add_argument("visuals")
    ap.add_argument("--start", type=float, default=160.0); ap.add_argument("--dur", type=float, default=30.0)
    ap.add_argument("--templates", default="hype,explosive,minimalist")
    ap.add_argument("--out", default=str(ROOT / "out" / "pycaps_test"))
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    doc = json.loads(Path(a.layer).read_text(encoding="utf-8"))
    words = window_words(doc["words"], a.start, a.dur)
    # whisper_json: {"segments":[{"start","end","text","words":[{"word","start","end"}]}]} ; one segment per sentence
    segs, cur = [], []
    for w in words:
        cur.append(w)
        if w["hinglish"][-1:] in ".?!" or len(cur) >= 12:
            segs.append(cur); cur = []
    if cur:
        segs.append(cur)
    wj = {"language": "hi", "segments": [{"start": s[0]["start"], "end": s[-1]["end"],
                                          "text": " ".join(x["hinglish"] for x in s),
                                          "words": [{"word": " " + x["hinglish"], "start": x["start"], "end": x["end"]} for x in s]}
                                         for s in segs]}
    tj = out / "transcript_whisper.json"
    tj.write_text(json.dumps(wj, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp = out / "_tmp"; tmp.mkdir(exist_ok=True)
    bg = background_args(a.visuals, a.start, a.dur, "9:16", 30, tmp)
    clip = out / f"input_9x16_{int(a.start)}s.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(bg), "-ss", str(a.start), "-t", str(a.dur), "-i", a.audio,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-shortest", str(clip)], check=True)
    shutil.rmtree(tmp, ignore_errors=True)
    report = {"tool": "pycaps", "licence": "MIT", "draft_layer": doc.get("status") != "accepted_text", "runs": []}
    for t in a.templates.split(","):
        o = out / f"pycaps_{t}_{int(a.start)}s.mp4"
        t0 = time.time()
        r = subprocess.run([sys.executable, "-c", "import sys; from pycaps.cli import app; sys.argv[0]='pycaps'; app()", "render", "--input", str(clip), "--template", t, "--transcript", str(tj),
                            "--transcript-format", "whisper_json", "--output", str(o)], capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
        report["runs"].append({"template": t, "ok": r.returncode == 0 and o.exists(), "seconds": round(time.time() - t0, 1),
                               "stderr_tail": r.stderr[-1500:]})
        print(t, "OK" if report["runs"][-1]["ok"] else "FAIL", report["runs"][-1]["seconds"], "s")
    (out / "pycaps_test_report.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return 0 if all(x["ok"] for x in report["runs"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
