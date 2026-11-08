"""v13 moving text cards and map clips: plan (values from narration, timing from beats, layout, safe zone) + render.

Card: navy gradient with slowly drifting glows (background drift), gold accent bar, lines slide in from the left
when the narration says them. v17b: every value appears already final (line fade/slide-in <= 0.3 s, a later value of
the same line pops in whole); no count-up unless a value opts in with "count_up": true in the spec AND it is the
only value of its line, a number >= 100 - then every in-between frame shows a rounded step (count_up_step) <= final. A card that holds a topic longer than ~8 s
has phases: lines of a phase leave at its end (kept lines - kicker/title - stay). Map: see core/map_route.py.

Plan is a pure function of (spec, beats, words) so it is unit-testable without rendering.
"""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from . import motion_draw as D
from . import narration_values as NV

ROOT = Path(__file__).resolve().parent.parent
SPEC = ROOT / "config" / "motion_cards.json"
W, H, FPS = 1920, 1080, 25
ROLE = {"kicker": ("body", 44, D.BLUE), "title": ("title", 98, D.WHITE), "big": ("number", 150, D.GOLD),
        "value": ("number", 88, D.GOLD), "text": ("body", 72, D.WHITE), "small": ("body", 52, D.SOFT)}
GAP = {"kicker": 10, "title": 18, "big": 14, "value": 16, "text": 14, "small": 12}
X0 = 170            # text block left edge
ENTER_S, EXIT_S, COUNT_S = 0.5, 0.3, 0.9
VALUE_ENTER_S = 0.3  # v17b: a line that carries a value fades/slides in within 0.3 s (values never count)
NUM_RE = re.compile(r"\d[\d,]*(?:\.\d+)?(?::\d\d)?")
NAME_WINDOW_S = 20.0
MAX_LEAD_S = 0.25   # v13b: no value / label earlier than 0.25 s before its spoken word start (was 2.0 s WARN)
LEAD_S = 0.2        # target lead


def load_spec(path: Optional[str | Path] = None) -> Dict[str, Any]:
    return json.loads(Path(path or SPEC).read_text(encoding="utf-8"))


def _norm(s: str) -> str:
    return " " + re.sub(r"[^a-z0-9]+", " ", s.lower()).strip() + " "


def place_aliases() -> Dict[str, List[str]]:
    rules = json.loads((ROOT / "config" / "beat_rules.json").read_text(encoding="utf-8"))
    skip = {"sunset", "beach", "sgdhp exhibits", "excavation", "lighthouse"}
    al = {k: v for k, v in rules["places"].items() if k not in skip}
    al["dwarka"] = ["dwarka", "dwarika", "dwaraka"]
    al["gujarat"] = ["gujarat"]
    al["mathura"] = ["mathura"]
    return al


CURRENCY_WORDS = {"रुपये", "रुपए", "रुपया", "बजट", "rupaye", "rupe", "budget"}


def static_checks(text: str, words, hw, t0: float, t1: float, currency_id: Optional[int] = None) -> Tuple[str, str]:
    """-> (status, note). Static text: no digits; the rupee sign only when a spoken currency word (rupaye / budget)
    is named by currency_id; a place name in it must be spoken near the clip."""
    if re.search(r"[0-9]", text):
        return "FAIL", f"static text '{text}' contains a number - numbers must come from word ids"
    if "₹" in text:
        cw = {re.sub(r"[,।.]+$", "", words[currency_id]["word"]), hw[currency_id]["hinglish"].lower().strip(",.")} \
            if currency_id is not None else set()
        if not cw & CURRENCY_WORDS:
            return "FAIL", f"'₹' in '{text}' needs currency_id pointing at a spoken 'rupaye'/'budget' word"
    spoken = _norm(" ".join(w["hinglish"] for w in hw if t0 - NAME_WINDOW_S <= w["start"] < t1))
    for key, al in place_aliases().items():
        hit = [a for a in al if _norm(a) in _norm(text)]
        if hit and not any(_norm(a) in spoken for a in al):
            return "WARN", f"place '{hit[0]}' in static text is not spoken within {NAME_WINDOW_S:g} s before/during the clip"
    return "PASS", ""


def _beat_span(ids: Sequence[str], beats: Dict[str, Dict[str, Any]]) -> Tuple[float, float]:
    bs = [beats[b] for b in ids]
    for a, b in zip(bs, bs[1:]):
        if abs(float(a["end"]) - float(b["start"])) > 1e-6:
            raise ValueError(f"beats {ids} are not contiguous")
    return float(bs[0]["start"]), float(bs[-1]["end"])


