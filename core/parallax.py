"""2.5D parallax layer (0.7.0-dev): one still -> depth map -> slow depth-based camera move -> MP4.

Depth: Depth Anything V2 Small (hf:depth-anything/Depth-Anything-V2-Small-hf, Apache-2.0, 24.8M params, CPU),
revision pinned in MODEL_REV / config/model_licenses.json. Base/Large are CC-BY-NC and are never used.
Depth maps are cached under assets/depth_cache/<image sha256>_<rev8>.npz, so a still is estimated once.

Renderer (own code, numpy + OpenCV remap, frames piped to FFmpeg). The approach was studied from
longweekendlabs/parallax-studio (MIT) @ 32e4cb451abf117a148594269219691f7144ce88 (app/core/animator.py,
app/core/depth_model.py): backward remap where every output pixel samples the source at
  grid - influence * d - (grid - centre) * zoom * influence,  influence = (depth - focus) * 2,
a gradient-weighted feather of the depth map so silhouettes do not tear, and the fold rule (the sampling grid
must never run backwards). No file of that project is copied. Backward warping leaves no holes; what would be a
disocclusion shows up as local stretch at depth edges, which the gate measures. Samples outside the photo use a
mirror pad (BORDER_REFLECT_101) and are counted (black_border gate).

Quality gate per clip (status PASS / WARN / FAIL):
  fold      : Jacobian of the sampling map <= 0.05 anywhere at the extreme frames  -> tearing (FAIL)
  stretch   : share of pixels whose local scale departs > 25 % from the frame's global scale -> rubber-sheet look
  border    : share of samples that fall outside the photo (mirror-padded) + near-black frame edges
  smooth    : frame-to-frame luma change series (max/median, spike vs neighbours)
A FAIL clip is retried once at 0.6x strength; if it still fails, the timeline keeps the existing Ken Burns still.
Labels never change: a parallax clip carries its photo's match label plus motion = parallax_2_5d (depth-based
motion of a real photo, not AI-generated imagery).
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import statistics
import subprocess
import time
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
MODEL_ID = "depth-anything/Depth-Anything-V2-Small-hf"
MODEL_REV = "5426e4f0f36572d16453bbda7a8389317b1bef99"
FORBIDDEN_MODELS = ("Depth-Anything-V2-Base", "Depth-Anything-V2-Large")  # CC-BY-NC
CACHE_DIR = ROOT / "assets" / "depth_cache"
MOVES = ("dolly", "pan", "zoom")
MOTION_LABEL = "parallax_2_5d"
NO_PARALLAX_MATCH = ("text_card", "archival")  # cards / labelled archival keep Ken Burns (text must not warp)
DEPTH_LONG_SIDE = 768  # cached depth resolution (long side); upsampled at render time

FEATHER_PASSES = (6.0, 14.0, 28.0)  # depth feather sigma (depth-map px at DEPTH_LONG_SIDE)
GATE = {"fold_j": 0.05, "stretch_dev": 0.25, "stretch_warn": 0.001, "stretch_fail": 0.012,
        "oob_warn": 0.0005, "oob_fail": 0.004, "jitter_ratio_fail": 3.5, "spike_fail": 2.5}
REPORT_COLUMNS = ["clip", "beat", "scene", "asset", "source_dir", "match", "duration_s", "move", "strength", "edge_sigma",
                  "status", "fold_px", "stretch_frac", "max_dev", "oob_frac", "edge_black", "jitter_ratio",
                  "spike", "path_smooth", "luma_diff_max", "frames", "render_s", "render_s_per_video_s", "parallax_clip", "fallback", "notes"]


# --------------------------------------------------------------------------- depth
def sha256_bytes(path: str | Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load_rgb(path: str | Path) -> np.ndarray:
    from PIL import Image
    with Image.open(path) as im:
        return np.asarray(im.convert("RGB"))


class HFDepth:
    """Lazy transformers estimator, CPU, pinned revision. Only the Small (Apache-2.0) model is allowed."""

    def __init__(self, model_id: str = MODEL_ID, revision: str = MODEL_REV, threads: Optional[int] = None):
        if any(f in model_id for f in FORBIDDEN_MODELS):
            raise ValueError(f"{model_id} is CC-BY-NC; KANG uses only {MODEL_ID}")
        self.model_id, self.revision, self.threads = model_id, revision, threads
        self._proc = self._model = None

    def __call__(self, rgb: np.ndarray) -> np.ndarray:
        import torch
        from PIL import Image
        from transformers import AutoImageProcessor, AutoModelForDepthEstimation
        if self.threads:
            torch.set_num_threads(self.threads)
        if self._model is None:
            self._proc = AutoImageProcessor.from_pretrained(self.model_id, revision=self.revision)
            self._model = AutoModelForDepthEstimation.from_pretrained(self.model_id, revision=self.revision).eval()
        h, w = rgb.shape[:2]
        k = min(1.0, 1280 / max(h, w))
        im = Image.fromarray(rgb)
        if k < 1.0:
            im = im.resize((round(w * k), round(h * k)), Image.BILINEAR)
        with torch.inference_mode():
            pred = self._model(**self._proc(images=im, return_tensors="pt")).predicted_depth  # (1, h', w') relative inverse depth
        return pred[0].float().numpy()


def normalize_depth(raw: np.ndarray) -> np.ndarray:
    """Robust 0..1, 1 = near (DA-V2 predicts relative inverse depth: larger = closer)."""
    lo, hi = np.percentile(raw, 1.0), np.percentile(raw, 99.0)
    if hi - lo < 1e-6:
        return np.full(raw.shape, 0.5, np.float32)
    return np.clip((raw - lo) / (hi - lo), 0.0, 1.0).astype(np.float32)


def depth_for(path: str | Path, estimator: Optional[Callable[[np.ndarray], np.ndarray]] = None,
              cache_dir: Optional[str | Path] = None, model_rev: str = MODEL_REV) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Depth map (float32 0..1, near=1) at DEPTH_LONG_SIDE, cached by image sha256 + model revision."""
    import cv2
    cache = Path(cache_dir or CACHE_DIR)
    sha = sha256_bytes(path)
    cf = cache / f"{sha}_{model_rev[:8]}.npz"
    if cf.is_file():
        z = np.load(cf, allow_pickle=False)
        return z["depth"].astype(np.float32), {"cache": "hit", "cache_file": str(cf), "image_sha256": sha,
                                                 "model_revision": model_rev, "depth_s": 0.0}
    rgb = load_rgb(path)
    t = time.time()
    raw = (estimator or HFDepth())(rgb)
    dt = time.time() - t
    h, w = rgb.shape[:2]
    k = DEPTH_LONG_SIDE / max(h, w)
    size = (max(1, round(w * k)), max(1, round(h * k)))
    d = normalize_depth(cv2.resize(raw.astype(np.float32), size, interpolation=cv2.INTER_CUBIC))
    cache.mkdir(parents=True, exist_ok=True)
    tmp = cf.with_name(cf.stem + ".tmp.npz")
    np.savez_compressed(tmp, depth=d.astype(np.float16), image_sha256=np.array(sha), model=np.array(MODEL_ID),
                        revision=np.array(model_rev), image_size=np.array([w, h]))
    os.replace(tmp, cf)
    return d, {"cache": "miss", "cache_file": str(cf), "image_sha256": sha, "model_revision": model_rev,
               "depth_s": round(dt, 2)}


