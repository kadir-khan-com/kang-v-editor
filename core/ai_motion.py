"""v17 AI motion: subtle natural motion (water, waves, clouds, flags, light) on REAL photos via image-to-video.

Model: Wan2.2-TI2V-5B (hf:Wan-AI/Wan2.2-TI2V-5B-Diffusers, Apache-2.0), run on Kaggle T4 (tools/kaggle_ai_motion);
licence evidence in config/model_licenses.json -> ai_motion_i2v. Rejected (licence): LTX-Video (RAIL-M / LTXV Open
Weights License), CogVideoX-5B-I2V (CogVideoX License), Stable Video Diffusion (Stability AI Community License).

Flow
  ai-motion-plan  : visuals_beats.csv -> candidate clips (merged beats, real still, exact/representative, hold 3-8.5 s,
                    sea/water/boat/sky/flag by file-name keywords + sky share, no face; agent eye list in
                    config/ai_motion.json) -> jobs.json + 1280x704 model inputs (= centre of the 16:9 cover framing).
  Kaggle kernel   : raw 1280x704 24 fps MP4 per job (no post-processing).
  ai-motion-apply : raw MP4 -> quality gate -> MASKED COMPOSITE onto the original 1920x1080 photo framing: only pixels
                    that (a) move in the AI clip AND (b) are sky / flat / water-coloured (or a small flag blob near the
                    top for kind=flag) come from the AI clip; every other pixel is the untouched photo, so buildings,
                    people and places cannot be re-drawn. Retimed to the beat (natural speed, or slowed <= max_slow with
                    frame blending), small on-screen "AI animated" label, 1920x1080 25 fps H.264, no audio.
                    Only clips that pass the gate AND are in config eye_pass replace the Ken Burns / parallax shot.
Gate (raw AI clip, work width 640): SSIM(first frame, input) / global + per-cell luma flicker / edge-structure
stability of rigid (non-sky, non-water) cells vs the first frame (Canny F-score, 2 px tolerance) / camera drift
(phase correlation on rigid pixels, first vs last) / some motion at all / mask area; composite: first frame SSIM vs
the photo. FAIL -> the shot keeps its existing parallax / Ken Burns.
Labels: the photo's own match label (exact / representative) never changes; motion = ai_animated;
CREDITS: model name + licence + "modified (AI motion)".
"""
from __future__ import annotations

import csv
import json
import math
import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
CFG_PATH = ROOT / "config" / "ai_motion.json"
MOTION_LABEL = "ai_animated"
AI_COLUMNS = ["ai_motion_clip", "ai_motion_dir", "ai_motion_status", "ai_motion_model"]
REPORT_COLUMNS = ["job", "beat", "beats", "asset", "source_dir", "match", "kind", "duration_s", "raw_frames", "out_frames",
                  "slow", "ssim_first", "flicker_max", "cell_flicker_max", "cell_flicker_fluid_max", "rigid_cells", "warp_cells", "drift_px",
                  "motion", "mask_area", "new_blobs", "blob_max_px", "ghost_frac", "composite_ssim_first", "status", "why", "eye", "clip", "kernel_s"]


def load_cfg(path: Optional[str | Path] = None) -> Dict[str, Any]:
    return json.loads(Path(path or CFG_PATH).read_text(encoding="utf-8"))


# --------------------------------------------------------------------------- selection
def is_still(asset: str, cfg: Dict[str, Any]) -> bool:
    return Path(asset).suffix.lower() in cfg["select"]["still_ext"]


def kinds_for(asset: str, title: str, cfg: Dict[str, Any]) -> List[str]:
    s = (asset + " " + (title or "")).lower().replace(" ", "_").replace("-", "_")
    return [k for k in cfg["kind_order"] if any(w in s for w in cfg["keywords"].get(k, []))]


def frames_for(dur_s: float, cfg: Dict[str, Any]) -> int:
    """Raw frame count (4k+1, Wan VAE) so that natural speed covers the beat, or a slow-down <= max_slow does."""
    m = cfg["model"]
    need = dur_s * m["fps"] / m["max_slow"]
    n = int(math.ceil((max(need, m["min_frames"]) - 1) / 4.0)) * 4 + 1
    return int(min(m["max_frames"], n))


def analyse_still(path: str | Path, face_detector: Optional[Callable] = None) -> Dict[str, Any]:
    """Sky share (flat bright pixels in the top 40 % of the cover framing), fluid share (water/sky hue), faces."""
    import cv2
    fr = cover_frame(path)
    small = cv2.resize(fr, (640, 360), interpolation=cv2.INTER_AREA)
    flat, fluid = allowed_maps(small)
    top = slice(0, int(360 * 0.4))
    gray = cv2.cvtColor(small, cv2.COLOR_RGB2GRAY)
    sky = flat[top] & (gray[top] > 90)
    faces = face_detector(cv2.cvtColor(fr, cv2.COLOR_RGB2BGR)) if face_detector else []
    w = _img_size(path)[0]
    return {"sky_frac": round(float(sky.mean()) * 0.4, 3), "fluid_frac": round(float(fluid.mean()), 3),
            "flat_frac": round(float(flat.mean()), 3), "faces": len(faces),
            "face_px": max([int(b[3]) for b in faces], default=0), "width": w}


def _img_size(path: str | Path) -> Tuple[int, int]:
    from PIL import Image
    with Image.open(path) as im:
        return im.size


