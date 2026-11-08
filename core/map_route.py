"""v13 map route animation: stylised Gujarat coast map, dots, animated route line, Roman labels. Own code.

Data: Natural Earth 1:10m land + Gujarat state lines (public domain), clipped once by tools/prep_map_data.py
into assets/map_data/ne_10m_gujarat_clip.json. Place points: config/map_places.json (Wikidata CC0 coordinates;
Gopi Talav from one OpenStreetMap Nominatim lookup, ODbL -> credit '© OpenStreetMap contributors').
No map tiles are fetched or drawn (OSM tile usage policy forbids bulk use; we render vectors ourselves).

Rules: a place is only labelled when the narration names it (checked against the Hinglish words of the clip);
route lines are schematic (bezier between points, not the road); every distance shown is read from the
narration (core/narration_values.py), never computed from the map.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np

from . import motion_draw as D

ROOT = Path(__file__).resolve().parent.parent
MAP_DATA = ROOT / "assets" / "map_data" / "ne_10m_gujarat_clip.json"
PLACES = ROOT / "config" / "map_places.json"
FINE_DATA = ROOT / "assets" / "map_data" / "osm_dwarka_gulf_coast.json"
KM_LAT = 110.57
FEATHER_PX = 40   # v13b: NE -> OSM coastline cross-fade width inside the fine-data box
KM_LON_EQ = 111.32
SEA_TOP, SEA_BOT = (12, 34, 58), (6, 18, 34)
LAND, COAST, STATE = (34, 56, 74), (96, 165, 250), (148, 163, 184)
CREDIT = "Map data: Natural Earth (public domain) · © OpenStreetMap contributors · route schematic, distances as narrated"


# --------------------------------------------------------------------------- clipping (used by tools/prep_map_data.py)
def clip_polygon(pts: Sequence[Tuple[float, float]], bbox: Sequence[float]) -> List[Tuple[float, float]]:
    """Sutherland-Hodgman against an axis-aligned box (lon0, lat0, lon1, lat1)."""
    x0, y0, x1, y1 = bbox
    edges = [(lambda p: p[0] >= x0, lambda a, b: _ix(a, b, x=x0)), (lambda p: p[0] <= x1, lambda a, b: _ix(a, b, x=x1)),
             (lambda p: p[1] >= y0, lambda a, b: _ix(a, b, y=y0)), (lambda p: p[1] <= y1, lambda a, b: _ix(a, b, y=y1))]
    out = list(pts)
    for inside, inter in edges:
        if not out:
            break
        inp, out = out, []
        prev = inp[-1]
        for cur in inp:
            if inside(cur):
                if not inside(prev):
                    out.append(inter(prev, cur))
                out.append(cur)
            elif inside(prev):
                out.append(inter(prev, cur))
            prev = cur
    return out


def _ix(a, b, x=None, y=None):
    if x is not None:
        t = (x - a[0]) / ((b[0] - a[0]) or 1e-12)
        return (x, a[1] + t * (b[1] - a[1]))
    t = (y - a[1]) / ((b[1] - a[1]) or 1e-12)
    return (a[0] + t * (b[0] - a[0]), y)


def clip_polyline(pts: Sequence[Tuple[float, float]], bbox: Sequence[float]) -> List[List[Tuple[float, float]]]:
    """Liang-Barsky per segment; consecutive inside pieces are joined."""
    x0, y0, x1, y1 = bbox
    runs: List[List[Tuple[float, float]]] = []
    cur: List[Tuple[float, float]] = []
    for a, b in zip(pts, pts[1:]):
        dx, dy = b[0] - a[0], b[1] - a[1]
        t0, t1, ok = 0.0, 1.0, True
        for p, q in ((-dx, a[0] - x0), (dx, x1 - a[0]), (-dy, a[1] - y0), (dy, y1 - a[1])):
            if abs(p) < 1e-15:
                if q < 0:
                    ok = False
                    break
                continue
            r = q / p
            if p < 0:
                t0 = max(t0, r)
            else:
                t1 = min(t1, r)
        if not ok or t0 > t1:
            if len(cur) > 1:
                runs.append(cur)
            cur = []
            continue
        pa = (a[0] + t0 * dx, a[1] + t0 * dy)
        pb = (a[0] + t1 * dx, a[1] + t1 * dy)
        if not cur or abs(cur[-1][0] - pa[0]) > 1e-9 or abs(cur[-1][1] - pa[1]) > 1e-9:
            if len(cur) > 1:
                runs.append(cur)
            cur = [pa]
        cur.append(pb)
        if t1 < 1.0:
            runs.append(cur)
            cur = []
    if len(cur) > 1:
        runs.append(cur)
    return runs


def point_in_poly(lon: float, lat: float, ring: Sequence[Sequence[float]]) -> bool:
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i]
        xj, yj = ring[j]
        if (yi > lat) != (yj > lat) and lon < (xj - xi) * (lat - yi) / ((yj - yi) or 1e-12) + xi:
            inside = not inside
        j = i
    return inside


# --------------------------------------------------------------------------- data
def load_map_data(path: Optional[str | Path] = None, fine_path: Optional[str | Path] = None) -> Dict[str, Any]:
    d = json.loads(Path(path or MAP_DATA).read_text(encoding="utf-8"))
    d["_land"] = [np.asarray(r, np.float64) for r in d["land"]]
    d["_state"] = [np.asarray(s["coords"], np.float64) for s in d["state_lines"]]
    d["_intl"] = [np.asarray(s["coords"], np.float64) for s in d["intl_lines"]]
    fine_p = Path(fine_path) if fine_path else FINE_DATA
    if fine_p and fine_p.is_file():
        fd = json.loads(fine_p.read_text(encoding="utf-8"))
        fd["_rings"] = [np.asarray(r, np.float64) for r in fd["rings"]]
        fd["_holes"] = [np.asarray(r, np.float64) for r in fd["holes"]]
        d["_fine"] = fd
    return d


def load_places(path: Optional[str | Path] = None) -> Dict[str, Any]:
    return json.loads(Path(path or PLACES).read_text(encoding="utf-8"))


def haversine_km(a: Sequence[float], b: Sequence[float]) -> float:
    (la1, lo1), (la2, lo2) = (math.radians(a[0]), math.radians(a[1])), (math.radians(b[0]), math.radians(b[1]))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371.0 * math.asin(math.sqrt(h))


# --------------------------------------------------------------------------- camera
class Cam:
    def __init__(self, lon: float, lat: float, km: float, w: int = 1920, h: int = 1080):
        self.lon, self.lat, self.km, self.w, self.h = lon, lat, km, w, h
        self.k = w / km  # px per km
        self.cx = KM_LON_EQ * math.cos(math.radians(lat))

    def xy(self, lon, lat):
        lon = np.asarray(lon, np.float64)
        lat = np.asarray(lat, np.float64)
        return (self.w / 2 + (lon - self.lon) * self.cx * self.k, self.h / 2 - (lat - self.lat) * KM_LAT * self.k)

    def as_dict(self) -> Dict[str, float]:
        return {"lon": round(self.lon, 5), "lat": round(self.lat, 5), "km": round(self.km, 2)}


def fit_cam(points: Sequence[Tuple[float, float]], w: int = 1920, h: int = 1080, box=(0.18, 0.13, 0.82, 0.62),
            min_km: float = 40.0, pad_km: float = 0.0) -> Cam:
    """Camera that puts (lat, lon) points inside the box (fractions of the frame), above the caption zone."""
    lats = [p[0] for p in points]
    lons = [p[1] for p in points]
    clat = (min(lats) + max(lats)) / 2
    cx = KM_LON_EQ * math.cos(math.radians(clat))
    span_x = (max(lons) - min(lons)) * cx + 2 * pad_km
    span_y = (max(lats) - min(lats)) * KM_LAT + 2 * pad_km
    bw, bh = (box[2] - box[0]) * w, (box[3] - box[1]) * h
    k = min(bw / max(span_x, 1e-6), bh / max(span_y, 1e-6))
    km = max(min_km, w / k)
    k = w / km
    bx, by = (box[0] + box[2]) / 2 * w, (box[1] + box[3]) / 2 * h
    clon = (min(lons) + max(lons)) / 2
    lat_c = clat - (h / 2 - by) / (KM_LAT * k)
    lon_c = clon - (bx - w / 2) / (cx * k)
    return Cam(lon_c, lat_c, km, w, h)


def lerp_cam(a: Cam, b: Cam, p: float) -> Cam:
    e = D.ease_in_out(p)
    km = math.exp(math.log(a.km) * (1 - e) + math.log(b.km) * e)
    return Cam(a.lon + (b.lon - a.lon) * e, a.lat + (b.lat - a.lat) * e, km, a.w, a.h)


def cam_inside_bbox(cam: Cam, bbox: Sequence[float]) -> bool:
    lon0 = cam.lon - (cam.w / 2) / (cam.cx * cam.k)
    lon1 = cam.lon + (cam.w / 2) / (cam.cx * cam.k)
    lat1 = cam.lat + (cam.h / 2) / (KM_LAT * cam.k)
    lat0 = cam.lat - (cam.h / 2) / (KM_LAT * cam.k)
    return bbox[0] <= lon0 and lon1 <= bbox[2] and bbox[1] <= lat0 and lat1 <= bbox[3]


# --------------------------------------------------------------------------- route geometry
def bezier(a: Tuple[float, float], b: Tuple[float, float], bend: float, n: int = 48) -> np.ndarray:
    """Quadratic bezier in pixel space from a to b; control point offset perpendicular by bend * length."""
    a, b = np.asarray(a, np.float64), np.asarray(b, np.float64)
    d = b - a
    ln = float(np.hypot(*d)) or 1.0
    nrm = np.array([-d[1], d[0]]) / ln
    c = (a + b) / 2 + nrm * bend * ln
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * a + 2 * (1 - t) * t * c + t ** 2 * b


def partial(path: np.ndarray, p: float) -> np.ndarray:
    if p <= 0:
        return path[:1]
    if p >= 1:
        return path
    seg = np.hypot(*np.diff(path, axis=0).T)
    cum = np.concatenate([[0], np.cumsum(seg)])
    L = cum[-1] * p
    i = int(np.searchsorted(cum, L)) - 1
    i = max(0, min(i, len(seg) - 1))
    f = (L - cum[i]) / (seg[i] or 1.0)
    head = path[i] + (path[i + 1] - path[i]) * f
    return np.vstack([path[:i + 1], head])


# --------------------------------------------------------------------------- rendering
class MapRenderer:
    def __init__(self, data: Dict[str, Any], w: int = 1920, h: int = 1080):
        self.d, self.w, self.h = data, w, h
        self.sea = D.gradient(w, h, SEA_TOP, SEA_BOT).astype(np.uint8)

    def base(self, cam: Cam, labels: Sequence[Dict[str, Any]] = (), boxes: Optional[list] = None,
             feather: bool = True, avoid: Sequence[Tuple[int, int, int, int]] = ()) -> np.ndarray:
        """Sea gradient, land (Natural Earth; OSM-refined coast inside the fine box, cross-faded over FEATHER_PX
        inside the box edge so the NE/OSM coastline has no step), coastline, state lines, region labels (5 % margin)."""
        import cv2
        S = 8.0  # shift=3 -> 1/8 px precision

        def proj(r):
            x, y = cam.xy(r[:, 0], r[:, 1])
            return np.stack([x * S, y * S], 1).round().astype(np.int32)
        m = np.zeros((self.h, self.w), np.uint8)
        cv2.fillPoly(m, [proj(r) for r in self.d["_land"]], 255, lineType=cv2.LINE_AA, shift=3)
        fine = self.d.get("_fine")
        if fine:
            m_ne = m.copy()
            e = fine.get("step_deg", 0.0005) * 1.5  # erase slightly inside the box: fine rings overlap NE, no seam
            b = (fine["bbox"][0] + e, fine["bbox"][1] + e, fine["bbox"][2] - e, fine["bbox"][3] - e)
            rect = np.array([[b[0], b[1]], [b[2], b[1]], [b[2], b[3]], [b[0], b[3]]], np.float64)
            cv2.fillPoly(m, [proj(rect)], 0, lineType=cv2.LINE_8, shift=3)
            cv2.fillPoly(m, [proj(r) for r in fine["_rings"]], 255, lineType=cv2.LINE_AA, shift=3)
            if fine["_holes"]:
                cv2.fillPoly(m, [proj(r) for r in fine["_holes"]], 0, lineType=cv2.LINE_AA, shift=3)
            if feather:  # v13b: blend NE -> OSM over FEATHER_PX inside the box edge (no coastline step)
                box = np.zeros_like(m)
                cv2.fillPoly(box, [proj(rect)], 255, lineType=cv2.LINE_8, shift=3)
                if box.any():
                    wgt = np.clip(cv2.distanceTransform(box, cv2.DIST_L2, 3) / FEATHER_PX, 0, 1)
                    m = (m_ne.astype(np.float32) * (1 - wgt) + m.astype(np.float32) * wgt).round().astype(np.uint8)
        a = (m.astype(np.float32) / 255.0)[..., None]
        f = self.sea.astype(np.float32) * (1 - a) + np.array(LAND, np.float32) * a
        edge = cv2.morphologyEx(m, cv2.MORPH_GRADIENT, np.ones((3, 3), np.uint8)).astype(np.float32)[..., None] / 255.0 * 0.6
        f = f * (1 - edge) + np.array(COAST, np.float32) * edge
        over = np.zeros((self.h, self.w), np.uint8)
        for s_ in self.d["_state"] + self.d["_intl"]:
            _dashed(over, proj(s_), 255)
        o = over.astype(np.float32)[..., None] / 255.0 * 0.4
        f = f * (1 - o) + np.array(STATE, np.float32) * o
        for lab in labels:  # faint region names (GUJARAT, Arabian Sea) only when the narration names them
            x, y = cam.xy(lab["lon"], lab["lat"])
            spr = D.text_sprite(lab["text"], "body", int(lab.get("size", 44)), (148, 163, 184), shadow=False)
            lx, ly = clamp_margin(float(x) - spr.shape[1] / 2, float(y) - spr.shape[0] / 2, spr, self.w, self.h)
            lx, ly = free_spot(lx, ly, spr, avoid, self.w, self.h)  # v13b: a clamped region label never covers a place label
            D.blit(f, spr, lx, ly, lab.get("alpha", 0.55))
            if boxes is not None:
                boxes.append((lab["text"], (int(lx), int(ly), int(lx + spr.shape[1]), int(ly + spr.shape[0]))))
        return f


def clamp_margin(x: float, y: float, spr: np.ndarray, w: int = 1920, h: int = 1080) -> Tuple[float, float]:
    """v13b: keep a label sprite inside the 5 % title-safe margin and above the caption line."""
    sh, sw = spr.shape[:2]
    mx, my = MARGIN * w, MARGIN * h
    x = min(max(x, mx), w - mx - sw)
    y = min(max(y, my), SAFE["bottom_px"] - FADE_PX - sh)  # fully opaque: above the 30 px fade band
    return x, y


def _hit(a, b, pad: int = 8) -> bool:
    return a[0] - pad < b[2] and b[0] - pad < a[2] and a[1] - pad < b[3] and b[1] - pad < a[3]


def free_spot(x: float, y: float, spr: np.ndarray, avoid, w: int = 1920, h: int = 1080) -> Tuple[float, float]:
    """First position (same, then stepped up / down / right inside the margin) whose box clears every avoid box."""
    sh, sw = spr.shape[:2]
    for dx, dy in [(0, 0)] + [(0, -k * (sh + 12)) for k in range(1, 5)] + [(0, k * (sh + 12)) for k in range(1, 5)] + \
            [(k * 120, 0) for k in range(1, 6)]:
        cx, cy = clamp_margin(x + dx, y + dy, spr, w, h)
        if not any(_hit((cx, cy, cx + sw, cy + sh), b) for b in avoid):
            return cx, cy
    return x, y


def place_label_boxes(plan: Dict[str, Any], cam: Cam, T: float) -> List[Tuple[int, int, int, int]]:
    """Boxes of the place dots + labels visible at T (same placement as map_frame), for region-label avoidance."""
    out = []
    for sh in plan["shows"]:
        if T < sh["reveal"]:
            continue
        x, y = (float(v) for v in cam.xy(sh["lon"], sh["lat"]))
        if y > SAFE["bottom_px"] - 20:
            continue
        out.append((int(x - 16), int(y - 16), int(x + 16), int(y + 16)))
        if T >= sh["label_at"]:
            spr = label_sprite(sh["label"], 42)
            lx, ly = anchor_xy(x, y, spr, sh["anchor"])
            if ly + spr.shape[0] > SAFE["bottom_px"] - FADE_PX:
                continue
            lx, ly = clamp_margin(lx, ly, spr, cam.w, cam.h)
            out.append((int(lx), int(ly - 10), int(lx + spr.shape[1]), int(ly + spr.shape[0])))
    return out


def label_box_problems(boxes, w: int = 1920, h: int = 1080) -> List[str]:
    """FAIL list: a label / badge / chip / region box outside the 5 % margin or below the caption line."""
    mx, my = MARGIN * w, MARGIN * h
    out = []
    for t, (x0, y0, x1, y1) in boxes:
        if t.split(":")[-1].startswith("route"):
            continue
        if x0 < mx - 0.5 or x1 > w - mx + 0.5 or y0 < my - 0.5:
            out.append(f"'{t}' box {x0},{y0},{x1},{y1} outside the 5% margin")
        if y1 > SAFE["bottom_px"] - FADE_PX + 0.5:
            out.append(f"'{t}' box {x0},{y0},{x1},{y1} reaches the fade band above the caption line (y>{SAFE['bottom_px'] - FADE_PX})")
    return out


def _dashed(img, pts, color, dash=10 * 8, gap=8 * 8):
    import cv2
    p = pts.astype(np.float64)
    seg = np.hypot(*np.diff(p, axis=0).T)
    pos, on = 0.0, True
    for a, b, L in zip(p, p[1:], seg):
        t = 0.0
        while t < L:
            step = min((dash if on else gap) - pos, L - t)
            if on:
                q0 = a + (b - a) * (t / L)
                q1 = a + (b - a) * ((t + step) / L)
                cv2.line(img, tuple(q0.round().astype(int)), tuple(q1.round().astype(int)), color, 1, cv2.LINE_AA, 3)
            t += step
            pos += step
            if pos >= (dash if on else gap) - 1e-9:
                pos, on = 0.0, not on


def draw_polyline_glow(f: np.ndarray, pts: np.ndarray, color=D.GOLD, core: int = 5, glow: int = 16) -> None:
    import cv2
    if len(pts) < 2:
        return
    S = 8.0
    ip = (pts * S).round().astype(np.int32).reshape(-1, 1, 2)
    x0, y0 = np.floor(pts.min(0) - glow * 2).astype(int)
    x1, y1 = np.ceil(pts.max(0) + glow * 2).astype(int)
    x0, y0, x1, y1 = max(0, x0), max(0, y0), min(f.shape[1], x1), min(f.shape[0], y1)
    if x0 >= x1 or y0 >= y1:
        return
    m = np.zeros((f.shape[0], f.shape[1]), np.uint8)
    cv2.polylines(m, [ip], False, 255, glow, cv2.LINE_AA, 3)
    g = cv2.GaussianBlur(m[y0:y1, x0:x1], (0, 0), glow / 2.5).astype(np.float32)[..., None] / 255.0 * 0.45
    reg = f[y0:y1, x0:x1]
    reg *= (1 - g)
    reg += np.array(color, np.float32) * g
    m2 = np.zeros_like(m)
    cv2.polylines(m2, [ip], False, 255, core, cv2.LINE_AA, 3)
    a = m2[y0:y1, x0:x1].astype(np.float32)[..., None] / 255.0
    reg *= (1 - a)
    reg += np.array(color, np.float32) * a


def draw_dot(f: np.ndarray, x: float, y: float, p_appear: float, t_since: float) -> None:
    import cv2
    if p_appear <= 0:
        return
    s = D.ease_out_back(p_appear)
    S = 16
    c = (int(round(x * S)), int(round(y * S)))
    if 0 <= t_since <= 1.2:  # one pulse ring when the place is named
        rr = 14 + 46 * D.ease_out_cubic(t_since / 1.2)
        over = f.copy()
        cv2.circle(over, c, int(rr * S), D.GOLD, 3, cv2.LINE_AA, 4)
        a = 0.8 * (1 - t_since / 1.2)
        f *= (1 - a)
        f += over * a
    cv2.circle(f, c, int(15 * s * S), (6, 14, 26), -1, cv2.LINE_AA, 4)
    cv2.circle(f, c, int(12 * s * S), D.GOLD, -1, cv2.LINE_AA, 4)
    cv2.circle(f, c, int(5 * s * S), D.WHITE, -1, cv2.LINE_AA, 4)


def label_sprite(text: str, size: int = 42, accent: bool = False) -> np.ndarray:
    tsp = D.text_sprite(text, "body", size, (6, 14, 26) if accent else D.WHITE, shadow=False)
    pw, ph = tsp.shape[1] + 28, tsp.shape[0] + 8
    pill = D.pill_sprite(pw, ph, D.GOLD if accent else (8, 20, 36), alpha=0.95 if accent else 0.82,
                         border=None if accent else (96, 165, 250))
    out = pill.copy()
    _blit_rgba(out, tsp, 14, 4)
    return out


def _blit_rgba(dst: np.ndarray, src: np.ndarray, x: int, y: int) -> None:
    h, w = src.shape[:2]
    h = min(h, dst.shape[0] - y)
    w = min(w, dst.shape[1] - x)
    s = src[:h, :w]
    a = s[..., 3:4]
    d = dst[y:y + h, x:x + w]
    d[..., :3] = d[..., :3] * (1 - a) + s[..., :3] * a
    d[..., 3:4] = d[..., 3:4] + a * (1 - d[..., 3:4])


def anchor_xy(x: float, y: float, spr: np.ndarray, anchor: str, gap: float = 24) -> Tuple[float, float]:
    h, w = spr.shape[:2]
    return {"r": (x + gap, y - h / 2), "l": (x - gap - w, y - h / 2), "t": (x - w / 2, y - gap - h),
            "b": (x - w / 2, y + gap), "tr": (x + gap * 0.7, y - gap * 0.7 - h), "tl": (x - gap * 0.7 - w, y - gap * 0.7 - h),
            "br": (x + gap * 0.7, y + gap * 0.7), "bl": (x - gap * 0.7 - w, y + gap * 0.7)}[anchor]


def _geo_raster(rings: Sequence[Sequence[Sequence[float]]], bbox: Sequence[float], w: int, h: int) -> np.ndarray:
    """Fill lon/lat rings into a w x h uint8 mask over bbox (row 0 = north)."""
    import cv2
    m = np.zeros((h, w), np.uint8)
    sx, sy = w / (bbox[2] - bbox[0]), h / (bbox[3] - bbox[1])
    pts = []
    for r in rings:
        a = np.asarray(r, np.float64)
        pts.append(np.stack([(a[:, 0] - bbox[0]) * sx * 8, (bbox[3] - a[:, 1]) * sy * 8], 1).round().astype(np.int32))
    cv2.fillPoly(m, pts, 1, lineType=cv2.LINE_8, shift=3)
    return m


# --------------------------------------------------------------------------- v13 plan + render of one map clip
FPS = 25
FLY_S = 1.2       # camera move between phases
SAFE = {"bottom_px": 800, "left_px": 10, "right_px": 1910, "top_px": 10}
MARGIN = 0.05     # v13b: labels inside a 5 % margin of the frame
FADE_PX = 30      # v13b: graphics fade out over the 30 px above the caption line; nothing below it
MAX_LEAD_S = 0.25  # v13b: no value / label earlier than 0.25 s before its spoken word start
LEAD_S = 0.2      # target lead when the clip allows it
LABEL_FADE_S = 0.15  # v17b: place labels reach full opacity by word start - 0.05 s (was 0.4 s: still dim at the word)
BADGE_FADE_S = 0.3   # v17b: km badge appears already final (fade/scale-in, no count-up)


def _reveal(at, p0, p1, words, k=0):
    """v13b: never earlier than LEAD_S before the spoken word (old code clamped to p1 - 1.2 s, which showed
    values up to 1.4 s early). p1 is kept in the signature; the caller drops an item that cannot fit."""
    lo = p0 + 0.15 + 0.1 * k
    if at is None:
        return lo, None
    wt = float(words[at]["start"])
    return max(lo, wt - LEAD_S), wt


def plan_map(spec: Dict[str, Any], beats: Dict[str, Dict[str, Any]], words, hw, places: Optional[Dict[str, Any]] = None,
             w: int = 1920, h: int = 1080) -> Dict[str, Any]:
    from . import narration_values as NV
    places = places or load_places()
    P = places["places"]
    rows, problems = [], []
    all_beats = [b for p in spec["phases"] for b in p["beats"]]
    bs = [beats[b] for b in all_beats]
    c0, c1 = float(bs[0]["start"]), float(bs[-1]["end"])
    spoken = " ".join(x["hinglish"] for x in hw if c0 - 20.0 <= x["start"] < c1).lower()
    phases, shows, routes, chips = [], [], [], []
    prev_cam = None
    for pi, ph in enumerate(spec["phases"]):
        pb = [beats[b] for b in ph["beats"]]
        p0, p1 = float(pb[0]["start"]), float(pb[-1]["end"])
        target = fit_cam([(P[k]["lat"], P[k]["lon"]) for k in ph["fit"]], w, h, min_km=ph.get("min_km", 40))
        if ph.get("cam_from"):
            cf = ph["cam_from"]
            start_cam, fly = Cam(cf["lon"], cf["lat"], cf["km"], w, h), float(ph.get("fly_s", 2.0))
        elif prev_cam is not None and (abs(prev_cam.km - target.km) > 0.5 or abs(prev_cam.lon - target.lon) > 1e-3):
            start_cam, fly = prev_cam, FLY_S
        else:
            start_cam, fly = target, 0.0
        regs = []
        for rk in ph.get("regions", []):
            r = places["region_labels"][rk]
            v = NV.read_value({"ids": r["word_ids"], "kind": "text", "expect": r["expect"]}, words, hw)
            rows.append(_row(spec["id"], pi, "region_label", r["text"], v, p0, None))
            if v["status"] == "PASS":
                regs.append(r)
        for k, sh in enumerate(ph.get("show", [])):
            pl = P[sh["place"]]
            ids = [sh["at"]] if sh.get("at") is not None else sh.get("name_ids")
            if ids:
                if sh.get("at") is not None:
                    ids = [sh["at"]] + ([sh["at"] + 1] if len(pl["expect"].split()) > 1 else [])
                v = NV.read_value({"ids": ids, "kind": "text", "expect": pl["expect"]}, words, hw)
            else:
                ok = _norm_l(pl["expect"]) in _norm_l(spoken)
                v = {"status": "PASS" if ok else "WARN", "display": pl["expect"], "word_ids": [], "hindi": "", "hinglish": "",
                     "time": "", "note": "" if ok else f"'{pl['expect']}' not spoken within 20 s before/during the clip"}
            rv, wt = _reveal(sh.get("at"), p0, p1, words, k)
            pulse = _reveal(sh["pulse_at"], p0, p1, words)[0] if sh.get("pulse_at") is not None else rv
            if v["status"] == "PASS" and rv > c1 - 0.3:
                v = dict(v, status="WARN", note=f"spoken at {wt} s, after the clip ends ({c1:.2f} s): not shown")
            rows.append(_row(spec["id"], pi, "place:" + sh["place"], pl["label"], v, rv, wt))
            if v["status"] == "PASS":
                shows.append({"place": sh["place"], "label": pl["label"], "lat": pl["lat"], "lon": pl["lon"],
                              "anchor": sh.get("anchor", "r"), "reveal": min(rv, pulse), "label_at": rv, "pulse": pulse, "phase": pi,
                              "word_t": wt})
        for rt in ph.get("routes", []):
            rv, wt = _reveal(rt.get("at"), p0, p1, words)
            dur = min(float(rt.get("dur", 1.2)), max(0.4, c1 - rv - 0.3))
            km = None
            if rt.get("km"):
                v = NV.read_value({**rt["km"], "kind": "number"}, words, hw)
                kr, kwt = _reveal(rt.get("km_at"), p0, p1, words)
                kr = max(kr, rv + 0.3)
                if v["status"] == "PASS" and v.get("time") != "":
                    kwt = float(v["time"]) if kwt is None else kwt
                    if kr < kwt - MAX_LEAD_S:
                        kr = kwt - LEAD_S
                if v["status"] == "PASS" and kr > c1 - 0.3:
                    v = dict(v, status="WARN", note=f"spoken at {kwt} s, after the clip ends ({c1:.2f} s): not shown")
                rows.append(_row(spec["id"], pi, "route_km " + "->".join(rt["path"]), f"{v.get('display', '')} km", v, kr, kwt))
                if v["status"] == "PASS":
                    pts = [(P[a]["lat"], P[a]["lon"]) for a in rt["path"]]
                    crow = haversine_km(pts[0], pts[-1])
                    if v["value"] + 1e-6 < crow * 0.95:
                        problems.append(f"{spec['id']}: narrated {v['value']:g} km < straight line {crow:.1f} km")
                    km = {"value": v["value"], "reveal": kr, "side": rt.get("badge_side", 1), "straight_km": round(crow, 1)}
            routes.append({"path": rt["path"], "pts": [(P[a]["lat"], P[a]["lon"]) for a in rt["path"]], "reveal": rv, "dur": dur,
                           "bend": float(rt.get("bend", 0.12)), "km": km, "phase": pi})
        for k, ch in enumerate(ph.get("chips", [])):
            vals = [NV.read_value(v, words, hw) for v in ch.get("values", [])]
            rv, wt = _reveal(ch.get("at"), p0, p1, words, k)
            for v in vals:  # every value of the chip spoken before it appears (minus LEAD_S)
                if v["status"] == "PASS" and v.get("time") != "" and rv < float(v["time"]) - MAX_LEAD_S:
                    rv = float(v["time"]) - LEAD_S
            if rv > p1 - 0.3:
                vals = [dict(v, status="WARN", note="spoken after the chip's phase ends: not shown") for v in vals] or vals
                if not vals:
                    r_ = _row(spec["id"], pi, "chip", ch["fmt"], None, rv, wt)
                    r_.update(status="WARN", note="chip would start after its phase ends: not shown")
                    rows.append(r_)
                    continue
            bad = [v for v in vals if v["status"] != "PASS"]
            txt = NV.fill(ch["fmt"], vals) if not bad else ""
            import re as _re
            if _re.search(r"[0-9₹]", _re.sub(r"\{\d+\}", "", ch["fmt"])):
                problems.append(f"{spec['id']}: chip static text has a number")
                bad = [1]
            for v in (vals or [None]):
                rows.append(_row(spec["id"], pi, "chip", txt or ch["fmt"], v, rv, wt))
            if not bad:
                chips.append({"text": txt, "reveal": rv, "phase": pi, "slot": k, "near_route": ch.get("near_route")})
        tl = [c for c in chips if c["phase"] == pi and not c.get("near_route")]
        for j, c in enumerate(tl):
            c["slot"] = j  # v17b: chips placed beside a route leave no gap in the top-left stack
        phases.append({"start": p0, "end": p1, "beats": ph["beats"], "cam0": start_cam, "cam1": target, "fly": fly, "regions": regs})
        prev_cam = target
    for ph in phases:
        if not cam_inside_bbox(ph["cam0"], load_map_data_bbox()) or not cam_inside_bbox(ph["cam1"], load_map_data_bbox()):
            problems.append(f"{spec['id']}: camera leaves the map data box")
        if ph["end"] - ph["start"] > 8.5:
            problems.append(f"{spec['id']}: phase longer than 8.5 s")
    return {"id": spec["id"], "type": "map", "start": c0, "end": c1, "beats": all_beats, "phases": phases, "shows": shows,
            "routes": routes, "chips": chips, "rows": rows, "problems": problems, "frames": round(c1 * FPS) - round(c0 * FPS)}


def _norm_l(s: str) -> str:
    import re as _re
    return _re.sub(r"[^a-z0-9]+", "", s.lower())


def load_map_data_bbox() -> Sequence[float]:
    return json.loads(MAP_DATA.read_text(encoding="utf-8"))["bbox"]


def _row(clip, pi, item, shown, v, rv, wt):
    return lead_check({"clip": clip, "type": "map", "phase": pi + 1, "item": item, "shown_text": shown,
            "value": "" if v is None else v.get("display", ""), "word_ids": "" if v is None else "+".join(map(str, v.get("word_ids", []))),
            "hindi": "" if v is None else v.get("hindi", ""), "hinglish": "" if v is None else v.get("hinglish", ""),
            "word_time": "" if v is None else v.get("time", ""), "shown_at": round(rv, 3),
            "display_lead_s": "" if wt is None else round(wt - rv, 3),
            "status": "PASS" if v is None else v["status"], "note": "editorial text (no number)" if v is None else v.get("note", "")})


def lead_check(row: Dict[str, Any]) -> Dict[str, Any]:
    """v13b: lead_s = spoken word start - time the value / label appears; FAIL if > MAX_LEAD_S (0.25 s).
    Rows whose value is not shown (WARN) or that have no spoken word keep lead_s empty."""
    wt, sa = row.get("word_time", ""), row.get("shown_at", "")
    row["lead_s"] = ""
    if wt == "" or sa == "" or wt is None or row.get("status") == "WARN":
        return row
    lead = round(float(wt) - float(sa), 3)
    row["lead_s"] = lead
    if lead > MAX_LEAD_S + 1e-6:
        row["status"] = "FAIL"
        row["note"] = "; ".join(x for x in (row.get("note", ""), f"shown {lead:.2f} s before it is spoken (max {MAX_LEAD_S} s)") if x)
    return row


def cam_at(plan: Dict[str, Any], T: float) -> Tuple[Cam, Dict[str, Any]]:
    ph = next((p for p in plan["phases"] if p["start"] - 1e-9 <= T < p["end"]), plan["phases"][-1])
    t = T - ph["start"]
    cam = lerp_cam(ph["cam0"], ph["cam1"], t / ph["fly"]) if ph["fly"] > 0 and t < ph["fly"] else ph["cam1"]
    rest = D.clamp01((T - plan["start"]) / max(0.5, plan["end"] - plan["start"]))
    cam = Cam(cam.lon, cam.lat, cam.km * (1 - 0.03 * rest), cam.w, cam.h)  # slow push-in over the whole clip (v13b: no jump at phase changes)
    return cam, ph


def route_px(rt: Dict[str, Any], cam: Cam) -> np.ndarray:
    xy = [tuple(float(v) for v in cam.xy(lon, lat)) for lat, lon in rt["pts"]]
    parts = [bezier(a, b, rt["bend"] * (1 if k % 2 == 0 else -1)) for k, (a, b) in enumerate(zip(xy, xy[1:]))]
    return np.vstack([parts[0]] + [p[1:] for p in parts[1:]])


def map_frame(plan: Dict[str, Any], rend: "MapRenderer", T: float, boxes: Optional[list] = None) -> np.ndarray:
    cam, ph = cam_at(plan, T)
    regs = [dict(r, alpha=0.55 * D.clamp01((cam.km - 160) / 220)) for r in ph["regions"]]
    base = rend.base(cam, [r for r in regs if r["alpha"] > 0.01], boxes=boxes, avoid=place_label_boxes(plan, cam, ph["end"]))  # final labels: no jump when one appears
    f = base.copy()
    pi = plan["phases"].index(ph)
    for rt in plan["routes"]:
        if T < rt["reveal"]:
            continue
        path = route_px(rt, cam)
        shown = partial(path, D.ease_in_out((T - rt["reveal"]) / rt["dur"]))
        draw_polyline_glow(f, shown)
        if boxes is not None and len(shown) > 1:
            boxes.append(("route " + "->".join(rt["path"]), tuple(int(v) for v in (*shown.min(0), *shown.max(0)))))
    for sh in plan["shows"]:
        if T < sh["reveal"]:
            continue
        x, y = (float(v) for v in cam.xy(sh["lon"], sh["lat"]))
        if y > SAFE["bottom_px"] - 20:  # place moved below the caption line by the camera: no dot, no label
            continue
        draw_dot(f, x, y, (T - sh["reveal"]) / 0.45, T - sh["pulse"])
        if T >= sh["label_at"]:
            spr = label_sprite(sh["label"], 42)
            lx, ly = anchor_xy(x, y, spr, sh["anchor"])
            if ly + spr.shape[0] > SAFE["bottom_px"] - FADE_PX:
                continue
            lx, ly = clamp_margin(lx, ly, spr, cam.w, cam.h)
            a = label_alpha(sh, T)
            D.blit(f, spr, lx, ly + 6 * (1 - a), a)
            if boxes is not None:
                boxes.append((sh["label"], (int(lx), int(ly), int(lx + spr.shape[1]), int(ly + spr.shape[0]))))
    for rt in plan["routes"]:
        km = rt["km"]
        if not km or T < km["reveal"]:
            continue
        path = route_px(rt, cam)
        q = partial(path, km.get("at_frac", 0.33))
        d = q[-1] - q[-2] if len(q) > 1 else path[1] - path[0]
        nrm = np.array([-d[1], d[0]]) / (np.hypot(*d) or 1.0)
        c = q[-1] + nrm * 58 * km["side"]
        fin = label_sprite(km_text(km, T), 46, accent=True)  # v17b: final value from the first frame, fade in only
        a = D.ease_out_cubic((T - km["reveal"]) / BADGE_FADE_S)
        fx, fy = clamp_margin(c[0] - fin.shape[1] / 2, c[1] - fin.shape[0] / 2, fin, cam.w, cam.h)
        D.blit(f, fin, fx, fy + 6 * (1 - a), a)
        if boxes is not None:
            boxes.append((f"{int(km['value'])} km", (int(fx), int(fy), int(fx + fin.shape[1]), int(fy + fin.shape[0]))))
    for ch in plan["chips"]:
        if ch["phase"] != pi or T < ch["reveal"]:
            continue
        spr = label_sprite(ch["text"], 46)
        e = D.ease_out_cubic((T - ch["reveal"]) / 0.45)
        a = e
        last = pi == len(plan["phases"]) - 1
        if not last and T > ph["end"] - 0.3:
            a *= (ph["end"] - T) / 0.3
        if ch.get("near_route") is not None:  # v17b: beside its route leg (5 % margin, above the fade band) or dropped
            pos = chip_route_xy(plan, ch, cam, spr, ph)
            if pos is None:
                continue
            x, y = pos
            D.blit(f, spr, x, y + 6 * (1 - e), a)
            if boxes is not None:
                boxes.append((ch["text"], (int(x), int(y), int(x + spr.shape[1]), int(y + spr.shape[0]))))
            continue
        y = 120 + ch["slot"] * 92
        D.blit(f, spr, 120 - 50 * (1 - e), y, a)
        if boxes is not None:
            boxes.append((ch["text"], (120, y, 120 + spr.shape[1], y + spr.shape[0])))
    keep_above_caption(f, base)
    cr = D.text_sprite(CREDIT, "body", 22, (203, 213, 225), shadow=False)
    D.blit(f, cr, cam.w - cr.shape[1] - 24, 14, 0.75)
    return f


def label_alpha(sh: Dict[str, Any], T: float) -> float:
    """v17b: 0.15 s fade that ends no later than the spoken word; a label that can only appear at/after its word
    (word at the clip start) pops in at full opacity."""
    if T < sh["label_at"]:
        return 0.0
    dur = LABEL_FADE_S
    wt = sh.get("word_t")
    if wt not in (None, ""):
        dur = min(dur, float(wt) - sh["label_at"])
    if dur <= 0.02:
        return 1.0
    return D.ease_out_cubic((T - sh["label_at"]) / dur)


def km_text(km: Dict[str, Any], T: float) -> str:
    """v17b: the km badge text is the final narrated value on every frame it is visible (no count-up)."""
    return f"{int(km['value']):,} km"


def _leg_px(rt: Dict[str, Any], cam: Cam, leg: int) -> np.ndarray:
    xy = [tuple(float(v) for v in cam.xy(lon, lat)) for lat, lon in rt["pts"]]
    return bezier(xy[leg], xy[leg + 1], rt["bend"] * (1 if leg % 2 == 0 else -1))


def _inside_safe(x0, y0, x1, y1, w=1920, h=1080) -> bool:
    return x0 >= MARGIN * w and x1 <= w - MARGIN * w and y0 >= MARGIN * h and y1 <= SAFE["bottom_px"] - FADE_PX


def chip_route_xy(plan: Dict[str, Any], ch: Dict[str, Any], cam: Cam, spr: np.ndarray, ph: Dict[str, Any]):
    """v17b: top-left of a chip placed beside route leg near_route = [route index, leg index, preferred fraction].
    Side / fraction are chosen once at the phase-end camera: the spot must be inside the 5 % margin, above the
    caption fade band, and clear of place labels, dots and the km badge (+12 px); else None (chip dropped).
    Per frame the chip then follows that point of the leg as the camera moves."""
    ri, leg, pref = (list(ch["near_route"]) + [0, 0, 0.5])[:3] if isinstance(ch["near_route"], (list, tuple)) else (int(ch["near_route"]), 0, 0.5)
    rt = plan["routes"][ri]
    sh_, sw_ = spr.shape[:2]

    def spot(c: Cam, frac: float, side: int):
        pts = _leg_px(rt, c, leg)
        q = partial(pts, frac)
        d = q[-1] - q[-2] if len(q) > 1 else pts[1] - pts[0]
        nrm = np.array([-d[1], d[0]]) / (np.hypot(*d) or 1.0)
        cx, cy = q[-1] + nrm * side * (28 + 0.5 * abs(nrm[0]) * sw_ + 0.5 * abs(nrm[1]) * sh_)
        return cx - sw_ / 2, cy - sh_ / 2

    if "_route_spot" not in ch:
        cend, _ = cam_at(plan, ph["end"] - 0.05)
        avoid = place_label_boxes(plan, cend, ph["end"] - 0.05)
        for rt2 in plan["routes"]:
            if rt2["km"]:
                path = route_px(rt2, cend)
                q = partial(path, rt2["km"].get("at_frac", 0.33))
                fin = label_sprite(km_text(rt2["km"], 0), 46, accent=True)
                avoid.append((int(q[-1][0] - fin.shape[1] / 2 - 70), int(q[-1][1] - fin.shape[0] / 2 - 70),
                              int(q[-1][0] + fin.shape[1] / 2 + 70), int(q[-1][1] + fin.shape[0] / 2 + 70)))
        ch["_route_spot"] = None
        fracs = sorted({round(x, 2) for x in np.arange(0.1, 0.91, 0.05)}, key=lambda x: (abs(x - pref), x))
        for frac in fracs:
            for side in (1, -1):
                x, y = spot(cend, frac, side)
                b = (x, y, x + sw_, y + sh_)
                if _inside_safe(*b) and not any(_hit(tuple(int(v) for v in b), a, 12) for a in avoid):
                    ch["_route_spot"] = (frac, side)
                    break
            if ch["_route_spot"]:
                break
    if not ch["_route_spot"]:
        return None
    x, y = spot(cam, *ch["_route_spot"])
    return clamp_margin(x, y, spr, cam.w, cam.h)


def displayed_value_problems(plan: Dict[str, Any], fps: int = FPS) -> List[str]:
    """v17b QA, every frame of the map (render-plan level): the km badge shows exactly its final value whenever it is
    visible, chips show their final text, and each place label with a spoken word is at full opacity by that word."""
    out = []
    n0 = round(plan["start"] * fps)
    for n in range(plan["frames"]):
        T = (n0 + n + 0.5) / fps
        for rt in plan["routes"]:
            km = rt["km"]
            if km and T >= km["reveal"] and km_text(km, T) != f"{int(km['value']):,} km":
                out.append(f"{plan['id']}: frame {n} ({T:.2f} s) km badge '{km_text(km, T)}' != final {int(km['value'])} km")
        if len(out) >= 5:
            return out
    for sh in plan["shows"]:
        wt = sh.get("word_t")
        if wt not in (None, "") and label_alpha(sh, float(wt)) < 0.999:
            out.append(f"{plan['id']}: label '{sh['label']}' alpha {label_alpha(sh, float(wt)):.2f} at its word ({float(wt):.2f} s)")
    return out


def keep_above_caption(f: np.ndarray, base: np.ndarray, bottom: int = SAFE["bottom_px"], fade: int = FADE_PX) -> None:
    """v13b safe zone: every graphic (route, dots, pulse rings, labels, badges, chips) fades out over `fade` px above
    the caption line and nothing is drawn below it - rows >= bottom are the plain map (base) again."""
    y0 = bottom - fade
    r = np.clip((bottom - np.arange(y0, f.shape[0], dtype=np.float32)) / fade, 0, 1)[:, None, None]
    f[y0:] = base[y0:] * (1 - r) + f[y0:] * r


def caption_zone_diff(plan: Dict[str, Any], rend: "MapRenderer", T: float) -> float:
    """Max |frame - plain map| below the caption line at time T (must be 0: no graphics there). Credit is at the top."""
    cam, ph = cam_at(plan, T)
    regs = [dict(r, alpha=0.55 * D.clamp01((cam.km - 160) / 220)) for r in ph["regions"]]
    base = rend.base(cam, [r for r in regs if r["alpha"] > 0.01])
    f = map_frame(plan, rend, T)
    b = SAFE["bottom_px"]
    return float(np.abs(f[b:] - base[b:]).max())


def render_map(plan: Dict[str, Any], out: str | Path, data: Optional[Dict[str, Any]] = None, fps: int = FPS) -> Dict[str, Any]:
    rend = MapRenderer(data or load_map_data())
    wr = D.FrameWriter(out, rend.w, rend.h, fps)
    n0 = round(plan["start"] * fps)
    try:
        for n in range(plan["frames"]):
            wr.write(map_frame(plan, rend, (n0 + n + 0.5) / fps))
    finally:
        n = wr.close()
    return {"frames": n}


def map_boxes(plan: Dict[str, Any], rend: "MapRenderer") -> List[Tuple[str, Tuple[int, int, int, int]]]:
    """Label / badge / chip boxes at the end of every phase (everything shown) for the safe-zone + overlap check."""
    out = []
    for ph in plan["phases"]:
        for k, T in enumerate(check_times_phase(ph)):  # v13b: start / middle / end of the phase (M0 sea label was cut at the start)
            bx: list = []
            map_frame(plan, rend, T, boxes=bx)
            out += [(f"p{plan['phases'].index(ph) + 1}@{k}:{t}", b) for t, b in bx]
    return out


def check_times_phase(ph: Dict[str, Any]) -> List[float]:
    a, b = ph["start"], ph["end"]
    return [round(a + min(0.3, (b - a) / 4), 3), round((a + b) / 2, 3), round(b - 0.05, 3)]


def safe_zone_problems(plan: Dict[str, Any], rend: "MapRenderer") -> List[str]:
    """v13b FAIL list: any pixel of a map graphic below the caption line (y >= 800 at 1080p) at the check times."""
    out = []
    for ph in plan["phases"]:
        for T in check_times_phase(ph):
            d = caption_zone_diff(plan, rend, T)
            if d > 0.5:
                out.append(f"{plan['id']}: graphics below y={SAFE['bottom_px']} at {T:.2f} s (max diff {d:.1f})")
    return out


def phase_sample_times(plan: Dict[str, Any]) -> List[float]:
    return [round(max(p["start"] + 0.2, p["end"] - 0.2), 3) for p in plan["phases"]]