def soften_depth(depth: np.ndarray, edge_sigma: float = 6.0, base_sigma: float = 1.5, grad_thr: float = 0.02) -> np.ndarray:
    """Gradient-weighted feather (idea: parallax-studio soften_for_parallax): steep depth steps get a wide blur,
    flat areas only a light one, so silhouettes stretch smoothly instead of tearing."""
    import cv2
    d = cv2.GaussianBlur(depth.astype(np.float32), (0, 0), base_sigma)
    gx = cv2.Sobel(d, cv2.CV_32F, 1, 0, ksize=3) / 8.0
    gy = cv2.Sobel(d, cv2.CV_32F, 0, 1, ksize=3) / 8.0
    g = np.sqrt(gx * gx + gy * gy)
    wgt = np.clip(g / grad_thr, 0.0, 1.0)
    wgt = cv2.dilate(wgt, np.ones((5, 5), np.uint8))
    wgt = cv2.GaussianBlur(wgt, (0, 0), edge_sigma * 0.6)
    wide = cv2.GaussianBlur(d, (0, 0), edge_sigma)
    return (d * (1.0 - wgt) + wide * wgt).astype(np.float32)


# --------------------------------------------------------------------------- camera
def ease(p: float) -> float:
    p = min(1.0, max(0.0, p))
    return 0.5 - 0.5 * math.cos(math.pi * p)