def _reveal(at: Optional[int], k: int, p0: float, p1: float, words) -> Tuple[float, Optional[float]]:
    lo = p0 + 0.15 + 0.12 * k
    if at is None:
        return lo, None
    wt = float(words[at]["start"])
    return max(lo, wt - LEAD_S), wt  # v13b: no clamp to p1 - 1.2 s (that showed values up to 1.75 s early)


def value_reveals(vals: Sequence[Dict[str, Any]], line_reveal: float) -> List[float]:
    """v13b: each value of a line appears at its own spoken time - LEAD_S (never before the line itself)."""
    out = []
    for v in vals:
        t = v.get("time")
        out.append(round(max(line_reveal, float(t) - LEAD_S), 3) if v.get("status") == "PASS" and t not in (None, "") else line_reveal)
    return out


def fit_size(text: str, role: str, max_w: int) -> Tuple[int, bool]:
    kind, size, _ = ROLE[role]
    s = size
    while s >= int(size * 0.6):
        if D.text_size(text, kind, s)[0] <= max_w:
            return s, True
        s -= 2
    return s, False


# --------------------------------------------------------------------------- plan
def plan_card(spec: Dict[str, Any], beats: Dict[str, Dict[str, Any]], words, hw, safe: Dict[str, int]) -> Dict[str, Any]:
    phases, rows, problems = [], [], []
    all_beats = [b for p in spec["phases"] for b in p["beats"]]
    c0, c1 = _beat_span(all_beats, beats)
    kept: List[Dict[str, Any]] = []
    max_w = safe["right_px"] - X0
    for pi, ph in enumerate(spec["phases"]):
        p0, p1 = _beat_span(ph["beats"], beats)
        lines = []
        for k, ln in enumerate(ph["lines"]):
            fmt = ln["fmt"]
            vals = [NV.read_value(v, words, hw) for v in ln.get("values", [])]
            for v, sv in zip(vals, ln.get("values", [])):
                v["count_up"] = bool(sv.get("count_up"))
            st, note = static_checks(re.sub(r"\{\d+\}", "", fmt), words, hw, c0, c1, ln.get("currency_id"))
            if "₹" in fmt and st == "PASS":
                note = f"₹ from spoken word {ln['currency_id']} '{hw[ln['currency_id']]['hinglish']}'"
            bad = [v for v in vals if v["status"] != "PASS"]
            reveal, wt = _reveal(ln.get("at"), k, p0, p1, words)
            lead = round(wt - reveal, 3) if wt is not None else None
            vrev = value_reveals(vals, reveal)
            status = "FAIL" if st == "FAIL" else ("WARN" if (st == "WARN" or bad) else "PASS")
            if status == "PASS" and max(vrev + [reveal]) > p1 - 0.3:
                status = "WARN"
                note = (f"spoken after the {'clip' if pi == len(spec['phases']) - 1 else 'phase'} ends ({p1:.2f} s): "
                        f"not shown (inside the clip it would be more than {MAX_LEAD_S} s early)")
            final = NV.fill(fmt, vals) if not bad else ""
            if ln["role"] == "kicker":
                final = final.upper()
            line = {"role": ln["role"], "fmt": fmt, "vals": vals, "text": final, "reveal": reveal, "keep": bool(ln.get("keep")),
                    "status": status, "phase": pi, "vreveal": vrev}
            if status == "PASS":
                size, ok = fit_size(final, ln["role"], max_w)
                line["size"] = size
                if not ok:
                    line["status"] = "FAIL"
                    problems.append(f"{spec['id']}: '{final}' does not fit {max_w} px even at 60 %")
            for vi, v in enumerate(vals or [None]):
                shown_at = vrev[vi] if v is not None else reveal
                rows.append({"clip": spec["id"], "type": "text_card", "phase": pi + 1, "item": ln["role"], "shown_text": final or fmt,
                             "value": "" if v is None else v.get("display", ""), "word_ids": "" if v is None else "+".join(map(str, v["word_ids"])),
                             "hindi": "" if v is None else v.get("hindi", ""), "hinglish": "" if v is None else v.get("hinglish", ""),
                             "word_time": "" if v is None else v.get("time", ""), "shown_at": round(shown_at, 3),
                             "display_lead_s": "" if lead is None else lead, "status": line["status"],
                             "note": "; ".join(x for x in ([note] if note else []) + ([v.get("note", "")] if v and v.get("note") else []) if x)
                             or ("editorial text (no number)" if v is None else "")})
                if line["status"] == "WARN":
                    rows[-1]["status"] = "WARN"
                lead_check(rows[-1])
            if line["status"] == "FAIL" and st == "FAIL":
                problems.append(f"{spec['id']}: {note}")
            if line["status"] == "PASS":
                lines.append(line)
        visible = kept + lines
        phases.append({"start": p0, "end": p1, "beats": ph["beats"], "lines": lines, "visible": visible})
        kept = kept + [l for l in lines if l["keep"]]
    # layout: same top for the whole clip (kept lines never jump), centred on the tallest phase
    def block_h(vis, scale=1.0):
        return sum(int(l["size"] * scale * 1.18) + GAP[l["role"]] for l in vis)
    tall = max((block_h(p["visible"]) for p in phases), default=0)
    avail = safe["bottom_px"] - 150
    scale = min(1.0, avail / tall) if tall else 1.0
    if scale < 0.72:
        problems.append(f"{spec['id']}: text block {tall}px does not fit {avail}px")
    if scale < 1.0:
        for p in phases:
            for l in p["lines"]:
                l["size"] = int(l["size"] * scale)
    tall = max((block_h(p["visible"]) for p in phases), default=0)
    top = max(150, int((150 + safe["bottom_px"]) / 2 - tall / 2) - 20)
    for p in phases:
        y = top
        for l in p["visible"]:
            if "y" not in l:
                l["y"] = y
            y = l["y"] + int(l["size"] * 1.18) + GAP[l["role"]]
        p["bottom"] = y
    durs = [p["end"] - p["start"] for p in phases]
    long_phase = [round(d, 2) for d in durs if d > 8.5]
    if long_phase:
        problems.append(f"{spec['id']}: phase longer than 8.5 s {long_phase} (add a phase)")
    return {"id": spec["id"], "type": "text_card", "start": c0, "end": c1, "beats": all_beats, "phases": phases, "rows": rows,
            "problems": problems, "frames": round(c1 * FPS) - round(c0 * FPS), "replaces_card": spec.get("replaces_card"),
            "seed": int(hashlib.sha256(spec["id"].encode()).hexdigest()[:6], 16)}


