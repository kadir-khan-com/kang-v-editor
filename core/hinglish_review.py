"""KANG Hinglish Transcript Layer v0 + Hinglish Review Assistant v0.

Flow (user-defined, 2026-11-01):
  Hindi words.json (immutable master) -> words_hinglish_v1.json (same timings, versioned)
  -> review_hinglish_v1.csv + review_hinglish_v1.html (blocks with audio clips) -> user listens / fixes
  -> apply -> words_hinglish_v1_accepted.json + captions_hinglish_v1_accepted.srt
  -> timing verification (separate) -> visuals / preview / Premiere.

Rules
* The Hindi words.json is never modified; it is copied into the run and its sha256 is carried on every entry.
* A spelling-only change keeps the Hindi timing (timing_method inherited_from_hindi). Any change of word COUNT
  (merge, split, insert) gets interpolated timing with timing_status "unverified".
* Acceptance only when EVERY block has a decision (ok / fix) by a human (decided_by listened / read).
  Without that the output is written as a draft and says so. Nothing is auto-approved.
"""
from __future__ import annotations

import csv
import difflib
import hashlib
import html
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from core.hinglish import (DictBackend, YapperBackend, build_hinglish_srt, capitalize_sentences, load_table,
                           mark_pending_spans, romanize_words, skeleton)

SCHEMA = "kang.hinglish_words/1"
DECIDERS = ("listened", "read", "user_bulk")  # read = text-only; user_bulk = user approved all blocks at once (recorded, not per-block)
BLOCK_FIELDS = ["block", "start", "end", "time", "clip", "words", "hinglish", "hindi", "flags", "spelling_issues",
                "table_changed", "other_asr_hints", "action", "corrected_hinglish", "decided_by", "note"]