def camera(move: str, p: float, strength: float = 1.0, direction: int = 1) -> Dict[str, float]:
    """Camera state at progress p. s = global scale over cover-fit; tx = global shift (fraction of frame width);
    par = depth-dependent horizontal shift (fraction of width at influence 1); parz = depth-dependent zoom."""
    if move not in MOVES:
        raise ValueError(f"move must be one of {MOVES}")
    e = ease(p)
    st = max(0.0, float(strength))
    if move == "dolly":   # push in: near layers grow faster than far ones, slight sideways drift
        return {"s": 1.05 + 0.05 * st * e, "tx": 0.0, "par": direction * 0.006 * st * (e - 0.5) * 2,
                "parz": 0.028 * st * e}
    if move == "pan":     # sideways truck: near layers slide more than far ones
        return {"s": 1.07, "tx": direction * 0.010 * st * (e - 0.5) * 2, "par": direction * 0.014 * st * (e - 0.5) * 2,
                "parz": 0.0}
    return {"s": 1.10 - 0.05 * st * e, "tx": 0.0, "par": 0.0, "parz": 0.022 * st * (1.0 - e)}  # zoom: pull out


class Warper:
    """Prepared source (cover-fit, pre-scaled once) + softened depth at the same size; frame(p) -> RGB uint8."""

    def __init__(self, rgb: np.ndarray, depth: np.ndarray, w: int, h: int, move: str = "dolly",
                 strength: float = 1.0, direction: int = 1, focus: Optional[float] = None, soften: bool = True,
                 edge_sigma: float = 6.0):
        import cv2
        self.w, self.h, self.move, self.strength, self.direction = w, h, move, strength, direction
        self.edge_sigma = edge_sigma
        ih, iw = rgb.shape[:2]
        k = max(w / iw, h / ih)
        smax = max(camera(move, p, strength, direction)["s"] for p in (0.0, 1.0))
        q = k * smax  # pre-scale once so the tightest frame samples the source 1:1
        self.q, self.k = q, k
        sw, sh = max(1, round(iw * q)), max(1, round(ih * q))
        interp = cv2.INTER_AREA if q < 1.0 else cv2.INTER_CUBIC
        self.src = np.ascontiguousarray(cv2.resize(rgb, (sw, sh), interpolation=interp)) if (sw, sh) != (iw, ih) else rgb
        d = soften_depth(depth, edge_sigma=edge_sigma, base_sigma=max(1.5, edge_sigma / 4)) if soften else depth.astype(np.float32)
        self.depth = cv2.resize(d, (sw, sh), interpolation=cv2.INTER_LINEAR)
        self.focus = float(np.percentile(self.depth, 40)) if focus is None else focus
        self.infl_full = (self.depth - self.focus) * 2.0
        self.sw, self.sh = sw, sh
        yy, xx = np.indices((h, w), dtype=np.float32)
        self.uc, self.vc = xx - w / 2.0, yy - h / 2.0

    def maps(self, p: float) -> Tuple[np.ndarray, np.ndarray, float]:
        import cv2
        c = camera(self.move, p, self.strength, self.direction)
        r = self.q / (self.k * c["s"])  # source px per output px
        cx, cy = self.sw / 2.0, self.sh / 2.0
        gx = cx + (self.uc - c["tx"] * self.w) * r
        gy = cy + self.vc * r
        infl = cv2.remap(self.infl_full, gx, gy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)
        mx = gx - infl * (c["par"] * self.w * r) - (gx - cx) * (c["parz"] * infl)
        my = gy - (gy - cy) * (c["parz"] * infl)
        return mx.astype(np.float32), my.astype(np.float32), r

    def frame_flat(self, p: float) -> np.ndarray:
        """Same camera, no depth term (= what a plain crop/zoom shows): reference for the border check."""
        import cv2
        c = camera(self.move, p, self.strength, self.direction)
        r = self.q / (self.k * c["s"])
        gx = (self.sw / 2.0 + (self.uc - c["tx"] * self.w) * r).astype(np.float32)
        gy = (self.sh / 2.0 + self.vc * r).astype(np.float32)
        return cv2.remap(self.src, gx, gy, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)

    def frame(self, p: float) -> np.ndarray:
        import cv2
        mx, my, _ = self.maps(p)
        return cv2.remap(self.src, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT_101)


