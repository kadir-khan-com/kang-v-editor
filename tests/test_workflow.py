import json
from pathlib import Path

from core import pipeline
from core.runs import media_summary


def _fake(samples):
    ws = [("नमस्ते", 0.5, 1.6), ("द्वारी", 2.5, 3.0), ("का", 3.0, 3.5), ("दोस्तों।", 4.25, 5.0)]
    return [{"start": 0.5, "end": 5.0, "text": " ".join(w for w, _, _ in ws),
             "words": [{"w": w, "start": s, "end": e, "p": 0.9} for w, s, e in ws]}]


def test_workflow_end_to_end_mock(media):
    r = pipeline.workflow_clip(str(media / "speech.wav"), 0.0, 5.5, formats=["9:16", "1:1"],
                               approver=lambda g, i: True, transcriber=_fake)
    assert r["pass"], json.dumps(r["checks"], ensure_ascii=False)
    d = Path(r["dir"])
    assert (d / "workflow_report.json").is_file()
    for fmt, size in (("9:16", (1080, 1920)), ("1:1", (1080, 1080))):
        m = media_summary(r["stages"]["finals"][fmt])
        assert (m["width"], m["height"]) == size
    tw = json.loads((Path(r["dir"]).parent / r["stages"]["transcribe"] / "words.json").read_text(encoding="utf-8"))
    assert "द्वारका" in [w["word"] for w in tw]          # glossary applied automatically
    loud = next(c for c in r["checks"] if c["name"] == "loudness")
    assert loud["pass"]


def test_workflow_stops_at_cut_gate(media):
    r = pipeline.workflow_clip(str(media / "speech.wav"), 0.0, 5.5, transcriber=_fake)  # default approver denies
    assert not r["pass"] and "audio" not in r["stages"]
    assert json.loads((Path(r["dir"]) / "manifest.json").read_text(encoding="utf-8"))["status"] == "awaiting_cut_approval"


def test_workflow_full_mode_whole_file_16x9(media):
    """--full: duration = whole file from start, default format 16:9, no 60 s cap."""
    src = media / "speech.wav"
    total = media_summary(src)["duration"]
    r = pipeline.workflow_clip(str(src), 0.0, 999.0, approver=lambda g, i: True, transcriber=_fake, full=True)
    assert r["pass"], json.dumps(r["checks"], ensure_ascii=False)
    assert r["full"] and abs(r["duration"] - total) < 0.01 and "seconds_taken" in r
    assert list(r["stages"]["finals"]) == ["16:9"]
    m = media_summary(r["stages"]["finals"]["16:9"])
    assert (m["width"], m["height"]) == (1920, 1080)


def test_clip_mode_keeps_60s_cap(media):
    import pytest
    with pytest.raises(ValueError, match="--full"):
        pipeline.workflow_clip(str(media / "speech.wav"), 0.0, 61.0, transcriber=_fake)