def _sha(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _ts(t: float) -> str:
    return f"{int(t // 60):02d}:{t % 60:05.2f}"


# ----------------------------------------------------------------------------- layer v0
def to_layer(rwords: List[Dict[str, Any]], source_sha: str) -> List[Dict[str, Any]]:
    out = []
    for i, w in enumerate(rwords):
        unverified = w.get("timing_status") == "unverified"
        out.append({"word_id": i, "hindi": w["devanagari"], "hinglish": w["roman"],
                    "start": w["start"], "end": w["end"],
                    "timing_method": "inherited_from_hindi",
                    "timing_status": "unverified" if unverified else "verified_pending",
                    "roman_source": w["roman_source"], "needs_review": w["needs_review"],
                    "review_reasons": w["review_reasons"], "source_words_sha256": source_sha})
    return out


def layer_doc(entries, source_path, source_sha, table_path, romanizer, version="v1", status="draft"):
    return {"schema": SCHEMA, "version": version, "status": status, "source_words": str(source_path),
            "source_words_sha256": source_sha, "table": str(table_path), "table_sha256": _sha(table_path),
            "romanizer": romanizer, "words": entries}


def layer_caption_words(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Adapter so core.hinglish.build_hinglish_srt can render a layer (roman/needs_review keys)."""
    return [{"roman": e["hinglish"], "start": e["start"], "end": e["end"], "devanagari": e["hindi"],
             "needs_review": e.get("needs_review", False), "review_reasons": e.get("review_reasons", []),
             "roman_source": e.get("roman_source", "")} for e in entries]


def hindi_srt(words: List[Dict[str, Any]]) -> str:
    from core.subtitles import build_srt, chunk_timings, chunk_words
    ch = chunk_words(words)
    return build_srt([{"start": s, "end": e, "text": " ".join(w["word"] for w in c)}
                      for c, (s, e) in zip(ch, chunk_timings(ch))])


# ----------------------------------------------------------------------------- spelling consistency
def canonical_names(table: Dict[str, Any]) -> List[str]:
    """Display spellings from the table that are proper names (start upper-case)."""
    vals = list(table["names"].values()) + list(table["phrases"].values())
    names = set()
    for v in vals:
        for tok in v.split():
            if tok[:1].isupper() and len(tok) > 2:
                names.add(tok)
    return sorted(names)


COMMON_LOWER = {"dwar", "shiv", "gopi", "ghat"}  # also ordinary words; lower-case is fine for these
NOT_NAMES = {"matra", "mitra", "meter", "mathra"}  # ordinary words that look like a name skeleton


def spelling_issues(entries: List[Dict[str, Any]], canon: List[str]) -> Dict[int, str]:
    """word_id -> 'found X, policy Y' when a word looks like a canonical name but is spelled differently:
    same letters in another case (krishna vs Krishna), or same consonant skeleton + same first letter +
    close spelling (difflib ratio >= 0.75: dwarika/dvaarika vs Dwarka). Words like matra/meter are not
    flagged against Mathura (ratio too low)."""
    sk = {c: skeleton(c) for c in canon}
    out = {}
    for e in entries:
        tok = re.sub(r"[^A-Za-z]", "", e["hinglish"])
        if len(tok) < 4:
            continue
        s, tl = skeleton(tok), tok.lower()
        if tl in NOT_NAMES:
            continue
        for c, cs in sk.items():
            if tok == c:
                break
            if tl == c.lower():
                if tl not in COMMON_LOWER:
                    out[e["word_id"]] = f"found '{tok}', policy '{c}' (case)"
                break
            if len(cs) >= 3 and s == cs and tl[0] == c[0].lower() and \
                    difflib.SequenceMatcher(a=tl, b=c.lower()).ratio() >= 0.75:
                out[e["word_id"]] = f"found '{tok}', policy '{c}'"
                break
    return out


# ----------------------------------------------------------------------------- blocks
def make_blocks(entries: List[Dict[str, Any]], block_s: float = 12.0, pause_s: float = 0.6) -> List[List[Dict[str, Any]]]:
    """~block_s seconds each, cut at a sentence end or a pause when possible."""
    blocks, cur = [], []
    for i, e in enumerate(entries):
        cur.append(e)
        dur = e["end"] - cur[0]["start"]
        nxt = entries[i + 1] if i + 1 < len(entries) else None
        sentence = e["hinglish"][-1:] in ".?!"
        pause = nxt is not None and nxt["start"] - e["end"] >= pause_s
        if nxt is None or dur >= block_s * 1.5 or (dur >= block_s * 0.6 and (sentence or pause)):
            blocks.append(cur)
            cur = []
    if cur:
        blocks.append(cur)
    return blocks


def block_rows(entries, blocks, table, clips: Optional[Dict[int, str]] = None, hints: Optional[List[Dict[str, Any]]] = None) -> List[Dict[str, Any]]:
    sp = spelling_issues(entries, canonical_names(table))
    rows = []
    for b, blk in enumerate(blocks, 1):
        flags = [f"{e['hinglish'] or '(empty)'}[{e['word_id']}]: {','.join(e['review_reasons'])}"
                 for e in blk if e.get("needs_review")]
        spi = [sp[e["word_id"]] for e in blk if e["word_id"] in sp]
        changed = [f"{e['hindi']}->{e['hinglish']}" for e in blk if e.get("roman_source") in ("name", "phrase", "word_fix")]
        hs = [f"{h['ours']} ~ {h['other_asr']}" for h in (hints or [])
              if blk[0]["start"] - 0.01 <= float(h["start"]) <= blk[-1]["end"] + 0.01]
        rows.append({"block": f"H{b:03d}", "start": blk[0]["start"], "end": blk[-1]["end"],
                     "time": f"{_ts(blk[0]['start'])}-{_ts(blk[-1]['end'])}", "clip": (clips or {}).get(b, ""),
                     "words": f"{blk[0]['word_id']}-{blk[-1]['word_id']}",
                     "hinglish": " ".join(e["hinglish"] for e in blk if e["hinglish"]),
                     "hindi": " ".join(e["hindi"] for e in blk),
                     "flags": " | ".join(flags), "spelling_issues": " | ".join(spi),
                     "table_changed": " | ".join(dict.fromkeys(changed)), "other_asr_hints": " | ".join(hs),
                     "action": "", "corrected_hinglish": "", "decided_by": "", "note": ""})
    return rows


def write_rows(path, rows, fields=BLOCK_FIELDS):
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def read_rows(path) -> List[Dict[str, str]]:
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def review_html(rows: List[Dict[str, Any]], title: str) -> str:
    """Self-contained page: one card per block with its audio clip, Hinglish, Hindi and flags. Read-only helper;
    decisions still go in the CSV."""
    css = ("body{font-family:Segoe UI,Arial,sans-serif;max-width:980px;margin:24px auto;padding:0 12px;background:#fafafa}"
           ".b{background:#fff;border:1px solid #ddd;border-radius:8px;padding:12px 14px;margin:10px 0}"
           ".h{font-size:19px;line-height:1.5}.d{color:#555;font-size:15px;margin-top:6px}"
           ".f{color:#b45309;font-size:13px;margin-top:6px}.s{color:#b91c1c;font-size:13px}.t{color:#666;font-size:13px}"
           "audio{width:100%;margin-top:6px}")
    parts = [f"<!doctype html><meta charset='utf-8'><title>{html.escape(title)}</title><style>{css}</style>",
             f"<h2>{html.escape(title)}</h2><p>Listen to each block, then fill <b>action</b> (ok / fix), "
             "<b>corrected_hinglish</b> (full block text, only for fix) and <b>decided_by</b> (listened / read) "
             "in review_hinglish CSV.</p>"]
    for r in rows:
        parts.append("<div class='b'>")
        parts.append(f"<div class='t'><b>{r['block']}</b> &nbsp; {r['time']} &nbsp; words {r['words']}</div>")
        if r.get("clip"):
            parts.append(f"<audio controls preload='none' src='{html.escape(r['clip'])}'></audio>")
        parts.append(f"<div class='h'>{html.escape(r['hinglish'])}</div><div class='d'>{html.escape(r['hindi'])}</div>")
        if r.get("spelling_issues"):
            parts.append(f"<div class='s'>spelling: {html.escape(r['spelling_issues'])}</div>")
        if r.get("other_asr_hints"):
            parts.append(f"<div class='t'>other ASR hears (hint only): {html.escape(r['other_asr_hints'])}</div>")
        if r.get("flags"):
            parts.append(f"<div class='f'>check: {html.escape(r['flags'])}</div>")
        parts.append("</div>")
    return "\n".join(parts) + "\n"


# ----------------------------------------------------------------------------- review pack (review-hinglish)
def review_pack(layer_path: str, *, media: Optional[str] = None, table_path: str = "config/hinglish_names.json",
                block_s: float = 12.0, clips: bool = True, other_asr: Optional[str] = None) -> Dict[str, Any]:
    """Layer -> review_hinglish_<ver>.csv + .html (+ one mp3 per block) next to the layer. Changes no words."""
    from core.runs import run_ffmpeg
    lp = Path(layer_path)
    doc = json.loads(lp.read_text(encoding="utf-8"))
    entries, ver = doc["words"], doc.get("version", "v1")
    table = load_table(table_path)
    blocks = make_blocks(entries, block_s)
    clip_map: Dict[int, str] = {}
    if media and clips:
        cdir = lp.parent / f"review_hinglish_{ver}_clips"
        cdir.mkdir(exist_ok=True)
        for b, blk in enumerate(blocks, 1):
            s, e = max(0.0, blk[0]["start"] - 0.3), blk[-1]["end"] + 0.3
            out = cdir / f"H{b:03d}_{int(s // 60):02d}m{int(s % 60):02d}s.mp3"
            run_ffmpeg(["-ss", f"{s:.2f}", "-t", f"{e - s:.2f}", "-i", media, "-vn", "-ac", "1", "-b:a", "96k", str(out)])
            clip_map[b] = f"{cdir.name}/{out.name}"
    hints = None
    if other_asr:
        from core.hinglish import diff_hints
        oc = json.loads(Path(other_asr).read_text(encoding="utf-8"))
        hints = diff_hints(layer_caption_words(entries), oc.get("chunks", oc))
    rows = block_rows(entries, blocks, table, clip_map, hints)
    cp = lp.parent / f"review_hinglish_{ver}.csv"
    if cp.exists():  # never overwrite a sheet the user may have filled
        return {"error": f"{cp.name} already exists; move it away first (it may hold your decisions)"}
    write_rows(cp, rows)
    htp = lp.parent / f"review_hinglish_{ver}.html"
    htp.write_text(review_html(rows, f"Hinglish review {ver} - {lp.parent.name}"), encoding="utf-8")
    return {"review_csv": str(cp), "review_html": str(htp), "clips": clip_map, "rows": rows, "blocks": len(rows),
            "blocks_with_flags": sum(1 for r in rows if r["flags"]),
            "blocks_with_spelling_issues": sum(1 for r in rows if r["spelling_issues"])}


# ----------------------------------------------------------------------------- run: convert + review pack
def hinglish_layer_run(words_path: str, *, media: Optional[str] = None, yapper_dir: Optional[str] = None,
                       backend=None, table_path: str = "config/hinglish_names.json",
                       master_review_csv: Optional[str] = None, block_s: float = 12.0, clips: bool = True,
                       run=None, version: str = "v1", other_asr: Optional[str] = None) -> Dict[str, Any]:
    from core.runs import Run
    if backend is None:
        if not yapper_dir:
            return {"error": "no romanizer: pass --yapper-dir (clone of github.com/ABHISHEKgauti25/yapper_transliterator)"}
        backend = YapperBackend(yapper_dir)
    run = run or Run()
    run.add_input(words_path, "W1")
    if media:
        run.add_input(media, "A1")
    src_copy = run.path("words.json")
    src_copy.write_bytes(Path(words_path).read_bytes())  # immutable copy of the master
    sha = _sha(src_copy)
    words = json.loads(src_copy.read_text(encoding="utf-8"))
    if master_review_csv:
        words_m = mark_pending_spans(words, read_rows(master_review_csv))
    else:
        words_m = words
    table = load_table(table_path)
    rw = romanize_words(words_m, backend, table)
    entries = to_layer(rw, sha)
    doc = layer_doc(entries, Path(words_path), sha, table_path, getattr(backend, "name", "?"), version)
    lp = run.path(f"words_hinglish_{version}.json")
    lp.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    srt_h, ev = build_hinglish_srt(layer_caption_words(entries))
    hp = run.path(f"captions_hinglish_{version}.srt")
    hp.write_text(srt_h, encoding="utf-8")
    dp = run.path("captions_hindi.srt")
    dp.write_text(hindi_srt(words), encoding="utf-8")
    rp = review_pack(str(lp), media=media, table_path=table_path, block_s=block_s, clips=clips, other_asr=other_asr)
    rows = rp["rows"]
    cp, htp, clip_map = Path(rp["review_csv"]), Path(rp["review_html"]), rp["clips"]
    for p, k in ((src_copy, "words_hindi_master_copy"), (lp, "words_hinglish"), (hp, "captions_hinglish_draft"),
                 (dp, "captions_hindi"), (cp, "review_hinglish_csv"), (htp, "review_hinglish_html")):
        run.add_output(p, k)
    n_sp = sum(1 for r in rows if r["spelling_issues"])
    run.log_step("hinglish_layer", version=version, words=len(entries), blocks=len(rows),
                 flagged_words=sum(e["needs_review"] for e in entries), blocks_with_spelling_issues=n_sp,
                 romanizer=doc["romanizer"], table_sha256=doc["table_sha256"])
    run.set_status("hinglish_review_required")
    return {"run_id": run.run_id, "dir": str(run.dir), "status": "WARN", "accepted": False,
            "words": len(entries), "caption_events": len(ev), "blocks": len(rows),
            "flagged_words": sum(e["needs_review"] for e in entries),
            "blocks_with_flags": sum(1 for r in rows if r["flags"]), "blocks_with_spelling_issues": n_sp,
            "clips": len(clip_map), "files": {"layer": str(lp), "srt_hinglish": str(hp), "srt_hindi": str(dp),
                                              "review_csv": str(cp), "review_html": str(htp)}}


# ----------------------------------------------------------------------------- apply review
def _retime(old: List[Dict[str, Any]], new_tokens: List[str], prev_end: float, next_start: float, reason: str):
    """Replace old entries with new tokens. Same count -> keep each timing (spelling change).
    Different count -> evenly spread over the old span (or the gap for a pure insert), unverified."""
    if old and len(old) == len(new_tokens):
        return [{**o, "hinglish": t, "timing_method": o["timing_method"] if o["hinglish"] == t else "inherited_from_hindi",
                 "edited": o["hinglish"] != t, "edit_reason": reason if o["hinglish"] != t else ""}
                for o, t in zip(old, new_tokens)]
    if old:
        s, e = old[0]["start"], old[-1]["end"]
        hindi = " ".join(o["hindi"] for o in old)
        method = "merged_after_review" if len(new_tokens) < len(old) else "split_after_review"
    else:
        s, e = prev_end, max(next_start, prev_end + 0.05)
        hindi, method = "", "inserted_after_review"
    if not new_tokens:
        return []
    step = (e - s) / len(new_tokens)
    sha = old[0]["source_words_sha256"] if old else ""
    return [{"word_id": None, "hindi": hindi, "hinglish": t, "start": round(s + k * step, 3),
             "end": round(s + (k + 1) * step, 3), "timing_method": method, "timing_status": "unverified",
             "roman_source": "review", "needs_review": False, "review_reasons": [], "source_words_sha256": sha,
             "from_word_ids": [o["word_id"] for o in old], "edited": True, "edit_reason": reason}
            for k, t in enumerate(new_tokens)]


def apply_block(blk: List[Dict[str, Any]], corrected: str, prev_end: float, next_start: float, block_id: str):
    old_t = [e["hinglish"] for e in blk]
    new_t = corrected.split()
    key = lambda t: re.sub(r"[^\w]", "", t.lower())
    sm = difflib.SequenceMatcher(a=[key(t) for t in old_t], b=[key(t) for t in new_t], autojunk=False)
    out: List[Dict[str, Any]] = []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            # same letters; punctuation/case may differ -> spelling change, timing kept
            out.extend(_retime(blk[i1:i2], new_t[j1:j2], 0, 0, f"{block_id}:case/punct"))
            continue
        pe = out[-1]["end"] if out else prev_end
        ns = blk[i2]["start"] if i2 < len(blk) else next_start
        out.extend(_retime(blk[i1:i2], new_t[j1:j2], pe, ns, f"{block_id}:{op}"))
    return out


def apply_hinglish_review(layer_path: str, review_csv: str, *, allow_partial: bool = False,
                          out: Optional[str] = None) -> Dict[str, Any]:
    """Writes <layer>_accepted.json + captions_..._accepted.srt only when every block is decided by a human.
    With allow_partial, undecided blocks keep the draft text and the output is <layer>_draft_reviewed.json."""
    lp = Path(layer_path)
    doc = json.loads(lp.read_text(encoding="utf-8"))
    entries = doc["words"]
    rows = read_rows(review_csv)
    by_id = {e["word_id"]: e for e in entries}
    problems, undecided = [], []
    plan = []
    for r in rows:
        act = (r.get("action") or "").strip().lower()
        db = (r.get("decided_by") or "").strip().lower()
        try:
            a, b = (int(x) for x in r["words"].split("-"))
        except Exception:
            problems.append(f"{r.get('block')}: bad words range {r.get('words')!r}")
            continue
        blk = [by_id[i] for i in range(a, b + 1) if i in by_id]
        cur = " ".join(e["hinglish"] for e in blk if e["hinglish"])
        if cur != (r.get("hinglish") or "").strip():
            problems.append(f"{r['block']}: layer changed since the CSV was made")
            continue
        if not act:
            undecided.append(r["block"])
            plan.append((blk, None, r["block"]))
            continue
        if act not in ("ok", "fix"):
            problems.append(f"{r['block']}: action must be ok or fix, got {act!r}")
            continue
        if db not in DECIDERS:
            problems.append(f"{r['block']}: decided_by must be one of {DECIDERS}, got {db!r}")
            continue
        corr = (r.get("corrected_hinglish") or "").strip()
        if act == "fix" and not corr:
            problems.append(f"{r['block']}: action=fix needs corrected_hinglish (the full block text)")
            continue
        plan.append((blk, corr if act == "fix" else None, r["block"]))
    if problems:
        return {"ok": False, "accepted": False, "problems": problems}
    if undecided and not allow_partial:
        return {"ok": False, "accepted": False,
                "problems": [f"{len(undecided)} block(s) without a decision: {', '.join(undecided[:12])}"
                             + (" ..." if len(undecided) > 12 else "") + " (use --partial for a draft)"]}
    new: List[Dict[str, Any]] = []
    edited_blocks = 0
    for k, (blk, corr, bid) in enumerate(plan):
        if corr is None:
            new.extend(dict(e) for e in blk)
            continue
        prev_end = new[-1]["end"] if new else 0.0
        nxt = plan[k + 1][0][0]["start"] if k + 1 < len(plan) and plan[k + 1][0] else blk[-1]["end"]
        rep = apply_block(blk, corr, prev_end, nxt, bid)
        edited_blocks += any(e.get("edited") for e in rep)
        new.extend(rep)
    accepted = not undecided
    out_doc = {**doc, "status": "accepted_text" if accepted else "draft_reviewed",
               "review_csv": str(review_csv), "review_csv_sha256": _sha(review_csv),
               "parent_layer_sha256": _sha(lp), "words": new,
               "timing_note": "text accepted by human review; timing still needs verification "
                              "(verified_pending = inherited from Hindi ASR, unverified = changed word count)"}
    suffix = "_accepted" if accepted else "_draft_reviewed"
    op = Path(out) if out else lp.with_name(lp.stem + suffix + ".json")
    if not accepted and out and "accepted" in Path(out).name:
        op = Path(out).with_name(Path(out).name.replace("accepted", "draft_reviewed"))
    op.write_text(json.dumps(out_doc, ensure_ascii=False, indent=1), encoding="utf-8")
    srt, ev = build_hinglish_srt(layer_caption_words(new))
    sp = op.with_name(op.stem.replace("words_", "captions_") + ".srt")
    sp.write_text(srt, encoding="utf-8")
    from collections import Counter
    acc = {"schema": "kang.hinglish_acceptance/1", "accepted": accepted,
           "status": "accepted_text_timing_pending" if accepted else "draft_reviewed",
           "layer_in": str(lp), "layer_in_sha256": _sha(lp), "review_csv": str(review_csv),
           "review_csv_sha256": _sha(review_csv), "layer_out": str(op), "layer_out_sha256": _sha(op),
           "blocks": len(rows), "undecided": undecided,
           "decided_by": dict(Counter((r.get("decided_by") or "").strip().lower() for r in rows if (r.get("action") or "").strip())),
           "acceptance_mode": ("user_bulk_approval" if any((r.get("decided_by") or "").strip().lower() == "user_bulk"
                                                            for r in rows) else "per_block"),
           "edited_blocks": edited_blocks, "timing_status": dict(Counter(e["timing_status"] for e in new)),
           "timing_verified": False,
           "note": "verified_pending = timing inherited unchanged from the Hindi ASR word (not yet checked by ear "
                   "against captions); unverified = word count changed in review (interpolated)."}
    ap = op.with_name(("hinglish_acceptance" if accepted else "hinglish_acceptance_DRAFT") + ".json")
    ap.write_text(json.dumps(acc, ensure_ascii=False, indent=2), encoding="utf-8")
    if (lp.parent / "manifest.json").exists():
        from core.runs import Run
        r = Run(lp.parent.name, root=lp.parent.parent)
        r.add_output(op, "words_hinglish_accepted" if accepted else "words_hinglish_draft_reviewed")
        r.add_output(sp, "captions_hinglish_accepted" if accepted else "captions_hinglish_draft_reviewed")
        r.add_output(ap, "hinglish_acceptance")
        r.log_step("apply_hinglish_review", accepted=accepted, undecided=len(undecided), edited_blocks=edited_blocks)
        r.set_status("hinglish_text_accepted_timing_pending" if accepted else "hinglish_review_in_progress")
    from collections import Counter
    return {"ok": True, "accepted": accepted, "status": "PASS" if accepted else "WARN",
            "blocks": len(rows), "undecided": len(undecided), "edited_blocks": edited_blocks,
            "timing_status": dict(Counter(e["timing_status"] for e in new)),
            "words_in": len(entries), "words_out": len(new),
            "files": {"layer": str(op), "srt": str(sp), "acceptance": str(ap)}}


def bulk_ok_csv(review_csv: str, statement: str, out_csv: Optional[str] = None) -> Path:
    """User's explicit 'approve everything' -> a filled COPY of the review CSV (original untouched).
    Only undecided rows are filled (action=ok, decided_by=user_bulk, note=statement); rows the user already
    decided are kept. The acceptance file then says acceptance_mode=user_bulk_approval."""
    if not statement.strip():
        raise ValueError("bulk approval needs the user's statement (who/when/what)")
    import csv
    rows = read_rows(review_csv)
    for r in rows:
        if not (r.get("action") or "").strip():
            r["action"], r["decided_by"], r["note"] = "ok", "user_bulk", statement.strip()
    op = Path(out_csv) if out_csv else Path(review_csv).with_name(Path(review_csv).stem + "_user_bulk_ok.csv")
    with open(op, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=BLOCK_FIELDS)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in BLOCK_FIELDS})
    return op