# --------------------------------------------------------------------------- gate
def geometry_check(warper: Warper, ps: Sequence[float] = (0.0, 0.5, 1.0)) -> Dict[str, Any]:
    """Fold / stretch / out-of-photo share from the sampling maps themselves (exact, no image heuristics).
    Local scale = Jacobian of the map divided by the frame's global scale r; 1.0 = same as a plain Ken Burns.
    The departure |J/r - 1| is the 'displacement vs depth edge strength' measure: d(displacement)/dx."""
    fold = 0
    stretch, maxdev, oob = 0.0, 0.0, 0.0
    for p in ps:
        mx, my, r = warper.maps(p)
        jx = np.diff(mx, axis=1)[:-1, :] / r
        jy = np.diff(my, axis=0)[:, :-1] / r
        fold += int((jx <= GATE["fold_j"]).sum() + (jy <= GATE["fold_j"]).sum())
        dev = np.maximum(np.abs(jx - 1.0), np.abs(jy - 1.0))
        stretch = max(stretch, float((dev > GATE["stretch_dev"]).mean()))
        maxdev = max(maxdev, float(np.percentile(dev, 99.99)))
        out = (mx < 0) | (mx > warper.sw - 1) | (my < 0) | (my > warper.sh - 1)
        oob = max(oob, float(out.mean()))
    return {"fold_px": fold, "stretch_frac": round(stretch, 5), "max_dev": round(maxdev, 3), "oob_frac": round(oob, 5)}


