"""Hinglish (Roman) caption layer on top of the Devanagari master transcript.

Design (2026-11-01):
  Devanagari words.json (timed, reviewed)  ->  word-by-word romanization  ->  fixed name/word table
  -> Roman words with the SAME timings -> Hinglish SRT + review sheet.

* The master stays Devanagari; this layer never edits it.
* Romanizer backend is pluggable. Default = Yapper Transliterator (github ABHISHEKgauti25/yapper_transliterator,
  code Apache-2.0; its map/Lipi weights carry upstream data terms -> used at runtime only, not bundled).
  Any object with ``map_lookup(word) -> str|None`` and ``model(word) -> str`` works (tests use a dict).
* Every word records where its Roman form came from (phrase / name / word_fix / xlit_map / xlit_model /
  passthrough) so the review sheet can show what was guessed. Model fallbacks, suspect ASR words, pending
  listening spans and low-probability words are flagged ``needs_review``. Nothing is auto-accepted.
* Optional second opinion: an untimed Hinglish ASR (e.g. Whisper-Hindi2Hinglish-Apex chunks.json) is lined up
  by time window and compared after a loose phonetic key; low-agreement windows go to the review sheet.
  It never changes words.
"""
from __future__ import annotations

import csv
import json
import re
import unicodedata
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

DEVA = re.compile(r"[\u0900-\u0963\u0966-\u097F]+")
DEVA_PUNCT = str.maketrans({"\u0964": ".", "\u0965": ".", "\u0970": "."})
LEAD_TRAIL = re.compile(r"^([^\w\u0900-\u097F]*)(.*?)([^\w\u0900-\u097F]*)$", re.S)

SOURCES = ("phrase", "name", "word_fix", "xlit_map", "xlit_model", "passthrough")


def _nfc(s: str) -> str:
    return unicodedata.normalize("NFC", s.replace("\u200d", "").replace("\u200c", ""))


def load_table(path: str | Path) -> Dict[str, Any]:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    norm = lambda m: {_nfc(k): v for k, v in (m or {}).items() if not k.startswith("_")}
    sus = d.get("suspect") or {}
    return {"phrases": norm(d.get("phrases")), "names": norm(d.get("names")), "words": norm(d.get("words")),
            "suspect": {_nfc(w) for w in (sus.get("words") if isinstance(sus, dict) else sus) or []},
            "version": d.get("version", ""), "decided_by": d.get("decided_by", "")}


def split_token(raw: str) -> Tuple[str, str, str]:
    """'(द्वारिका।' -> ('(', 'द्वारिका', '.'). Devanagari danda becomes '.'."""
    t = raw.translate(DEVA_PUNCT)
    m = LEAD_TRAIL.match(t)
    return (m.group(1), m.group(2), m.group(3)) if m else ("", t, "")


class YapperBackend:
    """Thin adapter over yapper_transliterator (imported from ``repo_dir``)."""

    def __init__(self, repo_dir: str | Path):
        import sys
        repo_dir = str(Path(repo_dir).resolve())
        if repo_dir not in sys.path:
            sys.path.insert(0, repo_dir)
        from yapper_transliterator import Transliterator  # type: ignore
        from yapper_transliterator.tokenizer import normalize_source  # type: ignore
        self._t = Transliterator()
        self._norm = normalize_source
        self.name = "yapper_transliterator(map_lipi)"

    def map_lookup(self, word: str) -> Optional[str]:
        return self._t.exact_map.get(self._norm(word))

    def model(self, word: str) -> str:
        return self._t.transliterate_word(word)


class DictBackend:
    """Test/offline backend: a plain dict, unknown words -> '?word?' via model()."""

    def __init__(self, mapping: Dict[str, str], name: str = "dict"):
        self.m = {_nfc(k): v for k, v in mapping.items()}
        self.name = name

    def map_lookup(self, word: str) -> Optional[str]:
        return self.m.get(_nfc(word))

    def model(self, word: str) -> str:
        return f"?{word}?"


