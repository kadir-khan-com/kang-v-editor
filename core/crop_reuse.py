"""v14 crop reuse (user decision 2026-11-04 07:37): the same photo may appear again, but only as a distinctly
different framing (e.g. the full temple first, later only the spire).

Rules (config/beat_rules.json -> crop_reuse):
- a reuse = a 16:9 crop of a still that is already on the timeline, written as a NEW derived file
  (runs/<run>/crop_reuse/CR_<beat>_<stem>.jpg) so the Premiere timeline never shows the same file twice;
- crop area <= 50 % of the first framing (the 16:9 cover view the first appearance shows), IoU with every earlier
  framing of the same photo (first framing + earlier crops) <= 0.3, crop >= 1280 px wide (1080p), else skipped;
- the reuse comes after the first appearance and is >= 4 beats away from every appearance of that photo; max 2 reuses;
- crop region chosen by detail: spectral-residual saliency (numpy, Hou & Zhang 2007) + Canny edge density; crops that
  touch a detected face (OpenCV YuNet) are refused; blurry / flat (sky, wall) crops are refused;
- only replaces (a) continued_with_motion beats and (b) representative beats whose narration names a place we have
  an exact photo for. Exact shots, text cards, maps, archival are never replaced. A beat in the middle of a multi-beat
  clip is not replaced (it would split one clip into two copies of the same file).
- label = the photo's own label (exact / representative); row gets reuse=crop_reuse + crop_box; credit says crop =
  modification of the original photo.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple

import numpy as np

from . import beats as B

ROOT = Path(__file__).resolve().parent.parent
FACE_MODEL = ROOT / "tools" / "models" / "face_detection_yunet_2023mar.onnx"
CROP_COLUMNS = ["reuse", "reuse_of", "crop_box"]
IMG_EXT = {".jpg", ".jpeg", ".png"}
DEFAULTS = {"max_area_ratio": 0.5, "max_iou": 0.3, "min_beats_apart": 4, "max_reuses_per_asset": 2,
            "min_crop_width": 1280, "aspect": [16, 9], "min_laplacian_var": 40.0, "min_edge_density": 0.03,
            "max_sky_fraction": 0.55, "min_score": 0.0, "step_px": 32, "width_steps": [1.0, 1.1, 1.2],
            "face_score": 0.75, "require_face_detector": True, "continued_exact_needs_exact": True, "replace_roles": ["continued_with_motion"],
            "never_replace_match": ["exact", "text_card", "map", "archival"], "extra_places": {}, "rejects": {}}


def settings(rules: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    rules = rules if rules is not None else B.load_rules()
    return {**DEFAULTS, **rules.get("crop_reuse", {})}


# --------------------------------------------------------------------------- geometry
Box = Tuple[int, int, int, int]  # x, y, w, h in original image pixels


def iou(a: Box, b: Box) -> float:
    ax0, ay0, aw, ah = a
    bx0, by0, bw, bh = b
    iw = max(0, min(ax0 + aw, bx0 + bw) - max(ax0, bx0))
    ih = max(0, min(ay0 + ah, by0 + bh) - max(ay0, by0))
    inter = iw * ih
    u = aw * ah + bw * bh - inter
    return inter / u if u else 0.0


def first_framing(iw: int, ih: int, focus: Optional[Sequence[float]] = None, aspect=(16, 9)) -> Box:
    """The 16:9 cover view a still shows on its first appearance (motion starts / ends at scale 1.0 = this view)."""
    ar = aspect[0] / aspect[1]
    if iw / ih >= ar:
        w, h = round(ih * ar), ih
    else:
        w, h = iw, round(iw / ar)
    fx, fy = (focus or (0.5, 0.5))
    x = int(round(min(max(fx * iw - w / 2, 0), iw - w)))
    y = int(round(min(max(fy * ih - h / 2, 0), ih - h)))
    return (x, y, w, h)


def candidate_boxes(iw: int, ih: int, earlier: Sequence[Box], cfg: Dict[str, Any]) -> List[Box]:
    """Every 16:9 window (>= min width) that passes area <= max_area_ratio * first framing and IoU <= max_iou with
    each earlier framing."""
    ar = cfg["aspect"][0] / cfg["aspect"][1]
    first = earlier[0]
    area0 = first[2] * first[3]
    out: List[Box] = []
    for f in cfg["width_steps"]:
        w = int(round(cfg["min_crop_width"] * f))
        h = int(round(w / ar))
        if w > iw or h > ih or w * h > cfg["max_area_ratio"] * area0 + 1e-6:
            continue
        step = cfg["step_px"]
        xs = sorted(set(list(range(0, iw - w + 1, step)) + [iw - w]))
        ys = sorted(set(list(range(0, ih - h + 1, step)) + [ih - h]))
        for y in ys:
            for x in xs:
                b = (x, y, w, h)
                if all(iou(b, e) <= cfg["max_iou"] + 1e-9 for e in earlier):
                    out.append(b)
    return out


# --------------------------------------------------------------------------- image analysis
def spectral_residual(gray: np.ndarray, size: int = 128) -> np.ndarray:
    """Spectral-residual saliency (Hou & Zhang 2007), returned at the input size, 0..1."""
    import cv2
    h, w = gray.shape
    k = size / max(h, w)
    small = cv2.resize(gray, (max(8, int(w * k)), max(8, int(h * k))), interpolation=cv2.INTER_AREA).astype(np.float32)
    f = np.fft.fft2(small)
    amp = np.log(np.abs(f) + 1e-8)
    ph = np.angle(f)
    resid = amp - cv2.blur(amp, (3, 3))
    sal = np.abs(np.fft.ifft2(np.exp(resid + 1j * ph))) ** 2
    sal = cv2.GaussianBlur(sal.astype(np.float32), (0, 0), 2.5)
    sal = cv2.resize(sal, (w, h), interpolation=cv2.INTER_LINEAR)
    m = float(sal.max())
    return sal / m if m > 0 else sal


class Analysis:
    """Per-image maps at a working width (default 480 px) + full-res gray for the blur test."""

    def __init__(self, path: str | Path, work_w: int = 480, face_detector: Optional[Callable] = None):
        import cv2
        img = cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError(f"cannot read image {path}")
        self.img = img
        self.ih, self.iw = img.shape[:2]
        self.k = work_w / self.iw
        small = cv2.resize(img, (work_w, max(1, int(round(self.ih * self.k)))), interpolation=cv2.INTER_AREA)
        g = cv2.cvtColor(small, cv2.COLOR_BGR2GRAY)
        self.sal = spectral_residual(g)
        self.edges = (cv2.Canny(g, 60, 160) > 0).astype(np.float32)
        hsv = cv2.cvtColor(small, cv2.COLOR_BGR2HSV)
        grad = cv2.blur(np.abs(cv2.Laplacian(g, cv2.CV_32F)), (7, 7))
        # sky-like: smooth AND (bright or blue-ish hue); flat sky / haze / plain wall all fall in here
        blue = (hsv[..., 0] > 85) & (hsv[..., 0] < 135) & (hsv[..., 1] > 25)
        self.sky = ((grad < 4.0) & ((hsv[..., 2] > 150) | blue)).astype(np.float32)
        self.gray_full = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.faces: List[Box] = []
        self.face_status = "not_run"
        if face_detector is not None:
            self.faces = list(face_detector(img))
            self.face_status = "checked"

    def _win(self, m: np.ndarray, b: Box) -> np.ndarray:
        x, y, w, h = (int(round(v * self.k)) for v in b)
        return m[y:y + max(1, h), x:x + max(1, w)]

    def measure(self, b: Box) -> Dict[str, float]:
        import cv2
        x, y, w, h = b
        lap = float(cv2.Laplacian(self.gray_full[y:y + h, x:x + w], cv2.CV_64F).var())
        return {"saliency": float(self._win(self.sal, b).mean()), "edges": float(self._win(self.edges, b).mean()),
                "sky": float(self._win(self.sky, b).mean()), "lap_var": lap}

    def touches_face(self, b: Box, frac: float = 0.2) -> bool:
        for f in self.faces:
            fa = f[2] * f[3]
            if fa and iou_inter(b, f) / fa > frac:
                return True
        return False


def iou_inter(a: Box, b: Box) -> float:
    iw = max(0, min(a[0] + a[2], b[0] + b[2]) - max(a[0], b[0]))
    ih = max(0, min(a[1] + a[3], b[1] + b[3]) - max(a[1], b[1]))
    return float(iw * ih)


def yunet_detector(model: Path = FACE_MODEL, score: float = 0.75) -> Optional[Callable]:
    """OpenCV YuNet face detector (MIT, opencv_zoo). Returns None when the model file / API is missing."""
    try:
        import cv2
        if not Path(model).is_file() or not hasattr(cv2, "FaceDetectorYN"):
            return None
    except Exception:  # pragma: no cover
        return None

    try:  # OpenCV 5 prints a harmless backend warning on every create(); create once, quiet
        cv2.utils.logging.setLogLevel(cv2.utils.logging.LOG_LEVEL_ERROR)
    except Exception:  # pragma: no cover
        pass
    det = cv2.FaceDetectorYN.create(str(model), "", (320, 320), score)

    def detect(img) -> List[Box]:
        h, w = img.shape[:2]
        k = min(1.0, 1280 / max(h, w))
        sm = cv2.resize(img, (int(w * k), int(h * k))) if k < 1.0 else img
        det.setInputSize((sm.shape[1], sm.shape[0]))
        _, faces = det.detect(sm)
        out = []
        for f in (faces if faces is not None else []):
            x, y, fw, fh = (float(v) / k for v in f[:4])
            out.append((int(x), int(y), int(fw), int(fh)))
        return out
    return detect


def best_crop(an: Analysis, earlier: Sequence[Box], cfg: Dict[str, Any]) -> Dict[str, Any]:
    """-> {box, score, metrics} or {box: None, reason, tried}."""
    boxes = candidate_boxes(an.iw, an.ih, earlier, cfg)
    if not boxes:
        return {"box": None, "reason": f"no 16:9 window >= {cfg['min_crop_width']} px wide with area <= "
                                       f"{cfg['max_area_ratio']:.0%} of the first framing and IoU <= {cfg['max_iou']} "
                                       f"(image {an.iw}x{an.ih})", "tried": 0}
    why: Dict[str, int] = {}
    best = None
    for b in boxes:
        if an.touches_face(b):
            why["face"] = why.get("face", 0) + 1
            continue
        m = an.measure(b)
        if m["sky"] > cfg["max_sky_fraction"]:
            why["sky_or_flat"] = why.get("sky_or_flat", 0) + 1
            continue
        if m["edges"] < cfg["min_edge_density"]:
            why["low_detail"] = why.get("low_detail", 0) + 1
            continue
        if m["lap_var"] < cfg["min_laplacian_var"]:
            why["blurry"] = why.get("blurry", 0) + 1
            continue
        s = 0.6 * m["saliency"] + 0.4 * min(1.0, m["edges"] / 0.25) - 0.3 * m["sky"]
        if best is None or s > best["score"]:
            best = {"box": b, "score": round(s, 4), "metrics": {k: round(v, 4) for k, v in m.items()}}
    if best is None or best["score"] < cfg["min_score"]:
        return {"box": None, "reason": "every window refused: " + ", ".join(f"{k} {v}" for k, v in sorted(why.items())),
                "tried": len(boxes)}
    best["tried"] = len(boxes)
    best["refused"] = why
    return best


# --------------------------------------------------------------------------- places
def asset_places(row: Dict[str, Any], rules: Dict[str, Any], cfg: Dict[str, Any]) -> set:
    t = (row.get("title") or "") + " " + Path(row["asset"]).stem.replace("_", " ")
    pl = set(B.title_places(t, rules))
    nt = B._norm(t)
    for k, spec in cfg.get("extra_places", {}).items():
        if any(f" {B._norm(a).strip()} " in nt for a in spec.get("title", [])) and \
                not any(f" {B._norm(a).strip()} " in nt for a in spec.get("not_title", [])):
            pl.add(k)
    return pl


def narration_places(roman: str, rules: Dict[str, Any], cfg: Dict[str, Any]) -> set:
    """Real places named in the beat narration (Hinglish romanised words), kinds (beach, sunset) excluded."""
    nt = B._norm(roman)
    out = {k for k, al in rules["places"].items() if any(f" {B._norm(a).strip()} " in nt for a in al)}
    for k, spec in cfg.get("extra_places", {}).items():
        if any(f" {B._norm(a).strip()} " in nt for a in spec.get("narration", [])):
            out.add(k)
    return out - B.NON_PLACE_KEYS - set(cfg.get("narration_ignore", []))


def beat_roman(bp: Dict[str, Any], hw: Sequence[Dict[str, Any]]) -> Dict[str, str]:
    out = {}
    for b in bp["beats"]:
        out[b["id"]] = " ".join(hw[i]["hinglish"] for i in range(b["first_word"], b["last_word"] + 1) if i < len(hw))
    return out


# --------------------------------------------------------------------------- the pass
def is_still(row: Dict[str, Any]) -> bool:
    return Path(row["asset"]).suffix.lower() in IMG_EXT and not row["asset"].startswith(("CARD_", "MAP_"))


def plan_crop_reuse(rows: Sequence[Dict[str, Any]], bp: Dict[str, Any], hw: Sequence[Dict[str, Any]], rules: Dict[str, Any],
                    *, root: Path = ROOT, face_detector: Optional[Callable] = None,
                    analysis_cache: Optional[Dict[str, Analysis]] = None) -> Dict[str, Any]:
    """Decide the crop reuses (no files written). Returns {reuses: [...], skipped: [...], considered: n}."""
    cfg = settings(rules)
    rows = sorted([dict(r) for r in rows], key=lambda r: float(r["start"]))
    idx = {r["beat"]: k for k, r in enumerate(rows)}
    roman = beat_roman(bp, hw)
    focus = rules.get("focus", {})
    rejects = cfg.get("rejects", {})
    cache = analysis_cache if analysis_cache is not None else {}
    if face_detector is None and cfg.get("require_face_detector", True):
        face_detector = yunet_detector(score=cfg["face_score"])
        if face_detector is None:
            return {"reuses": [], "skipped": [{"beat": "*", "reason": "no face detector available (YuNet model missing); "
                                               "crop reuse refused (require_face_detector)"}], "considered": 0}
    # appearances of every still (by original file name) and their framings
    appear: Dict[str, List[int]] = {}
    meta: Dict[str, Dict[str, Any]] = {}
    for k, r in enumerate(rows):
        if is_still(r):
            appear.setdefault(r["asset"], []).append(k)
            meta.setdefault(r["asset"], r)
    framings: Dict[str, List[Box]] = {}
    reuses_n: Dict[str, int] = {}
    exact_by_place: Dict[str, List[str]] = {}
    for a, r in meta.items():
        if r["match"] == "exact":
            for p in asset_places(r, rules, cfg) - B.NON_PLACE_KEYS:
                exact_by_place.setdefault(p, []).append(a)

    def clip_bounds(k: int) -> Tuple[int, int]:
        a = rows[k]["asset"]
        s = k
        while s > 0 and rows[s - 1]["asset"] == a:
            s -= 1
        e = k
        while e + 1 < len(rows) and rows[e + 1]["asset"] == a:
            e += 1
        return s, e

    reuses, skipped, considered = [], [], 0
    for k, r in enumerate(rows):
        role, match = r["role"], r["match"]
        if match in cfg["never_replace_match"] and role not in cfg["replace_roles"]:
            continue
        if r["asset"].startswith(("CARD_", "MAP_")) or role in ("card_hold", "motion_card", "motion_map"):
            continue
        kind = "continued" if role in cfg["replace_roles"] else ("representative" if match == "representative" else None)
        if not kind:
            continue
        named = narration_places(roman.get(r["beat"], ""), rules, cfg)
        if kind == "representative":
            named = {p for p in named if exact_by_place.get(p)}
            if not named:
                continue  # narration names no place with an exact photo -> not a crop-reuse beat
        considered += 1
        s, e = clip_bounds(k)
        if s < k < e:
            skipped.append({"beat": r["beat"], "reason": "middle of a multi-beat clip (replacing it would split one clip into two copies)"})
            continue
        if kind == "continued":
            shot_pl = asset_places(r, rules, cfg) if is_still(r) else set()
            places = (named | shot_pl)
        else:
            places = named
        # candidate photos: exact photos of those places first; for a continued hold also stills of the same kind (beach/sunset)
        cands: List[str] = []
        for p in sorted(places - B.NON_PLACE_KEYS):
            cands += [a for a in exact_by_place.get(p, []) if a not in cands]
        if kind == "continued" and not (cfg.get("continued_exact_needs_exact") and match == "exact"):
            # a hold on an exact shot is only replaced by an exact photo (no downgrade to another place)
            for a, m in meta.items():
                if a not in cands and m["match"] in ("exact", "representative") and (asset_places(m, rules, cfg) & places):
                    cands.append(a)
        if not cands:
            skipped.append({"beat": r["beat"], "reason": f"no photo on the timeline shows {sorted(places) or 'a named place'}"})
            continue
        tried = []
        choice = None
        for a in cands:
            ap = appear[a]
            if ap[0] > k:
                tried.append(f"{a}: first appearance is later (beat {rows[ap[0]]['beat']})"); continue
            if min(abs(k - j) for j in ap) < cfg["min_beats_apart"]:
                tried.append(f"{a}: < {cfg['min_beats_apart']} beats from an appearance"); continue
            if reuses_n.get(a, 0) >= cfg["max_reuses_per_asset"]:
                tried.append(f"{a}: already {cfg['max_reuses_per_asset']} reuses"); continue
            rk = f"{a}@{r['beat']}"
            if rk in rejects:
                tried.append(f"{a}: rejected by eye ({rejects[rk]})"); continue
            if a not in cache:
                cache[a] = Analysis(root / meta[a]["source_dir"] / a, face_detector=face_detector)
            an = cache[a]
            if a not in framings:
                framings[a] = [first_framing(an.iw, an.ih, focus.get(a), cfg["aspect"])]
            bc = best_crop(an, framings[a], cfg)
            if bc["box"] is None:
                tried.append(f"{a}: {bc['reason']}"); continue
            pri = (0 if meta[a]["match"] == "exact" else 1, -bc["score"])
            if choice is None or pri < choice[0]:
                choice = (pri, a, bc)
        if not choice:
            skipped.append({"beat": r["beat"], "reason": "; ".join(tried)[:900]})
            continue
        _, a, bc = choice
        framings[a].append(bc["box"])
        reuses_n[a] = reuses_n.get(a, 0) + 1
        appear[a] = sorted(appear[a] + [k])
        an = cache[a]
        reuses.append({"beat": r["beat"], "kind": kind, "asset": a, "source_dir": meta[a]["source_dir"], "match": meta[a]["match"],
                       "title": meta[a].get("title", ""), "licence": meta[a].get("licence", ""),
                       "source_page": meta[a].get("source_page", ""), "box": list(bc["box"]), "image": [an.iw, an.ih],
                       "first_framing": list(framings[a][0]), "first_beat": rows[min(appear[a])]["beat"],
                       "iou_max": round(max(iou(bc["box"], f) for f in framings[a][:-1]), 3),
                       "area_ratio": round(bc["box"][2] * bc["box"][3] / (framings[a][0][2] * framings[a][0][3]), 3),
                       "score": bc["score"], "metrics": bc["metrics"], "faces_in_image": len(an.faces),
                       "face_check": an.face_status, "places": sorted(places),
                       "replaced": f"{r['asset']} [{match}/{role}]", "reuse_n": reuses_n[a]})
    return {"reuses": reuses, "skipped": skipped, "considered": considered}


def write_crops(reuses: Sequence[Dict[str, Any]], out_dir: Path, *, root: Path = ROOT, quality: int = 95) -> List[Dict[str, Any]]:
    """Cut every crop into its own JPEG + CREDITS.json (original credit + modification note)."""
    from PIL import Image
    out_dir.mkdir(parents=True, exist_ok=True)
    creds = []
    for u in reuses:
        x, y, w, h = u["box"]
        stem = re.sub(r"[^A-Za-z0-9_]+", "_", Path(u["asset"]).stem)[:48]
        name = f"CR_{u['beat']}_{stem}.jpg"
        with Image.open(root / u["source_dir"] / u["asset"]) as im:
            im.convert("RGB").crop((x, y, x + w, y + h)).save(out_dir / name, quality=quality)
        u["file"] = name
        orig = {}
        cj = root / u["source_dir"] / "CREDITS.json"
        if cj.is_file():
            orig = next((c for c in json.loads(cj.read_text(encoding="utf-8")) if c.get("file") == u["asset"]), {})
        box_s = f"x={x} y={y} w={w} h={h} of {u['image'][0]}x{u['image'][1]}"
        creds.append({**orig, "file": name, "title": orig.get("title") or u["title"], "licence": orig.get("licence") or u["licence"],
                      "source_page": orig.get("source_page") or u["source_page"], "reuse": "crop_reuse", "reuse_of": u["asset"],
                      "reuse_of_dir": u["source_dir"], "crop_box": box_s,
                      "modified": f"cropped by KANG ({box_s}); crop = modification of the original photo, content not altered "
                                  "or generated", "match": u["match"]})
    (out_dir / "CREDITS.json").write_text(json.dumps(creds, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return creds


def apply_reuses(rows: Sequence[Dict[str, Any]], reuses: Sequence[Dict[str, Any]], crop_dir_rel: str) -> List[Dict[str, Any]]:
    out = [dict(r) for r in rows]
    by = {r["beat"]: r for r in out}
    for u in reuses:
        r = by[u["beat"]]
        x, y, w, h = u["box"]
        r.update(asset=u["file"], source_dir=crop_dir_rel, asset_source="crop_reuse", match=u["match"], role="crop_reuse",
                 licence=u["licence"], title=u["title"], source_page=u["source_page"], parallax_clip="", parallax_dir="",
                 parallax_status="", reuse="crop_reuse", reuse_of=u["asset"],
                 crop_box=f"{x},{y},{w},{h} of {u['image'][0]}x{u['image'][1]}",
                 notes=f"v14 crop reuse #{u['reuse_n']} of {u['asset']} (first framing at {u['first_beat']}; area "
                       f"{u['area_ratio']:.0%} of it, IoU {u['iou_max']}); replaced {u['replaced']}; places "
                       f"{'/'.join(u['places'])}; agent-picked, not human-reviewed")
    return out


def crop_qa(rows: Sequence[Dict[str, Any]], reuses: Sequence[Dict[str, Any]], rules: Dict[str, Any]) -> List[str]:
    """Re-check every hard rule on the final rows."""
    cfg = settings(rules)
    rows = sorted(rows, key=lambda r: float(r["start"]))
    probs = []
    pos: Dict[str, List[int]] = {}
    for k, r in enumerate(rows):
        pos.setdefault(r.get("reuse_of") or r["asset"], []).append(k)
    by_asset: Dict[str, List[Dict[str, Any]]] = {}
    for u in reuses:
        by_asset.setdefault(u["asset"], []).append(u)
        if u["box"][2] < cfg["min_crop_width"]:
            probs.append(f"{u['beat']}: crop {u['box'][2]} px < {cfg['min_crop_width']}")
        if u["area_ratio"] > cfg["max_area_ratio"] + 1e-6 or u["iou_max"] > cfg["max_iou"] + 1e-6:
            probs.append(f"{u['beat']}: area {u['area_ratio']} / IoU {u['iou_max']} over the limit")
        if u["match"] == "exact" and u["kind"] == "representative" and not u["places"]:
            probs.append(f"{u['beat']}: representative beat replaced without a named place")
    for a, us in by_asset.items():
        if len(us) > cfg["max_reuses_per_asset"]:
            probs.append(f"{a}: {len(us)} reuses > {cfg['max_reuses_per_asset']}")
        boxes = [tuple(us[0]["first_framing"])] + [tuple(u["box"]) for u in us]
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                if iou(boxes[i], boxes[j]) > cfg["max_iou"] + 1e-6:
                    probs.append(f"{a}: framings {i}/{j} IoU {iou(boxes[i], boxes[j]):.2f}")
        p = pos.get(a, [])
        # distance between separate clips of the same photo (consecutive beats of one clip are one appearance)
        groups, cur = [], []
        for k in p:
            if cur and k == cur[-1] + 1 and rows[k]["asset"] == rows[cur[-1]]["asset"]:
                cur.append(k)
            else:
                if cur:
                    groups.append(cur)
                cur = [k]
        if cur:
            groups.append(cur)
        for g1, g2 in zip(groups, groups[1:]):
            if g2[0] - g1[-1] < cfg["min_beats_apart"]:
                probs.append(f"{a}: appearances {rows[g1[-1]]['beat']} and {rows[g2[0]]['beat']} < {cfg['min_beats_apart']} beats apart")
    return probs


# --------------------------------------------------------------------------- grid
def crop_grid(reuses: Sequence[Dict[str, Any]], out: str | Path, *, root: Path = ROOT, crop_dir: Optional[Path] = None,
              tw: int = 480) -> Path:
    """One row per reuse: full photo with both boxes | first framing | crop (as cut), with beat ids."""
    from PIL import Image, ImageDraw, ImageFont
    th = int(tw * 9 / 16)
    font = ImageFont.truetype(str(root / "fonts" / "Mukta-ExtraBold.ttf"), 15)
    rowh = th + 46
    sheet = Image.new("RGB", (3 * tw + 20, max(1, len(reuses)) * rowh), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    for n, u in enumerate(reuses):
        y0 = n * rowh
        with Image.open(root / u["source_dir"] / u["asset"]) as im:
            im = im.convert("RGB")
            iw, ih = im.size
            k = min(tw / iw, th / ih)
            full = im.resize((max(1, int(iw * k)), max(1, int(ih * k))))
            fd = ImageDraw.Draw(full)
            for b, col in ((u["first_framing"], (80, 200, 255)), (u["box"], (255, 200, 40))):
                fd.rectangle([b[0] * k, b[1] * k, (b[0] + b[2]) * k - 1, (b[1] + b[3]) * k - 1], outline=col, width=2)
            sheet.paste(full, (int((tw - full.width) / 2), y0))
            f = u["first_framing"]
            sheet.paste(im.crop((f[0], f[1], f[0] + f[2], f[1] + f[3])).resize((tw, th)), (tw + 10, y0))
        cp = (crop_dir / u["file"]) if crop_dir and u.get("file") else None
        if cp and cp.is_file():
            with Image.open(cp) as c:
                sheet.paste(c.convert("RGB").resize((tw, th)), (2 * tw + 20, y0))
        else:
            with Image.open(root / u["source_dir"] / u["asset"]) as im:
                b = u["box"]
                sheet.paste(im.convert("RGB").crop((b[0], b[1], b[0] + b[2], b[1] + b[3])).resize((tw, th)), (2 * tw + 20, y0))
        d.text((4, y0 + th + 2), f"{u['asset'][:58]}  [{u['match']}]", fill=(220, 220, 220), font=font)
        d.text((tw + 14, y0 + th + 2), f"first framing @ {u['first_beat']} (blue)", fill=(80, 200, 255), font=font)
        d.text((2 * tw + 24, y0 + th + 2), f"CROP @ {u['beat']} (yellow) {u['box'][2]}x{u['box'][3]}", fill=(255, 200, 40), font=font)
        d.text((4, y0 + th + 22), f"{u['kind']}: replaced {u['replaced'][:70]}  area {u['area_ratio']:.0%} IoU {u['iou_max']} "
                                  f"score {u['score']} faces {u['faces_in_image']}", fill=(200, 200, 200), font=font)
    out = Path(out)
    out.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out, quality=88)
    return out
