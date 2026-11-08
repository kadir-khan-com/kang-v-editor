import json

import pytest

pytest.importorskip("karaoke_subs")
from core.captions_adapter import build_ass, load_layer, load_preset, qa, window_words  # noqa: E402


def _layer(tmp_path, status="draft"):
    ws = [{"word_id": i, "hindi": "x", "hinglish": t, "start": 10 + i * 0.5, "end": 10 + i * 0.5 + 0.4,
           "timing_status": "verified_pending"} for i, t in enumerate(["Dwarka", "yatra,", "aur", "{\\b1}darshan"])]
    p = tmp_path / "l.json"
    p.write_text(json.dumps({"status": status, "words": ws}), encoding="utf-8")
    return p


def test_draft_gate(tmp_path):
    with pytest.raises(PermissionError):
        load_layer(str(_layer(tmp_path)), allow_draft=False)
    assert load_layer(str(_layer(tmp_path, "accepted_text")), allow_draft=False)[1] is True


@pytest.mark.parametrize("name", ["karaoke_yellow", "bold_pop", "clean_travel"])
def test_presets_build_ass(tmp_path, name):
    doc, acc = load_layer(str(_layer(tmp_path)), allow_draft=True)
    words = window_words(doc["words"], 10.0, 5.0)
    assert words[0]["start"] == 0.0
    pre = load_preset(name)
    ass, lines = build_ass(words, pre, "9:16")
    assert "PlayResX: 1080" in ass and "PlayResY: 1920" in ass and "\\k" in ass
    assert "{\\b1}" not in ass  # text can't inject tags
    if pre.get("uppercase"):
        assert "DWARKA" in ass
    rep = qa(lines, words, pre, "9:16", acc)
    assert rep["draft"] and rep["status"] == "WARN" and rep["checks"]["timing"] == "PASS"
    assert rep["checks"]["safe_zone_vertical"] == "PASS" and rep["human_playback_qa"] == "NOT_TESTED"


def test_unknown_preset():
    with pytest.raises(ValueError):
        load_preset("nope")
