"""Phase 1: words.json (word-level transcript) + anomaly audit.

words.json format (list):
  {"word": str, "start": float, "end": float, "probability": float}
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List


def rows_to_words(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Flatten engine transcript rows into words.json entries (order preserved)."""
    out: List[Dict[str, Any]] = []
    for r in rows:
        for w in r.get("words", []):
            text = str(w.get("w", w.get("word", ""))).strip()
            if not text:
                continue
            out.append({
                "word": text,
                "start": round(float(w["start"]), 3),
                "end": round(float(w["end"]), 3),
                "probability": round(float(w.get("p", w.get("probability", 1.0))), 3),
            })
    return merge_zero_duration(out)


def merge_zero_duration(words: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Words with end <= start (ASR clamp anomalies) get no invented duration: their text is
    attached to the previous word (or the next one if first), whose real timing is kept.
    Merged entries carry `merged` so the review sample can show them."""
    out: List[Dict[str, Any]] = []
    pending: List[str] = []
    for w in words:
        if w["end"] <= w["start"]:
            if out:
                prev = out[-1]
                prev["word"] = f'{prev["word"]} {w["word"]}'
                prev["end"] = max(prev["end"], w["end"])
                prev.setdefault("merged", []).append(w["word"])
            else:
                pending.append(w["word"])
            continue
        w = dict(w)
        if pending:
            w["word"] = " ".join(pending + [w["word"]])
            w["merged"] = pending
            pending = []
        out.append(w)
    return out


def audit_words(words: List[Dict[str, Any]], max_word_dur: float = 2.5, low_prob: float = 0.4) -> Dict[str, Any]:
    """Anomaly audit (Phase 1): long words, non-positive durations, overlaps, low confidence."""
    issues: List[Dict[str, Any]] = []
    for i, w in enumerate(words):
        d = w["end"] - w["start"]
        if w["start"] < 0:
            issues.append({"i": i, "word": w["word"], "issue": "negative_start"})
        if d <= 0:
            issues.append({"i": i, "word": w["word"], "issue": "non_positive_duration"})
        elif d > max_word_dur:
            issues.append({"i": i, "word": w["word"], "issue": "too_long", "dur": round(d, 3)})
        if i and words[i - 1]["end"] > w["start"] + 1e-6:
            issues.append({"i": i, "word": w["word"], "issue": "overlaps_previous"})
        if w.get("probability", 1.0) < low_prob:
            issues.append({"i": i, "word": w["word"], "issue": "low_confidence", "p": w["probability"]})
    return {"word_count": len(words), "issue_count": len(issues), "issues": issues,
            "ok": not any(x["issue"] in {"negative_start", "non_positive_duration", "overlaps_previous"} for x in issues)}


def validate_words(words: Any) -> None:
    if not isinstance(words, list) or not words:
        raise ValueError("words.json must be a non-empty list")
    for i, w in enumerate(words):
        for k in ("word", "start", "end"):
            if k not in w:
                raise ValueError(f"words[{i}] missing '{k}'")
        if float(w["end"]) <= float(w["start"]):
            raise ValueError(f"words[{i}] ('{w['word']}') end <= start")


def load_words(path: str | Path) -> List[Dict[str, Any]]:
    words = json.loads(Path(path).read_text(encoding="utf-8"))
    validate_words(words)
    for w in words:
        w.setdefault("probability", 1.0)
    return words


def review_sample(words: List[Dict[str, Any]], n: int = 25) -> str:
    """Human-review sample: first n words with timings (Phase 1 exit proof)."""
    lines = [f"{w['start']:7.2f} - {w['end']:7.2f}  p={w.get('probability', 1):.2f}  {w['word']}" for w in words[:n]]
    return "\n".join(lines)


# --- Glossary correction (proper nouns ASR keeps getting wrong) --------------------------
_PUNCT = "।,.!?;:\"'”“‘’()"


def _bare(token: str) -> str:
    return token.strip().strip(_PUNCT)


def load_glossary(path: str | Path) -> Dict[str, str]:
    """config/glossary.json: {"wrong form (may span tokens)": "correct form"}. Keys starting with '_' ignored."""
    p = Path(path)
    if not p.is_file():
        return {}
    data = json.loads(p.read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if not k.startswith("_") and isinstance(v, str)}


def apply_glossary(words: List[Dict[str, Any]], glossary: Dict[str, str]) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Run glossary passes until stable (max 3), so a fix can feed another rule:
    'द्वारी का दीश' -> 'द्वारका दीश' -> 'द्वारकाधीश'."""
    changes: List[Dict[str, Any]] = []
    for _ in range(3):
        words, ch = _glossary_pass(words, glossary)
        if not ch:
            break
        changes += ch
    return words, changes


def _glossary_pass(words: List[Dict[str, Any]], glossary: Dict[str, str]) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Replace mis-heard words/phrases. Multi-token matches merge into one word spanning
    first.start -> last.end (timing preserved, nothing fabricated). Trailing punctuation of the
    last matched token is kept. Returns (new_words, changes). Input is never mutated."""
    rules = sorted(((k.split(), v) for k, v in glossary.items()), key=lambda r: -len(r[0]))
    out, changes, i = [], [], 0
    while i < len(words):
        hit = None
        for src, dst in rules:
            n = len(src)
            if i + n <= len(words) and [_bare(w["word"]) for w in words[i:i + n]] == src:
                hit = (n, dst)
                break
        if not hit:
            out.append(dict(words[i])); i += 1
            continue
        n, dst = hit
        span = words[i:i + n]
        last = span[-1]["word"].strip()
        tail = last[len(last.rstrip(_PUNCT)):]
        new = dict(span[0])
        new.update(word=dst + tail, end=span[-1]["end"],
                   probability=min(w.get("probability", 1.0) for w in span), corrected_from=" ".join(w["word"] for w in span))
        changes.append({"at": new["start"], "from": new["corrected_from"], "to": new["word"]})
        out.append(new); i += n
    return out, changes


def join_split_tokens(words: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Whisper splits hyphen/comma joins into their own tokens: 'साथ' '-साथ', '10' ',000',
    '400' '-500'. A token that starts with '-' or ',' is glued onto the previous word (timing
    first.start -> last.end, nothing invented). Returns (words, joins)."""
    out: List[Dict[str, Any]] = []
    joins: List[Dict[str, Any]] = []
    for w in words:
        t = w["word"].strip()
        if out and len(t) > 1 and t[0] in "-," and (t[0] == "-" or t[1:2].isdigit()):
            prev = out[-1]
            new = prev["word"].rstrip() + t
            joins.append({"at": prev["start"], "from": f'{prev["word"]} {w["word"]}', "to": new})
            prev.update(word=new, end=max(prev["end"], w["end"]),
                        probability=min(prev.get("probability", 1.0), w.get("probability", 1.0)))
            continue
        out.append(dict(w))
    return out, joins


# --- Script sanity (Whisper hallucinations like "हैассור" / "¿ neutral") ------------------
def _allowed_char(ch: str) -> bool:
    o = ord(ch)
    return (0x0900 <= o <= 0x097F or 0xA8E0 <= o <= 0xA8FF or ch.isascii() or ch in "।॥–—‘’“”…₹ " or o in (0x200C, 0x200D))


def sanitize_script(words: List[Dict[str, Any]]) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Strip characters outside Devanagari + ASCII from each word (Cyrillic/Hebrew/Arabic
    fragments are ASR hallucinations for Hindi/Hinglish). A word left with no letters is dropped.
    ASCII-only words with p < 0.1 next to stripped garbage are dropped too. Returns (words, log)."""
    out, log = [], []
    for w in words:
        text = w["word"]
        clean = "".join(ch for ch in text if _allowed_char(ch)).strip()
        clean = clean.replace("¿", "").replace("¡", "").strip()
        if clean != text.strip():
            letters = [c for c in clean if c.isalpha() or 0x0900 <= ord(c) <= 0x097F]
            if not letters:
                log.append({"at": w["start"], "from": text, "action": "dropped"})
                continue
            log.append({"at": w["start"], "from": text, "to": clean, "action": "stripped"})
            w = {**w, "word": clean, "sanitized_from": text}
        out.append(dict(w))
    return out, log


def repeated_runs(words: List[Dict[str, Any]], n: int = 3) -> List[Dict[str, Any]]:
    """Same token n+ times in a row (classic ASR loop) -> review flag, never auto-deleted."""
    flags, i = [], 0
    while i < len(words):
        j = i
        while j + 1 < len(words) and _bare(words[j + 1]["word"]) == _bare(words[i]["word"]):
            j += 1
        if j - i + 1 >= n:
            flags.append({"i": i, "word": words[i]["word"], "count": j - i + 1, "issue": "repeated_run"})
        i = j + 1
    return flags
