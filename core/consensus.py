"""Three-model consensus for the transcript review (HINTS ONLY: never edits words.json).

Sources: our final words.json (timed), a second timed ASR (Nemotron via NeMo-Speech.cpp JSON with word
timestamps) and an optional untimed text (e.g. MAI-Transcribe-2 Playground). Each of our words gets what the
other models heard there; spans where anything differs become consensus rows:
  others_agree  - both other models agree with each other against ours  -> strongest flag, listen first
  all_differ    - three different readings                               -> listen
  ours_majority - ours matches one of the two others                     -> low priority
  format_only   - same meaning, only digits/number words, Latin/Devanagari English, units, punctuation
Kind 'amount' (numbers whose VALUE differs, e.g. 2,500,000 vs दो हजार से ढाई हजार) gets priority 0.
  name_hint     - a known mishearing pattern (config/name_suggestions.json) -> suggestion only
Timed source is aligned window by window (windows cut at the timed model's pauses), so a hint never jumps
to a far-away row. The untimed source is aligned on text over the whole file and marked text-only.
Agreement is NOT truth: three models can share a mistake. A human still decides every change."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from . import second_opinion as so
from . import hindi_numbers as hn

_CFG = Path(__file__).resolve().parent.parent / "config"
_EQ: Optional[Dict[str, str]] = None


def equivalents() -> Dict[str, str]:
    """norm(token) -> canonical norm, so 'train' == 'ट्रेन', 'km' == 'किलोमीटर', 'रुपए' == 'रुपये'."""
    global _EQ
    if _EQ is None:
        eq: Dict[str, str] = {}
        try:
            for lat, dev in json.loads((_CFG / "english_script.json").read_text(encoding="utf-8")).get("to_devanagari", {}).items():
                eq[so.norm(lat)] = so.norm(dev)
        except (OSError, ValueError):
            pass
        try:
            d = json.loads((_CFG / "script_equivalents.json").read_text(encoding="utf-8"))
            for lat, devs in d.get("latin", {}).items():
                for v in devs:
                    eq[so.norm(v)] = so.norm(devs[0])
                eq[so.norm(lat)] = so.norm(devs[0])
            for grp in d.get("same", []):
                for v in grp:
                    eq[so.norm(v)] = so.norm(grp[0])
        except (OSError, ValueError):
            pass
        _EQ = eq
    return _EQ


def canon(text: str) -> List[str]:
    """Comparison form: numbers -> '#value', English script/units/spelling variants -> one form, no punctuation."""
    toks = [t for t in text.split() if so.norm(t)]
    eq = equivalents()
    out = []
    for t in hn.canon_numbers(toks):
        if t.startswith("#"):
            out.append(t)
            continue
        n = so.norm(t)
        out.append(eq.get(n, n))
    return out

PRIORITY = {"others_agree": 1, "all_differ": 1, "name_hint": 2, "ours_majority": 3, "format_only": 3}


def timed_words(doc: Any) -> List[Dict[str, Any]]:
    """NeMo-Speech.cpp JSON ({'words': [{word,start,end}]}) or a plain words list."""
    ws = doc.get("words", []) if isinstance(doc, dict) else doc
    return [{"word": w["word"], "start": float(w["start"]), "end": float(w["end"])} for w in ws if str(w.get("word", "")).strip()]


def windows(tw: List[Dict[str, Any]], target: float = 25.0, min_gap: float = 0.25) -> List[Dict[str, Any]]:
    """Chunks of the timed model's words, cut at its pauses near `target` seconds."""
    out, cur, t0 = [], [], None
    for i, w in enumerate(tw):
        if t0 is None:
            t0 = w["start"]
        cur.append(w)
        nxt = tw[i + 1] if i + 1 < len(tw) else None
        gap = (nxt["start"] - w["end"]) if nxt else 99
        if nxt is None or (w["end"] - t0 >= target and gap >= min_gap) or w["end"] - t0 >= target * 1.6:
            cut = (w["end"] + nxt["start"]) / 2 if nxt else w["end"] + 5
            out.append({"start": out[-1]["end"] if out else 0.0, "end": cut, "text": " ".join(x["word"] for x in cur),
                        "toks": list(cur)})
            cur, t0 = [], None
    return out


