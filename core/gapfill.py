"""Speech-gap detection + bounded re-transcription.

Whisper sometimes skips 10-20 s of real speech inside one segment (found on Dwarika 60-120 s:
13.1 -> 29.98 s had speech at -20 dB mean but zero words). Subtitles then vanish.

find_speech_gaps(): gaps between consecutive words (and at clip edges) longer than `min_gap`
whose audio is mostly above `speech_db` (RMS, 100 ms frames).
fill_gaps(): re-transcribe only that window (with small padding), keep words that fall inside
the gap, offset back to clip time. Nothing is invented; if the retry returns nothing usable the
gap stays and is reported for human review.
"""
from __future__ import annotations

from typing import Any, Callable, Dict, List, Tuple

SR = 16000
# Roadmap v2 §6.2: every voiced gap > 2 s is detected, retried and either resolved or listed for review.
COVERAGE_GAP_S = 2.0
# A gap still this long after retry blocks the run (unchanged since the Dwarika runs); 2-3 s leftovers
# are reported as needs_review (RMS activity can be breath/music, so it is not "confirmed speech").
BLOCKING_GAP_S = 3.0


def no_overlap(words: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Trim each word's end to the next word's start. Never pushes an end past the next start (the old
    max(start+0.04, next) guard could). A word squeezed to zero length is not dropped and gets no
    invented duration: its text merges into the neighbour (words.merge_zero_duration); a squeezed but
    still positive word keeps its tiny duration and is flagged timing_squeezed for review."""
    from .words import merge_zero_duration
    out = sorted((dict(w) for w in words), key=lambda w: (w["start"], w["end"]))
    for a, b in zip(out, out[1:]):
        if b["start"] < a["end"]:
            a["end"] = max(a["start"], b["start"])
            if a["end"] - a["start"] < 0.04:
                a["timing_squeezed"] = True
    return merge_zero_duration(out)


def _active_ratio(samples, t0: float, t1: float, speech_db: float, frame: float = 0.1) -> float:
    import numpy as np
    a = samples[int(t0 * SR):int(t1 * SR)]
    n = int(frame * SR)
    if len(a) < n:
        return 0.0
    a = a[: len(a) // n * n].reshape(-1, n)
    rms = np.sqrt((a.astype("float64") ** 2).mean(axis=1)) + 1e-12
    db = 20 * np.log10(rms)
    return float((db > speech_db).mean())


def find_speech_gaps(words: List[Dict[str, Any]], samples, min_gap: float = COVERAGE_GAP_S,
                     speech_db: float = -35.0, min_active: float = 0.4) -> List[Dict[str, Any]]:
    total = len(samples) / SR
    edges = [0.0] + [x for w in words for x in (w["start"], w["end"])] + [total]
    gaps = []
    for i in range(0, len(edges), 2):
        g0, g1 = edges[i], edges[i + 1]
        if g1 - g0 >= min_gap:
            r = _active_ratio(samples, g0, g1, speech_db)
            if r >= min_active:
                gaps.append({"start": round(g0, 3), "end": round(g1, 3), "active": round(r, 2)})
    return gaps


def fill_gaps(words: List[Dict[str, Any]], samples, gaps: List[Dict[str, Any]],
              transcribe_fn: Callable[[Any], List[Dict[str, Any]]], pad: float = 0.3
              ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """transcribe_fn(samples_slice) -> engine rows. Returns (words, report)."""
    from .words import rows_to_words
    out = [dict(w) for w in words]
    report = []
    for g in gaps:
        c0 = max(0.0, g["start"] - pad)
        c1 = min(len(samples) / SR, g["end"] + pad)
        try:
            rows = transcribe_fn(samples[int(c0 * SR):int(c1 * SR)])
        except Exception as exc:  # pragma: no cover
            report.append({**g, "filled": 0, "error": str(exc)})
            continue
        new = []
        for w in rows_to_words(rows):
            s, e = round(w["start"] + c0, 3), round(w["end"] + c0, 3)
            s, e = max(s, g["start"]), min(e, g["end"])
            if e - s >= 0.04:
                new.append({**w, "start": s, "end": e, "gap_fill": True})
        report.append({**g, "filled": len(new)})
        out.extend(new)
    # guard: no overlaps introduced at the joins
    return no_overlap(out), report


# --- Suspect-span repair ---------------------------------------------------------------
# Found on Dwarika full (Kaggle T4, 2026-10-28): Whisper compressed whole sentences into one
# stretched token ("ले करने के" = 11.56 s at 571.5 s; "द" = 1.5 s + 2.2 s silence-free gap at
# 176 s). find_speech_gaps() never saw them: the stretched word *covers* the missing speech and
# the leftover gaps were below the old 3 s detector. A bounded re-transcription of a ~10 s window around each span
# recovered every missing word in tests. Nothing is invented: if the retry is not clearly better
# the original words stay and the span is reported for review.
LONG_WORD_S = 1.2       # a single Hindi word longer than this almost always hides dropped words
SHORT_GAP_S = 0.8       # inter-word gap that is mostly speech energy
# Dwarika v3 (2026-10-29, user review at 6:06): a gap-fill window ended exactly on a first-pass
# word, so 'जो भगवान शिव के' (369.3-370.2 s) survived as the first-pass hallucination 'टैक्सी के'
# (के p=0.10). Coverage looked fine, so neither trigger above fired. A very low-confidence word
# right at a gap-fill seam is now a suspect span, accepted on confidence instead of coverage.
SEAM_LOW_PROB = 0.2
SEAM_WINDOW_S = 1.5
CONTEXT_S = 3.0


def _uncovered_speech(words, samples, t0: float, t1: float, speech_db: float = -35.0, long_word: float = LONG_WORD_S) -> float:
    """Seconds of speech-energy audio in [t0, t1] not covered by a plausible-length word."""
    import numpy as np
    frame = 0.05
    n = max(0, int((t1 - t0) / frame))
    if n == 0:
        return 0.0
    cov = np.zeros(n, bool)
    for w in words:
        if w["end"] - w["start"] > long_word:
            s, e = w["start"], w["start"] + 0.6  # only the plausible head of a stretched word counts
        else:
            s, e = w["start"], w["end"]
        a, b = int((s - t0) / frame), int((e - t0) / frame) + 1
        cov[max(0, a):max(0, min(n, b))] = True
    a = samples[int(t0 * SR):int(t0 * SR) + n * int(frame * SR)]
    if len(a) < n * int(frame * SR):
        n = len(a) // int(frame * SR)
        cov = cov[:n]
        a = a[: n * int(frame * SR)]
    if n == 0:
        return 0.0
    rms = np.sqrt((a.astype("float64").reshape(n, -1) ** 2).mean(axis=1)) + 1e-12
    speech = 20 * np.log10(rms) > speech_db
    return round(float((speech & ~cov).sum() * frame), 2)


def _drop_edge_duplicates(new: List[Dict[str, Any]], neighbours: List[Dict[str, Any]], tol: float = 0.25) -> List[Dict[str, Any]]:
    """Retry windows overlap the kept words by a few frames, so the edge word can come back twice
    (Dwarika 169.1 s: 'को को'). Drop a new edge word whose text matches the adjacent kept word."""
    if not new or not neighbours:
        return new
    from .words import _bare
    left = max((w for w in neighbours if w["end"] <= new[0]["start"] + tol), key=lambda w: w["end"], default=None)
    right = min((w for w in neighbours if w["start"] >= new[-1]["end"] - tol), key=lambda w: w["start"], default=None)
    if left is not None and _bare(left["word"]) == _bare(new[0]["word"]) and new[0]["start"] - left["end"] <= tol:
        new = new[1:]
    if new and right is not None and _bare(right["word"]) == _bare(new[-1]["word"]) and right["start"] - new[-1]["end"] <= tol:
        new = new[:-1]
    return new


def find_suspect_spans(words: List[Dict[str, Any]], samples, speech_db: float = -35.0,
                       long_word: float = LONG_WORD_S, short_gap: float = SHORT_GAP_S,
                       merge_within: float = 2.0) -> List[Dict[str, Any]]:
    spans = []
    for i, w in enumerate(words):
        if w["end"] - w["start"] > long_word:
            spans.append({"start": w["start"], "end": w["end"], "why": f"long_word {w['word']!r} {w['end'] - w['start']:.2f}s"})
    for a, b in zip(words, words[1:]):
        if b["start"] - a["end"] >= short_gap and _active_ratio(samples, a["end"], b["start"], speech_db) >= 0.5:
            spans.append({"start": a["end"], "end": b["start"], "why": f"speech_gap {b['start'] - a['end']:.2f}s"})
    for i, w in enumerate(words):
        if w.get("gap_fill") or w.get("probability", 1.0) >= SEAM_LOW_PROB:
            continue
        near = [x for x in words[max(0, i - 4):i + 5]
                if x.get("gap_fill") and (abs(x["end"] - w["start"]) <= SEAM_WINDOW_S or abs(w["end"] - x["start"]) <= SEAM_WINDOW_S)]
        if near:
            first = next((x for x in words[i::-1] if x.get("gap_fill")), None)  # seam start = last filled word before
            s0 = first["end"] if first and first["end"] <= w["start"] else w["start"]
            spans.append({"start": s0, "end": w["end"], "why": f"seam_low_conf {w['word']!r} p={w['probability']:.2f}",
                          "seam": True})
    spans.sort(key=lambda s: s["start"])
    merged: List[Dict[str, Any]] = []
    for s in spans:
        if merged and s["start"] - merged[-1]["end"] <= merge_within:
            merged[-1]["end"] = max(merged[-1]["end"], s["end"])
            merged[-1]["why"] += "; " + s["why"]
            merged[-1]["seam"] = merged[-1].get("seam", False) or s.get("seam", False)
        else:
            merged.append(dict(s))
    return [{**s, "start": round(s["start"], 3), "end": round(s["end"], 3)} for s in merged]


def _conf(ws: List[Dict[str, Any]]) -> Tuple[float, float]:
    ps = [w.get("probability", 1.0) for w in ws] or [0.0]
    return min(ps), sum(ps) / len(ps)


SWALLOW_S = 0.9     # a repaired word this long ...
SWALLOW_PROB = 0.7  # ... and this unsure has usually swallowed several words
                    # (Dwarika 369.8 s: 'शिव के बारह ज्योतिर्लिंग' -> one 1.2 s 'श्योतिर्लिंग', p 0.57)


def _swallowed(w: Dict[str, Any]) -> bool:
    p = w.get("probability", w.get("p"))
    return p is not None and w["end"] - w["start"] > SWALLOW_S and p < SWALLOW_PROB


def repair_suspect_spans(words: List[Dict[str, Any]], samples, transcribe_fn: Callable[[Any], List[Dict[str, Any]]],
                         spans: List[Dict[str, Any]] | None = None, context: float = CONTEXT_S,
                         speech_db: float = -35.0, fallback_fns: List[Callable[[Any], List[Dict[str, Any]]]] | None = None
                         ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Re-transcribe a word-aligned window around each suspect span; swap in the new words only
    when they cover the span's speech better and contain no stretched word. If an attempt is not
    accepted, each fallback_fn (e.g. same model without the domain prompt) is tried in order.
    Returns (words, report)."""
    from .words import rows_to_words
    out = [dict(w) for w in words]
    spans = find_suspect_spans(out, samples, speech_db) if spans is None else spans
    total = len(samples) / SR
    report = []
    for sp in spans:
        rec: Dict[str, Any] = {**sp, "attempts": []}
        ok = False
        # Whisper is window-sensitive (Dwarika 571 s: a 568.3 s start merged garbage into one 4 s
        # token, 566.5 s came back clean), so try a wider window too, each with every transcriber.
        for ctx in (context, context + 2.0):
            inside = [w for w in out if w["start"] >= sp["start"] - ctx and w["end"] <= sp["end"] + ctx]
            w0 = min([w["start"] for w in inside] + [sp["start"]])
            w1 = max([w["end"] for w in inside] + [sp["end"]])
            c0, c1 = max(0.0, w0 - 0.3), min(total, w1 + 0.3)
            old = [w for w in out if w["start"] >= w0 - 1e-6 and w["end"] <= w1 + 1e-6]
            before = _uncovered_speech(old, samples, w0, w1, speech_db)
            for k, fn in enumerate([transcribe_fn] + list(fallback_fns or [])):
                try:
                    rows = fn(samples[int(c0 * SR):int(c1 * SR)])
                except Exception as exc:  # pragma: no cover
                    rec["attempts"].append({"context": ctx, "fn": k, "error": str(exc)})
                    continue
                new = []
                for w in rows_to_words(rows):
                    s, e = round(w["start"] + c0, 3), round(w["end"] + c0, 3)
                    if w0 - 0.05 <= (s + e) / 2 <= w1 + 0.05:
                        new.append({**w, "start": max(s, w0), "end": min(e, w1), "repaired": True})
                new = [w for w in new if w["end"] - w["start"] >= 0.04]
                new = _drop_edge_duplicates(new, [w for w in out if w["end"] <= w0 + 1e-6 or w["start"] >= w1 - 1e-6])
                after = _uncovered_speech(new, samples, w0, w1, speech_db)
                stretched = [w["word"] for w in new if w["end"] - w["start"] > LONG_WORD_S
                             or _swallowed(w)]
                ok = bool(new) and not stretched and after < before and len(new) >= len(old) * 0.8
                if not ok and sp.get("seam") and new and not stretched and len(new) >= len(old) and after <= before + 0.1:
                    (omin, omean), (nmin, nmean) = _conf(old), _conf(new)
                    ok = nmin >= max(omin + 0.15, SEAM_LOW_PROB) and nmean >= omean  # clearly more confident
                rec["attempts"].append({"context": ctx, "fn": k, "window": [round(w0, 3), round(w1, 3)],
                                        "old_words": len(old), "new_words": len(new), "uncovered_before": before,
                                        "uncovered_after": after, "stretched": stretched, "accepted": ok})
                if ok:
                    keep = [w for w in out if not (w["start"] >= w0 - 1e-6 and w["end"] <= w1 + 1e-6)]
                    out = sorted(keep + new, key=lambda w: (w["start"], w["end"]))
                    break
            if ok:
                break
        rec["accepted"] = ok
        report.append(rec)
    return no_overlap(out), report
