import numpy as np
from core.gapfill import SR, fill_gaps, find_speech_gaps


def _audio():
    t = np.arange(int(20 * SR)) / SR
    a = (0.2 * np.sin(2 * np.pi * 200 * t)).astype("float32")
    a[int(8 * SR):int(9 * SR)] = 0  # a real pause
    return a


W = [{"word": "एक", "start": 0.2, "end": 2.0, "probability": 0.9},
     {"word": "दो", "start": 2.0, "end": 3.0, "probability": 0.9},
     {"word": "नौ", "start": 15.0, "end": 19.8, "probability": 0.9}]


def test_detects_gap_with_speech_only():
    g = find_speech_gaps(W, _audio())
    assert len(g) == 1 and g[0]["start"] == 3.0 and g[0]["end"] == 15.0
    silent = np.zeros(int(20 * SR), dtype="float32")
    assert find_speech_gaps(W, silent) == []


def test_fill_offsets_and_bounds():
    def fake(clip):  # clip starts at 2.7 s (gap 3.0 - pad 0.3)
        return [{"words": [{"w": "तीन", "start": 0.0, "end": 0.6, "p": 0.8},   # 2.7-3.3 -> clamped 3.0-3.3
                           {"w": "चार", "start": 1.3, "end": 2.0, "p": 0.8},
                           {"w": "बाहर", "start": 12.5, "end": 12.9, "p": 0.8}]}]  # 15.2: outside gap
    out, rep = fill_gaps(W, _audio(), find_speech_gaps(W, _audio()), fake)
    words = [w["word"] for w in out]
    assert words == ["एक", "दो", "तीन", "चार", "नौ"] and rep[0]["filled"] == 2
    t = next(w for w in out if w["word"] == "तीन")
    assert (t["start"], t["end"]) == (3.0, 3.3) and t["gap_fill"]
    assert all(b["start"] >= a["end"] for a, b in zip(out, out[1:]))


def test_empty_retry_keeps_gap_reported():
    out, rep = fill_gaps(W, _audio(), find_speech_gaps(W, _audio()), lambda c: [])
    assert len(out) == 3 and rep[0]["filled"] == 0


def test_seam_low_conf_word_is_repaired():
    """Dwarika v3 6:06: first-pass 'टैक्सी के' (के p=0.10) right after a gap-fill seam hid 'जो भगवान शिव के'."""
    import numpy as np
    from core import gapfill
    sr = gapfill.SR
    samples = (0.2 * np.sin(np.arange(int(8 * sr)) * 0.05)).astype("float32")
    W = [{"word": "मंदिर", "start": 1.0, "end": 1.4, "probability": 0.9, "gap_fill": True},
         {"word": "है।", "start": 1.4, "end": 1.8, "probability": 0.9, "gap_fill": True},
         {"word": "टैक्सी", "start": 2.1, "end": 2.5, "probability": 0.92},
         {"word": "के", "start": 2.5, "end": 2.66, "probability": 0.10},
         {"word": "बारह", "start": 2.66, "end": 3.1, "probability": 0.93}]
    spans = gapfill.find_suspect_spans(W, samples)
    assert any(s.get("seam") for s in spans)

    def fn(clip):  # retry returns the real words with good confidence (clip-relative times)
        return [{"start": 0, "end": 6, "words": [
            {"word": w, "start": s, "end": e, "probability": 0.9} for w, s, e in
            [("मंदिर", 0.3, 0.7), ("है,", 0.7, 1.1), ("जो", 1.1, 1.3), ("भगवान", 1.3, 1.6),
             ("शिव", 1.6, 1.8), ("के", 1.8, 1.96), ("बारह", 1.96, 2.4)]]}]  # clip starts 0.3 s before the window
    out, rep = gapfill.repair_suspect_spans(W, samples, fn, spans=[s for s in spans if s.get("seam")])
    txt = " ".join(w["word"] for w in out)
    assert "टैक्सी" not in txt and "भगवान शिव" in txt, (txt, rep)


def test_seam_not_triggered_by_confident_words():
    import numpy as np
    from core import gapfill
    samples = np.zeros(int(4 * gapfill.SR), "float32")
    W = [{"word": "है।", "start": 1.0, "end": 1.4, "probability": 0.9, "gap_fill": True},
         {"word": "जो", "start": 1.5, "end": 1.7, "probability": 0.6}]
    assert not any(s.get("seam") for s in gapfill.find_suspect_spans(W, samples))
