"""Regressions from the Dwarika full-length Kaggle T4 run (2026-10-28)."""
import json
from pathlib import Path

import numpy as np

from core.gapfill import SR, find_suspect_spans, repair_suspect_spans
from core.words import apply_glossary, join_split_tokens, load_glossary

ROOT = Path(__file__).resolve().parents[1]


def _speech(seconds: float) -> np.ndarray:
    t = np.arange(int(seconds * SR)) / SR
    return (0.2 * np.sin(2 * np.pi * 220 * t)).astype("float32")  # loud everywhere = "speech"


def _w(word, s, e):
    return {"word": word, "start": s, "end": e, "probability": 0.9}


def test_stretched_word_is_a_suspect_span():
    words = [_w("कर", 0.0, 0.3), _w("लिया", 0.3, 0.6), _w("ले करने के", 0.6, 12.2), _w("बाद", 12.2, 12.5)]
    spans = find_suspect_spans(words, _speech(13))
    assert len(spans) == 1 and spans[0]["start"] == 0.6 and "long_word" in spans[0]["why"]


def test_repair_swaps_in_better_words_only():
    words = [_w("कर", 0.0, 0.3), _w("ले", 0.3, 6.0), _w("बाद", 6.0, 6.3)]
    good = lambda clip: [{"words": [{"w": f"श{i}", "start": 0.3 + i * 0.5, "end": 0.75 + i * 0.5, "p": 0.9} for i in range(12)]}]
    new, rep = repair_suspect_spans(words, _speech(7), good)
    assert rep[0]["accepted"] and all(w["end"] - w["start"] <= 1.2 for w in new) and len(new) >= 12
    bad = lambda clip: [{"words": [{"w": "ले", "start": 0.6, "end": 6.0, "p": 0.9}]}]  # still stretched
    same, rep2 = repair_suspect_spans(words, _speech(7), bad)
    assert not rep2[0]["accepted"] and [w["word"] for w in same] == ["कर", "ले", "बाद"]


def test_join_split_tokens():
    words = [_w("साथ", 0, 0.3), _w("-साथ,", 0.3, 0.6), _w("10", 1, 1.2), _w(",000", 1.2, 1.5), _w("400", 2, 2.2), _w("-500", 2.2, 2.5), _w("आप", 3, 3.2)]
    out, joins = join_split_tokens(words)
    assert [w["word"] for w in out] == ["साथ-साथ,", "10,000", "400-500", "आप"] and len(joins) == 3
    assert out[0]["start"] == 0 and out[0]["end"] == 0.6


def test_spelling_glossary_and_context_rules():
    g = load_glossary(ROOT / "config" / "glossary.json")
    words = [_w(t, i, i + 0.5) for i, t in enumerate("शुरी कृष्ण ने मतूरा से 2 किलोमेटर बारा जोतिर्लिंग मंदीर में".split())]
    out, _ = apply_glossary(words, g)
    assert " ".join(w["word"] for w in out) == "श्री कृष्ण ने मथुरा से 2 किलोमीटर बारह ज्योतिर्लिंग मंदिर में"
    # context-only rules must not fire alone
    alone, ch = apply_glossary([_w("बारा", 0, 0.4), _w("चपल", 0.4, 0.8)], g)
    assert [w["word"] for w in alone] == ["बारा", "चपल"] and not ch


def test_burn_full_copies_audio(monkeypatch):
    from core import render
    seen = {}
    monkeypatch.setattr(render, "run_ffmpeg", lambda args, log=None: seen.setdefault("a", args))
    render.burn_subtitles("in.mp4", "s.ass", "fonts", "out.mp4")
    a = seen["a"]
    assert a[a.index("-c:a") + 1] == "copy"
    seen.clear()
    render.burn_subtitles("in.mp4", "s.ass", "fonts", "out.mp4", start=5, duration=10)
    assert seen["a"][seen["a"].index("-c:a") + 1] == "aac"


def test_repair_drops_duplicate_edge_word():
    words = [_w("आपकी", 0.0, 0.3), _w("ले", 0.3, 3.0), _w("को", 3.0, 3.1), _w("जरूर", 3.1, 3.4)]
    retry = lambda clip: [{"words": [{"w": t, "start": 0.3 + i * 0.45, "end": 0.7 + i * 0.45, "p": 0.9}
                                     for i, t in enumerate("सभी मनोकामना पूरी हो करेंगे को".split())]}]
    new, rep = repair_suspect_spans(words, _speech(4), retry, context=0.0)
    texts = [w["word"] for w in new]
    assert rep[0]["accepted"] and texts.count("को") == 1


def test_ensure_final_true_peak_relimits_hot_file(tmp_path):
    import shutil, pytest
    if not shutil.which("ffmpeg"):
        pytest.skip("ffmpeg missing")
    from core import audio
    from core.runs import run_ffmpeg
    hot = tmp_path / "hot.mp4"
    run_ffmpeg(["-f", "lavfi", "-i", "color=c=black:s=320x240:r=30:d=3", "-f", "lavfi", "-i",
                "sine=f=997:d=3,volume=0dB", "-shortest", "-c:v", "libx264", "-c:a", "aac", "-b:a", "160k", str(hot)])
    r = audio.ensure_final_true_peak(hot, -1.5)
    assert r["pass"] and r["measured"]["true_peak_dbtp"] <= -1.5
