"""v18 cold open: a VISUAL-ONLY teaser over the unchanged opening narration.

- No time is inserted and the narration / captions are untouched (dead air would fail R-400). The teaser covers
  0 .. T where T = (onset of words[end_word_index]) - 0.2 s, frame aligned (lead rule), so the next real shot lands
  on that word.
- 3-4 quick shots cut from clips already in the project (YouTube CC eye_exact clips, the gate-passed AI clip),
  each a NEW derived file TSR_*.mp4 (1920x1080, 25 fps, H.264, no audio) with a CREDITS.json in its folder that
  copies the source's credit record (+ what was modified).
- A Hinglish title overlay in the existing card style (navy gradient panel, gold accent bar, Mukta ExtraBold, own
  text) slides in at ~0.3 s and stays over every teaser shot -> first on-screen text < 1 s (R-112 <= 10 s).
- CSV: beats wholly inside the teaser leave (their stills drop off the timeline); the beat that straddles T keeps its
  narration beat but shows the NEXT shot's asset from T (role cold_open_hold, merges into that shot). Teaser rows:
  role 'teaser', reuse 'teaser', overlay_text = the title. The critic (core/creative.py) turns them into ONE hook
  beat (kind hook, tease=True, overlay) and exempts it from the still-hold rules (G-004 etc.).
"""
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from . import motion_draw as D
from . import picture_desk as PD

ROOT = Path(__file__).resolve().parent.parent
W, H, FPS = 1920, 1080, 25
SPEC = ROOT / "config" / "cold_open.json"
LEAD_S = 0.2
ASSET_COLS = PD.ASSET_COLS


def load_spec(path: Optional[str | Path] = None) -> Dict[str, Any]:
    return json.loads(Path(path or SPEC).read_text(encoding="utf-8"))


def teaser_end(spec: Dict[str, Any]) -> float:
    ws = json.loads((ROOT / spec["words"]).read_text(encoding="utf-8"))
    ws = ws["words"] if isinstance(ws, dict) else ws
    return PD.fa(float(ws[int(spec["end_word_index"])]["start"]) - LEAD_S)


# ------------------------------------------------------------- overlay ----
class TitleOverlay:
    """Card-style lower-left title panel (navy gradient, gold bar, kicker + title)."""

    def __init__(self, kicker: str, title: str, enter_at: float = 0.3, enter_s: float = 0.5):
        self.k = D.text_sprite(kicker, "body", 44, D.BLUE)
        self.t = D.text_sprite(title, "title", 98, D.WHITE)
        self.enter_at, self.enter_s = enter_at, enter_s
        pad_x, pad_y, gap = 64, 34, 4
        self.pw = int(max(self.k.shape[1], self.t.shape[1]) + 2 * pad_x)
        self.ph = int(self.k.shape[0] + gap + self.t.shape[0] + 2 * pad_y)
        self.x, self.y = 150, H - 230 - self.ph          # clear of bottom captions, inside 16:9 title safe
        g = D.gradient(self.pw, self.ph)
        m = D.pill_sprite(self.pw, self.ph, (0, 0, 0), alpha=0.84, radius=22)[..., 3:4]
        self.panel = np.concatenate([g, m], axis=2).astype(np.float32)
        self.pad_x, self.pad_y, self.gap = pad_x, pad_y, gap

    def progress(self, t: float) -> float:
        return D.ease_out_cubic((t - self.enter_at) / self.enter_s)

    def draw(self, f: np.ndarray, t: float) -> None:
        p = self.progress(t)
        if p <= 0:
            return
        dx = -40 * (1 - p)
        D.blit(f, self.panel, self.x + dx, self.y, alpha=p)
        bar_h = (self.ph - 2 * self.pad_y) * p
        bx = int(self.x + dx + 26)
        y0 = int(self.y + self.pad_y)
        f[y0:y0 + int(bar_h), max(0, bx):max(0, bx) + 9] = np.array(D.GOLD, np.float32)
        tx = self.x + dx + self.pad_x
        D.blit(f, self.k, tx, self.y + self.pad_y - 6, alpha=p)
        D.blit(f, self.t, tx, self.y + self.pad_y + self.k.shape[0] + self.gap - 10, alpha=p)


