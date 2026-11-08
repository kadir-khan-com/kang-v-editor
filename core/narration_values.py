"""Read every number / time / name shown on a v13 card or map FROM the narration words (never typed by hand).

A value reference names word ids. The value is parsed from the Devanagari master words.json (immutable
runs/2026-10-31_KANG_004/words.json) and cross-checked with the accepted Hinglish layer at the same ids
(runs/2026-11-01_KANG_001/words_hinglish_v1_accepted.json). Both must give the same value, otherwise the value
is WARN and the line using it is skipped (never guessed).
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional, Sequence

from . import hindi_numbers as HN

# English number words spoken in Hindi narration (Devanagari spelling) and Roman number words of the Hinglish layer
DEV_EN = {"टू": 2.0, "थ्री": 3.0, "वन": 1.0, "फोर": 4.0, "फाइव": 5.0}
ROMAN = {"ek": 1, "do": 2, "teen": 3, "tin": 3, "char": 4, "chaar": 4, "panch": 5, "paanch": 5, "chhe": 6, "chhah": 6,
         "saat": 7, "aath": 8, "nau": 9, "das": 10, "gyarah": 11, "barah": 12, "sau": 100, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
ROMAN_PRE = {"sadhe": 0.5, "saadhe": 0.5}
UNIT_TOKENS = {"बजे", "baje"}
MERIDIEM = {"सुबह": "AM", "दोपहर": "PM", "शाम": "PM", "रात": "PM", "शांको": "PM"}  # 'शांको' = ASR of 'शाम को'


def _toks(s: str) -> List[str]:
    return [t for t in re.split(r"\s+", s.strip()) if t and re.sub(r"[,।.?!]+$", "", t) not in UNIT_TOKENS]


def _dev_value(toks: Sequence[str]) -> Optional[float]:
    toks = [re.sub(r"[,।.?!]+$", "", t) if not re.match(r"^\d", t) else t.rstrip(".") for t in toks]
    if len(toks) == 1 and toks[0] in DEV_EN:
        return DEV_EN[toks[0]]
    return HN.parse_run(list(toks))


def _roman_value(toks: Sequence[str]) -> Optional[float]:
    total, pre, seen = 0.0, 0.0, False
    for raw in toks:
        t = raw.lower().strip(",.!?")
        if re.match(r"^\d[\d,]*(\.\d+)?$", t):
            total += float(t.replace(",", "")); seen = True
        elif t in ROMAN_PRE:
            pre = ROMAN_PRE[t]
        elif t in ROMAN:
            v = ROMAN[t]
            total = (total or 1) * v if v == 100 and seen else total + v + pre
            pre, seen = 0.0, True
        else:
            return None
    return total if seen else None


def word_text(words: Sequence[Dict[str, Any]], hw: Sequence[Dict[str, Any]], ids: Sequence[int]) -> Dict[str, str]:
    return {"hindi": " ".join(words[i]["word"] for i in ids), "hinglish": " ".join(hw[i]["hinglish"] for i in ids)}


def read_value(ref: Dict[str, Any], words: Sequence[Dict[str, Any]], hw: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """ref = {ids:[..], kind: number|time|text, expect?: str, meridiem_id?: int}.
    -> {value, display, status PASS/WARN, word_ids, hindi, hinglish, time, note}"""
    ids = list(ref["ids"])
    out: Dict[str, Any] = {"word_ids": ids, "kind": ref.get("kind", "number"), "status": "WARN", "value": None,
                           "display": "", "note": ""}
    if not ids or any(i < 0 or i >= len(words) for i in ids):
        out["note"] = "word id out of range"
        return out
    out.update(word_text(words, hw, ids))
    out["time"] = round(float(words[ids[0]]["start"]), 3)
    kind = out["kind"]
    if kind == "text":
        exp = ref["expect"]
        norm = lambda s: re.sub(r"[^a-z0-9]+", "", s.lower())  # noqa: E731
        if norm(exp) and norm(exp) in norm(out["hinglish"]):
            out.update(status="PASS", value=exp, display=exp)
            sid = ref.get("spoken_id")  # v13b: name first spoken as an ASR variant at another word ('Siddhnath' 916)
            if sid is not None and 0 <= sid < len(words):
                out["time"] = round(float(words[sid]["start"]), 3)
                out["note"] = f"first spoken as '{hw[sid]['hinglish']}' (word {sid}, ASR variant); name checked at words {ids}"
        else:
            out["note"] = f"name '{exp}' not found in Hinglish words '{out['hinglish']}'"
        return out
    dev_toks = [t for i in ids for t in _toks(words[i]["word"])]
    rom_toks = [t for i in ids for t in _toks(hw[i]["hinglish"])]
    if ref.get("tok"):  # merged ASR token ('बारह ज्योतिर्लिंग'): only this slice of the tokens is the number
        a, b = ref["tok"]
        dev_toks, rom_toks = dev_toks[a:b], rom_toks[a:b]
    dv, rv = _dev_value(dev_toks), _roman_value(rom_toks)
    if dv is None:
        out["note"] = f"Hindi master tokens {dev_toks} are not a number"
        return out
    if rv is None or abs(rv - dv) > 1e-6:
        out["note"] = f"Hindi {dev_toks} = {dv:g} but Hinglish {rom_toks} = {rv}"
        return out
    out["value"] = dv
    if kind == "number":
        out.update(status="PASS", display=f"{int(dv):,}" if float(dv).is_integer() else f"{dv:g}")
    elif kind == "time":
        mid = ref.get("meridiem_id")
        mer = MERIDIEM.get(re.sub(r"[,।.]+$", "", words[mid]["word"])) if mid is not None else None
        if not mer:
            out["note"] = "time without a spoken part of day (subah/dopahar/shaam/raat)"
            return out
        hh = int(dv)
        mm = int(round((dv - hh) * 60))
        if ref.get("after_hour") is not None and mer == "AM" and hh < int(ref["after_hour"]):
            mer = "PM"  # 'subah 7 baje se ek baje tak': 1 o'clock after a 7 AM start is 1 PM
            out["note"] = f"PM inferred: {hh} o'clock follows a {ref['after_hour']} AM start in the same spoken range"
        if not 1 <= hh <= 12:
            out["note"] = f"hour {dv:g} outside 1-12"
            return out
        out.update(status="PASS", display=f"{hh}:{mm:02d} {mer}", meridiem_word=words[mid]["word"], meridiem_id=mid)
    else:
        out["note"] = f"unknown kind {kind}"
        out["status"] = "WARN"
    return out


def fill(fmt: str, vals: Sequence[Dict[str, Any]], progress: "float | Sequence[float]" = 1.0) -> str:
    """'₹{0}–{1}' with numbers counted up to progress (0..1, or one progress per value); times/text appear as they are."""
    parts = []
    for i, v in enumerate(vals):
        if v["kind"] == "number":
            pr = progress[i] if isinstance(progress, (list, tuple)) else progress
            x = v["value"] * pr
            parts.append(f"{int(round(x)):,}" if float(v["value"]).is_integer() else f"{x:.1f}")
        else:
            parts.append(v["display"])
    return fmt.format(*parts)
