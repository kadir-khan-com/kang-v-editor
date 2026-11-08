"""Picture desk (Creative Office milestone 2, planner side) - rule-based, deterministic.

Input : a visuals_beats CSV (v17b: one row per narration beat, consecutive rows on the same asset = one shot,
        exactly as core.beats.merge_clips builds the timeline).
Output: a new visuals_beats CSV (for the next package) + a plan (JSON + CSV) where EVERY decision carries a rule id
        and a plain reason. Nothing is rendered here; beat markers still come from beats_lead.json (unchanged), only
        shot boundaries / motions move.

Rules (ids are the creative rulebook ids in config/creative_rulebook_kang.json; PD-* = desk mechanics):
  G-004  narrated still holds 3-10 s. A still shot < 3 s first borrows time from a same-scene neighbour by moving
         the cut to another word onset - 0.2 s (the lead rule, frame aligned); the donor keeps its own floor
         (still 3 s, video 2.5 s); cards / maps / teaser never donate (word-timed); an AI motion clip may donate down to 3 s.
         If no cut works the short still is MERGED into its neighbour still (neighbour's asset runs on over it,
         role desk_hold, combined <= 8 s). Otherwise WARN (unresolved).
  G-008  parallax is a spice: never two different parallax shots back to back (later one -> Ken Burns zoom).
         A continued_with_motion hold on the SAME photo is one shot (merge) - kept as long as its parallax clip
         covers the whole shot, else -> zoom (PD-PXLEN).
  Q-006  accent budget: accents (parallax / AI motion shots) at most ~1 per 3 cuts, i.e. >= 3 shots apart.
         Priority: AI motion (fixed, never removed), scene openers, exact over representative, earlier first.
         An accent over budget -> Ken Burns zoom.
         Among valid cuts the smallest shift wins unless it leaves 3 shots of ~equal length (Q-002, +-0.25 s).
  G-006  no 3 identical camera moves in a row (zoom_in / zoom_out / parallax). The CSV move is kept unless it
         makes a 3rd in a row (then flipped); shots that lost parallax get the opposite of the previous still move.
  PD-PXLEN a parallax clip shorter than its (new) shot -> Ken Burns zoom of the same photo.

The package honours the desk's move via the `desk_motion` column (core.beats_package._clips); old CSVs without
that column keep the old alternating motion_for().
"""
from __future__ import annotations

import csv
import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parent.parent
FPS = 25
STILL_MOVES = ("zoom_in", "zoom_out", "parallax_2_5d")
STILL_MIN, STILL_MAX, MERGE_MAX = 3.0, 10.0, 8.0
VIDEO_MIN = 2.5
LEAD_S = 0.2
ROW_MIN = 0.4          # a donor row keeps at least this much (rows = beats; none disappears by a cut shift)
ACCENT_GAP = 3         # accents >= 3 shots apart (~1 of every 3 cuts)
ASSET_COLS = ("asset", "source_dir", "asset_source", "match", "v9_shot", "licence", "title", "source_page",
              "parallax_clip", "parallax_dir", "parallax_status", "reuse", "reuse_of", "crop_box",
              "ai_motion_clip", "ai_motion_dir", "ai_motion_status", "ai_motion_model")
DESK_COLS = ("desk_motion", "desk_rule", "desk_note")


# ------------------------------------------------------------------ io ----
def read_rows(path: str | Path) -> Tuple[List[str], List[Dict[str, Any]]]:
    with open(path, encoding="utf-8-sig", newline="") as fh:
        rd = csv.DictReader(fh)
        fields = list(rd.fieldnames or [])
        rows = [dict(r) for r in rd]
    for r in rows:
        r["start"], r["end"] = float(r["start"]), float(r["end"])
    return fields, rows


