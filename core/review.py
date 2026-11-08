"""Transcript review loop (human acceptance before scenes/package are final).

review_spans(words)  -> list of spans a human must listen to: amounts/numbers, units, stutter
                        repeats ("विराजमान विराजमान", "बरकेश्वर पेश्वर"), low-confidence runs.
write_review_csv()   -> review.csv (UTF-8 BOM so Excel shows Devanagari) with an empty
                        `correct_text` column + `action` (keep / fix).
apply_review()       -> new words list: rows with action=fix replace exactly their word span
                        [first, last] with correct_text, timing spread evenly over the span.
Nothing is changed unless a human wrote it in the CSV. Rows left blank keep the ASR words.
Timing: same word count keeps ASR timing; a different count is evenly interpolated and marked
timing_method=interpolated_after_review / timing_status=unverified (needs a sync check or re-align).
Text reviewed and timing verified are separate statuses; no fake probability is written.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

NUM_RE = re.compile(r"[0-9०-९]")
UNIT_WORDS = {"रुपये", "रुपए", "रुपया", "रु", "km", "किलोमीटर", "किमी", "मीटर", "लाख", "करोड़", "हजार", "हज़ार",
              "सौ", "घंटे", "घंटा", "मिनट", "बजे", "प्रतिशत", "%", "₹"}
PUNCT = "।?!,.॥\"'()"
LOW_P = 0.45
CTX = 4  # words of context each side


def _clean(w: str) -> str:
    return w.strip().strip(PUNCT)


AUX = {"गया", "गई", "गए", "गयी", "दिया", "लिया", "मना", "ना", "था", "थी", "थे", "है", "हैं", "जाता", "जाती"}


def _stutter(a: str, b: str) -> bool:
    """b repeats a (exact) or b is a >=3-char tail fragment of a (द्वारिकाधीश दीश, बरकेश्वर पेश्वर)."""
    a, b = _clean(a), _clean(b)
    if not a or not b:
        return False
    if a == b:
        return True
    if b in AUX:
        return False
    if len(b) >= 3 and len(a) > len(b) and (a.endswith(b) or a.endswith(b[1:])):
        return True
    return False


def review_spans(words: List[Dict[str, Any]], low_p: float = LOW_P) -> List[Dict[str, Any]]:
    flags: Dict[int, List[str]] = {}

    def flag(i: int, why: str) -> None:
        flags.setdefault(i, [])
        if why not in flags[i]:
            flags[i].append(why)

    for i, w in enumerate(words):
        t = _clean(w["word"])
        if NUM_RE.search(t) or "₹" in t:
            flag(i, "amount/number")
        elif t in UNIT_WORDS and i > 0:
            flag(i, "amount/number")
            flag(i - 1, "amount/number")
        if i > 0 and _stutter(words[i - 1]["word"], w["word"]):
            why = "repeat (may be intentional)" if _clean(words[i - 1]["word"]) == t else "fragment"
            flag(i - 1, why)
            flag(i, why)
        p = w.get("probability")
        if p is not None and p < low_p:
            flag(i, "low_confidence")
    # merge flagged indices that sit within 2 words of each other into one span
    idx = sorted(flags)
    spans: List[Dict[str, Any]] = []
    for i in idx:
        if spans and i - spans[-1]["last"] <= 2:
            for k in range(spans[-1]["last"] + 1, i + 1):
                for why in flags.get(k, []):
                    if why not in spans[-1]["reasons"]:
                        spans[-1]["reasons"].append(why)
            spans[-1]["last"] = i
        else:
            spans.append({"first": i, "last": i, "reasons": list(flags[i])})
    for n, s in enumerate(spans):
        f, l = s["first"], s["last"]
        s["id"] = f"R{n + 1:03d}"
        s["start"] = round(words[f]["start"], 3)
        s["end"] = round(words[l]["end"], 3)
        s["asr_text"] = " ".join(words[k]["word"] for k in range(f, l + 1))
        s["context"] = (" ".join(words[k]["word"] for k in range(max(0, f - CTX), f)) + " [" + s["asr_text"] + "] "
                        + " ".join(words[k]["word"] for k in range(l + 1, min(len(words), l + 1 + CTX)))).strip()
        # amounts and names first: they change meaning
        r = s["reasons"]
        s["priority"] = (1 if "amount/number" in r or "manual" in r else 2 if "fragment" in r or "low_confidence" in r
                         else 3)
    return spans


def find_phrase(words: List[Dict[str, Any]], phrase: str, reason: str = "manual") -> Optional[Dict[str, Any]]:
    """Locate a reviewer-quoted phrase (e.g. 'विश्वा प्रशित दमंदीर') as a word span."""
    toks = [_clean(t) for t in phrase.split()]
    n = len(toks)
    for i in range(len(words) - n + 1):
        if [_clean(words[i + k]["word"]) for k in range(n)] == toks:
            f, l = i, i + n - 1
            return {"first": f, "last": l, "reasons": [reason], "start": round(words[f]["start"], 3),
                    "end": round(words[l]["end"], 3), "asr_text": " ".join(words[k]["word"] for k in range(f, l + 1)),
                    "context": " ".join(words[k]["word"] for k in range(max(0, f - CTX), min(len(words), l + 1 + CTX)))}
    return None


def merge_manual(spans: List[Dict[str, Any]], manual: List[Dict[str, Any]], words: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Add manual spans; an auto span overlapping a manual one is absorbed (one row per word span)."""
    out = []
    for s in spans:
        hit = next((m for m in manual if not (s["last"] < m["first"] or s["first"] > m["last"])), None)
        if hit:
            hit["first"], hit["last"] = min(hit["first"], s["first"]), max(hit["last"], s["last"])
            hit["reasons"] = list(dict.fromkeys(hit["reasons"] + s["reasons"]))
        else:
            out.append(s)
    for m in manual:
        m["start"], m["end"] = round(words[m["first"]]["start"], 3), round(words[m["last"]]["end"], 3)
        m["asr_text"] = " ".join(words[k]["word"] for k in range(m["first"], m["last"] + 1))
        m["priority"] = 1
    allr = sorted(out + manual, key=lambda r: r["first"])
    for n, r in enumerate(allr):
        r["id"] = f"R{n + 1:03d}"
    return allr


