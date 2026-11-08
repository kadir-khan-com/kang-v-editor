"""app.py /upload must use the same transcription stack as kang.py (not the old engine.run_pipeline)."""
import json
from pathlib import Path

from core import pipeline


def _fake(samples):
    ws = [("नमस्ते", 0.5, 1.6), ("द्वारी", 2.5, 3.0), ("का", 3.0, 3.5), ("दोस्तों।", 4.25, 5.0)]
    return [{"start": 0.5, "end": 5.0, "text": " ".join(w for w, _, _ in ws),
             "words": [{"w": w, "start": s, "end": e, "p": 0.9} for w, s, e in ws]}]


def test_app_worker_uses_pipeline_not_old_engine():
    src = (Path(__file__).resolve().parent.parent / "app.py").read_text(encoding="utf-8")
    assert "pipeline.api_transcribe(" in src
    assert "engine.run_pipeline(" not in src


def test_api_transcribe_keeps_contract_and_applies_glossary(media, tmp_path, monkeypatch):
    monkeypatch.setenv("ENGINE_VOTE", "0")
    out = tmp_path / "storage" / "outputs" / "abcd1234"
    r = pipeline.api_transcribe(str(media / "speech.wav"), str(out), transcriber=_fake)
    assert (out / "transcript.srt").is_file() and (out / "transcript.json").is_file()
    rows = json.loads((out / "transcript.json").read_text(encoding="utf-8"))
    assert rows and {"start", "end", "text", "words"} <= set(rows[0])      # old row shape kept
    words = [w["w"] for row in rows for w in row["words"]]
    assert "द्वारका" in words and "द्वारी" not in words                    # glossary reached the API output
    srt = (out / "transcript.srt").read_text(encoding="utf-8")
    assert "द्वारका" in srt and "-->" in srt
    assert Path(r["run_dir"], "manifest.json").is_file()                     # own run folder + manifest


def test_words_to_rows_splits_on_pause_and_danda():
    ws = [{"word": "एक।", "start": 0.0, "end": 0.5}, {"word": "दो", "start": 0.6, "end": 1.0},
          {"word": "तीन", "start": 2.5, "end": 3.0}]
    rows = pipeline.words_to_rows(ws)
    assert [r["text"] for r in rows] == ["एक।", "दो", "तीन"]
