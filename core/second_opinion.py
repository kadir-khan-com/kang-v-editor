"""Second-opinion ASR hints (e.g. Nemotron 3.5 ASR) for the human transcript review.

HINTS ONLY: nothing here changes words.json. The second model's text is aligned to our words chunk by
chunk (difflib on normalized tokens), so each review row gets `nemotron_hint` (what the other model
heard for that span) and `nemotron_agrees` (yes/no after normalization). `disagreements()` lists every
other place the two models differ, classed content / spelling / spacing / number / script. `number` is NOT
formatting-only: digits vs number words can hide a real amount error (2,500,000 vs दो हजार से ढाई हजार),
so number rows always need a listen; only `script` (Latin vs Devanagari) is usually cosmetic. Neither model is ground truth; a human still decides.
"""
from __future__ import annotations

import csv
import difflib
import re
import unicodedata
from pathlib import Path
from typing import Any, Dict, List, Tuple

_P = re.compile(r"[\u0964\u0965.,!?;:\"'()\[\]\u2018\u2019\u201c\u201d\-\u2013\u2014]")
_DIGIT = re.compile(r"\d")
_LATIN = re.compile(r"[A-Za-z]")
_NUMWORDS = {"एक", "दो", "तीन", "चार", "पांच", "पाँच", "छह", "छे", "सात", "आठ", "नौ", "दस", "बारह", "सत्रह",
             "बाईस", "पच्चीस", "बावन", "सौ", "हजार", "हज़ार", "लाख", "ढाई", "डेढ़", "पंद्रह", "पैंतीस",
             "चालीस", "सवा", "साढ़े"}


def norm(tok: str) -> str:
    t = unicodedata.normalize("NFC", tok.lower())
    t = _P.sub("", t).replace("\u093c", "").replace("\u0901", "\u0902")
    return t


def _toks(text: str) -> List[str]:
    return [t for t in text.split() if norm(t)]


def align(words: List[Dict[str, Any]], chunks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Map each of our word indices to the other model's surface tokens."""
    mapped: Dict[int, List[str]] = {}
    ops: List[Dict[str, Any]] = []
    for c in chunks:
        idx = [i for i, w in enumerate(words) if c["start"] <= (w["start"] + w["end"]) / 2 < c["end"]]
        ours = [norm(words[i]["word"]) for i in idx]
        theirs_s = _toks(c.get("text", ""))
        theirs = [norm(t) for t in theirs_s]
        sm = difflib.SequenceMatcher(None, ours, theirs, autojunk=False)
        for tag, a0, a1, b0, b1 in sm.get_opcodes():
            if tag == "equal":
                for k in range(a1 - a0):
                    mapped[idx[a0 + k]] = [theirs_s[b0 + k]]
                continue
            seg = theirs_s[b0:b1]
            if a1 > a0:
                mapped[idx[a0]] = list(seg)
                for k in range(a0 + 1, a1):
                    mapped[idx[k]] = []
                first, last = idx[a0], idx[a1 - 1]
            else:  # insertion: attach to the previous word of ours (or next if none)
                anchor = idx[a0 - 1] if a0 > 0 else (idx[0] if idx else None)
                if anchor is None:
                    continue
                mapped.setdefault(anchor, []).extend(seg)
                first = last = anchor
            ops.append({"tag": tag, "first": first, "last": last, "start": words[first]["start"],
                        "ours": " ".join(words[i]["word"] for i in idx[a0:a1]), "theirs": " ".join(seg)})
    return {"mapped": mapped, "ops": ops}


def hint(al: Dict[str, Any], first: int, last: int) -> str:
    return " ".join(t for i in range(first, last + 1) for t in al["mapped"].get(i, []))


def classify(ours: str, theirs: str) -> str:
    o, t = ours.split(), theirs.split()
    if o and t and norm("".join(o)) == norm("".join(t)):
        return "spacing"
    if _DIGIT.search(ours) and (any(norm(x) in _NUMWORDS for x in t) or _DIGIT.search(theirs)):
        return "number"
    if _LATIN.search(ours) and not _LATIN.search(theirs):
        return "script"
    if o and t and len(o) == len(t) and all(difflib.SequenceMatcher(None, norm(a), norm(b)).ratio() >= 0.75
                                            for a, b in zip(o, t)):
        return "spelling"
    return "content"


def disagreements(al: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [dict(op, kind=classify(op["ours"], op["theirs"])) for op in al["ops"]]


def annotate_rows(rows: List[Dict[str, str]], al: Dict[str, Any], words: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    out = []
    for r in rows:
        r = dict(r)
        f, l = int(r["first"]), int(r["last"])
        h = hint(al, f, l)
        ours = " ".join(words[i]["word"] for i in range(f, l + 1))
        r["nemotron_hint"] = h
        same = [norm(x) for x in ours.split()] == [norm(x) for x in h.split()]
        r["nemotron_agrees"] = "yes" if same else "no"
        r["nemotron_diff"] = "" if same else classify(ours, h)
        out.append(r)
    return out


def write_csv(path: str | Path, rows: List[Dict[str, str]]) -> Path:
    path = Path(path)
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)
    return path
