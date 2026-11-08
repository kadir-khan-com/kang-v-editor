"""Roadmap v2 §11.2: every font and every model weight has a licence on record."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_every_font_has_ofl_file():
    fonts = ROOT / "fonts"
    lic = {p.name for p in fonts.glob("OFL-*.txt")}
    for ttf in fonts.glob("*.ttf"):
        family = ttf.stem.split("-")[0].replace("NotoSansDevanagari", "Noto")
        assert f"OFL-{family}.txt" in lic, f"licence missing for {ttf.name}"


def test_every_voter_model_has_licence_and_revision():
    voters = json.loads((ROOT / "config" / "voters.json").read_text(encoding="utf-8"))["voters"]
    lic = json.loads((ROOT / "config" / "model_licenses.json").read_text(encoding="utf-8"))
    for name in voters:
        meta = lic["voters"].get(name)
        assert meta and meta.get("licence") and meta.get("revision") and meta.get("source"), name
    assert lic["base_asr"]["licence"] and lic["wordlist"]["licence"]


def test_wx_align_copies_identical():
    a = (ROOT / "tools" / "kaggle_ab" / "wx_align.py").read_bytes()
    b = (ROOT / "tools" / "kaggle_wx" / "wx_align.py").read_bytes()
    assert a == b, "kaggle kernels need a self-contained copy; edit tools/kaggle_wx/wx_align.py and copy it"
