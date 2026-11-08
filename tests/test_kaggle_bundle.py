"""Kaggle bundle regression tests: notebook Cell 1 -> sync -> setup_kaggle, fully offline.

Everything that would touch the network or the machine (apt-get, pip, fc-cache, font download,
cloudflared download) is stubbed. Paths are redirected with ENGINE_BASE_DIR / KAGGLE_INPUT_DIR,
so nothing is written to /kaggle or system folders.
"""
import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
NB = ROOT / "ai_video_engine_kaggle_ready.ipynb"
BUNDLE = ROOT / "kaggle_sync_bundle.py"
pytestmark = pytest.mark.skipif(not NB.is_file(), reason="notebook not in this tree")


def cell1() -> str:
    nb = json.loads(NB.read_text(encoding="utf-8"))
    return "".join(nb["cells"][1]["source"])


@pytest.fixture
def kaggle(tmp_path, monkeypatch):
    base, inp = tmp_path / "working" / "ai-video-engine", tmp_path / "input"
    (inp / "dataset").mkdir(parents=True)
    monkeypatch.setenv("ENGINE_BASE_DIR", str(base))
    monkeypatch.setenv("KAGGLE_INPUT_DIR", str(inp))
    real_run, real_which = subprocess.run, shutil.which

    def fake_run(cmd, *a, **k):
        if isinstance(cmd, str) and any(t in cmd for t in ("apt-get", "pip install", "fc-cache")):
            return subprocess.CompletedProcess(cmd, 0, "", "")
        if isinstance(cmd, list) and (any(str(c).endswith("fetch_fonts.py") for c in cmd)
                                      or ("install" in cmd and any("pip" in str(c) for c in cmd))
                                      or any(str(c) in ("apt-get", "fc-cache") for c in cmd)):
            return subprocess.CompletedProcess(cmd, 0, "", "")
        if isinstance(cmd, list) and "install" in cmd:  # never let an "offline" test reach the network
            raise AssertionError(f"unstubbed install in offline test: {cmd}")
        return real_run(cmd, *a, **k)

    def offline(*a, **k):
        raise urllib.error.URLError("Kaggle internet OFF (simulated)")

    monkeypatch.setattr(subprocess, "run", fake_run)
    monkeypatch.setattr(urllib.request, "urlretrieve", offline)
    monkeypatch.setattr(shutil, "which", lambda n, *a, **k: None if n == "cloudflared" else real_which(n, *a, **k))
    return base, inp / "dataset"


def run_cell():
    exec(compile(cell1(), "bundle_cell", "exec"), {"__name__": "__main__"})


def test_notebook_cell1_matches_bundle_file():
    assert cell1() == BUNDLE.read_text(encoding="utf-8"), "run generate_bundle.py"


def test_sync_and_setup_with_internet_off(kaggle, media, capsys):
    base, ds = kaggle
    shutil.copy(media / "speech.wav", ds / "6 Dwarika enhanced.mp3")  # content is probed by ffprobe, not extension
    run_cell()
    out = capsys.readouterr().out
    for rel in ("core/engine.py", "core/pipeline.py", "kang.py", "setup_kaggle.py", "brand.json", "presets/promo.json"):
        assert (base / rel).is_file(), rel
    for d in ("storage/inputs", "storage/temp", "storage/outputs"):
        assert (base / d).is_dir(), d
    assert (base / "storage/inputs/voiceover.mp3").stat().st_size > 0
    assert "WARNING: cloudflared not installed" in out      # offline must not abort setup
    assert "STAGE 1 VERIFICATION REPORT" in out


def test_missing_audio_stops_with_clear_error(kaggle):
    with pytest.raises(FileNotFoundError, match="6 Dwarika enhanced.mp3"):
        run_cell()


def test_ambiguous_audio_is_not_guessed(kaggle, media):
    _, ds = kaggle
    shutil.copy(media / "speech.wav", ds / "dwarika take1.mp3")
    shutil.copy(media / "speech.wav", ds / "voiceover take2.mp3")
    with pytest.raises(RuntimeError, match="AMBIGUOUS"):
        run_cell()


def test_build_and_check_passes_in_runtime_tree(kaggle, media):
    """On Kaggle only runtime files exist (no tests/, test_offline.py, generate_bundle.py)."""
    base, ds = kaggle
    shutil.copy(media / "speech.wav", ds / "6 Dwarika enhanced.mp3")
    run_cell()
    shutil.copytree(ROOT / "fonts", base / "fonts", dirs_exist_ok=True)   # Kaggle: fetch_fonts (internet on)
    r = subprocess.run([sys.executable, "build_and_check.py", "--no-bundle"], cwd=base,
                       capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=300)
    assert r.returncode == 0, r.stdout + r.stderr
    assert "SKIP" in r.stdout and "RESULT: PASS" in r.stdout
