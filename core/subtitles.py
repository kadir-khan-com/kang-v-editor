"""F01 Animated subtitles (word highlight) + F02 subtitle presets.

Option A (Phase 2): one ASS event per chunk with \\kf karaoke tags.
    SecondaryColour = text (white, not yet spoken), PrimaryColour = highlight.
Option B (Phase 3): one ASS event per word; the active word gets highlight colour
    plus a \\t(\\fscx108\\fscy108) scale pop.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from pydantic import BaseModel, Field

from .brand import CANVAS, Brand, font_family_name, hex_to_ass

SENTENCE_END = "।?!.॥"
SOFT_BREAK = ",;:"


# --------------------------------------------------------------------------- F02
class Preset(BaseModel):
    name: str
    description: str = ""
    font_role: str = Field("hindi", pattern="^(heading|body|hindi)$")
    size_pct: float = Field(gt=1, le=15, description="font size as % of canvas height")
    outline_px: float = Field(6, ge=0, le=20)
    shadow_px: float = Field(2, ge=0, le=20)
    uppercase: bool = False
    bold: bool = True
    box: bool = False
    max_chars: int = Field(32, ge=8, le=80)
    max_words: int = Field(4, ge=1, le=10)
    min_words: int = Field(2, ge=1, le=10)
    max_dur: float = Field(2.0, gt=0.3, le=8)
    pause_break: float = Field(0.35, ge=0.05, le=3)
    highlight: str = Field("kf", pattern="^(kf|pop)$")
    position: str = Field("bottom", pattern="^(bottom|middle)$")


def load_preset(name_or_path: str, presets_dir: str | Path = "presets") -> Preset:
    p = Path(name_or_path)
    if not p.suffix:
        p = Path(presets_dir) / f"{name_or_path}.json"
    return Preset.model_validate(json.loads(p.read_text(encoding="utf-8")))


def list_presets(presets_dir: str | Path = "presets") -> List[str]:
    return sorted(p.stem for p in Path(presets_dir).glob("*.json"))


# --------------------------------------------------------------------------- chunking
def _text_len(words: List[Dict[str, Any]]) -> int:
    return len(" ".join(w["word"] for w in words))


def chunk_words(words: List[Dict[str, Any]], max_words: int = 4, min_words: int = 2,
                max_chars: int = 32, max_dur: float = 2.0, pause_break: float = 0.35,
                fits=None) -> List[List[Dict[str, Any]]]:
    """Split words into 2-4 word chunks.

    Break when: adding the word exceeds max_words/max_chars/max_dur, a pause > pause_break
    precedes the word, or the previous word ends a sentence. `fits(text)` (optional) is a
    pixel-width check; a chunk that would not fit the safe width is broken early.
    """
    chunks: List[List[Dict[str, Any]]] = []
    cur: List[Dict[str, Any]] = []
    for w in words:
        if cur:
            prev = cur[-1]
            pause = w["start"] - prev["end"]
            cand = cur + [w]
            too_many = len(cand) > max_words
            too_long = _text_len(cand) > max_chars
            too_slow = (w["end"] - cur[0]["start"]) > max_dur
            no_fit = fits is not None and not fits(" ".join(x["word"] for x in cand))
            sentence = prev["word"][-1:] in SENTENCE_END
            soft = prev["word"][-1:] in SOFT_BREAK and len(cur) >= min_words
            if too_many or too_long or too_slow or no_fit or pause > pause_break or sentence or soft:
                chunks.append(cur)
                cur = []
        cur.append(w)
    if cur:
        chunks.append(cur)
    return chunks


def chunk_timings(chunks: List[List[Dict[str, Any]]], merge_gap: float = 0.08) -> List[Tuple[float, float]]:
    """Event start/end per chunk. Gap < merge_gap -> previous end extended (no flicker);
    overlap -> previous end trimmed to next start."""
    times = [(c[0]["start"], c[-1]["end"]) for c in chunks]
    out: List[Tuple[float, float]] = []
    for i, (s, e) in enumerate(times):
        if i + 1 < len(times):
            ns = times[i + 1][0]
            if e > ns:            # overlap -> trim
                e = ns
            elif ns - e < merge_gap:  # tiny gap -> merge
                e = ns
        out.append((round(s, 3), round(max(e, s + 0.01), 3)))
    return out


# --------------------------------------------------------------------------- ASS
def ass_time(t: float) -> str:
    cs = int(round(max(t, 0) * 100))
    h, cs = divmod(cs, 360000)
    m, cs = divmod(cs, 6000)
    s, cs = divmod(cs, 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def _escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("{", "(").replace("}", ")").replace("\n", " ")


class Layout(BaseModel):
    fmt: str
    width: int
    height: int
    font_size: int
    margin_lr: int
    margin_v: int
    font_family: str


def make_layout(brand: Brand, preset: Preset, fmt: str, font_path: str | Path) -> Layout:
    w, h = CANVAS[fmt]
    size = int(round(h * preset.size_pct / 100))
    if fmt == "16:9":
        size = int(round(size * 1.35))  # landscape: height is small, keep legible
    margin_v = brand.subtitle_bottom_for(fmt) if preset.position == "bottom" else int(h * 0.42)
    return Layout(fmt=fmt, width=w, height=h, font_size=size, margin_lr=brand.margin_for(fmt),
                  margin_v=margin_v, font_family=font_family_name(font_path))


def make_fit_checker(layout: Layout, font_path: str | Path, outline_px: float):
    """Pixel-width check with the real font (HarfBuzz shaping via Pillow raqm when available)."""
    from PIL import ImageFont
    font = ImageFont.truetype(str(font_path), layout.font_size)
    max_w = layout.width - 2 * layout.margin_lr - 2 * outline_px

    def fits(text: str) -> bool:
        l, t, r, b = font.getbbox(text)
        return (r - l) <= max_w * 1.08  # libass scale-pop headroom handled by 108% factor
    return fits


def build_ass(words: List[Dict[str, Any]], brand: Brand, preset: Preset, layout: Layout,
              font_path: Optional[str | Path] = None, option: Optional[str] = None) -> Tuple[str, List[Dict[str, Any]]]:
    """Return (ASS text, events). events = [{start,end,text,words:[...]}] for QA."""
    option = option or ("B" if preset.highlight == "pop" else "A")
    c = brand.colors
    primary = hex_to_ass(c.highlight)
    secondary = hex_to_ass(c.text)
    outline_col = hex_to_ass(c.outline)
    back = hex_to_ass(c.primary, alpha=0x40) if preset.box else hex_to_ass("#000000", alpha=0x80)
    border_style = 3 if preset.box else 1
    bold = -1 if preset.bold else 0
    align = 2  # bottom-center

    if option == "A":
        style_primary, style_secondary = primary, secondary
    else:
        style_primary, style_secondary = secondary, secondary

    header = f"""[Script Info]