def lead_check(row: Dict[str, Any]) -> Dict[str, Any]:
    from .map_route import lead_check as _lc
    return _lc(row)


def card_boxes(plan: Dict[str, Any]) -> List[Tuple[str, Tuple[int, int, int, int]]]:
    """Final (fully revealed) box of every line, for the safe-zone / overflow check."""
    out = []
    for p in plan["phases"]:
        for l in p["visible"]:
            kind = ROLE[l["role"]][0]
            w, h = D.text_size(l["text"], kind, l["size"])
            out.append((l["text"], (X0, l["y"], X0 + w, l["y"] + int(l["size"] * 1.18))))
    return out


# --------------------------------------------------------------------------- render
def count_up_allowed(l: Dict[str, Any], i: int) -> bool:
    """v17b: count-up only when the spec opts in for this value AND it is the line's only value, a number >= 100."""
    vals = l["vals"]
    v = vals[i]
    return bool(v.get("count_up")) and len(vals) == 1 and v.get("kind") == "number" and float(v.get("value", 0)) >= 100


def count_up_step(final: float) -> int:
    """Rounding step for an opted-in count-up: 2 significant digits (5,000 -> steps of 100; 135 -> 10)."""
    return max(1, 10 ** max(0, len(str(int(abs(final)))) - 2))


