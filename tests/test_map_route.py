"""v13/v13b map route clips: clipping, camera fit, caption-line safe zone, 5 % label margin, names must be
spoken, value lead <= 0.25 s, exact frame count. Offline (Natural Earth / OSM vectors from assets/map_data)."""
import subprocess

import numpy as np
import pytest

cv2 = pytest.importorskip("cv2")

from core import map_route as M
from core import motion_draw as D

if not M.MAP_DATA.is_file() or not M.PLACES.is_file():
    pytest.skip("map data / places not in this checkout", allow_module_level=True)


def _words(pairs, t0=10.0, step=0.4):
    w = [{"word": h, "start": round(t0 + i * step, 3), "end": round(t0 + i * step + 0.3, 3)} for i, (h, _) in enumerate(pairs)]
    hw = [{"word_id": i, "hinglish": r, "start": w[i]["start"]} for i, (_, r) in enumerate(pairs)]
    return w, hw


# 0 ab 1 chalenge 2 Bet 3 Dwarka 4 jo 5 Gopi 6 Talab 7 se 8 22 9 km ... 14 Sudarshan 15 setu
WORDS, HW = _words([("अब", "ab"), ("चलेंगे", "chalenge"), ("बेट", "Bet"), ("द्वारिका", "Dwarka"), ("जो", "jo"), ("गोपी", "Gopi"),
                    ("तालाब", "Talab"), ("से", "se"), ("22", "22"), ("किलोमीटर", "kilometre"), ("की", "ki"), ("दूरी", "doori"),
                    ("पर", "par"), ("है", "hai"), ("सुदर्शन", "Sudarshan"), ("सेतु", "setu")])
BEATS = {"Y_b01": {"beat": "Y_b01", "start": 10.0, "end": 14.0}, "Y_b02": {"beat": "Y_b02", "start": 14.0, "end": 16.6}}


def _spec(**over):
    ph1 = {"beats": ["Y_b01"], "fit": ["gopi_talav", "bet_dwarka", "sudarshan_setu"], "min_km": 34,
           "show": [{"place": "gopi_talav", "at": 5, "anchor": "r"}, {"place": "bet_dwarka", "at": 2, "anchor": "r"}],
           "routes": [{"path": ["gopi_talav", "sudarshan_setu", "bet_dwarka"], "at": 2, "dur": 1.2, "bend": 0.15,
                       "km": {"ids": [8]}, "km_at": 8, "badge_side": -1}]}
    ph2 = {"beats": ["Y_b02"], "fit": ["sudarshan_setu", "bet_dwarka"], "min_km": 26,
           "show": [{"place": "sudarshan_setu", "at": 14, "anchor": "tl"}]}
    spec = {"id": "MT_test", "phases": [ph1, ph2]}
    spec.update(over)
    return spec


@pytest.fixture(scope="module")
def rend():
    return M.MapRenderer(M.load_map_data())


@pytest.fixture(scope="module")
def plan():
    return M.plan_map(_spec(), BEATS, WORDS, HW)


# --------------------------------------------------------------------------- geometry
def test_clip_polygon_and_polyline_to_box():
    sq = [(-1, -1), (2, -1), (2, 2), (-1, 2)]
    out = M.clip_polygon(sq, (0, 0, 1, 1))
    assert all(0 - 1e-9 <= x <= 1 + 1e-9 and 0 - 1e-9 <= y <= 1 + 1e-9 for x, y in out)
    assert {(round(x, 6), round(y, 6)) for x, y in out} == {(0, 0), (1, 0), (1, 1), (0, 1)}
    runs = M.clip_polyline([(-1, 0.5), (0.5, 0.5), (2, 0.5), (2, 3), (0.5, 3), (0.5, 0.2)], (0, 0, 1, 1))
    assert len(runs) == 2
    assert runs[0][0] == pytest.approx((0, 0.5)) and runs[0][-1] == pytest.approx((1, 0.5))
    assert runs[1][0] == pytest.approx((0.5, 1)) and runs[1][-1] == pytest.approx((0.5, 0.2))
    assert M.point_in_poly(0.5, 0.5, [(0, 0), (1, 0), (1, 1), (0, 1)]) and not M.point_in_poly(2, 2, [(0, 0), (1, 0), (1, 1), (0, 1)])


