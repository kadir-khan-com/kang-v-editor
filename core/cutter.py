"""F03 Silence + filler cut (non-destructive).

1) silencedetect=n=-34dB:d=0.45 -> silent ranges
2) filler words (dictionary 'auto') merged with silence as removal candidates;
   'review' words only flagged (never auto-cut)
3) padding: 80 ms lead-in, 90 ms lead-out around kept speech
4) cuts.json (keep list = EDL cuts) + cut_list.txt for the human approval gate.
Guarantee: a removal range never intersects a kept word (words.json boundaries).
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from .runs import filter_script_args, run_ffmpeg

Range = Tuple[float, float]

_SIL_START = re.compile(r"silence_start:\s*(-?[\d.]+)")
_SIL_END = re.compile(r"silence_end:\s*(-?[\d.]+)")


def detect_silence(media: str | Path, noise_db: float = -34.0, min_dur: float = 0.45,
                   total: Optional[float] = None) -> List[Range]:
    cmd = ["ffmpeg", "-hide_banner", "-nostdin", "-i", str(media), "-vn", "-af",
           f"silencedetect=n={noise_db}dB:d={min_dur}", "-f", "null", "-"]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        raise RuntimeError(res.stderr[-1500:])
    return parse_silencedetect(res.stderr, total)


def parse_silencedetect(log: str, total: Optional[float] = None) -> List[Range]:
    out: List[Range] = []
    start = None
    for line in log.splitlines():
        m = _SIL_START.search(line)
        if m:
            start = max(0.0, float(m.group(1)))
            continue
        m = _SIL_END.search(line)
        if m and start is not None:
            out.append((round(start, 3), round(float(m.group(1)), 3)))
            start = None
    if start is not None and total is not None and total > start:
        out.append((round(start, 3), round(total, 3)))
    return out


def load_fillers(path: str | Path) -> Dict[str, List[str]]:
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    return {"auto": [w.lower() for w in d.get("auto", [])], "review": [w.lower() for w in d.get("review", [])]}


def _norm(w: str) -> str:
    return re.sub(r"[।?!.,;:\"'\-\s]", "", w).lower()


def merge_ranges(ranges: List[Range], join_gap: float = 0.0) -> List[Range]:
    out: List[Range] = []
    for s, e in sorted(ranges):
        if out and s <= out[-1][1] + join_gap:
            out[-1] = (out[-1][0], max(out[-1][1], e))
        else:
            out.append((s, e))
    return out


def tighten_words(words: List[Dict[str, Any]], silences: List[Range], min_word: float = 0.06) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Whisper word boundaries often swallow the following/preceding pause (e.g. a word
    stamped 24.02-24.80 while 24.04-24.60 is measured silence). Trust the audio: trim a
    word's edge that lies inside a detected silence. A word fully inside silence is
    reported (likely mis-timed) and left untouched. Returns (tightened_words, notes)."""
    out, notes = [], []
    for w in words:
        s, e = float(w["start"]), float(w["end"])
        for a, b in silences:
            if b <= s or a >= e:
                continue
            if a <= s and b >= e:
                notes.append({"word": w["word"], "start": s, "end": e, "note": "inside_silence_untouched"})
                break
            if a - s < min_word and b < e:   # silence covers (or nearly covers) the word start
                if e - b >= min_word:
                    s = b
            elif e - b < min_word and a > s:  # silence covers (or nearly covers) the word end
                if a - s >= min_word:
                    e = a
        nw = dict(w)
        if (s, e) != (float(w["start"]), float(w["end"])):
            nw["start"], nw["end"] = round(s, 3), round(e, 3)
            notes.append({"word": w["word"], "from": [w["start"], w["end"]], "to": [nw["start"], nw["end"]], "note": "tightened"})
        out.append(nw)
    return out, notes


def plan_cuts(words: List[Dict[str, Any]], silences: List[Range], total: float,
              fillers: Optional[Dict[str, List[str]]] = None, lead_in: float = 0.08,
              lead_out: float = 0.09, min_keep: float = 0.10) -> Dict[str, Any]:
    """Return {keep:[(in,out)], remove:[...], flagged:[...], stats}.

    Removal candidates = silences + 'auto' filler words. Each removal is shrunk by the
    padding (lead-out after previous speech, lead-in before next speech) and then
    clipped so it can never overlap a word we keep.
    """
    fillers = fillers or {"auto": [], "review": []}
    words, tighten_notes = tighten_words(words, silences)
    auto, review = set(map(_norm, fillers["auto"])), set(map(_norm, fillers["review"]))
    filler_ranges: List[Range] = []
    flagged: List[Dict[str, Any]] = []
    kept_words: List[Dict[str, Any]] = []
    for i, w in enumerate(words):
        n = _norm(w["word"])
        if n in auto:
            filler_ranges.append((w["start"], w["end"]))
            flagged.append({"i": i, "word": w["word"], "start": w["start"], "end": w["end"], "action": "cut_proposed"})
        else:
            kept_words.append(w)
            if n in review:
                flagged.append({"i": i, "word": w["word"], "start": w["start"], "end": w["end"], "action": "review_only"})

    candidates = merge_ranges(list(silences) + filler_ranges, join_gap=0.05)
    removes: List[Range] = []
    for s, e in candidates:
        s2 = s + (lead_out if s > 0 else 0.0)
        e2 = e - (lead_in if e < total else 0.0)
        # never touch a kept word (+ its padding)
        for w in kept_words:
            ws, we = w["start"] - lead_in, w["end"] + lead_out
            if we <= s2 or ws >= e2:
                continue
            # word intersects removal: clip to the side that keeps more removal
            if ws - s2 >= e2 - we:
                e2 = min(e2, ws)
            else:
                s2 = max(s2, we)
        if e2 - s2 >= 0.05:
            removes.append((round(s2, 3), round(e2, 3)))
    removes = merge_ranges(removes)

    keep: List[Range] = []
    cur = 0.0
    for s, e in removes:
        if s - cur >= min_keep:
            keep.append((round(cur, 3), round(s, 3)))
        cur = e
    if total - cur >= min_keep:
        keep.append((round(cur, 3), round(total, 3)))

    removed = round(sum(e - s for s, e in removes), 3)
    return {
        "params": {"lead_in": lead_in, "lead_out": lead_out, "min_keep": min_keep},
        "keep": keep, "remove": removes, "flagged": flagged,
        "words_tightened": words, "tighten_notes": tighten_notes,
        "stats": {"source_dur": round(total, 3), "removed_dur": removed,
                  "kept_dur": round(sum(e - s for s, e in keep), 3), "cut_count": len(removes)},
    }


