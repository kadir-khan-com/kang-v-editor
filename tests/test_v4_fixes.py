"""v4 Kaggle run fixes: swallowed-word guard in span repair, batched voter fallback."""
from core import gapfill, pipeline


def test_swallowed_word_flags_long_unsure_word():
    assert gapfill._swallowed({"word": "श्योतिर्लिंग", "start": 369.79, "end": 370.99, "probability": 0.57})
    assert not gapfill._swallowed({"word": "ज्योतिर्लिंग", "start": 0.0, "end": 1.0, "probability": 0.9})
    assert not gapfill._swallowed({"word": "है", "start": 0.0, "end": 0.3, "probability": 0.2})
    assert not gapfill._swallowed({"word": "x", "start": 0.0, "end": 1.0})  # no probability -> no opinion


def test_alt_pass_falls_back_when_batched_empty(monkeypatch):
    import sys, types
    calls = {}

    class M:
        def __init__(self, *a, **k): pass

    class B:
        def __init__(self, model): pass
        def transcribe(self, *a, **k): return iter([]), None

    fw = types.SimpleNamespace(WhisperModel=M, BatchedInferencePipeline=B)
    monkeypatch.setitem(sys.modules, "faster_whisper", fw)
    from core import engine

    def fake_transcribe(samples, **k):
        calls["seq"] = True
        return [{"start": 0, "end": 1, "text": "a", "words": [{"word": "a", "start": 0.0, "end": 0.5, "probability": 0.9}]}], {}
    monkeypatch.setattr(engine, "transcribe", fake_transcribe)
    monkeypatch.setattr(pipeline, "VOTE_BATCH", 8)
    out = pipeline._alt_pass("m", [0.0] * 16000, "hi", "cpu", 0, min_words=5)
    assert calls.get("seq") and out and out[0]["word"] == "a"


def test_alt_passes_never_share_a_gpu(monkeypatch, tmp_path):
    import threading, time
    from core.runs import Run
    busy, clash = set(), []
    lock = threading.Lock()

    def fake(src, samples, language, dev, gi, min_words=0):
        with lock:
            if gi in busy:
                clash.append(gi)
            busy.add(gi)
        time.sleep(0.05 if src != "a" else 0.01)
        with lock:
            busy.discard(gi)
        return [{"word": "x", "start": 0.0, "end": 0.1, "probability": 0.9}]
    monkeypatch.setattr(pipeline, "_alt_pass", fake)
    monkeypatch.setattr(pipeline, "_cuda_count", lambda: 2)
    monkeypatch.setattr(pipeline, "_ALT_CACHE", {})
    voters = {n: n for n in "abcd"}
    wl = tmp_path / "w.dic"; wl.write_text("x\n", encoding="utf-8")
    class R:
        def warn(self, m): raise AssertionError(m)
        def log_step(self, *a, **k): pass
    words = [{"word": "x", "start": 0.0, "end": 0.1, "probability": 0.9}]
    pipeline._spelling_vote(words, [0.0] * 1600, voters, str(wl), True, {}, "cuda", "hi", R(), audio_path="")
    assert not clash
