"""Whisper A/B harness: run the REAL Kang transcription stage (transcribe -> refine -> gap-fill ->
suspect-span repair -> sanitize -> joins -> glossary) under several ASR configs on one file and score
each one. Measurement only: it never changes defaults.

Metrics per config
  time_s            wall time of the whole transcription stage
  raw_suspects      stretched words (>1.2 s) + speech gaps (>=0.8 s) in the untouched first pass
  raw_max_word_s    longest single word in the first pass
  spans_repaired / unfilled
  final_max_word_s  longest word after repair
  wer_raw / wer_final  word error rate vs a reference transcript (punctuation ignored)
  oov_pct           final tokens not in a Hindi wordlist (+ glossary targets), digits ignored
  glossary_fixes    how many patches our glossary still had to make (lower = model spelled better)
Plus run-to-run agreement between two identical runs (determinism).

usage: python tools/ab_whisper.py <audio> --ref ref_words.json [--wordlist hi.dic] [--configs a,b] [--device cuda]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

HOTWORDS = ("राधे राधे द्वारका द्वारकाधीश बेट द्वारका गोमती घाट रुक्मिणी दुर्वासा ऋषि नागेश्वर ज्योतिर्लिंग "
            "सुदर्शन सेतु गोपी तालाब चार धाम मथुरा वज्रनाभ श्री कृष्ण सुदामा जगत मंदिर शिखर ध्वजा प्रसाद")
HOTWORDS_SHORT = "द्वारकाधीश रुक्मिणी दुर्वासा ज्योतिर्लिंग गोमती सुदामा"
VAD_TIGHT = {"min_silence_duration_ms": 500, "speech_pad_ms": 300}

CONFIGS = {
    "turbo_base":      {"model": "large-v3-turbo", "opts": {}},
    "turbo_repeat":    {"model": "large-v3-turbo", "opts": {}},
    "turbo_hot":       {"model": "large-v3-turbo", "opts": {"hotwords": HOTWORDS}},
    "turbo_vad":       {"model": "large-v3-turbo", "opts": {"vad_parameters": VAD_TIGHT}},
    "v3_base":         {"model": "large-v3", "opts": {}},
    "v3_hot":          {"model": "large-v3", "opts": {"hotwords": HOTWORDS}},
    "v3_hot_vad":      {"model": "large-v3", "opts": {"hotwords": HOTWORDS, "vad_parameters": VAD_TIGHT}},
    # Hindi fine-tuned Whisper checkpoints, converted to CTranslate2 float16 by kaggle_ab/kang_ab_run.py
    # (skipped when the folder is missing). Licences: collabora cc-by-4.0, vasista22 + ARTPARK apache-2.0.
    "hi_medium":       {"model": "ct2/collabora-whisper-medium-hindi", "opts": {}},
    "hi_large_v2":     {"model": "ct2/vasista22-whisper-hindi-large-v2", "opts": {}},
    "hi_vaani_v3":     {"model": "ct2/ARTPARK-IISc-whisper-large-v3-vaani-hindi", "opts": {}},
    # Round 2 (engine.SEED fixed by default): determinism pairs + hotwords ONLY inside repair windows.
    "turbo_s1":        {"model": "large-v3-turbo", "opts": {}},
    "turbo_s2":        {"model": "large-v3-turbo", "opts": {}},
    "v3_s1":           {"model": "large-v3", "opts": {}},
    "v3_s2":           {"model": "large-v3", "opts": {}},
    "v3_rhot":         {"model": "large-v3", "opts": {}, "repair_opts": {"hotwords": HOTWORDS_SHORT}},
    # Round 3: voter built into the pipeline (pipeline.transcribe_to_words voters=...)
    "turbo_vote":      {"model": "large-v3-turbo", "opts": {}, "vote": True},
    "v3_vote":         {"model": "large-v3", "opts": {}, "vote": True},
}
VOTE_ARGS: dict = {}
PAIRS = [("turbo_base", "turbo_repeat"), ("turbo_s1", "turbo_s2"), ("v3_s1", "v3_s2")]

_PUNCT = re.compile(r"[।॥,\.\!\?;:\"'“”‘’\(\)\-–—]")


def norm_tokens(words) -> list[str]:
    out = []
    for w in words:
        for t in _PUNCT.sub(" ", w["word"]).split():
            out.append(t.replace("\u200c", "").replace("\u200d", ""))
    return out


def wer(ref: list[str], hyp: list[str]) -> float:
    if not ref:
        return 0.0
    prev = list(range(len(hyp) + 1))
    for i, r in enumerate(ref, 1):
        cur = [i] + [0] * len(hyp)
        for j, h in enumerate(hyp, 1):
            cur[j] = min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (r != h))
        prev = cur
    return round(100.0 * prev[-1] / len(ref), 2)


def load_wordlist(path: str | None, glossary: dict) -> set[str] | None:
    if not path or not Path(path).exists():
        return None
    words = set()
    for line in Path(path).read_text(encoding="utf-8", errors="ignore").splitlines()[1:]:
        t = line.split("/")[0].strip()
        if t:
            words.add(t)
    for v in glossary.values():
        words.update(_PUNCT.sub(" ", v).split())
    return words


def oov_pct(tokens: list[str], vocab: set[str] | None) -> float | None:
    if vocab is None:
        return None
    toks = [t for t in tokens if not re.fullmatch(r"[0-9०-९,]+", t)]
    if not toks:
        return 0.0
    return round(100.0 * sum(t not in vocab for t in toks) / len(toks), 2)


def run_config(name: str, cfg: dict, audio: str, device: str | None) -> dict:
    from core import engine, pipeline
    from core.gapfill import find_suspect_spans
    from core.runs import Run
    engine.ASR_OPTIONS.clear()
    engine.ASR_OPTIONS.update(cfg["opts"])
    engine.REPAIR_ASR_OPTIONS.clear()
    engine.REPAIR_ASR_OPTIONS.update(cfg.get("repair_opts", {}))
    run = Run()
    t = time.time()
    res = pipeline.transcribe_to_words(audio, run=run, model_size=cfg["model"], device=device,
                                       **(VOTE_ARGS if cfg.get("vote") else {}))
    took = time.time() - t
    raw = json.loads((Path(res["dir"]) / "words_raw.json").read_text(encoding="utf-8"))
    final = json.loads((Path(res["dir"]) / "words.json").read_text(encoding="utf-8"))
    samples = engine.load_audio(audio)
    raw_spans = find_suspect_spans(raw, samples)
    dur = lambda ws: round(max((w["end"] - w["start"] for w in ws), default=0.0), 2)
    return {"name": name, "model": cfg["model"], "opts": {k: (v if k != "hotwords" else "domain list") for k, v in cfg["opts"].items()},
            "run_id": res["run_id"], "time_s": round(took, 1), "raw_words": len(raw), "final_words": len(final),
            "raw_suspects": len(raw_spans), "raw_max_word_s": dur(raw),
            "spans_repaired": sum(r["accepted"] for r in res["suspect_spans"]), "spans_checked": len(res["suspect_spans"]),
            "unfilled": len(res["gaps_unfilled"]), "final_max_word_s": dur(final),
            "glossary_fixes": len(res["glossary_fixes"]),
            "vote_changes": None if res.get("vote_changes") is None else
            [f"{c['start']:.2f}s {c['from']} -> {c['to']} ({'+'.join(c['by'])})" for c in res["vote_changes"]],
            "_raw": raw, "_final": final}


def alt_words(model_dir: str, audio: str, device: str | None) -> tuple[list, float]:
    """Whole-file pass with a second model (no domain prompt: the Hindi fine-tunes were trained without one)."""
    from faster_whisper import WhisperModel
    from core import engine
    from core.words import rows_to_words
    dev = device or "cuda"
    m = WhisperModel(model_dir, device=dev, compute_type="float16" if dev == "cuda" else "int8")
    t = time.time()
    saved = dict(engine.ASR_OPTIONS)
    engine.ASR_OPTIONS.clear()
    rows, _ = engine.transcribe(engine.load_audio(audio), initial_prompt="", model=m)
    engine.ASR_OPTIONS.update(saved)
    del m
    return rows_to_words(rows), round(time.time() - t, 1)


def run_voters(a, base_final: list, ref: list, vocab, glossary) -> list:
    from core.voter import load_wordlist as voter_vocab, spelling_vote
    from core.words import apply_glossary
    vv = voter_vocab(a.wordlist, extra=glossary.values())
    alts, out = {}, []
    for spec in a.voters.split(","):
        name, path = spec.split("=", 1)
        if not (Path(path) / "model.bin").exists():
            out.append({"name": f"vote_{name}", "error": f"{path} not converted"})
            continue
        print(f"\n=== alt pass {name} ===", flush=True)
        try:
            alts[name], took = alt_words(path, a.audio, a.device)
            print(f"{name}: {len(alts[name])} words in {took}s", flush=True)
        except Exception as e:
            import traceback
            traceback.print_exc()
            out.append({"name": f"vote_{name}", "error": f"{type(e).__name__}: {e}"})
    combos = [(f"vote_{k}", {k: v}, False) for k, v in alts.items()]
    if len(alts) >= 2:
        combos.append(("vote_agree", alts, True))
    for name, use, agree in combos:
        voted, changes = spelling_vote(base_final, use, vv, require_agree=agree)
        voted, _ = apply_glossary(voted, glossary)
        toks = norm_tokens(voted)
        out.append({"name": name, "base": a.vote_base, "vote_changes": len(changes), "wer_final": wer(ref, toks),
                    "oov_pct": oov_pct(toks, vocab), "changes": [f"{c['start']:.2f}s {c['from']} -> {c['to']}" for c in changes]})
        print(json.dumps({k: v for k, v in out[-1].items() if k != "changes"}, ensure_ascii=False), flush=True)
        Path(a.out).with_name(f"{name}_words.json").write_text(json.dumps(voted, ensure_ascii=False, indent=1), encoding="utf-8")
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("audio")
    ap.add_argument("--ref", required=True, help="reference words.json (human-approved transcript)")
    ap.add_argument("--wordlist", default=None, help="hunspell .dic / one word per line (spelling metric)")
    ap.add_argument("--configs", default=",".join(CONFIGS))
    ap.add_argument("--device", default=None)
    ap.add_argument("--out", default="ab_report.json")
    ap.add_argument("--voters", default="", help="name=model_dir,... second models for the spelling voter")
    ap.add_argument("--vote-base", default="v3_s1", help="config whose final words the voter corrects")
    a = ap.parse_args(argv)
    from core.words import apply_glossary, join_split_tokens, load_glossary
    glossary = load_glossary(ROOT / "config" / "glossary.json")
    ref_words, _ = apply_glossary(json.loads(Path(a.ref).read_text(encoding="utf-8")), glossary)
    ref = norm_tokens(ref_words)
    vocab = load_wordlist(a.wordlist, glossary)
    if a.voters:
        VOTE_ARGS.update(voters=dict(x.split("=", 1) for x in a.voters.split(",")
                                     if (Path(x.split("=", 1)[1]) / "model.bin").exists()),
                         wordlist=a.wordlist)
        print("voters:", VOTE_ARGS["voters"], flush=True)
    results, finals, final_words = [], {}, {}
    for name in a.configs.split(","):
        print(f"\n=== {name} ===", flush=True)
        m = CONFIGS[name]["model"]
        if m.startswith("ct2/") and not (Path(m) / "model.bin").exists():
            print(f"skip {name}: {m} not converted", flush=True)
            results.append({"name": name, "error": "model not converted"})
            continue
        try:
            r = run_config(name, CONFIGS[name], a.audio, a.device)
        except Exception as e:  # one broken config must not hide the others
            import traceback
            traceback.print_exc()
            results.append({"name": name, "error": f"{type(e).__name__}: {e}"})
            continue
        raw_fixed, _ = join_split_tokens(r.pop("_raw"))
        raw_fixed, _ = apply_glossary(raw_fixed, glossary)  # same patches as final: isolates what repair changes
        final = r.pop("_final")
        r["wer_raw"] = wer(ref, norm_tokens(raw_fixed))
        r["wer_final"] = wer(ref, norm_tokens(final))
        r["oov_pct"] = oov_pct(norm_tokens(final), vocab)
        finals[name] = norm_tokens(final)
        final_words[name] = final
        print(json.dumps(r, ensure_ascii=False), flush=True)
        results.append(r)
        Path(a.out).write_text(json.dumps({"results": results}, ensure_ascii=False, indent=2), encoding="utf-8")
    if any(CONFIGS[n].get("vote") for n in a.configs.split(",")):
        pass  # voters already used inside the pipeline configs
    elif a.voters and a.vote_base in final_words:
        results += run_voters(a, final_words[a.vote_base], ref, vocab, glossary)
    det = {f"{x}~{y}": wer(finals[x], finals[y]) for x, y in PAIRS if x in finals and y in finals}
    report = {"audio": a.audio, "ref_tokens": len(ref), "wordlist": bool(vocab), "determinism_wer": det, "results": results}
    Path(a.out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("\nAB SUMMARY")
    for r in results:
        if "error" in r:
            print(f"{r['name']:<14} ERROR {r['error']}")
        else:
            if "vote_changes" in r and "time_s" not in r:
                print(f"{r['name']:<14} changes={r['vote_changes']} werF={r['wer_final']} oov={r['oov_pct']}")
                continue
            print(f"{r['name']:<14} t={r['time_s']:>6}s suspects={r['raw_suspects']:>3} unfilled={r['unfilled']} "
                  f"maxw={r['final_max_word_s']} werR={r['wer_raw']} werF={r['wer_final']} oov={r['oov_pct']} gl={r['glossary_fixes']}"
                  + (f" votes={len(r['vote_changes'])}" if r.get("vote_changes") is not None else ""))
    print("determinism WER (same config twice):", det)
    return 0


if __name__ == "__main__":
    sys.exit(main())
