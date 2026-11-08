"""Windows regressions found on the user's PC (2026-10-28): cp1252 default encoding, FFmpeg 9."""
import re
from pathlib import Path

from core import runs

ROOT = Path(__file__).resolve().parent.parent
SRC = [p for d in ("core", "tests", "scripts") for p in (ROOT / d).glob("*.py")] + \
      [ROOT / f for f in ("kang.py", "build_and_check.py", "generate_bundle.py", "app.py")]


def test_no_default_encoding_text_io():
    bad = []
    for p in SRC:
        if p.name == "test_windows_compat.py":
            continue
        for i, line in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if ("read_text()" in line or ("text=True" in line and "encoding=" not in line)
                    or re.search(r"\.write_text\([^)]*\)\s*$", line) and "encoding=" not in line):
                bad.append(f"{p.relative_to(ROOT)}:{i}")
    assert not bad, f"text I/O without encoding='utf-8' (breaks Hindi on Windows): {bad}"


def test_filter_script_args_by_ffmpeg_version(monkeypatch, tmp_path):
    s = tmp_path / "f.txt"
    monkeypatch.setattr(runs, "_FF_MAJOR", 9)
    assert runs.filter_script_args(s) == ["-/filter_complex", str(s)]
    monkeypatch.setattr(runs, "_FF_MAJOR", 6)
    assert runs.filter_script_args(s) == ["-filter_complex_script", str(s)]


def test_no_removed_ffmpeg_options_in_core():
    for p in (ROOT / "core").glob("*.py"):
        if p.name == "runs.py":  # home of the version-aware helper
            continue
        assert "-filter_complex_script" not in p.read_text(encoding="utf-8"), p.name


def test_glossary_chains_to_dwarkadhish():
    """Seen on the user's Windows run (2026-10-28): 'प्राचीन द्वारका दीश मंदिर'."""
    from core.words import apply_glossary, load_glossary
    g = load_glossary(ROOT / "config" / "glossary.json")
    ws = [{"word": w, "start": i, "end": i + 0.5} for i, w in enumerate(["प्राचीन", "द्वारी", "का", "दीश", "मंदिर"])]
    out, ch = apply_glossary(ws, g)
    assert [w["word"] for w in out] == ["प्राचीन", "द्वारकाधीश", "मंदिर"]
    assert out[1]["start"] == 1 and out[1]["end"] == 3.5 and len(ch) == 2
    out2, _ = apply_glossary([{"word": "द्वारका", "start": 0, "end": 1}, {"word": "दीश", "start": 1, "end": 2}], g)
    assert [w["word"] for w in out2] == ["द्वारकाधीश"]