; Generated by Kang AI (F01/F02) preset={preset.name} option={option}
ScriptType: v4.00+
PlayResX: {layout.width}
PlayResY: {layout.height}
WrapStyle: 2
ScaledBorderAndShadow: yes
YCbCr Matrix: TV.709

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Kang,{layout.font_family},{layout.font_size},{style_primary},{style_secondary},{outline_col},{back},{bold},0,0,0,100,100,0,0,{border_style},{preset.outline_px},{preset.shadow_px},{align},{layout.margin_lr},{layout.margin_lr},{layout.margin_v},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    fits = make_fit_checker(layout, font_path, preset.outline_px) if font_path else None
    chunks = chunk_words(words, preset.max_words, preset.min_words, preset.max_chars, preset.max_dur,
                         preset.pause_break, fits=fits)
    timings = chunk_timings(chunks)
    lines: List[str] = []
    events: List[Dict[str, Any]] = []

    def disp(w: str) -> str:
        return _escape(w.upper() if preset.uppercase else w)

    for chunk, (cs, ce) in zip(chunks, timings):
        if option == "A":
            parts = []
            pos = int(round(cs * 100))  # integer centiseconds -> no drift
            for i, w in enumerate(chunk):
                s_cs, e_cs = int(round(w["start"] * 100)), int(round(w["end"] * 100))
                if s_cs > pos:
                    parts.append(f"{{\\k{s_cs - pos}}}")
                    pos = s_cs
                d = max(e_cs - pos, 1)
                parts.append(f"{{\\kf{d}}}{disp(w['word'])}" + (" " if i + 1 < len(chunk) else ""))
                pos += d
            text = "".join(parts)
            lines.append(f"Dialogue: 0,{ass_time(cs)},{ass_time(ce)},Kang,,0,0,0,,{text}")
            events.append({"start": cs, "end": ce, "text": " ".join(w["word"] for w in chunk), "words": chunk})
        else:  # Option B: per-word events with scale pop
            for i, w in enumerate(chunk):
                ws = w["start"] if i else cs
                we = chunk[i + 1]["start"] if i + 1 < len(chunk) else ce
                if we <= ws:
                    continue
                segs = []
                for j, x in enumerate(chunk):
                    t = disp(x["word"])
                    if j == i:
                        segs.append(f"{{\\c{primary}\\fscx100\\fscy100\\t(0,80,\\fscx108\\fscy108)\\t(80,160,\\fscx104\\fscy104)}}{t}{{\\c{secondary}\\fscx100\\fscy100}}")
                    else:
                        segs.append(t)
                lines.append(f"Dialogue: 0,{ass_time(ws)},{ass_time(we)},Kang,,0,0,0,,{' '.join(segs)}")
            events.append({"start": cs, "end": ce, "text": " ".join(w["word"] for w in chunk), "words": chunk})
    return header + "\n".join(lines) + "\n", events


# --------------------------------------------------------------------------- SRT
def srt_time(t: float) -> str:
    ms = int(round(max(t, 0) * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def build_srt(events: List[Dict[str, Any]]) -> str:
    return "\n".join(f"{i}\n{srt_time(e['start'])} --> {srt_time(e['end'])}\n{e['text']}\n"
                     for i, e in enumerate(events, 1))


# --------------------------------------------------------------------------- QA helpers
_DIALOGUE_RE = re.compile(r"^Dialogue: \d+,([\d:.]+),([\d:.]+),")
_KF_RE = re.compile(r"\{\\k(f?)(\d+)\}([^{]*)")


def parse_ass_time(s: str) -> float:
    h, m, rest = s.split(":")
    return int(h) * 3600 + int(m) * 60 + float(rest)


def ass_word_onsets(ass_text: str) -> List[Tuple[str, float]]:
    """Recover (word, onset seconds) from Option-A \\kf karaoke events."""
    out: List[Tuple[str, float]] = []
    for line in ass_text.splitlines():
        m = _DIALOGUE_RE.match(line)
        if not m:
            continue
        t = parse_ass_time(m.group(1))
        body = line.split(",", 9)[9]
        for kf, cs, word in _KF_RE.findall(body):
            if kf == "f" and word.strip():
                out.append((word.strip(), round(t, 3)))
            t += int(cs) / 100.0
    return out


def ass_events(ass_text: str) -> List[Tuple[float, float]]:
    ev = []
    for line in ass_text.splitlines():
        m = _DIALOGUE_RE.match(line)
        if m:
            ev.append((parse_ass_time(m.group(1)), parse_ass_time(m.group(2))))
    return ev
