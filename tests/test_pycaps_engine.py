import json

import pytest

from core import pycaps_engine as pe
from core.captions_adapter import load_preset, make_reel
from core.runs import Run


def _layer(tmp_path, status="draft"):
    (tmp_path / "runs").mkdir(exist_ok=True)
    toks = ["Dwarka", "yatra.", "aur", "darshan", "karein"]
    ws = [{"word_id": i, "hindi": "x", "hinglish": t, "start": 10 + i * 0.5, "end": 10 + i * 0.5 + 0.4,
           "timing_status": "verified_pending"} for i, t in enumerate(toks)]
    p = tmp_path / "l.json"
    p.write_text(json.dumps({"status": status, "words": ws}), encoding="utf-8")
    return p


def test_whisper_json_segments():
    words = [{"hinglish": t, "start": i * 0.5, "end": i * 0.5 + 0.4} for i, t in enumerate(["a", "b.", "c"])]
    wj = pe.to_whisper_json(words)
    assert [s["text"] for s in wj["segments"]] == ["a b.", "c"]
    assert wj["segments"][0]["words"][1] == {"word": " b.", "start": 0.5, "end": 0.9}


def test_stage_template_copies_font_and_bans_audio_ai(tmp_path):
    pre = load_preset("pop_safe")
    tj = pe.stage_template(pre, tmp_path / "t")
    assert (tmp_path / "t" / "resources" / "Montserrat-Black.ttf").exists()
    cfg = json.loads(tj.read_text(encoding="utf-8"))
    va = cfg["layout"]["vertical_align"]
    assert va["align"] == "center" and cfg["layout"]["max_number_of_lines"] == 2
    assert cfg["layout"]["on_text_overflow_strategy"] == "exceed_width"  # never a 3rd line
    # pycaps centre: top = (H - h) * (offset + 0.5); 2-line block h ~ 250 px at 1920
    H, h = 1920, 250
    bottom = ((H - h) * (va["offset"] + 0.5) + h) / H
    assert abs(bottom - pre["text_bottom_ratio"]) < 0.01
    cfg["sound_effects"] = [{"type": "preset", "name": "ding"}]
    tj.write_text(json.dumps(cfg), encoding="utf-8")
    bad = dict(pre, template_dir=str(tmp_path / "t"))
    with pytest.raises(ValueError):
        pe.stage_template(bad, tmp_path / "t2")


def test_pop_safe_no_render_draft(tmp_path):
    (tmp_path / "a.mp3").write_bytes(b"x")
    r = make_reel(str(tmp_path / "a.mp3"), str(_layer(tmp_path)), style="pop_safe", start=10, dur=5,
                  allow_draft=True, render=False, run=Run(root=tmp_path / "runs"))
    assert r["draft"] and r["status"] == "WARN"
    assert r["checks"]["safe_zone_vertical_config"] == "PASS" and r["checks"]["timing"] == "PASS"
    assert "DRAFT_reel_pop_safe" in r["files"]["qa"]
    wj = json.loads(open(r["files"]["transcript"], encoding="utf-8").read())
    assert wj["segments"][0]["start"] == 0.0


def test_pop_safe_draft_gate(tmp_path):
    with pytest.raises(PermissionError):
        make_reel("a.mp3", str(_layer(tmp_path)), style="pop_safe", render=False, run=Run(root=tmp_path / "runs"))


def test_missing_engine_message(tmp_path, monkeypatch):
    import builtins
    real = builtins.__import__

    def fake(name, *a, **k):
        if name == "pycaps":
            raise ImportError("No module named 'pycaps'")
        return real(name, *a, **k)
    monkeypatch.setattr(builtins, "__import__", fake)
    with pytest.raises(RuntimeError, match="pip install"):
        pe.render(tmp_path / "c.mp4", tmp_path / "t.json", tmp_path / "x.json", tmp_path / "o.mp4")