def _line_text(l: Dict[str, Any], T: float) -> str:
    """v13b: a value appears only from its own reveal time; until then the line is cut before its placeholder
    (left-aligned, so nothing jumps). v17b: values are always shown final (no count-up) unless count_up_allowed."""
    vals = l["vals"]
    if not vals:
        return l["text"]
    vrev = l.get("vreveal") or [l["reveal"]] * len(vals)
    fmt = l["fmt"]
    pending = [i for i, r in enumerate(vrev) if T < r]
    if pending:
        cut = min(fmt.index("{%d}" % i) for i in pending if "{%d}" % i in fmt)
        fmt = re.sub(r"[\s–\-·/,&+]+$", "", fmt[:cut])
        if not fmt.strip():
            return ""
    shown = []
    for i, v in enumerate(vals):
        if count_up_allowed(l, i) and T < vrev[i] + COUNT_S:
            step = count_up_step(float(v["value"]))
            x = float(v["value"]) * D.ease_out_cubic((T - vrev[i]) / COUNT_S)
            shown.append(dict(v, value=float(int(x // step) * step)))
        else:
            shown.append(v)
    txt = NV.fill(fmt, shown)
    return txt.upper() if l["role"] == "kicker" else txt


def enter_s(l: Dict[str, Any]) -> float:
    return VALUE_ENTER_S if l["vals"] else ENTER_S


def displayed_value_problems(plan: Dict[str, Any], fps: int = FPS) -> List[str]:
    """v17b QA: every frame of the card (render-plan level, same _line_text the renderer draws): each number shown
    must equal the number at the same position of the line's final text (a line may still be cut before a later
    value - then fewer numbers - but never a different one). Opted-in count-ups may show a rounded step <= final."""
    out = []
    n0 = round(plan["start"] * fps)
    for n in range(plan["frames"]):
        T = (n0 + n + 0.5) / fps
        ph = next((p for p in plan["phases"] if p["start"] - 1e-9 <= T < p["end"]), plan["phases"][-1])
        for l in ph["visible"]:
            if T < l["reveal"]:
                continue
            txt = _line_text(l, T)
            got, fin = NUM_RE.findall(txt), NUM_RE.findall(l["text"])
            ok = len(got) <= len(fin)
            for k, g in enumerate(got[:len(fin)]):
                if g == fin[k]:
                    continue
                cu = len(l["vals"]) == 1 and count_up_allowed(l, 0)
                gv, fv = float(g.replace(",", "")), float(fin[k].replace(",", ""))
                if not (cu and gv <= fv and gv % count_up_step(fv) == 0):
                    ok = False
            if not ok:
                out.append(f"{plan['id']}: frame {n} ({T:.2f} s) shows '{txt}' - final '{l['text']}'")
                break
        if len(out) >= 5:
            break
    return out


def card_frame(plan: Dict[str, Any], bg: D.DriftBackground, T: float) -> np.ndarray:
    f = bg.frame(T)
    ph = next((p for p in plan["phases"] if p["start"] - 1e-9 <= T < p["end"]), plan["phases"][-1])
    last = ph is plan["phases"][-1]
    vis = ph["visible"]
    if not vis:
        return f
    top = min(l["y"] for l in vis)
    shown = [l for l in vis if T >= l["reveal"]]
    bottom = max((l["y"] + int(l["size"] * 1.18) for l in shown), default=top + 10)
    grow = D.ease_out_cubic((T - plan["start"]) / 0.6)
    bar_h = max(8.0, (bottom - top) * grow)
    f[int(top + 6):int(top + 6 + bar_h), X0 - 46:X0 - 37] = np.array(D.GOLD, np.float32)
    for l in vis:
        if T < l["reveal"]:
            continue
        e = D.ease_out_cubic((T - l["reveal"]) / enter_s(l))
        a, dx = e, -60.0 * (1 - e)
        if not l["keep"] and not last and T > ph["end"] - EXIT_S:
            x = (ph["end"] - T) / EXIT_S
            a *= x
            dx += 40.0 * (1 - x)
        kind, _, col = ROLE[l["role"]]
        txt = _line_text(l, T)
        if not txt:
            continue
        spr = D.text_sprite(txt, kind, l["size"], col)
        pad = max(6, l["size"] // 10)
        D.blit(f, spr, X0 - pad + dx, l["y"] - pad, a)
    return f


def render_card(plan: Dict[str, Any], out: str | Path, fps: int = FPS) -> Dict[str, Any]:
    if plan["type"] != "text_card":
        raise ValueError("not a card plan")
    bg = D.DriftBackground(W, H, seed=plan["seed"])
    wr = D.FrameWriter(out, W, H, fps)
    n0 = round(plan["start"] * fps)
    try:
        for n in range(plan["frames"]):
            T = (n0 + n + 0.5) / fps
            wr.write(card_frame(plan, bg, T))
    finally:
        n = wr.close()
    return {"frames": n}


def phase_sample_times(plan: Dict[str, Any]) -> List[float]:
    """Moments for the review grid: just before the end of each phase (everything of that phase shown)."""
    return [round(max(p["start"] + 0.2, p["end"] - 0.25), 3) for p in plan["phases"]]