def _roman_core(core: str, backend, table) -> Tuple[str, str]:
    """Romanize one punctuation-free token (may mix scripts). Returns (roman, source)."""
    c = _nfc(core)
    if not DEVA.search(c):
        return core, "passthrough"
    if " " in c.strip():  # one timed token holding several words (e.g. after a review fix)
        c = " ".join(c.split())
        if c in table["phrases"]:
            return table["phrases"][c], "phrase"
        parts = [_roman_core(p, backend, table) for p in c.split()]
        rank = {k: i for i, k in enumerate(SOURCES)}
        return " ".join(p[0] for p in parts), max((p[1] for p in parts), key=lambda x: rank[x])
    if c in table["names"]:
        return table["names"][c], "name"
    if c in table["words"]:
        return table["words"][c], "word_fix"
    hit = backend.map_lookup(c)
    if hit is not None and DEVA.fullmatch(c):
        return hit, "xlit_map"
    # mixed / unknown: romanize each Devanagari run
    srcs = []

    def rep(m):
        part = m.group(0)
        h = backend.map_lookup(part)
        srcs.append("xlit_map" if h is not None else "xlit_model")
        return h if h is not None else backend.model(part)

    out = DEVA.sub(rep, c)
    return out, ("xlit_model" if "xlit_model" in srcs else "xlit_map")


def romanize_words(words: List[Dict[str, Any]], backend, table: Dict[str, Any],
                   low_prob: float = 0.5) -> List[Dict[str, Any]]:
    """Same words, same timings, plus roman / roman_source / needs_review / review_reasons."""
    out: List[Dict[str, Any]] = []
    cores = [split_token(w["word"]) for w in words]
    keys = [_nfc(c[1]) for c in cores]
    phrases = sorted(((k.split(), v) for k, v in table["phrases"].items()), key=lambda x: -len(x[0]))
    i = 0
    while i < len(words):
        ph = next(((p, v) for p, v in phrases if keys[i:i + len(p)] == p), None)
        if ph:
            n = len(ph[0])
            romans = ph[1].split()
            # keep word count: spread roman tokens over the original words (last word takes the rest)
            if len(romans) >= n:
                parts = romans[:n - 1] + [" ".join(romans[n - 1:])]
            else:
                parts = romans + [""] * (n - len(romans))
            for k in range(n):
                w = words[i + k]
                lead, _, trail = cores[i + k]
                txt = parts[k]
                out.append(_mk(w, (lead + txt + trail) if txt else "", "phrase", table, keys[i + k], low_prob))
            i += n
            continue
        lead, core, trail = cores[i]
        r, src = _roman_core(core, backend, table)
        out.append(_mk(words[i], lead + r + trail, src, table, keys[i], low_prob))
        i += 1
    return out


def _mk(w, roman, src, table, key, low_prob):
    reasons = []
    if src == "xlit_model":
        reasons.append("model_guess")
    if key in table["suspect"]:
        reasons.append("suspect_asr_word")
    if w.get("pending_listen"):
        reasons.append("pending_listen_in_master")
    if w.get("content_review_pending"):
        reasons.append("content_review_pending")
    p = w.get("probability")
    if isinstance(p, (int, float)) and p < low_prob:
        reasons.append(f"low_asr_prob<{low_prob}")
    if w.get("timing_status") == "unverified":
        reasons.append("timing_interpolated")
    d = dict(w)
    d["devanagari"] = w["word"]
    d["roman"] = roman
    d["roman_source"] = src
    d["needs_review"] = bool(reasons)
    d["review_reasons"] = reasons
    return d