def test_fit_cam_puts_points_in_box_above_caption():
    P = M.load_places()["places"]
    pts = [(P[k]["lat"], P[k]["lon"]) for k in ("dwarka", "jamnagar")]
    box = (0.18, 0.13, 0.82, 0.62)
    cam = M.fit_cam(pts, box=box, min_km=10)
    for lat, lon in pts:
        x, y = (float(v) for v in cam.xy(lon, lat))
        assert box[0] * 1920 - 1 <= x <= box[2] * 1920 + 1 and box[1] * 1080 - 1 <= y <= box[3] * 1080 + 1
        assert y < M.SAFE["bottom_px"]
    assert M.fit_cam(pts[:1] * 2, min_km=40).km == pytest.approx(40)   # one point -> min_km
    assert M.cam_inside_bbox(cam, M.load_map_data_bbox())


# --------------------------------------------------------------------------- safe zone / caption line
def test_graphics_never_below_caption_line(plan, rend):
    """Phase 2 zooms on the bridge: Gopi Talav (route start) is below the frame, so the route crosses y=800.
    Every pixel below the caption line must equal the plain map, and the check must find nothing."""
    T = plan["phases"][1]["end"] - 0.05
    cam, _ = M.cam_at(plan, T)
    path = M.route_px(plan["routes"][0], cam)
    assert path[:, 1].max() > M.SAFE["bottom_px"]                     # the route geometry does cross the caption line
    assert M.caption_zone_diff(plan, rend, T) == 0.0
    assert M.safe_zone_problems(plan, rend) == []