def _ts(t: float) -> str:
    m, s = divmod(t, 60)
    return f"{int(m):02d}:{s:05.2f}"


FIELDS = ["id", "priority", "time", "start", "end", "scene", "first", "last", "reasons", "asr_text", "context",
          "action", "correct_text", "clip"]


def write_review_csv(path: str | Path, spans: List[Dict[str, Any]], scenes: Optional[Dict[str, Any]] = None,
                     extra: Optional[List[Dict[str, Any]]] = None) -> Path:
    """extra: manual spans (e.g. from an outside reviewer) with first/last/asr_text/reasons."""
    rows = list(spans) + list(extra or [])
    sc = (scenes or {}).get("scenes", [])
    path = Path(path)
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=FIELDS)
        wr.writeheader()
        for s in sorted(rows, key=lambda r: (r["priority"], r["start"])):
            scene = next((x["id"] for x in sc if x["first_word"] <= s["first"] <= x["last_word"]), "")
            wr.writerow({"id": s["id"], "priority": s["priority"], "time": _ts(s["start"]), "start": s["start"],
                         "end": s["end"], "scene": scene, "first": s["first"], "last": s["last"],
                         "reasons": "; ".join(s["reasons"]), "asr_text": s["asr_text"], "context": s["context"],
                         "action": "", "correct_text": "", "clip": s.get("clip", "")})
    return path


def read_review_csv(path: str | Path) -> List[Dict[str, str]]:
    with Path(path).open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


DECIDED_BY = {"listened": "human_reviewed", "auto-extraction": "auto_extraction_recommended",
              "editorial-policy": "editorial_policy"}


