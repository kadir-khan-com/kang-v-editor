"""Hindi number words / digits -> values, so 'दो किलोमीटर', '2 km' and '2 किलोमीटर' compare as the same,
while '2,500,000 रुपये' vs 'दो हजार से ढाई हजार रुपये' is flagged as a real amount mismatch."""
from __future__ import annotations

import re
from typing import List, Optional, Tuple

_ONES = ("शून्य एक दो तीन चार पांच छह सात आठ नौ दस ग्यारह बारह तेरह चौदह पंद्रह सोलह सत्रह अठारह उन्नीस बीस "
         "इक्कीस बाईस तेईस चौबीस पच्चीस छब्बीस सत्ताईस अट्ठाईस उनतीस तीस इकतीस बत्तीस तैंतीस चौंतीस पैंतीस छत्तीस "
         "सैंतीस अड़तीस उनतालीस चालीस इकतालीस बयालीस तैंतालीस चवालीस पैंतालीस छियालीस सैंतालीस अड़तालीस उनचास पचास "
         "इक्यावन बावन तिरपन चौवन पचपन छप्पन सत्तावन अट्ठावन उनसठ साठ इकसठ बासठ तिरसठ चौंसठ पैंसठ छियासठ सड़सठ "
         "अड़सठ उनहत्तर सत्तर इकहत्तर बहत्तर तिहत्तर चौहत्तर पचहत्तर छिहत्तर सतहत्तर अठहत्तर उन्यासी अस्सी इक्यासी "
         "बयासी तिरासी चौरासी पचासी छियासी सत्तासी अट्ठासी नवासी नब्बे इक्यानवे बानवे तिरानवे चौरानवे पचानवे छियानवे "
         "सत्तानवे अट्ठानवे निन्यानवे").split()
BASE = {w: float(i) for i, w in enumerate(_ONES)}
BASE.update({"पाँच": 5.0, "छः": 6.0, "छे": 6.0, "छ": 6.0, "ढाई": 2.5, "डेढ़": 1.5, "डेढ": 1.5})
MULT_SMALL = {"सौ": 100.0}
MULT_BIG = {"हजार": 1e3, "हज़ार": 1e3, "लाख": 1e5, "करोड़": 1e7, "करोड": 1e7}
PRE = {"साढ़े": 0.5, "साढे": 0.5, "सवा": 0.25, "पौने": -0.25}
_DIG = re.compile(r"^\d[\d,]*(\.\d+)?$")


def _clean(t: str) -> str:
    return re.sub(r"[\u0964\u0965.,!?;:\"'()\-]+$", "", t.strip()) if not _DIG.match(t.strip()) else t.strip()


def is_num_token(t: str) -> bool:
    c = _clean(t)
    return bool(_DIG.match(c)) or c in BASE or c in MULT_SMALL or c in MULT_BIG or c in PRE


def parse_run(toks: List[str]) -> Optional[float]:
    """Value of one run of number tokens ('एक सौ पैंतीस' -> 135, 'पैंतीस सौ' -> 3500, '2,500' -> 2500)."""
    total, cur, pre = 0.0, 0.0, 0.0
    seen = False
    for raw in toks:
        t = _clean(raw)
        if _DIG.match(t):
            cur += float(t.replace(",", "")); seen = True
        elif t in PRE:
            pre = PRE[t]
        elif t in BASE:
            cur += BASE[t] + pre; pre = 0.0; seen = True
        elif t in MULT_SMALL:
            cur = (cur or 1.0) * MULT_SMALL[t]; seen = True
        elif t in MULT_BIG:
            total += (cur or 1.0) * MULT_BIG[t]; cur = 0.0; seen = True
        else:
            return None
    return total + cur if seen else None


def canon_numbers(toks: List[str]) -> List[str]:
    """Replace each run of number tokens with '#<value>' (other tokens unchanged)."""
    out: List[str] = []
    i = 0
    while i < len(toks):
        if is_num_token(toks[i]) and _clean(toks[i]) not in PRE or (_clean(toks[i]) in PRE and i + 1 < len(toks) and is_num_token(toks[i + 1])):
            j = i
            while j < len(toks) and is_num_token(toks[j]):
                j += 1
            v = parse_run(toks[i:j])
            if v is None:
                out.extend(toks[i:j])
            else:
                out.append("#" + (str(int(v)) if v == int(v) else str(v)))
            i = j
        else:
            out.append(toks[i]); i += 1
    return out


def values(toks: List[str]) -> List[float]:
    return [float(t[1:]) for t in canon_numbers(toks) if t.startswith("#")]


def to_digits(text: str) -> str:
    """Write every number run as plain digits ('पैंतीस सौ से 4,000 रुपये' -> '3500 से 4000 रुपये')."""
    toks = text.split()
    out = []
    for t in canon_numbers(toks):
        out.append(t[1:] if t.startswith("#") else t)
    return " ".join(out)