def test_keep_above_caption_restores_base_and_fades():
    base = np.zeros((1080, 64, 3), np.float32)
    f = np.full((1080, 64, 3), 200.0, np.float32)
    M.keep_above_caption(f, base)
    b = M.SAFE["bottom_px"]
    assert f[b:].max() == 0.0 and f[b - M.FADE_PX - 1].min() == 200.0
    assert 0.0 < f[b - M.FADE_PX // 2, 0, 0] < 200.0                  # feathered, not a hard edge


def test_safe_zone_check_fails_when_graphics_leak(plan, rend, monkeypatch):
    monkeypatch.setattr(M, "keep_above_caption", lambda f, base, **k: None)   # old behaviour: no clamp
    assert M.safe_zone_problems(plan, rend), "a route through the caption area must FAIL"


# --------------------------------------------------------------------------- 5 % label margin
def test_clamp_margin_and_box_check():
    spr = np.zeros((40, 300, 4), np.float32)
    x, y = M.clamp_margin(-200, 1050, spr)
    assert x == pytest.approx(0.05 * 1920) and y + 40 <= M.SAFE["bottom_px"] - M.FADE_PX
    x, y = M.clamp_margin(1900, -50, spr)
    assert x + 300 == pytest.approx(0.95 * 1920) and y == pytest.approx(0.05 * 1080)
    assert M.label_box_problems([("p1@0:Arabian Sea", (10, 400, 200, 440))])          # cut at the left edge
    assert M.label_box_problems([("p1@0:22 km", (500, 760, 600, 790))])               # in the fade band
    assert M.label_box_problems([("p1@0:route a->b", (-50, 0, 3000, 1500))]) == []   # routes: pixel check instead
    assert M.label_box_problems([("p1@0:Dwarka", (400, 300, 600, 340))]) == []


def test_all_plan_labels_inside_margin(plan, rend):
    boxes = M.map_boxes(plan, rend)
    assert boxes and M.label_box_problems(boxes) == []
    labels = {t.split(":", 1)[1] for t, _ in boxes}
    assert {"Gopi Talav", "Bet Dwarka", "Sudarshan Setu", "22 km"} <= labels


def test_region_label_avoids_place_labels(rend):
    cam = M.Cam(69.0, 22.3, 120.0)
    lab = {"text": "Arabian Sea", "lat": 22.3, "lon": 69.0, "alpha": 0.55}
    a, b = [], []
    rend.base(cam, [lab], boxes=a)
    x0, y0, x1, y1 = a[0][1]
    rend.base(cam, [lab], boxes=b, avoid=[(x0, y0, x1, y1)])
    assert b[0][1] != a[0][1] and not M._hit(b[0][1], (x0, y0, x1, y1))


# --------------------------------------------------------------------------- names must be spoken / lead
def test_plan_names_must_exist_in_narration():
    spec = _spec()
    spec["phases"][0]["show"].append({"place": "nageshwar", "at": 3, "anchor": "l"})   # word 3 is 'Dwarka', not Nageshwar
    spec["phases"][0]["show"].append({"place": "shivrajpur", "anchor": "l"})            # no word id, never spoken
    p = M.plan_map(spec, BEATS, WORDS, HW)
    st = {r["item"]: r["status"] for r in p["rows"]}
    assert st["place:nageshwar"] == "WARN" and st["place:shivrajpur"] == "WARN"
    shown = {s["place"] for s in p["shows"]}
    assert "nageshwar" not in shown and "shivrajpur" not in shown
    assert {"gopi_talav", "bet_dwarka", "sudarshan_setu"} <= shown
    for r in p["rows"]:                     # every shown name is in the Hinglish words it cites
        if r["status"] == "PASS" and r["item"].startswith("place:") and r["word_ids"]:
            assert M._norm_l(r["value"]) in M._norm_l(r["hinglish"])


def test_values_never_more_than_025s_early(plan):
    for r in plan["rows"]:
        if r["lead_s"] != "":
            assert r["lead_s"] <= M.MAX_LEAD_S + 1e-9 and r["status"] != "FAIL", r
    km = plan["routes"][0]["km"]
    assert km["reveal"] == pytest.approx(WORDS[8]["start"] - 0.2)
    setu = next(s for s in plan["shows"] if s["place"] == "sudarshan_setu")
    assert setu["label_at"] >= WORDS[14]["start"] - M.MAX_LEAD_S


def test_word_after_clip_end_is_warn_not_shown_early():
    beats = {"Y_b01": BEATS["Y_b01"], "Y_b02": {"beat": "Y_b02", "start": 14.0, "end": 15.6}}   # 'Sudarshan' at 15.6
    p = M.plan_map(_spec(), beats, WORDS, HW)
    row = next(r for r in p["rows"] if r["item"] == "place:sudarshan_setu")
    assert row["status"] == "WARN" and "after the clip ends" in row["note"]
    assert "sudarshan_setu" not in {s["place"] for s in p["shows"]}


def test_lead_check_marks_fail():
    r = M.lead_check({"word_time": 92.47, "shown_at": 91.36, "status": "PASS", "note": ""})
    assert r["status"] == "FAIL" and r["lead_s"] == pytest.approx(1.11)
    r = M.lead_check({"word_time": 92.47, "shown_at": 92.27, "status": "PASS", "note": ""})
    assert r["status"] == "PASS" and r["lead_s"] == pytest.approx(0.2)
    assert M.lead_check({"word_time": "", "shown_at": 1.0, "status": "PASS"})["lead_s"] == ""


# --------------------------------------------------------------------------- frames
def test_render_frame_count_exact(tmp_path, rend):
    beats = {"Y_b01": {"beat": "Y_b01", "start": 10.0, "end": 10.4}}
    spec = {"id": "MT_short", "phases": [{"beats": ["Y_b01"], "fit": ["dwarka", "bet_dwarka"], "min_km": 40,
                                          "show": [{"place": "bet_dwarka", "at": 2, "anchor": "r"}]}]}
    p = M.plan_map(spec, beats, WORDS, HW)
    assert p["frames"] == round(10.4 * 25) - round(10.0 * 25) == 10
    out = tmp_path / "m.mp4"
    res = M.render_map(p, out, rend.d)
    n = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                            "stream=nb_read_frames", "-of", "csv=p=0", str(out)], capture_output=True, text=True, encoding="utf-8").stdout.strip())
    assert n == res["frames"] == p["frames"]


