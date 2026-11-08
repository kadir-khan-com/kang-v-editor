"""Prepare the small map-data file used by core/map_route.py (run once; output is committed to the repo).

Source: Natural Earth 1:10m vector data (PUBLIC DOMAIN, naturalearthdata.com), GeoJSON copies from
github.com/nvkelso/natural-earth-vector (master). Layers: ne_10m_land, ne_10m_admin_1_states_provinces_lines,
ne_10m_admin_0_boundary_lines_land. Clipped to a Gujarat box by own code (Sutherland-Hodgman for polygons,
segment clipping for lines). NO OpenStreetMap tiles are used anywhere.

Usage: python tools/prep_map_data.py [--src DIR_WITH_GEOJSON] [--out assets/map_data/ne_10m_gujarat_clip.json]
Without --src the three files are downloaded once (about 33 MB) from raw.githubusercontent.com.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from core.map_route import clip_polygon, clip_polyline  # noqa: E402

BBOX = (66.5, 19.8, 75.0, 25.2)  # lon0, lat0, lon1, lat1
BASE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/"
LAYERS = {"land": "ne_10m_land", "admin1_lines": "ne_10m_admin_1_states_provinces_lines",
          "admin0_lines": "ne_10m_admin_0_boundary_lines_land"}


def _rings(geom):
    if geom["type"] == "Polygon":
        yield from geom["coordinates"][:1]  # outer ring (holes = lakes are dropped: not needed at this scale)
    elif geom["type"] == "MultiPolygon":
        for poly in geom["coordinates"]:
            yield poly[0]


def _lines(geom):
    if geom["type"] == "LineString":
        yield geom["coordinates"]
    elif geom["type"] == "MultiLineString":
        yield from geom["coordinates"]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src")
    ap.add_argument("--out", default=str(ROOT / "assets" / "map_data" / "ne_10m_gujarat_clip.json"))
    ap.add_argument("--osm-only", action="store_true", help="only rebuild the OSM-refined Dwarka/Gulf coast file")
    ap.add_argument("--fetch-osm", action="store_true", help="fetch the 2 Nominatim district polygons if missing")
    a = ap.parse_args(argv)
    md = ROOT / "assets" / "map_data"
    if a.osm_only:
        print(json.dumps(refine_osm(str(md / "osm_dwarka_gulf_coast.json"), a.out, str(md / "_osm_nominatim"), a.fetch_osm)))
        return 0
    src = {}
    for key, name in LAYERS.items():
        if a.src:
            data = (Path(a.src) / f"{name}.geojson").read_bytes()
        else:
            req = urllib.request.Request(BASE + name + ".geojson", headers={"User-Agent": "KANG map prep"})
            data = urllib.request.urlopen(req, timeout=120).read()
        src[key] = {"file": f"{name}.geojson", "url": BASE + name + ".geojson", "bytes": len(data),
                    "sha256": hashlib.sha256(data).hexdigest(), "data": json.loads(data.decode("utf-8"))}
    land = []
    for ft in src["land"]["data"]["features"]:
        for ring in _rings(ft["geometry"]):
            c = clip_polygon([tuple(p[:2]) for p in ring], BBOX)
            if len(c) >= 3:
                land.append([[round(x, 5), round(y, 5)] for x, y in c])
    state_lines, intl = [], []
    for ft in src["admin1_lines"]["data"]["features"]:
        nm = (ft["properties"].get("NAME") or "")
        if "Gujarat" not in nm:
            continue
        for ln in _lines(ft["geometry"]):
            for seg in clip_polyline([tuple(p[:2]) for p in ln], BBOX):
                state_lines.append({"name": nm, "coords": [[round(x, 5), round(y, 5)] for x, y in seg]})
    for ft in src["admin0_lines"]["data"]["features"]:
        for ln in _lines(ft["geometry"]):
            for seg in clip_polyline([tuple(p[:2]) for p in ln], BBOX):
                intl.append({"coords": [[round(x, 5), round(y, 5)] for x, y in seg]})
    out = {"schema": "kang.map_data/1.0", "bbox": BBOX,
           "source": "Natural Earth 1:10m (public domain), naturalearthdata.com; GeoJSON from github.com/nvkelso/natural-earth-vector",
           "licence": "Public domain (Natural Earth terms of use)", "prepared": _dt.date.today().isoformat(),
           "inputs": {k: {kk: v[kk] for kk in ("file", "url", "bytes", "sha256")} for k, v in src.items()},
           "land": land, "state_lines": state_lines, "intl_lines": intl}
    Path(a.out).parent.mkdir(parents=True, exist_ok=True)
    Path(a.out).write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    print(json.dumps({"out": a.out, "land_rings": len(land), "land_points": sum(len(r) for r in land),
                      "state_lines": len(state_lines), "intl_lines": len(intl)}))
    return 0



# --------------------------------------------------------------------------- OSM coast refinement (Dwarka / Okha / Gulf)
FINE_BBOX = (68.80, 21.95, 70.25, 22.70)
FINE_STEP = 0.0005  # degrees (~55 m)
OSM_FILES = ["relation_8259845_devbhumi_dwaraka.json", "relation_8271162_jamnagar.json"]
NOMINATIM = ("https://nominatim.openstreetmap.org/search?format=json&polygon_geojson=1&polygon_threshold=0.0003&limit=1&q=")
OSM_QUERIES = {"relation_8259845_devbhumi_dwaraka.json": "Devbhumi Dwaraka", "relation_8271162_jamnagar.json": "Jamnagar district"}


def refine_osm(out_path: str, ne_path: str, osm_dir: str, fetch: bool = False) -> dict:
    """Natural Earth 10m is ~1-2 km off at Dwarka and has no Beyt Dwarka island. The two coastal district
    polygons from OpenStreetMap (ODbL; via 2 Nominatim lookups, polygon_geojson) follow the coastline, so inside
    FINE_BBOX: land = district polygons + NE land that is not a coastal bulge next to them. Raster at 55 m,
    vectorised back to rings (cv2.findContours) = derived ODbL data, credit '© OpenStreetMap contributors'."""
    import time
    import cv2
    import numpy as np
    from core.map_route import _geo_raster
    od = Path(osm_dir)
    od.mkdir(parents=True, exist_ok=True)
    polys = []
    for fn in OSM_FILES:
        p = od / fn
        if not p.is_file() and fetch:
            import urllib.parse
            req = urllib.request.Request(NOMINATIM + urllib.parse.quote(OSM_QUERIES[fn]),
                                         headers={"User-Agent": "KANG-video-tool/0.7 (map prep)"})
            p.write_bytes(urllib.request.urlopen(req, timeout=60).read())
            time.sleep(1.5)
        g = json.loads(p.read_text(encoding="utf-8"))[0]["geojson"]
        for poly in (g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]):
            polys.append(poly[0])
    ne = json.loads(Path(ne_path).read_text(encoding="utf-8"))
    w = int(round((FINE_BBOX[2] - FINE_BBOX[0]) / FINE_STEP))
    h = int(round((FINE_BBOX[3] - FINE_BBOX[1]) / FINE_STEP))
    ne_m = _geo_raster(ne["land"], FINE_BBOX, w, h)
    d_m = _geo_raster(polys, FINE_BBOX, w, h)
    r = int(4.0 / (FINE_STEP * 110.57))  # 4 km
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))
    near_d = cv2.dilate(d_m, k)
    near_sea = cv2.dilate((1 - ne_m).astype(np.uint8), k)
    bulge = (ne_m == 1) & (d_m == 0) & (near_d == 1) & (near_sea == 1)
    land = ((ne_m == 1) & ~bulge) | (d_m == 1)
    cnts, hier = cv2.findContours(land.astype(np.uint8), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    rings, holes = [], []
    for c, hh in zip(cnts, hier[0]):
        if cv2.contourArea(c) < 6:
            continue
        c = cv2.approxPolyDP(c, 0.6, True)[:, 0, :].astype(float)
        ll = [[round(FINE_BBOX[0] + (x + 0.5) * FINE_STEP, 5), round(FINE_BBOX[3] - (y + 0.5) * FINE_STEP, 5)] for x, y in c]
        (holes if hh[3] >= 0 else rings).append(ll)
    out = {"schema": "kang.map_data_fine/1.0", "bbox": FINE_BBOX, "step_deg": FINE_STEP,
           "source": "OpenStreetMap district boundaries (Devbhumi Dwaraka relation 8259845, Jamnagar relation 8271162; "
                     "coast-following admin polygons) via Nominatim polygon_geojson + Natural Earth 10m land inland",
           "licence": "ODbL 1.0 (derived from OpenStreetMap) - credit '© OpenStreetMap contributors'; NE part public domain",
           "inputs": {fn: hashlib.sha256((od / fn).read_bytes()).hexdigest() for fn in OSM_FILES},
           "prepared": _dt.date.today().isoformat(), "rings": rings, "holes": holes,
           "bulge_cells_removed": int(bulge.sum())}
    Path(out_path).write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    return {"out": out_path, "rings": len(rings), "holes": len(holes), "points": sum(len(x) for x in rings + holes),
            "bulge_cells_removed": int(bulge.sum())}


if __name__ == "__main__":
    raise SystemExit(main())