def check_no_word_truncated(words: List[Dict[str, Any]], keep: List[Range], fillers_auto: Optional[List[str]] = None) -> List[str]:
    """QA: every non-filler word must lie fully inside one keep range."""
    auto = set(map(_norm, fillers_auto or []))
    bad = []
    for w in words:
        if _norm(w["word"]) in auto:
            continue
        if not any(s - 1e-3 <= w["start"] and w["end"] <= e + 1e-3 for s, e in keep):
            bad.append(f"{w['word']}@{w['start']}-{w['end']}")
    return bad


def remap_words(words: List[Dict[str, Any]], keep: List[Range]) -> List[Dict[str, Any]]:
    """Map word timestamps onto the cut timeline (for subtitles after cutting)."""
    out = []
    offset_table = []
    t = 0.0
    for s, e in keep:
        offset_table.append((s, e, t))
        t += e - s
    for w in words:
        for s, e, t0 in offset_table:
            if s - 1e-3 <= w["start"] and w["end"] <= e + 1e-3:
                nw = dict(w)
                nw["start"] = round(t0 + max(w["start"], s) - s, 3)
                nw["end"] = round(t0 + min(w["end"], e) - s, 3)
                out.append(nw)
                break
    return out


def cut_list_text(plan: Dict[str, Any]) -> str:
    lines = ["KANG cut list (approve before render)", "=" * 40]
    for i, (s, e) in enumerate(plan["remove"], 1):
        lines.append(f"CUT {i:03d}: {s:8.3f} -> {e:8.3f}  ({e - s:.2f}s)")
    for f in plan["flagged"]:
        lines.append(f"{'FILLER' if f['action'] == 'cut_proposed' else 'REVIEW'}: '{f['word']}' @ {f['start']:.2f}s ({f['action']})")
    st = plan["stats"]
    lines.append(f"Source {st['source_dur']}s -> kept {st['kept_dur']}s (removed {st['removed_dur']}s in {st['cut_count']} cuts)")
    return "\n".join(lines) + "\n"


def render_cuts(media: str | Path, keep: List[Range], out: str | Path, video: bool = True,
                log: Optional[Path] = None, afade_ms: float = 5.0) -> Path:
    """Concatenate keep ranges via trim/atrim + concat. A 5 ms fade at every joint
    prevents audible clicks at cut boundaries."""
    if not keep:
        raise ValueError("Nothing to keep")
    f = afade_ms / 1000.0
    parts, labels = [], []
    for i, (s, e) in enumerate(keep):
        d = e - s
        a = (f"[0:a]atrim=start={s:.3f}:end={e:.3f},asetpts=PTS-STARTPTS,"
             f"afade=t=in:st=0:d={f:.3f},afade=t=out:st={max(d - f, 0):.3f}:d={f:.3f}[a{i}]")
        if video:
            parts.append(f"[0:v]trim=start={s:.3f}:end={e:.3f},setpts=PTS-STARTPTS[v{i}]")
            labels.append(f"[v{i}][a{i}]")
        else:
            labels.append(f"[a{i}]")
        parts.append(a)
    n = len(keep)
    if video:
        parts.append(f"{''.join(labels)}concat=n={n}:v=1:a=1[v][a]")
        maps = ["-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p"]
    else:
        parts.append(f"{''.join(labels)}concat=n={n}:v=0:a=1[a]")
        maps = ["-map", "[a]"]
    script = Path(out).with_suffix(".filter.txt")
    script.write_text(";\n".join(parts), encoding="utf-8")
    acodec = ["-c:a", "aac", "-b:a", "192k"] if str(out).endswith((".mp4", ".m4a", ".mov")) else ["-c:a", "pcm_s16le"] if str(out).endswith(".wav") else []
    run_ffmpeg(["-i", str(media), *filter_script_args(script), *maps, *acodec, str(out)], log)
    return Path(out)