def test_coast_feather_has_no_step(rend):
    """Inside the OSM box edge the land mask is a blend (values between 0 and 255), not a hard switch."""
    fine = rend.d.get("_fine")
    if not fine:
        pytest.skip("no OSM fine coast data")
    cam = M.Cam(70.25, 22.55, 60.0)                       # east edge of the fine box, Jamnagar coast
    a = rend.base(cam, feather=True)
    b = rend.base(cam, feather=False)
    assert np.abs(a - b).max() > 1                       # the feather changes the seam
    x, _ = cam.xy(fine["bbox"][2], 22.55)
    assert abs(float(x) - 960) < 2                        # box edge is in view


# --------------------------------------------------------------------------- v17b
def test_v17b_km_badge_final_on_every_frame_and_labels_full_at_word(plan):
    assert M.displayed_value_problems(plan) == []
    km = plan["routes"][0]["km"]
    assert M.km_text(km, km["reveal"]) == M.km_text(km, km["reveal"] + 0.05) == "22 km"
    for sh in plan["shows"]:
        if sh["word_t"] not in (None, ""):
            assert M.label_alpha(sh, float(sh["word_t"])) == pytest.approx(1.0)
            assert M.label_alpha(sh, sh["label_at"] - 0.01) == 0.0


def test_v17b_label_spoken_at_clip_start_pops_in_full():
    sh = {"label_at": 10.15, "word_t": 10.1}
    assert M.label_alpha(sh, 10.15) == 1.0
    sh = {"label_at": 10.0, "word_t": 10.2}                                   # normal: 0.15 s fade ends before the word
    assert 0 < M.label_alpha(sh, 10.05) < 1 and M.label_alpha(sh, 10.15) == pytest.approx(1.0)


def test_v17b_label_alpha_check_fails_slow_fade(plan, monkeypatch):
    monkeypatch.setattr(M, "LABEL_FADE_S", 0.4)
    sh = dict(plan["shows"][1], word_t=None)
    assert M.label_alpha(sh, sh["label_at"] + 0.2) < 1.0                      # the v17 0.4 s fade: still dim 0.2 s in


def _chip_plan(text="Good highway"):
    sp = _spec()
    sp["phases"][1]["chips"] = [{"fmt": text, "at": 14, "near_route": [0, 0, 0.5]}, {"fmt": "New bridge", "at": 14}]
    return M.plan_map(sp, BEATS, WORDS, HW)


def test_v17b_route_chip_beside_its_route_inside_margin(rend):
    p = _chip_plan()
    T = p["phases"][1]["end"] - 0.05
    bx: list = []
    M.map_frame(p, rend, T, boxes=bx)
    box = dict(bx)["Good highway"]
    x0, y0, x1, y1 = box
    assert x0 >= 0.05 * 1920 and x1 <= 0.95 * 1920 and y0 >= 0.05 * 1080 and y1 <= M.SAFE["bottom_px"] - M.FADE_PX
    cam, _ = M.cam_at(p, T)
    leg = M._leg_px(p["routes"][0], cam, 0)
    c = np.array([(x0 + x1) / 2, (y0 + y1) / 2])
    assert np.hypot(*(leg - c).T).min() < 0.5 * (x1 - x0) + 80               # next to the route, not in a corner
    assert dict(bx)["New bridge"][:2] == (120, 120)                           # top-left stack has no gap
    assert M.label_box_problems(bx) == []


def test_v17b_route_chip_dropped_when_no_space(rend):
    p = _chip_plan("A chip text far too long to ever fit beside a route line inside the title safe margin")
    bx: list = []
    M.map_frame(p, rend, p["phases"][1]["end"] - 0.05, boxes=bx)
    assert not any(t.startswith("A chip") for t, _ in bx)
