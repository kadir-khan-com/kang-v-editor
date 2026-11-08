import json
from pathlib import Path

import pytest

from core import script_style as ss

ROOT = Path(__file__).resolve().parents[1]
TAB = ss.load_table(ROOT / "config" / "english_script.json")


def W(*toks):
    return [{"word": t, "start": i * 1.0, "end": i * 1.0 + 0.5} for i, t in enumerate(toks)]


def test_asr_mode_changes_nothing():
    w = W("railway", "station", "थ्री", "डेज")
    out, rep = ss.apply(w, "asr", TAB)
    assert [x["word"] for x in out] == ["railway", "station", "थ्री", "डेज"] and rep["changed"] == 0


def test_devanagari_keeps_timing_and_punctuation():
    w = W("well", "connected", "railway", "station,", "AC")
    out, rep = ss.apply(w, "devanagari", TAB)
    assert [x["word"] for x in out] == ["वेल", "कनेक्टेड", "रेलवे", "स्टेशन,", "एसी"]
    assert [(x["start"], x["end"]) for x in out] == [(x["start"], x["end"]) for x in w]
    assert w[0]["word"] == "well"  # input untouched
    assert rep["unmapped"] == []


def test_devanagari_reports_unmapped_latin():
    out, rep = ss.apply(W("wifi", "station"), "devanagari", TAB)
    assert out[0]["word"] == "wifi" and rep["unmapped"] == ["wifi"]


def test_latin_phrase_only_in_context():
    # 'वन' alone means forest in Hindi -> must NOT change; 'वन नाइट' does
    out, _ = ss.apply(W("घना", "वन", "है"), "latin", TAB)
    assert [x["word"] for x in out] == ["घना", "वन", "है"]
    out, rep = ss.apply(W("टू", "डेज", "और", "वन", "नाइट"), "latin", TAB)
    assert [x["word"] for x in out] == ["two", "days", "और", "one", "night"] and rep["changed"] == 4


def test_bad_mode_and_bad_phrase(tmp_path):
    with pytest.raises(ValueError):
        ss.apply(W("a"), "roman", TAB)
    p = tmp_path / "t.json"
    p.write_text(json.dumps({"to_latin_phrases": [{"dev": "थ्री डेज", "lat": "3days"}]}), encoding="utf-8")
    with pytest.raises(ValueError):
        ss.load_table(p)