def select(rows: Sequence[Dict[str, Any]], cfg: Dict[str, Any], analyse: Optional[Callable[[Path], Dict[str, Any]]] = None
           ) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Candidate clips for AI motion. Hard rules: real still, exact/representative, hold in [min,max], width >= min,
    no crop reuse, no face, not eye-rejected. Needs a natural-motion kind (keywords / eye_kind) or sky share >= 0.12."""
    from . import beats as B
    sel = cfg["select"]
    eye_rej = cfg.get("eye_rejects_plan", {})
    eye_kind = cfg.get("eye_kind", {})
    cands, rejected = [], []
    for c in B.merge_clips(rows):
        dur = c["end"] - c["start"]
        why = None
        if not is_still(c["asset"], cfg):
            why = "not a still"
        elif c["match"] not in sel["matches"]:
            why = f"match {c['match']}"
        elif sel.get("skip_crop_reuse") and c.get("reuse") == "crop_reuse":
            why = "crop reuse (lower resolution)"
        elif not (sel["min_hold_s"] - 1e-6 <= dur <= sel["max_hold_s"] + 1e-6):
            why = f"hold {dur:.2f} s"
        elif c["first_beat"] in eye_rej:
            why = "eye: " + eye_rej[c["first_beat"]]
        if why:
            rejected.append({"beat": c["first_beat"], "asset": c["asset"], "why": why})
            continue
        path = ROOT / c["source_dir"] / c["asset"]
        st = analyse(path) if analyse else {}
        kinds = [eye_kind[c["first_beat"]]] if c["first_beat"] in eye_kind else kinds_for(c["asset"], c.get("title", ""), cfg)
        if st.get("faces"):
            rejected.append({"beat": c["first_beat"], "asset": c["asset"], "why": f"face detected ({st['faces']})"})
            continue
        if st.get("width") and st["width"] < sel["min_width"]:
            rejected.append({"beat": c["first_beat"], "asset": c["asset"], "why": f"width {st['width']}"})
            continue
        if not kinds and st.get("sky_frac", 0) >= 0.12:
            kinds = ["sky"]
        if not kinds:
            rejected.append({"beat": c["first_beat"], "asset": c["asset"], "why": "no water/sky/flag element"})
            continue
        if sel.get("kinds_only") and kinds[0] not in sel["kinds_only"]:
            rejected.append({"beat": c["first_beat"], "asset": c["asset"], "why": f"kind {kinds[0]} not used (kinds_only)"})
            continue
        score = {"sea": 3, "boat": 3, "water": 2.5, "sea_flag": 3, "flag": 2, "sky": 1}.get(kinds[0], 1) + 2 * st.get("sky_frac", 0) \
            + st.get("fluid_frac", 0) + min(dur, 8) / 8
        cands.append({**c, "kind": kinds[0], "kinds": kinds, "duration_s": round(dur, 3), "score": round(score, 3),
                      "stats": st, "path_local": str(path)})
    cands.sort(key=lambda x: -x["score"])
    return cands, rejected


def prompt_for(kind: str, cfg: Dict[str, Any]) -> str:
    return cfg["prompts"][kind]


def negative_for(beat: str, cfg: Dict[str, Any]) -> str:
    """Base negative prompt + config negative_extra (v17 attempt 2: against fake birds / new objects) for the beats in
    negative_extra_beats (empty / missing = every job)."""
    extra = cfg.get("negative_extra", "")
    beats = cfg.get("negative_extra_beats") or []
    if extra and (not beats or beat in beats):
        return cfg["negative"] + ", " + extra
    return cfg["negative"]


def job_id(beat: str) -> str:
    return "AI_" + beat


# --------------------------------------------------------------------------- framing
def cover_frame(path: str | Path, w: int = 1920, h: int = 1080) -> np.ndarray:
    """Centre 16:9 cover framing of the still (what Premiere shows at cover-fit scale 1.00), RGB uint8."""
    from PIL import Image
    im = Image.open(path).convert("RGB")
    k = max(w / im.width, h / im.height)
    nw, nh = max(w, round(im.width * k)), max(h, round(im.height * k))
    im = im.resize((nw, nh), Image.LANCZOS)
    x0, y0 = (nw - w) // 2, (nh - h) // 2
    return np.asarray(im.crop((x0, y0, x0 + w, y0 + h)))


def model_input(frame: np.ndarray, mw: int = 1280, mh: int = 704) -> np.ndarray:
    """1920x1080 framing -> 1280x720 -> centre rows -> 1280x704 (Wan 2.2 5B 720P size, multiple of 32)."""
    import cv2
    h16 = round(mw * 9 / 16)
    sm = cv2.resize(frame, (mw, h16), interpolation=cv2.INTER_AREA)
    y0 = (h16 - mh) // 2
    return np.ascontiguousarray(sm[y0:y0 + mh])


def band_rows(mw: int = 1280, mh: int = 704, h: int = 1080) -> Tuple[int, int]:
    """Rows of the 1920x1080 frame covered by the model's 1280x704 window."""
    s = h / round(mw * 9 / 16)
    y0 = round(((round(mw * 9 / 16) - mh) // 2) * s)
    return y0, y0 + round(mh * s)


# --------------------------------------------------------------------------- metrics
def ssim(a: np.ndarray, b: np.ndarray) -> float:
    """Gaussian-window SSIM on grayscale float images (0..255)."""
    import cv2
    a = a.astype(np.float64)
    b = b.astype(np.float64)
    c1, c2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    g = lambda x: cv2.GaussianBlur(x, (11, 11), 1.5)  # noqa: E731
    ma, mb = g(a), g(b)
    va, vb, cov = g(a * a) - ma * ma, g(b * b) - mb * mb, g(a * b) - ma * mb
    s = ((2 * ma * mb + c1) * (2 * cov + c2)) / ((ma * ma + mb * mb + c1) * (va + vb + c2))
    return float(s.mean())


def gray(fr: np.ndarray) -> np.ndarray:
    import cv2
    return cv2.cvtColor(fr, cv2.COLOR_RGB2GRAY)


def allowed_maps(rgb: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """flat = low local edge density (sky, calm water, haze); fluid = water/sky hue (cyan-blue, some saturation)."""
    import cv2
    g = cv2.GaussianBlur(gray(rgb), (3, 3), 0)
    e = cv2.Canny(g, 60, 160).astype(np.float32) / 255.0
    dens = cv2.GaussianBlur(e, (0, 0), 6)
    hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
    fluid = (hsv[..., 0] >= 80) & (hsv[..., 0] <= 130) & (hsv[..., 1] > 25)
    return dens < 0.06, fluid


def edge_f(a: np.ndarray, b: np.ndarray, tol: int = 2) -> float:
    """Symmetric edge F-score with a pixel tolerance (a, b = boolean edge maps)."""
    import cv2
    k = np.ones((2 * tol + 1, 2 * tol + 1), np.uint8)
    da = cv2.dilate(a.astype(np.uint8), k) > 0
    db = cv2.dilate(b.astype(np.uint8), k) > 0
    na, nb = a.sum(), b.sum()
    if na == 0 and nb == 0:
        return 1.0
    p = (a & db).sum() / max(na, 1)
    r = (b & da).sum() / max(nb, 1)
    return float(0.0 if p + r == 0 else 2 * p * r / (p + r))


def drift_px(a: np.ndarray, b: np.ndarray, weight: Optional[np.ndarray] = None) -> float:
    import cv2
    win = cv2.createHanningWindow((a.shape[1], a.shape[0]), cv2.CV_64F)
    if weight is not None:
        win = win * (0.2 + 0.8 * weight.astype(np.float64))
    (dx, dy), _ = cv2.phaseCorrelate(a.astype(np.float64), b.astype(np.float64), win)
    return float(math.hypot(dx, dy))


FLAG_KINDS = ("flag", "sea_flag")


def flag_hue(rgb: np.ndarray, G: Dict[str, Any]) -> np.ndarray:
    """Saffron / red / pink flag cloth: hue <= flag_h_hi or >= flag_h_lo (OpenCV 0..180), saturated, not dark."""
    import cv2
    hsv = cv2.cvtColor(np.ascontiguousarray(rgb), cv2.COLOR_RGB2HSV)
    h, sat, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    return (((h <= G.get("flag_h_hi", 22)) | (h >= G.get("flag_h_lo", 160))) & (sat >= G.get("flag_s_min", 100))
            & (v >= G.get("flag_v_min", 50)))


def flag_colour_core(src_rgb: np.ndarray, frames_rgb: Sequence[np.ndarray], moving: np.ndarray, G: Dict[str, Any]
                     ) -> np.ndarray:
    """v17 attempt 2 (KANG_021, S16_b06 ghost fix): the whole area the flag occupies in the photo OR in ANY AI frame
    (flag-coloured pixels, union over all frames), kept only for components that move (>= flag_move_frac of their pixels)
    and are not big (<= flag_max_area of the frame, so saffron-tinted stone is not taken), dilated by flag_dilate px and
    closed. Inside it the composite is 100 % AI, so the photo's own flag can never show through as a ghost."""
    import cv2
    u = flag_hue(src_rgb, G)
    for f in frames_rgb:
        u |= flag_hue(f, G)
    # seeds = the photo's own flags: flag-coloured photo components >= flag_photo_min of the frame (stone specks with a
    # warm tint are smaller); the AI flag in every frame grows out of its photo flag, so the union over all frames is
    # one connected sweep area per flag that contains its seed. KANG_024: without seeds, warm-tinted moving stone
    # specks of the AI frames were taken as flag and the carving shimmered.
    ps = flag_hue(src_rgb, G)
    pn, plab, pst, _ = cv2.connectedComponentsWithStats(ps.astype(np.uint8), 8)
    seeds = np.zeros(u.shape, bool)
    for i in range(1, pn):
        if pst[i, cv2.CC_STAT_AREA] >= G.get("flag_photo_min", 0.0004) * u.size:
            seeds |= plab == i
    # label on a slightly dilated union so a flag swinging across its thin pole stays one component
    ud = cv2.dilate(u.astype(np.uint8), np.ones((5, 5), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(ud, 8)
    keep = np.zeros(u.shape, bool)
    mv = cv2.dilate(moving.astype(np.uint8), np.ones((5, 5), np.uint8)) > 0
    for i in range(1, n):
        comp = (lab == i) & u
        a = int(comp.sum())
        if a < G.get("flag_min_px", 12) or a > G.get("flag_max_area", 0.03) * u.size:
            continue
        if seeds[comp].any() and mv[comp].mean() >= G.get("flag_move_frac", 0.2):
            keep |= comp
    d = int(G.get("flag_dilate", 4))
    keep = cv2.dilate(keep.astype(np.uint8), np.ones((2 * d + 1, 2 * d + 1), np.uint8))
    keep = cv2.morphologyEx(keep, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    return keep > 0


def keep_rows_mask(shape: Tuple[int, int], limits: Optional[Dict[str, Any]]) -> np.ndarray:
    """Rows the AI clip may touch (config mask_keep[beat] = {y_min, y_max} as fractions of the frame height): for beach
    shots everything below the open water (breakers, shoreline, wet sand) stays the photo."""
    keep = np.ones(shape, bool)
    if limits:
        h = shape[0]
        keep[: int(round(float(limits.get("y_min", 0.0)) * h))] = False
        keep[int(round(float(limits.get("y_max", 1.0)) * h)):] = False
    return keep


def motion_mask(frames_g: np.ndarray, src_rgb: np.ndarray, kind: str, cfg_gate: Dict[str, Any],
                frames_rgb: Optional[Sequence[np.ndarray]] = None, limits: Optional[Dict[str, Any]] = None
                ) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Soft mask (0..1, work size) of pixels that may come from the AI clip: moving AND (flat | fluid | flag blob);
    flag kinds: + the flag colour core (hard 1.0, see flag_colour_core); limits: rows outside y_min..y_max = photo."""
    import cv2
    std = frames_g.astype(np.float32).std(axis=0)
    moving = cv2.GaussianBlur(std, (0, 0), 2) > cfg_gate["mask_std"]
    flat, fluid = allowed_maps(src_rgb)
    allowed = flat | fluid
    core = None
    if kind in FLAG_KINDS and frames_rgb is not None:
        core = flag_colour_core(src_rgb, frames_rgb, moving, cfg_gate)
        if kind == "flag":
            # v17 attempt 2: a temple-flag shot has no water, so AI pixels only in FLAT sky-coloured areas + the flag
            # core. KANG_023 heat map: 'fluid' (blue-grey hue) alone let shadowed stone carving shimmer in the AI layer.
            sky = flat & (fluid | (gray(src_rgb) > 120))
            n, lab, st, _ = cv2.connectedComponentsWithStats(sky.astype(np.uint8), 8)
            big = np.zeros(sky.shape, bool)
            for i in range(1, n):  # sky = LARGE flat components only (small flat bits on stone stay photo)
                if st[i, cv2.CC_STAT_AREA] >= cfg_gate.get("flag_sky_min", 0.02) * sky.size:
                    big |= lab == i
            allowed = big | core
        else:
            allowed |= core
    if kind == "flag" and core is None:
        h = moving.shape[0]
        top = np.zeros_like(moving)
        top[: int(h * 0.6)] = moving[: int(h * 0.6)]
        n, lab, st, _ = cv2.connectedComponentsWithStats(top.astype(np.uint8), 8)
        area = moving.size
        for i in range(1, n):
            if 20 <= st[i, cv2.CC_STAT_AREA] <= 0.015 * area:
                allowed |= cv2.dilate((lab == i).astype(np.uint8), np.ones((7, 7), np.uint8)) > 0
    keep = keep_rows_mask(moving.shape, limits)
    m = (moving & allowed & keep).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    m = cv2.dilate(m, np.ones((5, 5), np.uint8))
    soft = np.clip(cv2.GaussianBlur(m.astype(np.float32), (0, 0), 3), 0, 1)
    if core is not None and core.any():
        cd = core & keep
        feather = cv2.GaussianBlur(cv2.dilate(cd.astype(np.uint8), np.ones((5, 5), np.uint8)).astype(np.float32), (0, 0), 1.5)
        soft = np.maximum(soft, np.clip(feather, 0, 1))
        soft[cd] = 1.0
    if limits:
        soft = soft * cv2.GaussianBlur(keep.astype(np.float32), (0, 0), 2) * keep
    # pixels outside the keep rows always come from the photo -> not judged as rigid AI structure (no seam there
    # except the boundary row, which the agent eye check judges)
    return soft, {"moving_frac": round(float(moving.mean()), 3), "allowed_frac": round(float(allowed.mean()), 3),
                  "mask_area": round(float((soft > 0.5).mean()), 3), "rigid": ~allowed & keep,
                  "flag_core": core if core is not None else np.zeros(moving.shape, bool)}


def new_blobs(frames_rgb: Sequence[np.ndarray], soft: np.ndarray, exclude: Optional[np.ndarray], G: Dict[str, Any]
              ) -> Dict[str, Any]:
    """v17 attempt 2 (KANG_021, S12_b01 fake seagull): bright / high-contrast blobs that APPEAR inside the water/sky
    motion mask vs the first frame. Local contrast = luma - median(luma, blob_med_k); a pixel is new when |contrast| >=
    blob_contrast in frame k AND its contrast rose by >= blob_rise vs frame 0 (so whitecaps / boats already in the photo
    do not count). Connected components blob_min_px .. blob_max_frac*frame inside the eroded mask (flag core
    excluded), at least 2 px high and not longer than blob_max_aspect (ripple troughs are 1-2 px dark lines), bright, or
    dark and compact (h >= 3, w/h <= blob_dark_aspect: a bird); FAIL when found in >= blob_min_frames sampled frames.
    Calibrated KANG_021 on the attempt-1 raws: S12_b01 seagull + streak + dark sky blob -> FAIL (>= 10 frames); S11_b06
    open water (y <= 0.55) and S16_b06 (flag core excluded) -> 0-1 frames."""
    import cv2
    m = (soft > 0.5)
    if exclude is not None:
        m &= ~(cv2.dilate(exclude.astype(np.uint8), np.ones((7, 7), np.uint8)) > 0)
    e = int(G.get("blob_erode", 3))
    m = cv2.erode(m.astype(np.uint8), np.ones((2 * e + 1, 2 * e + 1), np.uint8)) > 0
    k = int(G.get("blob_med_k", 21)) | 1

    def lc(f):
        g = gray(f)
        return g.astype(np.float32) - cv2.medianBlur(g, k).astype(np.float32)

    c0 = lc(frames_rgb[0])
    n = len(frames_rgb)
    idx = sorted(set(np.linspace(1, n - 1, min(int(G.get("blob_samples", 16)), n - 1)).astype(int))) if n > 1 else []
    hits, frames_hit, biggest = [], 0, 0
    amax = G.get("blob_max_frac", 0.01) * m.size
    for i in idx:
        ck = lc(frames_rgb[i])
        new = m & (np.abs(ck) >= G.get("blob_contrast", 40)) & (np.abs(ck) - np.abs(c0) >= G.get("blob_rise", 28))
        nn, lab, st, cen = cv2.connectedComponentsWithStats(new.astype(np.uint8), 8)
        found = []
        for j in range(1, nn):
            a, w, h = st[j, cv2.CC_STAT_AREA], st[j, cv2.CC_STAT_WIDTH], st[j, cv2.CC_STAT_HEIGHT]
            if not (G.get("blob_min_px", 6) <= a <= amax) or h < 2 or w / h > G.get("blob_max_aspect", 4.0):
                continue  # 1-px-high / long thin lines = ripple troughs and wave crests, not objects
            bright = float(ck[lab == j].mean()) > 0
            if bright or (h >= 3 and w / h <= G.get("blob_dark_aspect", 2.5)):  # bright blob, or compact dark one
                found.append((int(a), int(cen[j][0]), int(cen[j][1])))
        if found:
            frames_hit += 1
            biggest = max(biggest, max(a for a, _, _ in found))
            hits.append(f"f{i}:" + ",".join(f"{a}px@{x},{y}" for a, x, y in found[:3]))
    fail = frames_hit >= int(G.get("blob_min_frames", 2))
    return {"new_blobs": frames_hit, "blob_max_px": biggest, "blob_list": hits[:6], "blob_fail": bool(fail)}


def ghost_frac(src_rgb: np.ndarray, ai_rgb: Sequence[np.ndarray], mask: np.ndarray, core: np.ndarray,
               G: Dict[str, Any]) -> float:
    """Flag ghost check (work size): share of frame pixels where the PHOTO's flag (flag-coloured photo components that
    touch the flag core) would still show through the composite (mask < ghost_mask_max, so >= 10 % photo) while the AI frame
    has no flag there; max over the sampled AI frames. 0 = the photo flag is fully replaced by AI pixels."""
    import cv2
    fh = flag_hue(src_rgb, G)
    n, lab, st, _ = cv2.connectedComponentsWithStats(fh.astype(np.uint8), 8)
    photo_flag = np.zeros(fh.shape, bool)
    for i in range(1, n):  # the photo's flag cloth = flag-coloured components (>= flag_min_px) touching the core
        comp = lab == i
        if st[i, cv2.CC_STAT_AREA] >= G.get("flag_min_px", 12) and core[comp].any():
            photo_flag |= comp
    photo_flag &= mask < G.get("ghost_mask_max", 0.9)
    if not photo_flag.any():
        return 0.0
    return max(float((photo_flag & ~flag_hue(a, G)).mean()) for a in ai_rgb)


def gate_raw(src_in: np.ndarray, raw: np.ndarray, kind: str, cfg: Dict[str, Any],
             limits: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Quality gate on the raw AI clip (frames RGB, model size) vs the model input still."""
    import cv2
    G = cfg["gate"]
    ww = G["work_w"]
    wh = round(ww * src_in.shape[0] / src_in.shape[1])
    rs = lambda f: cv2.resize(f, (ww, wh), interpolation=cv2.INTER_AREA)  # noqa: E731
    src = rs(src_in)
    fr_rgb = [rs(f) for f in raw]
    fr = np.stack([gray(f) for f in fr_rgb])
    sg = gray(src)
    out: Dict[str, Any] = {}
    out["ssim_first"] = round(ssim(sg, fr[0]), 4)
    lum = fr.reshape(len(fr), -1).mean(axis=1)
    out["flicker_max"] = round(float(np.abs(np.diff(lum)).max()) if len(fr) > 1 else 0.0, 3)
    ch, cw = wh // 9, ww // 16
    cells = fr[:, : ch * 9, : cw * 16].reshape(len(fr), 9, ch, 16, cw).mean(axis=(2, 4))
    soft, mi = motion_mask(fr, src, kind, G, frames_rgb=fr_rgb, limits=limits)
    rigid = mi.pop("rigid")
    flag_core = mi.pop("flag_core")
    out["flag_core_area"] = round(float(flag_core.mean()), 4)
    out["_flag_core"] = flag_core
    out["_src_work"] = src
    out["_raw_work"] = fr_rgb
    out.update(mi)
    # v17 KANG_018 calibration on the first real Wan2.2 clips: per-cell flicker is judged separately for RIGID cells
    # (>= 50 % non-sky / non-water / non-flag pixels: structure must not pump) and FLUID cells (mostly sky / water /
    # flag blob: the cell mean legitimately jumps when a flag or a breaking wave passes through it).
    dcell = np.abs(np.diff(cells, axis=0)).max(axis=0) if len(fr) > 1 else np.zeros((9, 16))
    rfrac = rigid[: ch * 9, : cw * 16].reshape(9, ch, 16, cw).mean(axis=(1, 3))
    out["cell_flicker_max"] = round(float(dcell[rfrac >= 0.5].max()) if (rfrac >= 0.5).any() else 0.0, 3)
    out["cell_flicker_fluid_max"] = round(float(dcell[rfrac < 0.5].max()) if (rfrac < 0.5).any() else 0.0, 3)
    std = fr.astype(np.float32).std(axis=0)
    out["motion"] = round(float((std * (soft > 0.5)).sum() / max((soft > 0.5).sum(), 1)), 3)
    edges = [cv2.Canny(cv2.GaussianBlur(f, (3, 3), 0), 60, 160) > 0 for f in fr]
    idx = sorted(set(np.linspace(1, len(fr) - 1, min(8, len(fr) - 1)).astype(int))) if len(fr) > 1 else []
    rigid_cells, warp = 0, []
    for cy in range(9):
        for cx in range(16):
            sl = (slice(cy * ch, (cy + 1) * ch), slice(cx * cw, (cx + 1) * cw))
            rg = rigid[sl]
            if rg.mean() < 0.5 or edges[0][sl][rg].sum() < 0.03 * rg.size:
                continue
            rigid_cells += 1
            fmin = min((edge_f(edges[0][sl] & rg, edges[i][sl] & rg) for i in idx), default=1.0)
            if fmin < G["edge_f_min"]:
                warp.append(f"{cx},{cy}:{fmin:.2f}")
    out["rigid_cells"] = rigid_cells
    out["warp_cells"] = len(warp)
    out["warp_list"] = warp
    out["drift_px"] = round(drift_px(fr[0], fr[-1], rigid.astype(np.float32)), 2) if len(fr) > 1 else 0.0
    why, fail, warn = [], False, False
    if out["ssim_first"] < G["ssim_first_fail"]:
        fail = True; why.append(f"first frame SSIM {out['ssim_first']}")  # noqa: E702
    elif out["ssim_first"] < G["ssim_first_pass"]:
        warn = True; why.append(f"first frame SSIM {out['ssim_first']} (warn)")  # noqa: E702
    if (out["flicker_max"] > G["flicker_fail"] or out["cell_flicker_max"] > G["cell_flicker_fail"]
            or out["cell_flicker_fluid_max"] > G.get("cell_flicker_fluid_fail", G["cell_flicker_fail"])):
        fail = True; why.append(f"flicker {out['flicker_max']}/{out['cell_flicker_max']}/{out['cell_flicker_fluid_max']}")  # noqa: E702
    elif out["flicker_max"] > G["flicker_pass"]:
        warn = True; why.append(f"flicker {out['flicker_max']} (warn)")  # noqa: E702
    lim = max(G["warp_cells_fail_min"], int(G["warp_cells_fail_frac"] * max(rigid_cells, 1)))
    if len(warp) > lim:
        fail = True; why.append(f"structure warping in {len(warp)}/{rigid_cells} rigid cells")  # noqa: E702
    elif warp:
        warn = True; why.append(f"edge change in {len(warp)} rigid cells (masked out)")  # noqa: E702
    if out["drift_px"] > G["drift_px_fail"]:
        fail = True; why.append(f"camera drift {out['drift_px']} px")  # noqa: E702
    elif out["drift_px"] > G["drift_px_warn"]:
        warn = True; why.append(f"camera drift {out['drift_px']} px (warn)")  # noqa: E702
    if out["motion"] < G["motion_min"] or out["mask_area"] < 0.01:
        fail = True; why.append(f"no usable motion (motion {out['motion']}, mask {out['mask_area']})")  # noqa: E702
    if out["mask_area"] > G["mask_area_fail"]:
        fail = True; why.append(f"mask area {out['mask_area']}")  # noqa: E702
    nb = new_blobs(fr_rgb, soft, flag_core, G)
    out.update({k: v for k, v in nb.items() if k != "blob_fail"})
    if nb["blob_fail"]:
        fail = True; why.append(f"new object/blob in water/sky in {nb['new_blobs']} frames ({'; '.join(nb['blob_list'][:2])})")  # noqa: E702
    if kind in ("sea", "sea_flag") and G.get("sea_needs_limits", True) and not limits:
        fail = True; why.append("beach shot without shoreline limit (config mask_keep)")  # noqa: E702
    out["status"] = "FAIL" if fail else ("WARN" if warn else "PASS")
    out["why"] = why
    out["_mask"] = soft
    return out


# --------------------------------------------------------------------------- composite / render
def time_map(n_out: int, n_src: int, fps_out: int, fps_src: int) -> Tuple[np.ndarray, float]:
    """Source position (float frame index) per output frame: natural speed if the clip is long enough, else slowed."""
    nat = np.arange(n_out) * fps_src / fps_out
    if n_out == 0 or nat[-1] <= n_src - 1:
        return nat, 1.0
    pos = np.linspace(0, n_src - 1, n_out)
    slow = (n_out - 1) * fps_src / fps_out / max(n_src - 1, 1)
    return pos, round(float(slow), 3)


def color_match(ai0: np.ndarray, base: np.ndarray, w: Optional[np.ndarray] = None) -> Tuple[np.ndarray, np.ndarray]:
    """Per-channel gain/offset so the AI clip's first frame matches the photo (VAE colour shift)."""
    a = ai0.reshape(-1, 3).astype(np.float64)
    b = base.reshape(-1, 3).astype(np.float64)
    if w is not None:
        sel = w.reshape(-1) > 0.5
        if sel.sum() > 500:
            a, b = a[sel], b[sel]
    gain = np.clip(b.std(0) / np.maximum(a.std(0), 1e-3), 0.85, 1.15)
    off = b.mean(0) - gain * a.mean(0)
    return gain, off


def label_overlay(w: int, h: int, cfg: Dict[str, Any]) -> Optional[np.ndarray]:
    lc = cfg.get("onscreen_label", {})
    if not lc.get("enabled"):
        return None
    from PIL import Image, ImageDraw, ImageFont
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    try:
        font = ImageFont.truetype(str(ROOT / lc["font"]), lc["size"])
    except Exception:  # pragma: no cover
        font = ImageFont.load_default()
    t = lc["text"]
    x0, y0, x1, y1 = d.textbbox((0, 0), t, font=font)
    x = w - lc["margin"] - (x1 - x0)
    y = lc["margin"]
    a = int(255 * lc["opacity"])
    d.text((x + 2, y + 2), t, font=font, fill=(0, 0, 0, a // 2))
    d.text((x, y), t, font=font, fill=(255, 255, 255, a))
    return np.asarray(im).astype(np.float32) / 255.0


def read_video(path: str | Path) -> Tuple[np.ndarray, float]:
    """All frames of a video as RGB uint8 (n, h, w, 3) + fps (ffmpeg pipe)."""
    from .runs import ffprobe
    pr = ffprobe(path)
    vs = [s for s in pr.get("streams", []) if s.get("codec_type") == "video"][0]
    w, h = int(vs["width"]), int(vs["height"])
    num, den = (vs.get("r_frame_rate") or "24/1").split("/")
    fps = float(num) / float(den or 1)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3), fps


def encode(frames, out: str | Path, w: int, h: int, fps: int, crf: int = 18) -> Path:
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    tmpd = Path(tempfile.mkdtemp(prefix="kang_ai_"))
    tmp = tmpd / out.name
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{w}x{h}",
                             "-r", str(fps), "-i", "-", "-an", "-c:v", "libx264", "-preset", "veryfast", "-crf", str(crf),
                             "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(tmp)], stdin=subprocess.PIPE)
    try:
        for f in frames:
            proc.stdin.write(np.ascontiguousarray(f).tobytes())
    finally:
        proc.stdin.close()
        rc = proc.wait()
    if rc != 0:
        raise RuntimeError(f"ffmpeg encode failed ({rc}) for {out}")
    shutil.move(str(tmp), str(out))
    shutil.rmtree(tmpd, ignore_errors=True)
    return out


def composite_frames(base: np.ndarray, raw: np.ndarray, mask_work: np.ndarray, n_out: int, fps_out: int, fps_src: int,
                     cfg: Dict[str, Any], label: Optional[np.ndarray] = None):
    """Generator of 1920x1080 RGB frames: photo everywhere, AI pixels only inside the soft mask (inside the band)."""
    import cv2
    H, W = base.shape[:2]
    y0, y1 = band_rows(raw.shape[2], raw.shape[1], H)
    m = np.zeros((H, W), np.float32)
    m[y0:y1] = cv2.resize(mask_work, (W, y1 - y0), interpolation=cv2.INTER_LINEAR)
    m3 = m[..., None]
    basef = base.astype(np.float32)
    up0 = cv2.resize(raw[0], (W, y1 - y0), interpolation=cv2.INTER_CUBIC)
    gain, off = color_match(up0, base[y0:y1], m[y0:y1])
    pos, _ = time_map(n_out, len(raw), fps_out, fps_src)
    for p in pos:
        i0 = int(math.floor(p))
        i1 = min(i0 + 1, len(raw) - 1)
        t = float(p - i0)
        src = raw[i0].astype(np.float32) if t < 1e-3 else raw[i0] * (1 - t) + raw[i1].astype(np.float32) * t
        up = cv2.resize(src, (W, y1 - y0), interpolation=cv2.INTER_CUBIC) * gain + off
        ai = basef.copy()
        ai[y0:y1] = up
        fr = basef * (1 - m3) + ai * m3
        if label is not None:
            fr = fr * (1 - label[..., 3:4]) + label[..., :3] * 255.0 * label[..., 3:4]
        yield np.clip(fr + 0.5, 0, 255).astype(np.uint8)


def render_clip(still: str | Path, raw_mp4: str | Path, out: str | Path, n_out: int, kind: str, cfg: Dict[str, Any],
                fps: int = 25, limits: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Gate the raw clip; if not FAIL, write the masked composite (n_out frames, fps) to out. Returns the metrics."""
    import cv2
    t0 = time.time()
    base = cover_frame(still)
    raw, fps_src = read_video(raw_mp4)
    m = cfg["model"]
    src_in = model_input(base, raw.shape[2], raw.shape[1])
    g = gate_raw(src_in, raw, kind, cfg, limits=limits)
    pos, slow = time_map(n_out, len(raw), fps, round(fps_src))
    g.update(raw_frames=len(raw), out_frames=n_out, slow=slow)
    if slow > m["max_slow"] + 1e-6:
        g["status"] = "FAIL"
        g["why"].append(f"slow-down {slow} > {m['max_slow']}")
    mask = g.pop("_mask")
    g["composite_ssim_first"] = ""
    g["ghost_frac"] = ""
    if g["status"] != "FAIL":
        frames = list(composite_frames(base, raw, mask, n_out, fps, round(fps_src), cfg, label=None))
        ww = cfg["gate"]["work_w"]
        rs = lambda f: gray(cv2.resize(f, (ww, round(ww * 9 / 16)), interpolation=cv2.INTER_AREA))  # noqa: E731
        g["composite_ssim_first"] = round(ssim(rs(base), rs(frames[0])), 4)
        if kind in FLAG_KINDS:
            g["ghost_frac"] = round(ghost_frac(g["_src_work"], g["_raw_work"], mask, g["_flag_core"], cfg["gate"]), 5)
            if g["ghost_frac"] > cfg["gate"].get("ghost_frac_fail", 0.0002):
                g["status"] = "FAIL"
                g["why"].append(f"flag ghost {g['ghost_frac']}")
        if g["composite_ssim_first"] < cfg["gate"]["composite_ssim_first_min"]:
            g["status"] = "FAIL"
            g["why"].append(f"composite first frame SSIM {g['composite_ssim_first']}")
        elif g["status"] != "FAIL":
            lab = label_overlay(base.shape[1], base.shape[0], cfg)
            if lab is not None:
                frames = [np.clip(f * (1 - lab[..., 3:4]) + lab[..., :3] * 255.0 * lab[..., 3:4] + 0.5, 0, 255).astype(np.uint8)
                          for f in frames]
            encode(frames, out, base.shape[1], base.shape[0], fps)
            g["clip"] = Path(out).name
            g["_thumbs"] = [frames[0], frames[len(frames) // 2], frames[-1]]
    for k in ("_flag_core", "_src_work", "_raw_work"):
        g.pop(k, None)
    g["_raw0"] = raw[0]
    g["_mask_img"] = mask
    g["render_s"] = round(time.time() - t0, 1)
    return g


# --------------------------------------------------------------------------- apply to the timeline CSV
def apply_ai(rows: Sequence[Dict[str, Any]], report: Sequence[Dict[str, Any]], clips_dir: str | Path,
             eye_pass: Sequence[str], model_name: str, fps: int = 25) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Beats of a clip whose AI render passed the gate (PASS/WARN) AND the agent eye check get ai_motion_clip; the
    asset / match / licence stay the photo's own; any parallax clip of that shot is dropped (AI clip replaces it)."""
    from . import beats as B
    ok = {r["beat"]: r for r in report if r.get("status") in ("PASS", "WARN") and r.get("clip")}
    cdir = Path(clips_dir)
    out = [dict(r) for r in rows]
    by_beat = {r["beat"]: r for r in out}
    used, skipped = [], []
    for c in B.merge_clips(out):
        rep = ok.get(c["first_beat"])
        if not rep:
            continue
        if c["first_beat"] not in eye_pass:
            skipped.append(f"{c['first_beat']}: not in eye_pass")
            continue
        if rep.get("asset") and rep["asset"] != c["asset"]:
            skipped.append(f"{c['first_beat']}: asset changed")
            continue
        want = round(c["end"] * fps) - round(c["start"] * fps)
        if int(rep.get("out_frames") or 0) != want or not (cdir / rep["clip"]).is_file():
            skipped.append(f"{c['first_beat']}: frame count / file")
            continue
        for b in c["beats"]:
            by_beat[b].update(ai_motion_clip=rep["clip"], ai_motion_dir=str(cdir), ai_motion_status=rep["status"],
                              ai_motion_model=model_name, parallax_clip="", parallax_dir="", parallax_status="")
        used.append(c["first_beat"])
    return out, {"ai_clips": len(used), "used": used, "skipped": skipped}


def write_report(rows: Sequence[Dict[str, Any]], path: str | Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8-sig", newline="") as fh:
        wr = csv.DictWriter(fh, REPORT_COLUMNS, extrasaction="ignore")
        wr.writeheader()
        for r in rows:
            wr.writerow({**r, "why": "; ".join(r["why"]) if isinstance(r.get("why"), list) else r.get("why", ""),
                         "beats": " ".join(r["beats"]) if isinstance(r.get("beats"), list) else r.get("beats", "")})
    return p


def read_report(path: str | Path) -> List[Dict[str, str]]:
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return [dict(r) for r in csv.DictReader(fh)]


def contact_sheet(items: Sequence[Dict[str, Any]], out: str | Path, tw: int = 480) -> Path:
    """Per clip one row: photo | raw AI first | composite first / mid / last | mask; caption with metrics."""
    from PIL import Image, ImageDraw, ImageFont
    th = round(tw * 9 / 16)
    cols = 6
    capt = 44
    sheet = Image.new("RGB", (cols * tw, max(1, len(items)) * (th + capt)), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    try:
        font = ImageFont.truetype(str(ROOT / "fonts" / "Mukta-ExtraBold.ttf"), 17)
    except Exception:  # pragma: no cover
        font = ImageFont.load_default()
    for i, it in enumerate(items):
        y = i * (th + capt)
        tiles = [it.get("base"), it.get("raw0")] + list(it.get("thumbs") or [None, None, None]) + [it.get("mask")]
        for k, t in enumerate(tiles):
            if t is None:
                continue
            arr = t if t.dtype == np.uint8 else (np.clip(t, 0, 1) * 255).astype(np.uint8)
            im = Image.fromarray(arr).convert("RGB").resize((tw, th))
            sheet.paste(im, (k * tw, y + capt))
        d.text((6, y + 2), it.get("caption", ""), fill=(255, 255, 0), font=font)
        d.text((6, y + 22), "photo | raw AI f0 | composite first | mid | last | mask", fill=(200, 200, 200), font=font)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=88)
    return out


# --------------------------------------------------------------------------- commands
def _face_detector():
    from .crop_reuse import yunet_detector
    return yunet_detector()


def plan_cmd(visuals_csv: str, *, beats: Optional[Sequence[str]] = None, max_clips: Optional[int] = None,
             run_id: Optional[str] = None, cfg_path: Optional[str] = None,
             analyse: Optional[Callable[[Path], Dict[str, Any]]] = None) -> Dict[str, Any]:
    """Candidates + Kaggle jobs: run/ai_motion_jobs/{jobs.json, inputs/AI_<beat>.png}, ai_motion_plan.csv,
    ai_motion_candidates.jpg (eye check of the plan). --beats = only these first beats (e.g. the 3-still test)."""
    from . import beats as B
    from .runs import Run, write_json
    cfg = load_cfg(cfg_path)
    run = Run(run_id)
    run.add_input(visuals_csv, "VISUALS_BEATS")
    run.add_input(str(cfg_path or CFG_PATH), "AI_MOTION_CFG")
    rows = B.read_assign_csv(visuals_csv)
    if analyse is None:
        det = _face_detector()
        analyse = lambda p: analyse_still(p, det)  # noqa: E731
    cands, rejected = select(rows, cfg, analyse)
    if beats:
        want = list(beats)
        cands = [c for c in cands if c["first_beat"] in want]
        cands.sort(key=lambda c: want.index(c["first_beat"]))
        missing = [b for b in want if b not in {c["first_beat"] for c in cands}]
        rejected += [{"beat": b, "asset": "", "why": "requested but not a candidate"} for b in missing]
    else:
        cands = cands[: (max_clips or cfg["select"]["max_clips"])]
    jd = run.path("ai_motion_jobs")
    (jd / "inputs").mkdir(parents=True, exist_ok=True)
    m = cfg["model"]
    jobs = []
    from PIL import Image
    for c in cands:
        jid = job_id(c["first_beat"])
        inp = model_input(cover_frame(c["path_local"]), m["width"], m["height"])
        Image.fromarray(inp).save(jd / "inputs" / f"{jid}.png")
        jobs.append({"id": jid, "beat": c["first_beat"], "beats": c["beats"], "asset": c["asset"],
                     "source_dir": c["source_dir"], "match": c["match"], "kind": c["kind"],
                     "duration_s": c["duration_s"], "input": f"inputs/{jid}.png",
                     "prompt": prompt_for(c["kind"], cfg), "negative": negative_for(c["first_beat"], cfg),
                     "num_frames": frames_for(c["duration_s"], cfg), "width": m["width"], "height": m["height"],
                     "fps": m["fps"], "steps": m["steps"], "guidance": m["guidance"],
                     "seed": int(m.get("seed_overrides", {}).get(c["first_beat"], m["seed"]))})
    write_json(jd / "jobs.json", {"model": m, "jobs": jobs})
    with open(run.path("ai_motion_plan.csv"), "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["beat", "beats", "asset", "match", "kind", "kinds", "duration_s", "score", "sky_frac", "fluid_frac",
                    "faces", "status", "why"])
        for c in cands:
            st = c.get("stats", {})
            w.writerow([c["first_beat"], " ".join(c["beats"]), c["asset"], c["match"], c["kind"], " ".join(c["kinds"]),
                        c["duration_s"], c["score"], st.get("sky_frac", ""), st.get("fluid_frac", ""), st.get("faces", ""),
                        "candidate", ""])
        for r in rejected:
            w.writerow([r["beat"], "", r["asset"], "", "", "", "", "", "", "", "", "rejected", r["why"]])
    items = [{"base": np.asarray(Image.open(jd / "inputs" / f"{j['id']}.png")),
              "caption": f"{j['beat']} {j['kind']} {j['match']} {j['duration_s']} s {j['num_frames']} fr  {j['asset'][:60]}"}
             for j in jobs]
    sheet = contact_sheet(items, run.path("ai_motion_candidates.jpg")) if items else None
    run.log_step("ai_motion_plan", candidates=len(cands), jobs=len(jobs), rejected=len(rejected))
    run.set_status("planned")
    return {"run_id": run.run_id, "jobs": [j["id"] for j in jobs], "jobs_dir": str(jd), "rejected": len(rejected),
            "sheet": str(sheet) if sheet else None,
            "kinds": {k: sum(1 for j in jobs if j["kind"] == k) for k in cfg["kind_order"]}}


def apply_cmd(visuals_csv: str, jobs_json: str, raw_dir: str, out_csv: str, *, run_id: Optional[str] = None,
              cfg_path: Optional[str] = None, kernel_report: Optional[str] = None, fps: int = 25) -> Dict[str, Any]:
    """Raw Kaggle clips -> gate + masked composite (run/ai_motion_clips/AI_<beat>.mp4) + ai_motion_report.csv +
    ai_motion_sheet.jpg; visuals CSV with eye-passed clips (config eye_pass) -> out_csv."""
    from . import beats as B
    from .runs import Run, write_json
    cfg = load_cfg(cfg_path)
    run = Run(run_id)
    run.add_input(visuals_csv, "VISUALS_BEATS")
    run.add_input(jobs_json, "AI_JOBS")
    run.add_input(str(cfg_path or CFG_PATH), "AI_MOTION_CFG")
    rows = B.read_assign_csv(visuals_csv)
    jobs = json.loads(Path(jobs_json).read_text(encoding="utf-8"))["jobs"]
    kt = {}
    if kernel_report and Path(kernel_report).is_file():
        run.add_input(kernel_report, "KERNEL_REPORT")
        kt = {j["id"]: j for j in json.loads(Path(kernel_report).read_text(encoding="utf-8")).get("jobs", [])}
    clips_by_first = {c["first_beat"]: c for c in B.merge_clips(rows)}
    cdir = run.path("ai_motion_clips")
    cdir.mkdir(parents=True, exist_ok=True)
    rep, items = [], []
    eye_rej = cfg.get("eye_rejects", {})
    for j in jobs:
        r: Dict[str, Any] = {"job": j["id"], "beat": j["beat"], "beats": j["beats"], "asset": j["asset"],
                             "source_dir": j["source_dir"], "match": j["match"], "kind": j["kind"],
                             "duration_s": j["duration_s"], "kernel_s": kt.get(j["id"], {}).get("seconds", "")}
        raw = Path(raw_dir) / f"{j['id']}.mp4"
        c = clips_by_first.get(j["beat"])
        if not raw.is_file():
            r.update(status="FAIL", why=["no raw clip from the kernel" + (f" ({kt[j['id']].get('error', '')[:120]})"
                                                                           if j["id"] in kt else "")])
            rep.append(r)
            continue
        if not c or c["asset"] != j["asset"]:
            r.update(status="FAIL", why=["shot changed in the visuals CSV"])
            rep.append(r)
            continue
        n_out = round(c["end"] * fps) - round(c["start"] * fps)
        g = render_clip(ROOT / j["source_dir"] / j["asset"], raw, cdir / f"{j['id']}.mp4", n_out, j["kind"], cfg, fps,
                        limits=cfg.get("mask_keep", {}).get(j["beat"]))
        thumbs, raw0, mimg = g.pop("_thumbs", None), g.pop("_raw0"), g.pop("_mask_img")
        g.pop("warp_list", None)
        g.pop("blob_list", None)
        r.update({k: v for k, v in g.items() if not k.startswith("_")})
        r["eye"] = ("REJECT: " + eye_rej[j["beat"]]) if j["beat"] in eye_rej else \
            ("PASS" if j["beat"] in cfg.get("eye_pass", []) else "pending")
        rep.append(r)
        items.append({"base": model_input(cover_frame(ROOT / j["source_dir"] / j["asset"])), "raw0": raw0,
                      "thumbs": thumbs, "mask": mimg,
                      "caption": f"{j['beat']} {j['kind']} {j['match']} {r['status']} ssim {r.get('ssim_first')} flick "
                                 f"{r.get('flicker_max')} warp {r.get('warp_cells')}/{r.get('rigid_cells')} drift "
                                 f"{r.get('drift_px')} mask {r.get('mask_area')} slow {r.get('slow')} | eye {r['eye']}"})
    write_report(rep, run.path("ai_motion_report.csv"))
    sheet = contact_sheet(items, run.path("ai_motion_sheet.jpg")) if items else None
    eye_ok = [b for b in cfg.get("eye_pass", []) if b not in eye_rej]
    new_rows, info = apply_ai(rows, rep, cdir, eye_ok, cfg["model"]["name"], fps)
    write_assign_ai(new_rows, out_csv)
    run.add_output(out_csv, "visuals_beats_ai")
    if sheet:
        run.add_output(sheet, "ai_motion_sheet")
    for r in rep:
        if r.get("clip"):
            run.add_output(cdir / r["clip"], "ai_motion_clip")
    counts = {s: sum(1 for r in rep if r.get("status") == s) for s in ("PASS", "WARN", "FAIL")}
    write_json(run.path("ai_motion_apply.json"), {"counts": counts, **info})
    run.log_step("ai_motion_apply", **counts, applied=info["ai_clips"])
    run.set_status("done")
    return {"run_id": run.run_id, "counts": counts, "applied": info, "sheet": str(sheet) if sheet else None,
            "report": str(run.path("ai_motion_report.csv")), "out": out_csv}


def write_assign_ai(rows: Sequence[Dict[str, Any]], out: str | Path) -> Path:
    """beats.write_assign_csv + AI columns; motion = ai_animated where an AI clip is on the shot."""
    from . import beats as B
    return B.write_assign_csv(rows, out)