def apply_review(words: List[Dict[str, Any]], rows: List[Dict[str, str]],
                 text_status: str = "human_reviewed") -> Dict[str, Any]:
    """Apply human fixes. action: '' or keep = no change, fix = replace span with correct_text
    (empty correct_text with action=fix deletes the span's words, e.g. a stutter). Spans must not
    overlap and must still match asr_text (guards against a CSV made from other words)."""
    fixes, problems = [], []
    for r in rows:
        act = (r.get("action") or "").strip().lower()
        if act in ("", "keep", "ok"):
            continue
        if act not in ("fix", "delete"):
            problems.append(f"{r.get('id')}: unknown action {act!r} (use keep / fix / delete)")
            continue
        f, l = int(r["first"]), int(r["last"])
        if not (0 <= f <= l < len(words)):
            problems.append(f"{r['id']}: word span {f}-{l} out of range")
            continue
        cur = " ".join(words[k]["word"] for k in range(f, l + 1))
        if r.get("asr_text") and cur != r["asr_text"]:
            problems.append(f"{r['id']}: words.json changed since review.csv was made ({cur!r} != {r['asr_text']!r})")
            continue
        new = [] if act == "delete" else (r.get("correct_text") or "").split()
        part = [h.split(" -> ", 1)[1].strip() for h in (r.get("consensus_hint_PART") or "").split(" | ") if " -> " in h]
        if act == "fix" and new and " ".join(new) in part and len(new) < l - f + 1:
            problems.append(f"{r['id']}: correct_text is only the partial hint {' '.join(new)!r}; write the full "
                            f"replacement for the whole span {cur!r}")
            continue
        if act == "fix" and not new:
            problems.append(f"{r['id']}: action=fix but correct_text is empty (use delete to remove words)")
            continue
        db = (r.get("decided_by") or "").strip().lower()
        if db and db not in DECIDED_BY:
            problems.append(f"{r['id']}: unknown decided_by {db!r} (use {' / '.join(DECIDED_BY)})")
            continue
        st = DECIDED_BY.get(db, text_status)
        pending = (r.get("content_review") or "").strip().lower() == "pending"
        fixes.append((f, l, new, r["id"], st, pending))
    fixes.sort()
    for a, b in zip(fixes, fixes[1:]):
        if b[0] <= a[1]:
            problems.append(f"{a[3]} and {b[3]} overlap")
    if problems:
        return {"ok": False, "problems": problems, "words": words, "applied": []}
    out: List[Dict[str, Any]] = []
    pos = 0
    applied, unverified = [], []
    for f, l, new, rid, st, pending in fixes:
        out.extend(words[pos:f])
        s, e = words[f]["start"], words[l]["end"]
        if new:
            step = (e - s) / len(new)
            n_old = l - f + 1
            for k, t in enumerate(new):
                if len(new) == n_old:  # same word count: keep each word's own ASR timing
                    a, b = words[f + k]["start"], words[f + k]["end"]
                    tm = "asr_after_review"
                else:  # different count: evenly interpolated over the old span, NOT audio-aligned
                    a, b = s + k * step, s + (k + 1) * step
                    tm = "interpolated_after_review"
                # no fake model certainty: probability is dropped, review status carried instead
                out.append({"word": t, "start": round(a, 3), "end": round(b, 3), "reviewed": rid,
                            "text_status": st, "content_review_pending": pending, "timing_method": tm,
                            "timing_status": "asr" if tm == "asr_after_review" else "unverified"})
            if len(new) != n_old:
                unverified.append({"id": rid, "start": round(s, 3), "end": round(e, 3),
                                   "old_words": n_old, "new_words": len(new)})
        applied.append({"id": rid, "old": " ".join(words[k]["word"] for k in range(f, l + 1)), "new": " ".join(new),
                        "text_status": st, "content_review_pending": pending})
        pos = l + 1
    out.extend(words[pos:])
    return {"ok": True, "problems": [], "words": out, "applied": applied, "timing_unverified": unverified}