def roman_caption_words(rwords: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Words for the caption chunker: 'word' = Roman text; empty phrase tails merged into the previous word."""
    out: List[Dict[str, Any]] = []
    for w in rwords:
        if not w["roman"].strip():
            if out:
                out[-1] = {**out[-1], "end": w["end"]}
            continue
        out.append({"word": w["roman"], "start": w["start"], "end": w["end"]})
    return out


def capitalize_sentences(cw: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out, cap = [], True
    for w in cw:
        t = w["word"]
        if cap and t[:1].islower():
            t = t[:1].upper() + t[1:]
        cap = t[-1:] in ".?!"
        out.append({**w, "word": t})
    return out


def build_hinglish_srt(rwords: List[Dict[str, Any]], max_words: int = 4, max_chars: int = 32) -> Tuple[str, List[Dict[str, Any]]]:
    from core.subtitles import build_srt, chunk_timings, chunk_words
    cw = capitalize_sentences(roman_caption_words(rwords))
    chunks = chunk_words(cw, max_words=max_words, max_chars=max_chars)
    times = chunk_timings(chunks)
    events = [{"start": s, "end": e, "text": " ".join(w["word"] for w in c)} for c, (s, e) in zip(chunks, times)]
    return build_srt(events), events


# ----------------------------------------------------------------------------- second opinion (untimed Hinglish ASR)
_VOWEL_RUN = re.compile(r"([aeiou])\1+")


def phon_key(word: str) -> str:
    """Loose Roman-Hindi key: lowercase letters, w->v, z->j, ph->f, 'ee'->'i', 'oo'->'u', drop h after consonants,
    collapse doubled letters, drop final 'a'. Good enough to tell 'dvaarika'~'dwarka' apart from 'sansad'~'sunset'?
    No - it only removes spelling noise; meaning differences remain differences."""
    w = re.sub(r"[^a-z]", "", word.lower())
    w = w.replace("ph", "f").replace("w", "v").replace("z", "j").replace("ee", "i").replace("oo", "u")
    w = re.sub(r"([bcdfgjklmnpqrstvxy])h", r"\1", w)
    w = re.sub(r"(.)\1+", r"\1", w)
    w = w.replace("y", "i")
    if len(w) > 3 and w.endswith("a"):
        w = w[:-1]
    return w


def skeleton(text: str) -> str:
    """Consonant skeleton of a Roman-Hindi string (spaces ignored): kills vowel-length, schwa, w/v, z/j, sh/s,
    aspiration and nasal-ending noise. 'Krishna'=='krshn', 'Dwarka'=='dvaari ka', 'liye'=='lie'."""
    w = re.sub(r"[^a-z]", "", text.lower())
    w = w.replace("ph", "f").replace("w", "v").replace("z", "j").replace("x", "ks").replace("q", "k")
    w = w.replace("h", "")
    if not w:
        return ""
    head, rest = w[0], re.sub(r"[aeiouy]", "", w[1:])
    w = re.sub(r"(.)\1+", r"\1", head + rest)
    return w[:-1] if len(w) > 1 and w.endswith("n") else w


def _tokens(text: str) -> List[str]:
    return [k for k in (phon_key(t) for t in re.findall(r"[A-Za-z]+", text)) if k]


def _lcs(a: Sequence[str], b: Sequence[str]) -> int:
    if not a or not b:
        return 0
    prev = [0] * (len(b) + 1)
    for x in a:
        cur = [0]
        for j, y in enumerate(b, 1):
            cur.append(prev[j - 1] + 1 if x == y else max(prev[j], cur[-1]))
        prev = cur
    return prev[-1]


def compare_with_untimed(rwords: List[Dict[str, Any]], chunks: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Per ASR chunk window: our Roman text vs theirs, agreement = LCS / max(len) on phon keys (0..1)."""
    rows = []
    for k, c in enumerate(chunks):
        s, e = float(c["start"]), float(c["end"])
        ours = [w for w in rwords if w["start"] >= s - 0.05 and w["start"] < e - 0.05]
        ot = " ".join(w["roman"] for w in ours if w["roman"])
        a, b = _tokens(ot), _tokens(c.get("text", ""))
        agree = round(_lcs(a, b) / max(len(a), len(b), 1), 3)
        rows.append({"chunk": k + 1, "start": round(s, 2), "end": round(e, 2), "agreement": agree,
                     "ours_hinglish": ot, "other_asr": c.get("text", "").strip(),
                     "ours_devanagari": " ".join(w["devanagari"] for w in ours),
                     "flagged_words_here": sum(1 for w in ours if w["needs_review"])})
    return rows


def diff_hints(rwords: List[Dict[str, Any]], chunks: List[Dict[str, Any]], max_span: int = 4) -> List[Dict[str, Any]]:
    """Word-level disagreements between our Roman words and an untimed Hinglish ASR, per chunk window.
    Spelling noise is removed by phon_key; spans touching digits are skipped (ours has digits, theirs words).
    HINTS ONLY: the other ASR is often the one that is wrong."""
    import difflib
    rows = []
    for c in chunks:
        s, e = float(c["start"]), float(c["end"])
        ours = [w for w in rwords if w["start"] >= s - 0.05 and w["start"] < e - 0.05 and w["roman"].strip()]
        ot: List[Tuple[str, Dict[str, Any]]] = []
        for w in ours:
            for t in re.findall(r"[A-Za-z0-9,]+", w["roman"]):
                ot.append((t, w))
        th = re.findall(r"[A-Za-z0-9]+", c.get("text", ""))
        a = [phon_key(t) or t for t, _ in ot]
        b = [phon_key(t) or t for t in th]
        sm = difflib.SequenceMatcher(a=a, b=b, autojunk=False)
        for op, i1, i2, j1, j2 in sm.get_opcodes():
            if op == "equal":
                continue
            if (i2 - i1) > max_span or (j2 - j1) > max_span or i2 == i1:
                continue
            ours_txt = " ".join(t for t, _ in ot[i1:i2])
            if re.search(r"\d", ours_txt):
                continue
            if re.search(r"\d", " ".join(th[j1:j2])):
                continue  # their digits vs our number words
            if j2 > j1 and skeleton(ours_txt) == skeleton(" ".join(th[j1:j2])):
                continue  # same sounds, different spelling
            ws = [w for _, w in ot[i1:i2]]
            ctx = " ".join(t for t, _ in ot[max(0, i1 - 3):i2 + 3])
            rows.append({"start": round(ws[0]["start"], 2), "end": round(ws[-1]["end"], 2), "op": op,
                         "ours": ours_txt, "ours_devanagari": " ".join(dict.fromkeys(w["devanagari"] for w in ws)),
                         "other_asr": " ".join(th[j1:j2]) if j2 > j1 else "(nothing)", "context": ctx,
                         "already_flagged": any(w["needs_review"] for w in ws)})
    return rows


# ----------------------------------------------------------------------------- review sheet
REVIEW_FIELDS = ["idx", "start", "end", "devanagari", "roman", "roman_source", "review_reasons", "context",
                 "action", "correct_roman", "decided_by"]


def review_rows(rwords: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for i, w in enumerate(rwords):
        if not w["needs_review"]:
            continue
        ctx = " ".join(x["roman"] for x in rwords[max(0, i - 4):i + 5] if x["roman"])
        rows.append({"idx": i, "start": w["start"], "end": w["end"], "devanagari": w["devanagari"],
                     "roman": w["roman"], "roman_source": w["roman_source"],
                     "review_reasons": ";".join(w["review_reasons"]), "context": ctx,
                     "action": "", "correct_roman": "", "decided_by": ""})
    return rows


def write_csv(path: str | Path, rows: List[Dict[str, Any]], fields: Optional[List[str]] = None) -> None:
    fields = fields or (list(rows[0].keys()) if rows else [])
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields)
        wr.writeheader()
        for r in rows:
            wr.writerow({k: r.get(k, "") for k in fields})


def stats(rwords: List[Dict[str, Any]]) -> Dict[str, Any]:
    from collections import Counter
    src = Counter(w["roman_source"] for w in rwords)
    rs = Counter(r for w in rwords for r in w["review_reasons"])
    return {"words": len(rwords), "by_source": dict(src), "needs_review": sum(w["needs_review"] for w in rwords),
            "review_reasons": dict(rs)}


def mark_pending_spans(words: List[Dict[str, Any]], review_csv_rows: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    """Copy of words with pending_listen=True on words inside review.csv rows that have no decision yet.
    Matched by TIME (start/end columns) so it still works when words.json is a later run than the CSV
    (word indices shift after apply-review); falls back to first/last indices only without times."""
    out = [dict(w) for w in words]
    for r in review_csv_rows:
        if (r.get("action") or "").strip():
            continue
        try:
            s, e = float(r["start"]), float(r["end"])
        except (KeyError, ValueError, TypeError):
            s = e = None
        if s is not None:
            for w in out:
                if w["start"] < e - 0.02 and w["end"] > s + 0.02:
                    w["pending_listen"] = True
            continue
        try:
            f, l = int(r["first"]), int(r["last"])
        except (KeyError, ValueError):
            continue
        for k in range(max(f, 0), min(l, len(out) - 1) + 1):
            out[k]["pending_listen"] = True
    return out


# ----------------------------------------------------------------------------- one-call entry (CLI `kang.py hinglish`)
def run_hinglish(words_path: str | Path, out_prefix: str | Path, *, backend=None, yapper_dir: Optional[str] = None,
                 table_path: str | Path = "config/hinglish_names.json", review_csv: Optional[str] = None,
                 apply_review_fixes: bool = False, other_asr: Optional[str] = None) -> Dict[str, Any]:
    """words.json (Devanagari) -> <out>_words.json, <out>.srt, <out>_review.csv [, <out>_vs_other.csv], <out>_report.json.
    Writes only new files. review_csv: master review.csv; undecided rows are flagged pending_listen, and with
    apply_review_fixes the rows already decided (fix/delete) are applied in memory first (draft, master untouched)."""
    import hashlib
    import time
    words = json.loads(Path(words_path).read_text(encoding="utf-8"))
    applied = []
    if review_csv:
        with open(review_csv, encoding="utf-8-sig", newline="") as f:
            rrows = list(csv.DictReader(f))
        words = mark_pending_spans(words, rrows)
        if apply_review_fixes:
            from core.review import apply_review
            res = apply_review(words, rrows)
            if not res["ok"]:
                return {"error": "review.csv could not be applied", "problems": res["problems"]}
            words, applied = res["words"], res["applied"]
    if backend is None:
        if not yapper_dir:
            return {"error": "no romanizer: pass --yapper-dir (clone of github.com/ABHISHEKgauti25/yapper_transliterator)"}
        backend = YapperBackend(yapper_dir)
    table = load_table(table_path)
    t0 = time.time()
    rw = romanize_words(words, backend, table)
    srt, events = build_hinglish_srt(rw)
    secs = round(time.time() - t0, 2)
    out = Path(out_prefix)
    out.parent.mkdir(parents=True, exist_ok=True)
    files = {"words": f"{out}_words.json", "srt": f"{out}.srt", "review": f"{out}_review.csv",
             "report": f"{out}_report.json", "text": f"{out}.txt"}
    Path(files["words"]).write_text(json.dumps(rw, ensure_ascii=False, indent=0), encoding="utf-8")
    Path(files["srt"]).write_text(srt, encoding="utf-8")
    Path(files["text"]).write_text(" ".join(w["word"] for w in capitalize_sentences(roman_caption_words(rw))) + "\n",
                                   encoding="utf-8")
    write_csv(files["review"], review_rows(rw), REVIEW_FIELDS)
    rep: Dict[str, Any] = {
        "status": "WARN", "note": "draft Hinglish captions; review sheet + listening still required; master untouched",
        "source_words": str(words_path),
        "source_sha256": hashlib.sha256(Path(words_path).read_bytes()).hexdigest(),
        "romanizer": getattr(backend, "name", "?"), "table": str(table_path), "table_version": table["version"],
        "table_decided_by": table["decided_by"], "review_fixes_applied_in_memory": len(applied),
        "caption_events": len(events), "romanize_seconds": secs, "stats": stats(rw)}
    if other_asr:
        oc = json.loads(Path(other_asr).read_text(encoding="utf-8"))
        cmp_rows = compare_with_untimed(rw, oc.get("chunks", oc))
        files["vs_other"] = f"{out}_vs_other.csv"
        write_csv(files["vs_other"], sorted(cmp_rows, key=lambda r: r["agreement"]))
        ag = [r["agreement"] for r in cmp_rows if r["ours_hinglish"]]
        dh = diff_hints(rw, oc.get("chunks", oc))
        files["diff_hints"] = f"{out}_diff_hints.csv"
        write_csv(files["diff_hints"], dh)
        rep["vs_other"] = {"source": str(other_asr), "model": oc.get("model", ""), "chunks": len(cmp_rows),
                           "mean_agreement": round(sum(ag) / max(len(ag), 1), 3),
                           "below_0_5": sum(a < 0.5 for a in ag), "word_diff_hints": len(dh),
                           "_note": "agreement = loose phonetic token LCS; spelling noise removed, meaning not judged"}
    rep["files"] = files
    Path(files["report"]).write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    return rep