def write_rows(path: str | Path, fields: Sequence[str], rows: Sequence[Dict[str, Any]]) -> None:
    fl = list(fields) + [c for c in DESK_COLS if c not in fields]
    for r in rows:
        for k in r:
            if k not in fl and not k.startswith("_"):
                fl.append(k)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fl, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            o = dict(r)
            o["start"], o["end"] = f"{r['start']:.3f}", f"{r['end']:.3f}"
            o["duration_s"] = f"{r['end'] - r['start']:.2f}"
            w.writerow(o)


def load_onsets(words_path: Optional[str | Path]) -> List[float]:
    if not words_path:
        return []
    d = json.loads(Path(words_path).read_text(encoding="utf-8"))
    ws = d["words"] if isinstance(d, dict) else d
    return sorted(float(w["start"]) for w in ws)


def fa(t: float) -> float:
    """Frame aligned (25 fps)."""
    return round(round(t * FPS) / FPS, 3)


def probe_duration(p: Path) -> Optional[float]:
    if not p.is_file():
        return None
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    try:
        return float(r.stdout.strip())
    except ValueError:
        return None


# --------------------------------------------------------------- shots ----
def kind_of(r: Dict[str, Any]) -> str:
    if r.get("role") == "teaser":
        return "teaser"
    if r.get("match") in ("text_card", "map"):
        return "graphic"
    if r.get("motion") == "ai_animated" or r.get("ai_motion_clip"):
        return "ai"
    if r.get("motion") in STILL_MOVES:
        return "still"
    return "video"


