import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


@pytest.fixture(autouse=True)
def _runs_dir(tmp_path, monkeypatch):
    """Every test writes runs into its own temp folder (originals never touched)."""
    monkeypatch.setenv("KANG_RUNS_DIR", str(tmp_path / "runs"))
    yield


def ff(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-nostdin", "-y", "-v", "error", *args], check=True)


@pytest.fixture(scope="session")
def media(tmp_path_factory):
    """Synthetic offline media (no GPU, no downloads).

    speech.wav: 3 'words' of tone separated by silences:
        tone 0.5-1.5, silence 1.5-2.5, tone 2.5-3.5, silence 3.5-4.3, tone 4.3-5.0 (total 5.5 s)
    video_16x9.mp4: 1920x1080 testsrc 6 s with tone audio
    """
    d = tmp_path_factory.mktemp("media")
    expr = ("0.3*sin(2*PI*220*t)*(between(t,0.5,1.5)+between(t,2.5,3.5)+between(t,4.3,5.0))")
    ff("-f", "lavfi", "-i", f"aevalsrc='{expr}':s=48000:d=5.5", "-c:a", "pcm_s16le", str(d / "speech.wav"))
    ff("-f", "lavfi", "-i", "testsrc2=s=1920x1080:r=30:d=6", "-f", "lavfi", "-i", "sine=f=330:d=6:sample_rate=48000",
       "-shortest", "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p", "-c:a", "aac",
       str(d / "video_16x9.mp4"))
    ff("-f", "lavfi", "-i", "sine=f=440:d=8:sample_rate=48000", "-af", "volume=-30dB", "-c:a", "pcm_s16le",
       str(d / "quiet.wav"))
    return d


@pytest.fixture
def words_speech():
    """Word timings matching speech.wav (Whisper-style: edges slightly swallow silence)."""
    return [
        {"word": "नमस्ते", "start": 0.5, "end": 1.6, "probability": 0.95},
        {"word": "उम्म", "start": 2.5, "end": 3.5, "probability": 0.6},   # auto filler
        {"word": "दोस्तों।", "start": 4.25, "end": 5.0, "probability": 0.9},
    ]


@pytest.fixture
def hindi_words():
    text = "हेलो दोस्तों कैसे हैं आप सभी, यह है भारत का सबसे फेमस हिल स्टेशन दार्जिलिंग। आज द्वारका क्षत्रिय श्री की बात"
    out, t = [], 0.3
    for w in text.split():
        out.append({"word": w, "start": round(t, 3), "end": round(t + 0.32, 3), "probability": 0.9})
        t += 0.4
    return out