def align_timed(words: List[Dict[str, Any]], wins: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Like second_opinion.align, but inside a changed stretch each of the other model's tokens goes to OUR
    word nearest in time, so a hint never spills into the neighbouring row."""
    import difflib
    mapped: Dict[int, List[str]] = {}
    mid = lambda w: (w["start"] + w["end"]) / 2
    for c in wins:
        idx = [i for i, w in enumerate(words) if c["start"] <= mid(w) < c["end"]]
        th = c["toks"]
        a = [" ".join(canon(words[i]["word"])) for i in idx]
        b = [" ".join(canon(t["word"])) for t in th]
        for tag, a0, a1, b0, b1 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if tag == "equal":
                for k in range(a1 - a0):
                    mapped[idx[a0 + k]] = [th[b0 + k]["word"]]
                continue
            cand = idx[a0:a1] or [x for x in (idx[a0 - 1] if a0 > 0 else None, idx[a0] if a0 < len(idx) else None) if x is not None]
            for i in idx[a0:a1]:
                mapped.setdefault(i, [])
            for t in th[b0:b1]:
                if not cand:
                    break
                best = min(cand, key=lambda i: abs(mid(words[i]) - mid(t)))
                mapped.setdefault(best, []).append(t["word"])
    return {"mapped": mapped, "ops": []}


def align_text(words: List[Dict[str, Any]], text: str) -> Dict[str, Any]:
    end = (words[-1]["end"] + 1) if words else 1
    return so.align(words, [{"start": 0.0, "end": end, "text": text}])


def _n(s: str) -> List[str]:
    return canon(s)


def name_hits(words: List[Dict[str, Any]], names: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    toks = [so.norm(w["word"]) for w in words]
    hits = []
    for ent in names:
        sug = ent["suggest"]
        for heard in ent["heard"]:
            pat = _n(heard)
            if not pat or pat == _n(sug):
                continue
            k = len(pat)
            for i in range(len(toks) - k + 1):
                if toks[i:i + k] == pat:
                    hits.append({"first": i, "last": i + k - 1, "suggest": sug, "heard": heard})
    return hits


def consensus(words: List[Dict[str, Any]], timed: Optional[List[Dict[str, Any]]] = None,
              text: Optional[str] = None, names: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
    n_al = align_timed(words, windows(timed)) if timed else None
    m_al = align_text(words, text) if text else None
    names = names or []

    def at(al, i):
        return None if al is None else al["mapped"].get(i, [])

    def same(i, toks):
        return toks is None or canon(" ".join(toks)) == canon(words[i]["word"])

    bad = [not (same(i, at(n_al, i)) and same(i, at(m_al, i))) for i in range(len(words))]
    rows, i = [], 0
    while i < len(words):
        if not bad[i]:
            i += 1
            continue
        j = i
        while j + 1 < len(words) and bad[j + 1]:
            j += 1
        ours = " ".join(words[k]["word"] for k in range(i, j + 1))
        nem = so.hint(n_al, i, j) if n_al else None
        mai = so.hint(m_al, i, j) if m_al else None
        o, a, b = _n(ours), (_n(nem) if nem is not None else None), (_n(mai) if mai is not None else None)
        if all(x is None or x == o for x in (a, b)):
            status, sug = "format_only", ours  # digits/words, Latin/Devanagari, punctuation: same meaning
        elif a is not None and b is not None and a == b and a != o:
            status, sug = "others_agree", nem
        elif o == a or o == b:
            status, sug = "ours_majority", ours
        else:  # three readings differ (or the only other model differs)
            status, sug = "all_differ", ""
        diff_src = [x for x, c in ((nem, a), (mai, b)) if x is not None and c != o]
        other = diff_src[0] if diff_src else (nem if nem is not None else (mai or ""))
        ov = hn.values(ours.split())
        amount = any(hn.values(x.split()) != ov for x in diff_src) and (ov or any(hn.values(x.split()) for x in diff_src))
        kind = "amount" if amount else ("format" if status == "format_only" else so.classify(ours, other))
        rows.append({"first": i, "last": j, "start": words[i]["start"], "end": words[j]["end"], "status": status,
                     "kind": kind, "ours": ours, "nemotron": nem or "", "mai": mai or "",
                     "suggestion": sug, "mai_alignment": "text-only" if m_al else ""})
        i = j + 1
    for h in name_hits(words, names):
        rows.append({"first": h["first"], "last": h["last"], "start": words[h["first"]]["start"],
                     "end": words[h["last"]]["end"], "status": "name_hint", "kind": "name",
                     "ours": " ".join(words[k]["word"] for k in range(h["first"], h["last"] + 1)),
                     "nemotron": so.hint(n_al, h["first"], h["last"]) if n_al else "",
                     "mai": so.hint(m_al, h["first"], h["last"]) if m_al else "",
                     "suggestion": h["suggest"], "mai_alignment": "text-only" if m_al else ""})
    for r in rows:
        r["priority"] = PRIORITY[r["status"]]
        if r["kind"] == "amount" and r["status"] in ("others_agree", "all_differ"):
            r["priority"] = 0  # amounts that change meaning: listen first
        elif r["kind"] == "script" and r["status"] != "name_hint":
            r["priority"] = 3  # Latin vs Devanagari English: caption style, chosen at package time
        elif r["kind"] == "number" and r["status"] == "ours_majority":
            r["priority"] = 2  # amounts always deserve a listen
    rows.sort(key=lambda r: (r["priority"], r["start"]))
    for k, r in enumerate(rows, 1):
        r["id"], r["pattern"] = f"C{k:03d}", ""
    total = len(words)
    agree = total - sum(bad)
    counts = {s: sum(1 for r in rows if r["status"] == s) for s in PRIORITY}
    return {"rows": rows, "counts": counts, "patterns": patterns(rows, names=names), "words": total, "words_all_agree": agree,
            "all_agree_pct": round(100.0 * agree / total, 1) if total else 0.0,
            "sources": {"nemotron_timed": bool(timed), "mai_text": bool(text)}}


def patterns(rows: List[Dict[str, Any]], min_count: int = 2, names: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    """Same change suggested by both other models in several places (e.g. द्वारका -> द्वारिका x14):
    one decision for the whole pattern instead of N separate listens. Still decided by a human."""
    groups: Dict[tuple, List[Dict[str, Any]]] = {}
    for r in rows:
        if r["status"] == "others_agree" and r["kind"] in ("spelling", "spacing") and r["suggestion"] \
                and not (_name_toks(names) & set(_n(r["ours"]) + _n(r["suggestion"]))):
            groups.setdefault((" ".join(_n(r["ours"])), " ".join(_n(r["suggestion"]))), []).append(r)
    out = [{"ours": g[0]["ours"], "suggestion": g[0]["suggestion"], "count": len(g),
            "times": " ".join(f"{x['start']:.1f}" for x in g), "_rows": g} for g in groups.values() if len(g) >= min_count]
    out.sort(key=lambda p: -p["count"])
    for k, p in enumerate(out, 1):
        p["pattern"] = f"P{k:02d}"
        for r in p.pop("_rows"):
            r["pattern"] = p["pattern"]
    return out


def _name_toks(names: Optional[List[Dict[str, Any]]]) -> set:
    """Tokens of known proper names (and their mishearings): never grouped into a bulk 'all' pattern."""
    out: set = set()
    names = list(names or [])
    try:
        cfg = json.loads((Path(__file__).resolve().parent.parent / "config" / "name_suggestions.json").read_text(encoding="utf-8"))
        names += [{"suggest": t, "heard": []} for t in cfg.get("protected", [])]
    except (OSError, ValueError):
        pass
    for ent in names:
        for t in [ent["suggest"], *ent["heard"]]:
            out.update(_n(t))
    out.discard("")
    return out


def annotate_review(review_rows: List[Dict[str, str]], cons: Dict[str, Any],
                    words: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, str]]:
    """Add consensus columns to the user's review rows. A consensus part is often SMALLER than the review
    row (R038 '35,000 से 4,000 रुपये' vs part '35,000 -> पैंतीस सौ'), so:
      consensus_hint_PART           - the partial suggestion(s) only; never paste it as correct_text
      consensus_full_span_UNVERIFIED - the WHOLE row with only those parts replaced (amount rows in digits),
                                      left blank when a part needs a listen (all_differ) or crosses the row edge
    Both are hints. correct_text must be the full replacement for the whole row, chosen after listening."""
    from . import hindi_numbers as hn_
    out = []
    for r in review_rows:
        r = dict(r)
        f, l = int(r["first"]), int(r["last"])
        hit = sorted((c for c in cons["rows"] if c["first"] <= l and c["last"] >= f and c["status"] != "format_only"),
                     key=lambda c: c["priority"])
        r["consensus_status"] = hit[0]["status"] if hit else "all_agree"
        r["consensus_hint_PART"] = " | ".join(f"{c['ours']} -> {c['suggestion']}" for c in hit if c["suggestion"]
                                              and c["status"] in ("others_agree", "name_hint"))
        full, note = "", ""
        if words is not None and hit:
            edge = [c for c in hit if c["first"] < f or c["last"] > l]
            listen = [c for c in hit if c["status"] == "all_differ"]
            useful = sorted((c for c in hit if c["status"] in ("others_agree", "name_hint") and c["suggestion"]),
                            key=lambda c: c["first"])
            if edge:
                note = "span_mismatch: a part crosses this row's edge - write the full text yourself"
            elif listen:
                note = "needs_listen: models give 3 different readings"
            elif useful:
                toks, k = [], f
                for c in useful:
                    if c["first"] < k:
                        continue
                    toks += [words[x]["word"] for x in range(k, c["first"])] + c["suggestion"].split()
                    k = c["last"] + 1
                toks += [words[x]["word"] for x in range(k, l + 1)]
                full = " ".join(toks)
                ours_txt = " ".join(words[x]["word"] for x in range(f, l + 1))
                if any(c["kind"] == "amount" for c in useful) and any(ch.isdigit() for ch in ours_txt):
                    full = hn_.to_digits(full)  # keep the row's own style: digits only where ours used digits
        r["consensus_full_span_UNVERIFIED"] = full
        r["consensus_note"] = note
        out.append(r)
    return out


def load_names(path: str | Path) -> List[Dict[str, Any]]:
    p = Path(path)
    return json.loads(p.read_text(encoding="utf-8")).get("names", []) if p.exists() else []