def shots_of(rows: Sequence[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Consecutive rows on the same asset = one shot (same as core.beats.merge_clips)."""
    out: List[Dict[str, Any]] = []
    for i, r in enumerate(rows):
        if out and rows[out[-1]["idx"][-1]]["asset"] == r["asset"]:
            out[-1]["idx"].append(i)
            out[-1]["end"] = r["end"]
            continue
        out.append({"idx": [i], "start": r["start"], "end": r["end"], "asset": r["asset"], "kind": kind_of(r),
                    "scene": r.get("scene", ""), "match": r.get("match", "")})
    prev_scene = None
    for s in out:
        s["dur"] = round(s["end"] - s["start"], 3)
        s["opener"] = s["scene"] != prev_scene
        prev_scene = s["scene"]
        r0 = rows[s["idx"][0]]
        s["move"] = r0.get("desk_motion") or r0.get("motion", "")
        s["parallax"] = bool(r0.get("parallax_clip")) and s["kind"] == "still"
        s["beats"] = [rows[i]["beat"] for i in s["idx"]]
    return out


def px_len(r: Dict[str, Any], cache: Dict[str, Optional[float]]) -> Optional[float]:
    if not r.get("parallax_clip"):
        return None
    p = Path(r.get("parallax_dir", ""))
    p = (p if p.is_absolute() else ROOT / p) / r["parallax_clip"]
    key = str(p)
    if key not in cache:
        cache[key] = probe_duration(p)
    return cache[key]


# ---------------------------------------------------------------- plan ----
class Desk:
    def __init__(self, rows: List[Dict[str, Any]], onsets: Sequence[float], px_cache: Optional[Dict] = None):
        self.rows = rows
        self.onsets = list(onsets)
        self.px_cache: Dict[str, Optional[float]] = px_cache if px_cache is not None else {}
        self.decisions: List[Dict[str, Any]] = []

    def log(self, rule: str, beats: Sequence[str], action: str, reason: str, **kw: Any) -> None:
        self.decisions.append({"n": len(self.decisions) + 1, "rule": rule, "beats": list(beats), "action": action,
                               "reason": reason, **kw})
        for b in beats:
            for r in self.rows:
                if r["beat"] == b:
                    r["desk_rule"] = ";".join(filter(None, [r.get("desk_rule", ""), rule]))
                    r["desk_note"] = " | ".join(filter(None, [r.get("desk_note", ""), action]))

    # -- helpers
    def shots(self) -> List[Dict[str, Any]]:
        return shots_of(self.rows)

    def to_zoom(self, shot: Dict[str, Any], rule: str, reason: str, move: Optional[str] = None) -> None:
        for i in shot["idx"]:
            r = self.rows[i]
            r["_was_parallax"] = r.get("parallax_clip", "")
            r["parallax_clip"] = r["parallax_dir"] = r["parallax_status"] = ""
            r["motion"] = move or "zoom_in"
            r["desk_motion"] = r["motion"]
        self.log(rule, shot["beats"], f"parallax -> Ken Burns {move or 'zoom_in'}", reason)

    def floor(self, shot: Dict[str, Any]) -> Optional[float]:
        if shot["kind"] == "still":
            return STILL_MIN
        if shot["kind"] == "video":
            return VIDEO_MIN
        if shot["kind"] == "ai":
            return STILL_MIN  # AI motion clip plays from its start; only its length changes
        return None  # graphic (word-timed) / teaser never donate

    def cut_candidates(self, lo: float, hi: float) -> List[float]:
        """Lead-rule cut points (word onset - 0.2 s, frame aligned) strictly inside (lo, hi)."""
        out = sorted({fa(o - LEAD_S) for o in self.onsets if lo < fa(o - LEAD_S) < hi})
        return out

    # -- G-008 holds (same photo, continued_with_motion after parallax) = one shot
    def g008_holds(self) -> None:
        for s in self.shots():
            if s["kind"] != "still" or len(s["idx"]) < 2 or not s["parallax"]:
                continue
            roles = [self.rows[i].get("role") for i in s["idx"][1:]]
            if "continued_with_motion" not in roles:
                continue
            L = px_len(self.rows[s["idx"][0]], self.px_cache)
            if L is not None and L + 1e-6 >= s["dur"]:
                self.log("G-008", s["beats"], "merge (one shot, one parallax clip)",
                         f"continued_with_motion hold on the same photo = one {s['dur']:.2f} s shot; its parallax clip "
                         f"({L:.2f} s) covers it, so there is no second parallax back to back", parallax_len=L)
            else:
                self.to_zoom(s, "G-008", f"same-photo hold of {s['dur']:.2f} s longer than its parallax clip ({L}) -> zoom")

    # -- G-004 short stills
    def g004(self) -> None:
        guard = 0
        while guard < 500:
            guard += 1
            sh = self.shots()
            target = next((k for k, s in enumerate(sh) if s["kind"] == "still" and s["dur"] < STILL_MIN - 1e-6
                           and not any(self.rows[i].get("_g004_warn") for i in s["idx"])), None)
            if target is None:
                return
            if not self._shift(sh, target) and not self._merge(sh, target):
                s = sh[target]
                for i in s["idx"]:
                    self.rows[i]["_g004_warn"] = True
                self.log("G-004", s["beats"], "WARN unresolved",
                         f"still {s['dur']:.2f} s < 3 s: no same-scene donor can give time on a lead-rule cut and no "
                         f"neighbour still to merge into within {MERGE_MAX:g} s", status="WARN")

    @staticmethod
    def _q002_hit(durs: List[float], touched: Sequence[int]) -> bool:
        """Q-002: three consecutive shots within +-0.25 s of each other, touching a changed shot."""
        for i in range(2, len(durs)):
            if not any(j in touched for j in (i - 2, i - 1, i)):
                continue
            if abs(durs[i] - durs[i - 1]) < 0.25 and abs(durs[i - 1] - durs[i - 2]) < 0.25:
                return True
        return False

    def _shift(self, sh: List[Dict[str, Any]], k: int) -> bool:
        s = sh[k]
        opts = []
        # left donor: move the start earlier
        if k > 0:
            L = sh[k - 1]
            fl = self.floor(L)
            last = self.rows[L["idx"][-1]]
            if fl is not None and last.get("scene") == self.rows[s["idx"][0]].get("scene"):
                lo = max(L["start"] + fl, last["start"] + ROW_MIN) - 1e-6
                hi = s["end"] - STILL_MIN + 1e-6
                for t in self.cut_candidates(lo, s["start"]):
                    if t <= hi:
                        opts.append((round(s["start"] - t, 3), 0 if L["kind"] == "still" else 1, "left", t, L, k - 1))
        if k + 1 < len(sh):
            R = sh[k + 1]
            fl = self.floor(R)
            first = self.rows[R["idx"][0]]
            if fl is not None and first.get("scene") == self.rows[s["idx"][-1]].get("scene"):
                hi = min(R["end"] - fl, first["end"] - ROW_MIN) + 1e-6
                for t in self.cut_candidates(s["end"], hi):
                    if t >= s["start"] + STILL_MIN - 1e-6 and t - s["start"] <= STILL_MAX:
                        opts.append((round(t - s["end"], 3), 0 if R["kind"] == "still" else 1, "right", t, R, k + 1))
        if not opts:
            return False
        opts.sort(key=lambda o: (o[0], o[1], 0 if o[2] == "right" else 1, o[3]))
        base = [x["dur"] for x in sh]

        def durs_after(o):
            d = list(base)
            d[k] = round(d[k] + o[0], 3)
            d[o[5]] = round(d[o[5]] - o[0], 3)
            return d
        clean = [o for o in opts if not self._q002_hit(durs_after(o), (k, o[5]))]
        pick = clean[0] if clean else opts[0]
        shift, _, side, t, D, _j = pick
        before = (s["start"], s["end"], D["start"], D["end"])
        if side == "left":
            self.rows[D["idx"][-1]]["end"] = t
            self.rows[s["idx"][0]]["start"] = t
        else:
            self.rows[s["idx"][-1]]["end"] = t
            self.rows[D["idx"][0]]["start"] = t
        new_dur = round(s["dur"] + shift, 3)
        why = f"still under 3 s; new cut = a word onset - {LEAD_S} s (lead rule), donor keeps >= its floor, same scene"
        if clean and pick is not opts[0]:
            why += f"; smallest shift ({opts[0][0]:.2f} s) skipped: it made 3 shots of ~equal length (Q-002)"
        if not clean:
            why += "; WARN every possible cut leaves 3 ~equal shot lengths (Q-002)"
        self.log("G-004", (s["beats"] + D["beats"][:1]) if side == "right" else (D["beats"][-1:] + s["beats"]),
                 f"cut moved {side} by {shift:.2f} s to {t:.3f} (still {s['dur']:.2f} -> {new_dur:.2f} s; "
                 f"{D['kind']} {D['asset'][:28]} {D['dur']:.2f} -> {D['dur'] - shift:.2f} s)", why,
                 before=list(before), cut_at=t, **({} if clean else {"status": "WARN"}))
        self._check_px_len_after(s["idx"])
        return True

    def _merge(self, sh: List[Dict[str, Any]], k: int) -> bool:
        s = sh[k]
        cands = []
        for j in (k - 1, k + 1):
            if 0 <= j < len(sh):
                N = sh[j]
                if N["kind"] != "still" or N["scene"] != s["scene"]:
                    continue
                if N["dur"] + s["dur"] > MERGE_MAX + 1e-6:
                    continue
                cands.append((0 if N["match"] == "exact" else 1, N["dur"] + s["dur"], j, N))
        if not cands:
            return False
        cands.sort(key=lambda c: (c[0], c[1], c[2]))
        _, tot, j, N = cands[0]
        src = self.rows[N["idx"][0]]
        dropped = s["asset"]
        for i in s["idx"]:
            r = self.rows[i]
            for c in ASSET_COLS:
                if c in src:
                    r[c] = src[c]
            r["motion"] = src.get("motion", "")
            r["desk_motion"] = src.get("desk_motion", "")
            r["role"] = "desk_hold"
        self.log("G-004", N["beats"] + s["beats"],
                 f"merge: {N['asset'][:30]} runs on over {', '.join(s['beats'])} ({tot:.2f} s); dropped {dropped[:30]}",
                 "still under 3 s and no lead-rule cut shift possible; neighbour still (same scene) takes the beat",
                 dropped_asset=dropped)
        newshot = next(x for x in self.shots() if s["idx"][0] in x["idx"])
        self._check_px_len_after(newshot["idx"])
        return True

    def _check_px_len_after(self, idx: Sequence[int]) -> None:
        s = next(x for x in self.shots() if idx[0] in x["idx"])
        if not s["parallax"]:
            return
        L = px_len(self.rows[s["idx"][0]], self.px_cache)
        if L is None or L + 1e-6 < s["dur"]:
            self.to_zoom(s, "PD-PXLEN", f"shot is now {s['dur']:.2f} s, parallax clip {L} s -> same photo as Ken Burns")

    # -- G-008 different-photo parallax back to back
    def g008_pairs(self) -> None:
        sh = self.shots()
        for a, b in zip(sh, sh[1:]):
            if a["parallax"] and b["parallax"]:
                loser = a if (b["opener"] and not a["opener"]) else b
                self.to_zoom(loser, "G-008", "two different parallax shots back to back")
                return self.g008_pairs()

    # -- Q-006 accent budget
    def q006(self) -> None:
        sh = [s for s in self.shots() if s["kind"] != "teaser"]
        acc = [k for k, s in enumerate(sh) if s["parallax"] or s["kind"] == "ai"]

        def prio(k: int) -> tuple:
            s = sh[k]
            return (0 if s["kind"] == "ai" else 1, 0 if s["opener"] else 1, 0 if s["match"] == "exact" else 1, k)
        kept: List[int] = []
        for k in sorted(acc, key=prio):
            if sh[k]["kind"] == "ai" or all(abs(k - j) >= ACCENT_GAP for j in kept):
                kept.append(k)
            else:
                near = min(kept, key=lambda j: abs(k - j))
                self.to_zoom(sh[k], "Q-006", f"accent budget: another accent ({sh[near]['beats'][0]}) only "
                             f"{abs(k - near)} shot(s) away (need >= {ACCENT_GAP}); kept one has higher priority "
                             "(AI > scene opener > exact > earlier)")
        self.accents_kept = sorted(sh[k]["beats"][0] for k in kept)

    # -- G-006 moves
    def g006(self) -> None:
        sh = self.shots()
        prev: List[str] = []   # moves of the current run of adjacent still shots
        for s in sh:
            if s["kind"] != "still":
                prev = []
                continue
            r0 = self.rows[s["idx"][0]]
            mv = "parallax_2_5d" if s["parallax"] else (r0.get("motion") if r0.get("motion") in ("zoom_in", "zoom_out")
                                                          else "zoom_in")
            if not s["parallax"] and r0.get("_was_parallax") and prev:
                want = "zoom_out" if prev[-1] == "zoom_in" else "zoom_in"
                mv = want
            if len(prev) >= 2 and prev[-1] == prev[-2] == mv:
                if s["parallax"]:   # cannot flip a parallax by move; turn it into the other zoom
                    new = "zoom_out" if prev[-1] == "zoom_in" else "zoom_in"
                    self.to_zoom(s, "G-006", f"3rd '{mv}' in a row", move=new)
                    mv = new
                else:
                    new = "zoom_out" if mv == "zoom_in" else "zoom_in"
                    self.log("G-006", s["beats"], f"move {mv} -> {new}", f"would be the 3rd identical move ('{mv}') in a row")
                    mv = new
            if not s["parallax"]:
                for i in s["idx"]:
                    self.rows[i]["motion"] = mv
                    self.rows[i]["desk_motion"] = mv
            prev.append(mv)

    def run(self) -> None:
        self.g008_holds()
        self.g004()
        self.g008_pairs()
        self.q006()
        self.g006()


# -------------------------------------------------------------- checks ----
def measure(rows: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """Shot-level numbers for the rules the desk enforces (teaser exempt)."""
    sh = [s for s in shots_of(rows) if s["kind"] != "teaser"]
    short = [s["beats"][0] for s in sh if s["kind"] == "still" and not STILL_MIN - 1e-6 <= s["dur"] <= STILL_MAX]
    px_pairs = [b["beats"][0] for a, b in zip(sh, sh[1:]) if a["parallax"] and b["parallax"]]
    same3, run, last = [], 0, None
    for s in sh:
        mv = ("parallax_2_5d" if s["parallax"] else s["move"]) if s["kind"] == "still" else None
        run = run + 1 if (mv and mv == last) else (1 if mv else 0)
        last = mv
        if run == 3:
            same3.append(s["beats"][0])
    acc = [k for k, s in enumerate(sh) if s["parallax"] or s["kind"] == "ai"]
    close = [sh[b]["beats"][0] for a, b in zip(acc, acc[1:]) if b - a < ACCENT_GAP]
    d = [x["dur"] for x in sh]
    q002 = [sh[i]["beats"][0] for i in range(2, len(d)) if abs(d[i] - d[i - 1]) < 0.25 and abs(d[i - 1] - d[i - 2]) < 0.25]
    return {"shots": len(sh), "stills_outside_3_10s": short, "three_equal_lengths": q002, "parallax_back_to_back": px_pairs,
            "three_same_moves": same3, "accents": len(acc), "accents_closer_than_3": close,
            "parallax_shots": sum(1 for s in sh if s["parallax"])}


def plan(rows: List[Dict[str, Any]], onsets: Sequence[float], px_cache: Optional[Dict] = None) -> Dict[str, Any]:
    before = measure(rows)
    d = Desk(rows, onsets, px_cache)
    d.run()
    for r in rows:
        if kind_of(r) == "still" and not r.get("desk_motion"):
            r["desk_motion"] = "parallax_2_5d" if r.get("parallax_clip") else r.get("motion", "")
    after = measure(rows)
    return {"decisions": d.decisions, "before": before, "after": after,
            "accents_kept": getattr(d, "accents_kept", [])}


def plan_cmd(visuals_csv: str, out: str, *, words: Optional[str] = None, run_id: Optional[str] = None) -> Dict[str, Any]:
    """kang.py plan-pictures VISUALS --out PREFIX [--words words.json]"""
    from .runs import Run, write_json
    rn = Run(run_id)
    rn.add_input(visuals_csv, "VISUALS_BEATS")
    if words is None:
        words = str(ROOT / "runs" / "2026-10-31_KANG_004" / "words.json")
    rn.add_input(words, "WORDS")
    fields, rows = read_rows(visuals_csv)
    res = plan(rows, load_onsets(words))
    prefix = Path(out).name
    vpath = rn.path(f"{prefix}.csv")
    write_rows(vpath, fields, rows)
    rn.add_output(vpath, "visuals_beats")
    jpath = rn.path(f"{prefix}_plan.json")
    write_json(jpath, {"source": str(visuals_csv), "rules": ["G-004", "G-008", "Q-006", "G-006", "PD-PXLEN"], **res})
    rn.add_output(jpath, "picture_plan")
    cpath = rn.path(f"{prefix}_plan.csv")
    with open(cpath, "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["n", "rule", "beats", "action", "reason", "status"])
        for x in res["decisions"]:
            w.writerow([x["n"], x["rule"], " ".join(x["beats"]), x["action"], x["reason"], x.get("status", "DONE")])
    rn.add_output(cpath, "picture_plan_csv")
    by_rule: Dict[str, int] = {}
    for x in res["decisions"]:
        by_rule[x["rule"]] = by_rule.get(x["rule"], 0) + 1
    rn.log_step("plan-pictures", decisions=len(res["decisions"]), by_rule=by_rule, before=res["before"],
                after=res["after"])
    rn.set_status("done")
    return {"run": rn.run_id, "visuals_csv": str(vpath), "plan_json": str(jpath), "plan_csv": str(cpath),
            "decisions": len(res["decisions"]), "by_rule": by_rule, "before": res["before"], "after": res["after"]}
