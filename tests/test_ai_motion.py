"""v17 AI motion (core/ai_motion.py): selection, gate, masked composite, apply, CSV + package hooks.
No GPU, no model: the Kaggle I2V output is mocked with synthetic frames."""
import json
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
cv2 = pytest.importorskip("cv2")
from core import ai_motion as am  # noqa: E402
from core import beats as B  # noqa: E402

CFG = am.load_cfg()


def _row(beat, start, end, asset, match="exact", title="", **kw):
    return {"beat": beat, "scene": beat.split("_")[0], "start": start, "end": end, "first_word_time": start,
            "text": "", "asset": asset, "source_dir": "assets/x", "asset_source": "", "match": match, "role": "v9_shot",
            "v9_shot": "", "licence": "CC BY", "title": title or asset, "source_page": "", "motion": "", "notes": "", **kw}


def _scene(w=320, h=176, seed=0):
    """Top half flat sky (blue), bottom half a rigid 'building' texture (grid of rectangles)."""
    rng = np.random.default_rng(seed)
    im = np.zeros((h, w, 3), np.uint8)
    im[: h // 2] = (90, 150, 220)
    im[h // 2:] = (150, 130, 110)
    for y in range(h // 2 + 4, h - 8, 14):
        for x in range(4, w - 10, 18):
            c = int(rng.integers(40, 90))
            cv2.rectangle(im, (x, y), (x + 10, y + 8), (c, c, c), -1)
    return im


def _clouds(src, n=25, amp=12.0):
    """Sky region gets a slowly drifting soft blob pattern; building untouched."""
    h, w = src.shape[:2]
    yy, xx = np.mgrid[0:h // 2, 0:w].astype(np.float32)
    out = []
    for t in range(n):
        f = src.astype(np.float32).copy()
        blob = amp * np.sin((xx + 3 * t) / 9.0) * np.cos(yy / 7.0)
        f[: h // 2] += blob[..., None]
        out.append(np.clip(f, 0, 255).astype(np.uint8))
    return np.stack(out)


def test_frames_for_is_4k_plus_1_and_bounded():
    for d in (2.0, 3.16, 5.36, 8.12, 20.0):
        n = am.frames_for(d, CFG)
        assert (n - 1) % 4 == 0
        assert CFG["model"]["min_frames"] <= n <= CFG["model"]["max_frames"]
        m = CFG["model"]
        if d <= (m["max_frames"] - 1) * m["max_slow"] / m["fps"]:  # v17 T4 caps (81 fr x 2.0): longer holds -> max_frames,
            assert n * m["max_slow"] / m["fps"] >= d - 0.05            # render_clip then FAILs them on slow-down
        else:
            assert n == m["max_frames"]


def test_kinds_from_keywords():
    assert am.kinds_for("S18_2_shivrajpur_beach_daytime.jpg", "", CFG)[0] == "sea"
    assert am.kinds_for("x_gomti_river.jpg", "", CFG)[0] == "water"
    assert am.kinds_for("boat_ride.jpg", "", CFG)[0] == "boat"
    assert am.kinds_for("dwarkadhish_temple.jpg", "", CFG) == ["flag"]
    assert am.kinds_for("railway_station.jpg", "", CFG) == []


def test_select_rules_faces_holds_labels_videos_eye():
    cfg = json.loads(json.dumps(CFG))
    cfg["eye_rejects_plan"] = {"S05_b01": "crowd"}
    cfg["eye_kind"] = {}
    rows = [_row("S01_b01", 0.0, 5.0, "a_beach.jpg"),
            _row("S02_b01", 5.0, 6.0, "b_beach.jpg"),                       # too short
            _row("S03_b01", 6.0, 11.0, "c_beach.mp4"),                      # video
            _row("S04_b01", 11.0, 16.0, "CARD_x.jpg", match="text_card"),   # card
            _row("S05_b01", 16.0, 21.0, "e_beach.jpg"),                     # eye reject
            _row("S06_b01", 21.0, 26.0, "f_beach_people.jpg"),              # face (mock)
            _row("S07_b01", 26.0, 31.0, "g_station.jpg"),                   # no element
            _row("S08_b01", 31.0, 34.0, "h_gomti_river.jpg", match="representative"),
            _row("S08_b02", 34.0, 36.0, "h_gomti_river.jpg", match="representative")]  # merged 5 s clip
    an = lambda p: {"faces": 2 if "people" in p.name else 0, "width": 1920, "sky_frac": 0.05}  # noqa: E731
    c, rj = am.select(rows, cfg, an)
    got = {x["first_beat"]: x for x in c}
    assert set(got) == {"S01_b01", "S08_b01"}
    assert got["S08_b01"]["beats"] == ["S08_b01", "S08_b02"] and got["S08_b01"]["match"] == "representative"
    why = {r["beat"]: r["why"] for r in rj}
    assert "hold" in why["S02_b01"] and why["S03_b01"] == "not a still" and "text_card" in why["S04_b01"]
    assert why["S05_b01"].startswith("eye") and "face" in why["S06_b01"] and "no water" in why["S07_b01"]


def test_model_input_and_band():
    fr = np.zeros((1080, 1920, 3), np.uint8)
    mi = am.model_input(fr)
    assert mi.shape == (704, 1280, 3)
    y0, y1 = am.band_rows()
    assert (y0, y1) == (12, 1068)


def test_gate_pass_on_sky_motion_and_mask_excludes_building():
    src = _scene()
    raw = _clouds(src)
    g = am.gate_raw(src, raw, "sky", CFG)
    assert g["status"] in ("PASS", "WARN"), g["why"]
    m = g["_mask"]
    h = m.shape[0]
    assert m[: h // 2 - 6].mean() > 0.3          # sky can move
    assert m[h // 2 + 8:].max() < 0.05            # building never comes from the AI clip


def test_gate_fails_camera_drift_warping_and_no_motion():
    src = _scene()
    drift = np.stack([np.roll(src, k // 3, axis=1) for k in range(25)])          # camera pans ~8 px
    assert am.gate_raw(src, drift, "sky", CFG)["status"] == "FAIL"
    rng = np.random.default_rng(1)
    warp = []
    for t in range(25):  # building melts: random local displacement growing over time
        f = src.copy()
        dx = (rng.normal(0, 1, (src.shape[0], src.shape[1])) * t * 0.4).astype(np.float32)
        mx, my = np.meshgrid(np.arange(src.shape[1], dtype=np.float32), np.arange(src.shape[0], dtype=np.float32))
        mx = cv2.GaussianBlur(mx + dx * 6, (0, 0), 3)
        f = cv2.remap(src, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        warp.append(f)
    gw = am.gate_raw(src, np.stack(warp), "sky", CFG)
    assert gw["status"] == "FAIL" and any("warping" in w or "drift" in w or "flicker" in w for w in gw["why"]), gw
    still = np.stack([src] * 25)
    gs = am.gate_raw(src, still, "sky", CFG)
    assert gs["status"] == "FAIL" and any("no usable motion" in w for w in gs["why"])


def test_cell_flicker_split_rigid_vs_fluid_cells():
    """KANG_018 calibration: a sky cell whose mean jumps (flag / wave passing) is judged with cell_flicker_fluid_fail,
    a building cell that pumps brightness still fails with cell_flicker_fail."""
    src = _scene()
    base = _clouds(src)
    h, w = src.shape[:2]
    sky = []
    for t in range(len(base)):  # a dark 'flag' square jumping in/out of one sky cell every other frame
        f = base[t].copy()
        if t % 2:
            f[10:18, 44:52] = (150, 20, 30)
        sky.append(f)
    g = am.gate_raw(src, np.stack(sky), "sky", CFG)
    assert CFG["gate"]["cell_flicker_fail"] < g["cell_flicker_fluid_max"] < CFG["gate"]["cell_flicker_fluid_fail"], g
    assert g["cell_flicker_max"] < CFG["gate"]["cell_flicker_fail"]
    assert not any(x.startswith("flicker") for x in g["why"]), g["why"]
    pump = []
    for t in range(len(base)):  # building block pumps +/-25 luma every other frame
        f = base[t].astype(np.int16)
        if t % 2:
            f[h // 2 + 10: h - 10, 20:120] += 25
        pump.append(np.clip(f, 0, 255).astype(np.uint8))
    gp = am.gate_raw(src, np.stack(pump), "sky", CFG)
    assert gp["status"] == "FAIL" and gp["cell_flicker_max"] > CFG["gate"]["cell_flicker_fail"], gp


def test_time_map_natural_and_slow():
    pos, slow = am.time_map(50, 61, 25, 24)
    assert slow == 1.0 and abs(pos[1] - 0.96) < 1e-9
    pos, slow = am.time_map(130, 77, 25, 24)
    assert pos[0] == 0 and abs(pos[-1] - 76) < 1e-9 and 1.6 < slow < 1.7


def test_render_clip_masked_composite_keeps_photo_pixels(tmp_path):
    from PIL import Image
    big = cv2.resize(_scene(), (1920, 1056), interpolation=cv2.INTER_NEAREST)
    big = np.vstack([np.repeat(big[:1], 12, 0), big, np.repeat(big[-1:], 12, 0)])
    Image.fromarray(big).save(tmp_path / "photo.png")
    src_in = am.model_input(am.cover_frame(tmp_path / "photo.png"), 320, 176)
    raw = _clouds(src_in, n=25)
    am.encode(raw, tmp_path / "raw.mp4", 320, 176, 24, crf=4)
    cfg = json.loads(json.dumps(CFG))
    g = am.render_clip(tmp_path / "photo.png", tmp_path / "raw.mp4", tmp_path / "AI_x.mp4", 20, "sky", cfg)
    assert g["status"] in ("PASS", "WARN"), g["why"]
    assert (tmp_path / "AI_x.mp4").is_file() and g["out_frames"] == 20 and g["composite_ssim_first"] >= 0.95
    out, fps = am.read_video(tmp_path / "AI_x.mp4")
    assert out.shape == (20, 1080, 1920, 3) and round(fps) == 25
    base = am.cover_frame(tmp_path / "photo.png").astype(int)
    bottom = slice(700, 1040)  # building rows: must stay the photo (only codec noise)
    assert np.abs(out[-1][bottom, :1500].astype(int) - base[bottom, :1500]).mean() < 3.0
    top = slice(100, 400)
    assert np.abs(out[10][top].astype(int) - out[0][top].astype(int)).mean() > 2.0  # sky moves (half a wave period)


def test_apply_sets_ai_columns_keeps_label_and_needs_eye_pass(tmp_path):
    rows = [_row("S01_b01", 0.0, 2.0, "a_beach.jpg", match="representative", parallax_clip="PX_a.mp4",
                 parallax_dir="x", parallax_status="PASS"),
            _row("S01_b02", 2.0, 4.0, "a_beach.jpg", match="representative", parallax_clip="PX_a.mp4",
                 parallax_dir="x", parallax_status="PASS"),
            _row("S02_b01", 4.0, 8.0, "b_sea.jpg")]
    (tmp_path / "AI_S01_b01.mp4").write_bytes(b"x")
    (tmp_path / "AI_S02_b01.mp4").write_bytes(b"x")
    rep = [{"beat": "S01_b01", "asset": "a_beach.jpg", "status": "WARN", "clip": "AI_S01_b01.mp4", "out_frames": 100},
           {"beat": "S02_b01", "asset": "b_sea.jpg", "status": "PASS", "clip": "AI_S02_b01.mp4", "out_frames": 100}]
    out, info = am.apply_ai(rows, rep, tmp_path, ["S01_b01"], "Wan2.2-TI2V-5B")
    assert info["used"] == ["S01_b01"] and any("eye_pass" in s for s in info["skipped"])
    a = {r["beat"]: r for r in out}
    for b in ("S01_b01", "S01_b02"):
        assert a[b]["ai_motion_clip"] == "AI_S01_b01.mp4" and a[b]["match"] == "representative"
        assert a[b]["parallax_clip"] == "" and a[b]["asset"] == "a_beach.jpg"
    assert not a["S02_b01"].get("ai_motion_clip")
    rep[1]["out_frames"] = 99  # wrong length -> refused even with eye pass
    _, info2 = am.apply_ai(rows, rep, tmp_path, ["S01_b01", "S02_b01"], "Wan2.2-TI2V-5B")
    assert info2["used"] == ["S01_b01"]
    p = am.write_assign_ai(out, tmp_path / "v.csv")
    back = B.read_assign_csv(p)
    m = {r["beat"]: r for r in back}
    assert m["S01_b01"]["motion"] == "ai_animated" and m["S01_b01"]["ai_motion_model"] == "Wan2.2-TI2V-5B"
    assert m["S02_b01"]["motion"] != "ai_animated" and B.assign_qa(back)["pass"]


def test_package_clips_pick_up_ai_fields():
    from core import beats_package as bpk
    rows = [_row("S01_b01", 0.0, 2.0, "a_beach.jpg", ai_motion_clip="AI_S01_b01.mp4", ai_motion_dir="runs/x/ai",
                 ai_motion_status="PASS", ai_motion_model="Wan2.2-TI2V-5B")]
    c = bpk._clips(rows)[0]
    assert c["ai_clip"] == "AI_S01_b01.mp4" and c["ai_model"] == "Wan2.2-TI2V-5B" and c["ai_local"].endswith("AI_S01_b01.mp4")
    assert bpk.AI_MODEL_LICENCE == "Apache-2.0"


def test_label_overlay_and_licence_record():
    lab = am.label_overlay(1920, 1080, CFG)
    assert lab is not None and lab.shape == (1080, 1920, 4)
    ys, xs = np.nonzero(lab[..., 3] > 0)
    assert xs.min() > 1920 * 0.75 and ys.max() < 1080 * 0.15   # top-right, inside the 5 % margin
    lic = json.loads((am.ROOT / "config" / "model_licenses.json").read_text(encoding="utf-8"))["ai_motion_i2v"]
    assert lic["licence"] == "Apache-2.0" and CFG["model"]["id"] in lic["source"]
    assert all(r["verdict"].startswith("reject") for r in lic["rejected"].values())


# ---------------------------------------------------------------- v17 attempt 2 (KANG_021+): blobs, flag core, ghost, shoreline
def test_gate_fails_on_new_bright_blob_in_sky_and_passes_without():
    """S12_b01 fake seagull: a small bright blob that APPEARS (and drifts) inside the sky/water mask -> FAIL."""
    src = _scene()
    raw = _clouds(src)
    g0 = am.gate_raw(src, raw, "sky", CFG)
    assert g0["new_blobs"] < CFG["gate"]["blob_min_frames"] and not any("new object" in w for w in g0["why"]), g0
    bird = raw.copy()
    for t in range(10, len(bird)):  # white 6x4 'bird' appears at frame 10 and drifts right
        x = 60 + 3 * (t - 10)
        bird[t, 30:34, x:x + 6] = (250, 250, 250)
    g = am.gate_raw(src, bird, "sky", CFG)
    assert g["status"] == "FAIL" and any("new object/blob" in w for w in g["why"]), g["why"]
    assert g["new_blobs"] >= CFG["gate"]["blob_min_frames"] and g["blob_max_px"] >= 6


def test_gate_ignores_thin_ripple_lines():
    """1-2 px high dark lines (ripple troughs) appearing in the water are not objects."""
    src = _scene()
    raw = _clouds(src)
    rip = raw.copy()
    for t in range(5, len(rip)):
        y = 20 + (t % 5) * 6
        rip[t, y:y + 1, 30 + t:60 + t] = (40, 70, 110)
    g = am.gate_raw(src, rip, "sky", CFG)
    assert not any("new object" in w for w in g["why"]), g["why"]


def _flag_scene(w=320, h=176):
    """Blue sky, grey 'spire' at the bottom centre, red flag hanging right of a pole at the top."""
    im = np.zeros((h, w, 3), np.uint8)
    im[:] = (120, 165, 225)
    cv2.rectangle(im, (140, 100), (180, h - 1), (150, 140, 130), -1)
    cv2.line(im, (160, 20), (160, 100), (90, 80, 70), 2)
    cv2.rectangle(im, (162, 22), (176, 60), (200, 30, 40), -1)   # photo flag: hangs down
    return im


def _flag_clip(src, n=25):
    """AI clip: the flag swings out to the left (different place every frame), sky drifts slightly, spire fixed."""
    out = []
    for t in range(n):
        f = _clouds(src, n=n, amp=4.0)[t].copy()
        f[22:61, 161:178] = (120, 165, 225)                          # photo flag gone (AI redraws)
        L = 10 + t
        cv2.rectangle(f, (160 - L - 14, 22 + (t % 4)), (159, 38 + (t % 4)), (205, 35, 45), -1)
        out.append(f)
    return np.stack(out)


def test_flag_colour_core_covers_photo_flag_and_ai_sweep_no_ghost():
    src = _flag_scene()
    raw = _flag_clip(src)
    g = am.gate_raw(src, raw, "flag", CFG)
    m = g["_mask"]
    ww, wh = CFG["gate"]["work_w"], round(CFG["gate"]["work_w"] * src.shape[0] / src.shape[1])
    s = ww / src.shape[1]
    core = g["_flag_core"]
    # photo flag area and the farthest AI flag position are 100 % AI pixels
    assert m[int(30 * s):int(55 * s), int(165 * s):int(174 * s)].min() >= 0.999
    assert m[int(26 * s):int(34 * s), int(115 * s):int(140 * s)].min() >= 0.999
    assert core.any() and g["flag_core_area"] > 0
    assert m[int(120 * s):, int(145 * s):int(175 * s)].max() < 0.05   # spire stays the photo
    assert am.ghost_frac(g["_src_work"], g["_raw_work"], m, core, CFG["gate"]) == 0.0
    # attempt-1 style mask (moving blobs only, soft edges, no colour core) leaves the photo flag showing through
    fr = np.stack([am.gray(f) for f in g["_raw_work"]])
    old, _ = am.motion_mask(fr, g["_src_work"], "flag", CFG["gate"])
    half = old * 0.5
    assert am.ghost_frac(g["_src_work"], g["_raw_work"], half, core, CFG["gate"]) > CFG["gate"]["ghost_frac_fail"]


def test_flag_core_ignores_warm_stone_specks_without_photo_flag_seed():
    """KANG_024: moving warm-tinted specks on stone (no flag in the photo there) never enter the flag core."""
    src = _flag_scene()
    raw = _flag_clip(src).copy()
    for t in range(1, len(raw), 2):   # flickering orange specks on the spire
        raw[t, 130:134, 150:154] = (210, 90, 40)
    g = am.gate_raw(src, raw, "flag", CFG)
    s = CFG["gate"]["work_w"] / src.shape[1]
    assert not g["_flag_core"][int(126 * s):int(138 * s), int(146 * s):int(158 * s)].any()


def test_sea_needs_shoreline_limit_and_limit_zeroes_rows():
    src = _scene()
    raw = _clouds(src)
    g = am.gate_raw(src, raw, "sea", CFG)
    assert g["status"] == "FAIL" and any("shoreline limit" in w for w in g["why"])
    gl = am.gate_raw(src, raw, "sea", CFG, limits={"y_max": 0.3})
    assert not any("shoreline limit" in w for w in gl["why"])
    m = gl["_mask"]
    assert m[int(m.shape[0] * 0.3) + 1:].max() == 0.0
    keep = am.keep_rows_mask((100, 10), {"y_min": 0.1, "y_max": 0.6})
    assert not keep[:10].any() and keep[10:60].all() and not keep[60:].any()


def test_negative_extra_and_seed_override_in_jobs():
    cfg = json.loads(json.dumps(CFG))
    cfg["negative_extra"] = "birds, new objects"
    cfg["negative_extra_beats"] = []
    assert am.negative_for("S01_b01", cfg).endswith(", birds, new objects")
    cfg["negative_extra_beats"] = ["S12_b01"]
    assert am.negative_for("S01_b01", cfg) == cfg["negative"]
    assert "birds" in am.negative_for("S12_b01", cfg)
