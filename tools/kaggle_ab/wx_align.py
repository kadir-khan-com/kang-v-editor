"""WhisperX cross-check: force-align OUR final words with WhisperX's Hindi wav2vec2 model and compare.

Measurement only. Runs in its own venv on Kaggle (whisperx pins its own torch), never imported by kang.
Reports how far our word starts are from the wav2vec2 alignment and which words align badly
(low score = the audio there probably doesn't say that word -> candidate misheard/missing word).

usage: python wx_align.py <audio> <words.json> <out.json> [--device cuda]
"""
import json
import statistics
import sys
import time


def segments(words, max_gap=0.8, max_words=25, max_len=20.0):
    segs, cur = [], []
    for w in words:
        if cur and (w["start"] - cur[-1]["end"] > max_gap or len(cur) >= max_words or w["end"] - cur[0]["start"] > max_len):
            segs.append(cur)
            cur = []
        cur.append(w)
    if cur:
        segs.append(cur)
    return segs


def main():
    audio_path, words_path, out_path = sys.argv[1:4]
    device = sys.argv[sys.argv.index("--device") + 1] if "--device" in sys.argv else "cuda"
    import whisperx
    t = time.time()
    words = json.load(open(words_path, encoding="utf-8"))
    # glossary phrases ("बेट द्वारका") are one entry for us but several tokens for the aligner
    flat = []
    for w in words:
        parts = w["word"].split()
        for k, p in enumerate(parts):
            flat.append({"word": p, "start": w["start"], "end": w["end"], "cont": k > 0})
    groups = segments(flat)
    segs = [{"start": g[0]["start"], "end": g[-1]["end"], "text": " ".join(x["word"] for x in g)} for g in groups]
    audio = whisperx.load_audio(audio_path)
    model, meta = whisperx.load_align_model(language_code="hi", device=device)
    res = whisperx.align(segs, model, meta, audio, device, return_char_alignments=False)
    # whisperx re-splits segments into sentences (at ? and ।), so pair by the flat word list, not by segment.
    # R3 bug: zip(groups, segments) drifted ~7 s on v3 text. Only the FIRST token of a glossary phrase is
    # compared (its other tokens share the entry's start, e.g. "बहुत ही").
    aw = res.get("word_segments") or [x for s in res["segments"] for x in s.get("words", [])]
    deltas, low, unaligned, n = [], [], 0, 0
    if len(aw) != len(flat):
        print(f"WARNING token count differs: ours {len(flat)} vs whisperx {len(aw)}; pairing stops at the shorter")
    for ours, theirs in zip(flat, aw):
        if ours.get("cont"):
            continue
        n += 1
        if theirs.get("start") is None:
            unaligned += 1
            continue
        d = abs(float(theirs["start"]) - ours["start"])
        deltas.append(d)
        sc = float(theirs.get("score", 1.0))
        if sc < 0.2 or d > 1.0:
            low.append({"t": round(ours["start"], 2), "word": ours["word"], "score": round(sc, 3),
                        "wx_start": round(float(theirs["start"]), 2), "wx_word": theirs.get("word")})
    deltas.sort()
    rep = {"token_match": len(aw) == len(flat), "align_model": "whisperx default for hi",
           "words": n, "aligned": len(deltas), "unaligned": unaligned,
           "median_start_diff_s": round(statistics.median(deltas), 3) if deltas else None,
           "p90_start_diff_s": round(deltas[int(0.9 * (len(deltas) - 1))], 3) if deltas else None,
           "over_0_5s": sum(d > 0.5 for d in deltas), "flagged": len(low), "flagged_words": low[:80],
           "time_s": round(time.time() - t, 1)}
    json.dump(rep, open(out_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps({k: v for k, v in rep.items() if k != "flagged_words"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
