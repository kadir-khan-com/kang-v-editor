"""Spelling voter: keep the base model's words and timing, borrow spelling from a second model.

Why: Kaggle A/B 2026-10-28 on Dwarika (692 s). large-v3 had the most complete first pass but spelled
hard words badly (ज्योतिर्लिंग, किलोमीटर: 0 correct); Hindi fine-tunes (vaani, IndicWhisper) spelled
them right but dropped words. So: never take words FROM the second model, only fix the spelling of a
base word that sits at the same time.

A base word is replaced only when ALL hold:
  * its core token is Devanagari, not a number, and NOT in the wordlist (likely misspelled)
  * an alt word overlaps it in time (>= min_overlap of the shorter one)
  * the alt token IS in the wordlist and looks similar (difflib ratio >= min_ratio)
  * the alt token is not just the base with its ending cut off (protects inflections: मंदिरों -> मंदिर)
  * with require_agree, at least two alt models propose the same fix and none proposes another
Punctuation around the base word is preserved. Every change is reported for human review.
"""
from __future__ import annotations

import difflib
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Tuple

_DEV = re.compile(r"[\u0900-\u097F]")
_NUM = re.compile(r"^[0-9०-९,\.]+$")
_EDGE = re.compile(r"^([^\u0900-\u0963\u0966-\u097F0-9A-Za-z]*)(.*?)([^\u0900-\u0963\u0966-\u097F0-9A-Za-z]*)$", re.S)
_ZW = str.maketrans("", "", "\u200c\u200d")


def split_core(word: str) -> Tuple[str, str, str]:
    m = _EDGE.match(word)
    return (m.group(1), m.group(2).translate(_ZW), m.group(3)) if m else ("", word, "")


def load_wordlist(path: Optional[str | Path], extra: Iterable[str] = ()) -> Set[str]:
    """hunspell .dic (first line = count, 'word/FLAGS') or one word per line. Empty set if missing."""
    words: Set[str] = set()
    if path and Path(path).exists():
        for i, line in enumerate(Path(path).read_text(encoding="utf-8", errors="ignore").splitlines()):
            t = line.split("/")[0].strip().translate(_ZW)
            if t and not (i == 0 and t.isdigit()):
                words.add(t)
    for e in extra:
        for t in re.split(r"\s+", e):
            c = split_core(t)[1]
            if c:
                words.add(c)
    return words


def _overlap(a: Dict[str, Any], b: Dict[str, Any]) -> float:
    inter = min(a["end"], b["end"]) - max(a["start"], b["start"])
    shorter = max(min(a["end"] - a["start"], b["end"] - b["start"]), 0.05)
    return max(inter, 0.0) / shorter


def _is_trimmed_inflection(base: str, alt: str) -> bool:
    """alt is base with a piece cut off: an inflection (मंदिरों->मंदिर) or a compound half (पावनधाम->धाम)."""
    return len(alt) < len(base) and (base.startswith(alt) or base.endswith(alt))


def _same_nasal(a: str, b: str) -> bool:
    """यहाँ / यहां are both fine: chandrabindu vs anusvara is not a spelling error."""
    return a.replace("\u0901", "\u0902") == b.replace("\u0901", "\u0902")


def _best_alt(bw: Dict[str, Any], alt: Sequence[Dict[str, Any]], vocab: Set[str], core: str,
              min_overlap: float, min_ratio: float, lo: int) -> Tuple[Optional[str], int, bool]:
    """Return (token, new_lo, had_any_overlap). `alt` is sorted by start; lo is a moving cursor."""
    while lo < len(alt) and alt[lo]["end"] < bw["start"] - 1.0:
        lo += 1
    best, best_r, seen = None, 0.0, False
    j = lo
    while j < len(alt) and alt[j]["start"] <= bw["end"] + 0.5:
        aw = alt[j]
        j += 1
        if _overlap(bw, aw) < min_overlap:
            continue
        seen = True
        t = split_core(aw["word"])[1]
        if (not t or t == core or t not in vocab or _NUM.match(t) or _is_trimmed_inflection(core, t)
                or _same_nasal(core, t)):
            continue
        r = difflib.SequenceMatcher(None, core, t).ratio()
        if r >= min_ratio and r > best_r:
            best, best_r = t, r
    return best, lo, seen


def spelling_vote(base: List[Dict[str, Any]], alts: Dict[str, List[Dict[str, Any]]], vocab: Set[str],
                  min_overlap: float = 0.5, min_ratio: float = 0.6, require_agree: bool = False
                  ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    if not vocab or not alts:
        return [dict(w) for w in base], []
    sorted_alts = {k: sorted(v, key=lambda w: w["start"]) for k, v in alts.items()}
    cursors = {k: 0 for k in alts}
    out, changes = [], []
    for i, bw in enumerate(base):
        w = dict(bw)
        pre, core, post = split_core(w["word"])
        # a glossary phrase merged into one entry ("बेट द्वारका") is already curated: leave it
        if core and " " not in core and _DEV.search(core) and not _NUM.match(core) and core not in vocab:
            picks, seen_any = {}, {}
            for k, alt in sorted_alts.items():
                tok, cursors[k], seen = _best_alt(w, alt, vocab, core, min_overlap, min_ratio, cursors[k])
                seen_any[k] = seen
                if tok:
                    picks[k] = tok
            choice = None
            if picks:
                vals = set(picks.values())
                if require_agree:  # >= 2 models propose the same fix and none proposes another
                    if len(vals) == 1 and len(picks) >= 2:
                        choice = vals.pop()
                elif len(vals) == 1:
                    choice = vals.pop()
            if choice:
                w["word"] = pre + choice + post
                changes.append({"index": i, "start": w["start"], "end": w["end"], "from": bw["word"],
                                "to": w["word"], "by": sorted(picks)})
        out.append(w)
    return out, changes