def edge_black(frame: np.ndarray, ref: Optional[np.ndarray] = None, band: int = 3, thr: float = 10.0) -> bool:
    """True if a frame edge band is near-black while the frame centre is not (a black border). With `ref`
    (the same camera without depth, frame_flat) a band that is dark in the photo itself (night silhouette,
    dark foreground) is not a border."""
    lum = frame.mean(axis=2)
    centre = lum[lum.shape[0] // 4: 3 * lum.shape[0] // 4, lum.shape[1] // 4: 3 * lum.shape[1] // 4].mean()
    if centre < thr * 2:
        return False
    sl = (np.s_[:band], np.s_[-band:], np.s_[:, :band], np.s_[:, -band:])
    rl = ref.mean(axis=2) if ref is not None else None
    return any(lum[k].mean() < thr and (rl is None or rl[k].mean() >= thr * 2) for k in sl)


def smoothness(diffs: Sequence[float], floor: float = 1.0) -> Dict[str, float]:
    """diffs = mean |luma(t) - luma(t-1)| per frame (0..255). Eased camera -> a smooth hump; jitter -> spikes.
    ratio = max/median; spike = largest value vs the mean of its two neighbours. Values below `floor` luma levels
    are ignored: OpenCV remap quantises sample positions to 1/32 px, so a very slow move steps in 1/32-px jumps
    that change the frame by < 0.5 levels (not visible) but would look like spikes to a relative measure."""
    d = [float(x) for x in diffs]
    if len(d) < 3 or max(d) < floor:
        return {"ratio": 0.0, "spike": 0.0, "median": round(statistics.median(d), 4) if d else 0.0,
                "max": round(max(d), 4) if d else 0.0}
    med = statistics.median(d)
    spikes = [d[i] / max(1e-6, (d[i - 1] + d[i + 1]) / 2) for i in range(1, len(d) - 1) if d[i] >= floor]
    return {"ratio": round(max(d) / med, 2) if med > 1e-6 else 0.0, "spike": round(max(spikes), 2) if spikes else 0.0,
            "median": round(med, 4), "max": round(max(d), 4)}


def path_smoothness(move: str, strength: float, direction: int, n: int) -> float:
    """Camera path check (exact): max |second difference| / max |first difference| over the camera parameters
    across the n frames. An eased path gives ~pi/n; a jump or a restart gives ~1 or more."""
    keys = ("s", "tx", "par", "parz")
    cs = [camera(move, (i + 0.5) / n if n > 1 else 0.0, strength, direction) for i in range(max(n, 3))]
    worst = 0.0
    for k in keys:
        v = np.array([c[k] for c in cs])
        d1 = np.diff(v)
        if np.abs(d1).max() < 1e-12:
            continue
        worst = max(worst, float(np.abs(np.diff(d1)).max() / np.abs(d1).max()))
    return round(worst, 4)


def gate_status(geo: Dict[str, Any], smooth: Dict[str, float], black: bool) -> Tuple[str, List[str]]:
    why_fail, why_warn = [], []
    if geo["fold_px"] > 0:
        why_fail.append(f"fold {geo['fold_px']} px (tearing)")
    if geo["stretch_frac"] > GATE["stretch_fail"]:
        why_fail.append(f"stretch {geo['stretch_frac']:.2%} > {GATE['stretch_fail']:.1%}")
    elif geo["stretch_frac"] > GATE["stretch_warn"]:
        why_warn.append(f"stretch {geo['stretch_frac']:.2%}")
    if geo["oob_frac"] > GATE["oob_fail"]:
        why_fail.append(f"outside photo {geo['oob_frac']:.2%} (mirror pad visible)")
    elif geo["oob_frac"] > GATE["oob_warn"]:
        why_warn.append(f"outside photo {geo['oob_frac']:.3%} (mirror pad)")
    if black:
        why_fail.append("black frame edge")
    if smooth.get("path", 0) > 0.25:
        why_fail.append(f"camera path not smooth ({smooth['path']})")
    if smooth.get("max", 0) >= 1.0 and smooth.get("ratio", 0) > GATE["jitter_ratio_fail"]:
        why_fail.append(f"jitter ratio {smooth['ratio']}")
    if smooth.get("spike", 0) > GATE["spike_fail"]:
        why_fail.append(f"frame spike {smooth['spike']}")
    if why_fail:
        return "FAIL", why_fail + why_warn
    return ("WARN" if why_warn else "PASS"), why_warn


# --------------------------------------------------------------------------- render
def render(img: str | Path, out: str | Path, dur: float, *, move: str = "dolly", strength: float = 1.0,
           direction: int = 1, w: int = 1920, h: int = 1080, fps: int = 25, crf: int = 18,
           estimator: Optional[Callable[[np.ndarray], np.ndarray]] = None, cache_dir: Optional[str | Path] = None,
           depth: Optional[np.ndarray] = None, frames: Optional[int] = None, retry: bool = True,
           alt_moves: Sequence[Tuple[str, int]] = ()) -> Dict[str, Any]:
    """Render one parallax clip (video only, H.264, yuv420p). Gate runs on the maps before rendering; a FAIL is
    retried once at 0.6x strength, then given up (no file written, caller keeps Ken Burns)."""
    t0 = time.time()
    dinfo: Dict[str, Any] = {}
    if depth is None:
        depth, dinfo = depth_for(img, estimator, cache_dir)
    rgb = load_rgb(img)
    n = int(frames if frames is not None else round(dur * fps))
    # fold relaxation (idea: parallax-studio relax_paint_folds): wider depth feather first, then less strength.
    # The first setting whose map pre-check is PASS wins; if none, the first WARN; else the clip FAILs.
    tries = [(strength, sg) for sg in FEATHER_PASSES] + ([(round(strength * 0.6, 3), FEATHER_PASSES[-1])] if retry else [])
    res: Dict[str, Any] = {}
    pre_fail: List[str] = []
    pick = choose_setting(rgb, depth, w, h, move, direction, tries)
    pre_fail = list(pick["log"])
    for mv2, dr2 in alt_moves:  # the assigned move cannot pass: try the other camera moves (same photo)
        if pick["status"] == "PASS":
            break
        alt = choose_setting(rgb, depth, w, h, mv2, dr2, tries)
        pre_fail += [f"alt {mv2}: " + x for x in alt["log"]]
        if alt["status"] == "PASS" or (alt["status"] == "WARN" and pick["status"] == "FAIL"):
            pre_fail.append(f"move {move} -> {mv2} ({alt['status']})")
            pick, move, direction = alt, mv2, dr2
    if pick["status"] == "FAIL":
        res = {"move": move, "strength": tries[-1][0], "edge_sigma": tries[-1][1], "frames": n, "fps": fps, "width": w,
               "height": h, **pick["geo"], **dinfo, "status": "FAIL", "notes": pre_fail, "total_s": round(time.time() - t0, 2)}
        return res
    for st, sg in [(pick["strength"], pick["edge_sigma"])]:
        wp = pick["warper"]
        geo = pick["geo"]
        res = {"move": move, "strength": st, "edge_sigma": sg, "frames": n, "fps": fps, "width": w, "height": h,
               **geo, **dinfo, "focus": round(wp.focus, 3)}
        out = Path(out)
        out.parent.mkdir(parents=True, exist_ok=True)
        import tempfile
        tmpd = Path(tempfile.mkdtemp(prefix="kang_px_"))  # encode on local disk, then move (network FS + faststart)
        tmp = tmpd / out.name
        proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                                 "-s", f"{w}x{h}", "-r", str(fps), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                                 "-crf", str(crf), "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(tmp)],
                                stdin=subprocess.PIPE)
        diffs, prev, black = [], None, False
        tr = time.time()
        try:
            for i in range(n):
                fr = wp.frame((i + 0.5) / n if n > 1 else 0.0)
                proc.stdin.write(fr.tobytes())
                small = fr[::4, ::4].mean(axis=2)
                if prev is not None:
                    diffs.append(float(np.abs(small - prev).mean()))
                prev = small
                if i in (0, n // 2, n - 1):
                    black = black or edge_black(fr, wp.frame_flat((i + 0.5) / n if n > 1 else 0.0))
        finally:
            proc.stdin.close()
            rc = proc.wait()
        if rc != 0:
            raise RuntimeError(f"ffmpeg encode failed ({rc}) for {out}")
        sm = smoothness(diffs)
        sm["path"] = path_smoothness(move, st, direction, n)
        status, why = gate_status(geo, sm, black)
        rs = time.time() - tr
        res.update(status=status, notes=(why + ([f"relaxed: tried {'; '.join(pre_fail)}"] if pre_fail else [])),
                   jitter_ratio=sm["ratio"], spike=sm["spike"], path_smooth=sm["path"],
                   luma_diff_max=sm["max"], edge_black=black,
                   render_s=round(rs, 2), render_s_per_video_s=round(rs / max(1e-6, n / fps), 3))
        if status == "FAIL":
            tmp.unlink(missing_ok=True)
            continue  # pragma: no cover - pre-check already chose a passing setting
        import shutil
        shutil.move(str(tmp), str(out))
        shutil.rmtree(tmpd, ignore_errors=True)
        res["file"] = str(out)
        break
    res["total_s"] = round(time.time() - t0, 2)
    return res


def choose_setting(rgb: np.ndarray, depth: np.ndarray, w: int, h: int, move: str, direction: int,
                   tries: Sequence[Tuple[float, float]]) -> Dict[str, Any]:
    """Map pre-check over (strength, feather) settings in order: first PASS, else first WARN, else FAIL."""
    log, first_warn, last = [], None, None
    for st, sg in tries:
        wp = Warper(rgb, depth, w, h, move, st, direction, edge_sigma=sg)
        geo = geometry_check(wp)
        status, why = gate_status(geo, {}, False)
        cand = {"status": status, "strength": st, "edge_sigma": sg, "geo": geo, "warper": wp, "why": why}
        last = cand
        if status == "PASS":
            cand["log"] = log
            return cand
        log.append(f"s{st}/f{sg:g} {status}: " + ", ".join(why))
        if status == "WARN" and first_warn is None:
            first_warn = cand
    out = first_warn or last
    out["log"] = log
    return out


def ken_burns_frames(img: str | Path, dur_frames: int, w: int, h: int, k: int = 0, match: str = "exact"):
    """Reference Ken Burns (same motion as the package/preview) as a frame generator, for A/B."""
    from . import beats as B
    m = B.motion_for(k, match)
    src = B._cover_source(img, w, h, m["smax"])
    for i in range(dur_frames):
        yield np.asarray(B.frame_at(src, m, (i + 0.5) / dur_frames, w, h))


# --------------------------------------------------------------------------- selection / integration
def select_clips(rows: Sequence[Dict[str, Any]], min_hold: float = 6.0) -> List[Dict[str, Any]]:
    """Clips (merged beats) that get a parallax attempt: hold >= min_hold s or containing a continued_with_motion
    beat; never text cards / labelled archival."""
    from . import beats as B
    roles = {r["beat"]: r["role"] for r in rows}
    out = []
    for k, c in enumerate(B.merge_clips(rows)):
        if c["match"] in NO_PARALLAX_MATCH:
            continue
        cwm = any(roles.get(b) == "continued_with_motion" for b in c["beats"])
        if c["end"] - c["start"] >= min_hold - 1e-6 or cwm:
            out.append({**c, "index": k, "continued_with_motion": cwm})
    return out


def move_for(k: int) -> Tuple[str, int]:
    """Alternate moves along the timeline so consecutive parallax clips do not repeat the same push."""
    seq = [("dolly", 1), ("pan", 1), ("dolly", -1), ("pan", -1), ("zoom", 1)]
    return seq[k % len(seq)]


def clip_name(asset: str) -> str:
    return "PX_" + Path(asset).stem + ".mp4"


def write_report(rows: Sequence[Dict[str, Any]], path: str | Path) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8-sig", newline="") as fh:
        wr = csv.DictWriter(fh, REPORT_COLUMNS, extrasaction="ignore")
        wr.writeheader()
        for r in rows:
            wr.writerow({**r, "notes": "; ".join(r["notes"]) if isinstance(r.get("notes"), list) else r.get("notes", "")})
    return p


def read_report(path: str | Path) -> List[Dict[str, str]]:
    with open(path, encoding="utf-8-sig", newline="") as fh:
        return [dict(r) for r in csv.DictReader(fh)]


def apply_parallax(rows: Sequence[Dict[str, Any]], report: Sequence[Dict[str, str]], clips_dir: str | Path,
                   frames_tol: int = 0, fps: int = 25) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """Mark beats whose clip has a gate-passed parallax render: motion = parallax_2_5d, parallax_clip = file name,
    parallax_dir = folder. asset / match / licence stay the photo's own (same label, no new asset, no repeat).
    Only PASS/WARN rows with an existing file are used; the clip must cover exactly the same beats."""
    from . import beats as B
    ok = {(r["beat"], r["asset"]): r for r in report if r["status"] in ("PASS", "WARN") and r.get("parallax_clip")}
    cdir = Path(clips_dir)
    out = [dict(r) for r in rows]
    by_beat = {r["beat"]: r for r in out}
    used, skipped = [], []
    for c in B.merge_clips(out):
        rep = ok.get((c["first_beat"], c["asset"]))
        if not rep:
            continue
        f = cdir / rep["parallax_clip"]
        want = round(c["end"] * fps) - round(c["start"] * fps)
        if not f.is_file():
            skipped.append(f"{c['first_beat']}: file missing")
            continue
        if c["match"] in NO_PARALLAX_MATCH:
            skipped.append(f"{c['first_beat']}: {c['match']} keeps Ken Burns")
            continue
        if abs(int(rep.get("frames") or want) - want) > frames_tol:
            skipped.append(f"{c['first_beat']}: frame count differs")
            continue
        for b in c["beats"]:
            by_beat[b].update(motion=MOTION_LABEL, parallax_clip=rep["parallax_clip"], parallax_dir=str(cdir),
                              parallax_status=rep["status"])
        used.append(c["first_beat"])
    return out, {"parallax_clips": len(used), "used": used, "skipped": skipped}