# --------------------------------------------------------------- render ----
def render_shot(src: Path, in_s: float, frames: int, t0: float, out: Path, overlay: TitleOverlay) -> Dict[str, Any]:
    """Section [in_s, in_s + frames/25) of src -> 1920x1080 25 fps cover-fit + overlay at global time t0 + k/25."""
    dec = subprocess.Popen(["ffmpeg", "-v", "error", "-ss", f"{in_s:.3f}", "-i", str(src), "-an", "-vf",
                            f"fps={FPS},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1,"
                            f"tpad=stop_mode=clone:stop_duration=2",
                            "-frames:v", str(frames), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                           stdout=subprocess.PIPE)
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                            "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
    n = 0
    sz = W * H * 3
    assert dec.stdout is not None and enc.stdin is not None
    while n < frames:
        buf = dec.stdout.read(sz)
        if len(buf) < sz:
            break
        f = np.frombuffer(buf, np.uint8).reshape(H, W, 3).astype(np.float32)
        overlay.draw(f, t0 + n / FPS)
        enc.stdin.write(np.clip(f + 0.5, 0, 255).astype(np.uint8).tobytes())
        n += 1
    dec.stdout.close(); dec.wait()
    enc.stdin.close(); enc.wait()
    if n != frames or enc.returncode != 0:
        raise RuntimeError(f"teaser shot {out.name}: {n}/{frames} frames, encoder rc {enc.returncode}")
    return {"frames": n}


def _credit_record(shot: Dict[str, Any], src: Path) -> Dict[str, Any]:
    if shot.get("credit_from"):
        d, f = shot["credit_from"]
    else:
        d, f = str(src.parent.relative_to(ROOT)), src.name
    recs = json.loads((ROOT / d / "CREDITS.json").read_text(encoding="utf-8"))
    rec = next(x for x in recs if x.get("file") == f)
    return dict(rec), f"{d}/{f}"


# ----------------------------------------------------------------- csv ----
def build_rows(rows: List[Dict[str, Any]], spec: Dict[str, Any], t_end: float, clip_dir_rel: str,
               credits: Dict[str, Dict[str, Any]], words: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    keep, dropped, straddle = [], [], None
    for r in rows:
        if r["end"] <= t_end + 1e-6:
            dropped.append(r)
        elif r["start"] < t_end - 1e-6:
            straddle = r
            keep.append(r)
        else:
            keep.append(r)
    info: Dict[str, Any] = {"dropped_beats": [r["beat"] for r in dropped],
                            "dropped_assets": sorted({r["asset"] for r in dropped})}
    if straddle is not None:
        nxt = keep[keep.index(straddle) + 1] if keep.index(straddle) + 1 < len(keep) else None
        info["straddle_beat"] = straddle["beat"]
        info["straddle_asset_dropped"] = straddle["asset"]
        if nxt is not None:
            for c in ASSET_COLS:
                if c in nxt:
                    straddle[c] = nxt[c]
            straddle["motion"] = nxt.get("motion", "")
            straddle["desk_motion"] = nxt.get("desk_motion", "")
            straddle["role"] = "cold_open_hold"
            straddle["start"] = t_end
            straddle["desk_rule"] = ";".join(filter(None, [straddle.get("desk_rule", ""), "HOOK"]))
            straddle["desk_note"] = f"cold open: from {t_end:.3f} s shows {nxt['beat']}'s shot (starts earlier)"
            info["next_shot_starts_at"] = t_end
            info["next_shot_beat"] = nxt["beat"]
    title = f"{spec['title']['kicker']} | {spec['title']['title']}"
    tz, t = [], 0.0
    for sh in spec["shots"]:
        s, e = PD.fa(t), PD.fa(t + sh["frames"] / FPS)
        t = e
        rec = credits[sh["file"]]
        inside = [w for w in words if s <= float(w["start"]) < e]
        hi = " ".join(w["word"] for w in inside)
        fwt = f"{float(inside[0]['start']):.3f}" if inside else f"{s:.3f}"
        tz.append({"beat": sh["id"], "scene": "S01", "start": s, "end": e, "first_word_time": fwt,
                   "text": hi, "asset": sh["file"], "source_dir": clip_dir_rel, "asset_source": "teaser",
                   "match": sh["label"], "role": "teaser", "v9_shot": "", "licence": rec.get("licence", ""),
                   "title": f"{rec.get('title', '')} (teaser cut)", "source_page": rec.get("source_page", ""),
                   "motion": "video_clip", "notes": f"v18 cold open: {sh['why']}; agent-made, not human-reviewed",
                   "reuse": "teaser", "reuse_of": sh["src"], "overlay_text": title,
                   "desk_rule": "HOOK", "desk_note": "cold-open teaser shot (visual only, narration unchanged)"})
    if abs(t - t_end) > 1e-6:
        raise ValueError(f"teaser shots sum to {t:.3f} s, teaser end is {t_end:.3f} s")
    return tz + keep, info


def cold_open_cmd(visuals_csv: str, out: str, *, spec: Optional[str] = None, run_id: Optional[str] = None) -> Dict[str, Any]:
    from .runs import Run, write_json, media_summary
    sp = load_spec(spec)
    rn = Run(run_id)
    rn.add_input(visuals_csv, "VISUALS_BEATS")
    rn.add_input(str(Path(spec) if spec else SPEC), "COLD_OPEN_SPEC")
    fields, rows = PD.read_rows(visuals_csv)
    t_end = teaser_end(sp)
    clip_dir = rn.path("teaser_clips")
    clip_dir.mkdir(exist_ok=True)
    clip_dir_rel = clip_dir.relative_to(ROOT).as_posix()
    ov = TitleOverlay(sp["title"]["kicker"], sp["title"]["title"], sp["title"].get("enter_at_s", 0.3),
                      sp["title"].get("enter_s", 0.5))
    creds, cmap, t, rendered = [], {}, 0.0, []
    for k, sh in enumerate(sp["shots"]):
        src = ROOT / sh["src"]
        rn.add_input(src, f"TEASER_SRC_{k + 1}")
        dst = clip_dir / sh["file"]
        render_shot(src, float(sh["in_s"]), int(sh["frames"]), t, dst, ov)
        ms = media_summary(dst)
        rec, from_ = _credit_record(sh, src)
        mod = (f"v18 cold-open teaser cut: {sh['frames'] / FPS:.2f} s from {sh['in_s']:.2f} s of {Path(sh['src']).name}, "
               f"scaled/cropped to 1920x1080 {FPS} fps, no audio, title overlay '{sp['title']['kicker']} / "
               f"{sp['title']['title']}' (own text, Mukta OFL) burned in (KANG)")
        if sh.get("ai_model"):
            mod += (f"; source clip is AI motion ({sh['ai_model']}, {sh['ai_model_licence']}) of the photo below, "
                    "'AI animated' label kept on screen")
        rec.update({"file": sh["file"], "label": sh["label"], "place": sh.get("place", rec.get("place", "")),
                    "derived_from": sh["src"], "credit_record_from": from_, "teaser": True,
                    "modified": (rec.get("modified", "") + " | " if rec.get("modified") else "") + mod})
        if sh.get("ai_model"):
            rec.update({"ai_model": sh["ai_model"], "ai_model_licence": sh["ai_model_licence"], "motion": "ai_animated"})
        creds.append(rec)
        cmap[sh["file"]] = rec
        rendered.append({"shot": sh["id"], "file": sh["file"], "start": round(t, 3),
                         "end": round(t + sh["frames"] / FPS, 3), "frames": sh["frames"], "media": ms})
        t += sh["frames"] / FPS
    write_json(clip_dir / "CREDITS.json", creds)
    rn.add_output(clip_dir / "CREDITS.json", "teaser_credits")
    for x in rendered:
        rn.add_output(clip_dir / x["file"], "teaser_clip")
    ws = json.loads((ROOT / sp["words"]).read_text(encoding="utf-8"))
    ws = ws["words"] if isinstance(ws, dict) else ws
    new_rows, info = build_rows(rows, sp, t_end, clip_dir_rel, cmap, ws)
    fields = list(fields) + [c for c in ("overlay_text",) if c not in fields]
    vpath = rn.path(f"{Path(out).name}.csv")
    PD.write_rows(vpath, fields, new_rows)
    rn.add_output(vpath, "visuals_beats")
    qa = {"teaser_end_s": t_end, "first_text_at_s": sp["title"].get("enter_at_s", 0.3),
          "shots": rendered, "frames_ok": all(x["frames"] == round((x["end"] - x["start"]) * FPS) for x in rendered),
          "all_1080p_25fps_no_audio": all(x["media"].get("width") == W and x["media"].get("height") == H
                                          and not x["media"].get("has_audio") for x in rendered),
          **info}
    jpath = rn.path("cold_open_report.json")
    write_json(jpath, qa)
    rn.add_output(jpath, "cold_open_report")
    rn.log_step("cold-open", teaser_end=t_end, shots=len(rendered), dropped=info.get("dropped_beats"))
    rn.set_status("done")
    return {"run": rn.run_id, "visuals_csv": str(vpath), "report": str(jpath), "teaser_end_s": t_end,
            "frames_ok": qa["frames_ok"], "media_ok": qa["all_1080p_25fps_no_audio"], **info}
