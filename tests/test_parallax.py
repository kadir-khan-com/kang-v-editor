"""2.5D parallax layer: synthetic images + mock depth (no model download)."""
import json
from pathlib import Path

import numpy as np
import pytest

cv2 = pytest.importorskip("cv2")

from core import beats as B
from core import parallax as P


def _scene(w=960, h=720):
    """Textured background + a bright 'near' block; depth near=1 inside the block."""
    rng = np.random.default_rng(0)
    img = (rng.random((h, w, 3)) * 120 + 60).astype(np.uint8)
    img = cv2.GaussianBlur(img, (0, 0), 2)
    img[200:520, 300:660] = (230, 180, 60)
    depth = np.full((h, w), 0.2, np.float32)
    depth[200:520, 300:660] = 1.0
    return img, depth


def _img_file(tmp_path, img):
    from PIL import Image
    p = tmp_path / "still.jpg"
    Image.fromarray(img).save(p, quality=92)
    return p


def test_forbidden_models_rejected():
    with pytest.raises(ValueError):
        P.HFDepth("depth-anything/Depth-Anything-V2-Large-hf")
    with pytest.raises(ValueError):
        P.HFDepth("depth-anything/Depth-Anything-V2-Base-hf")
    lic = json.loads((Path(P.ROOT) / "config" / "model_licenses.json").read_text(encoding="utf-8"))["depth_parallax"]
    assert lic["licence"] == "Apache-2.0" and lic["revision"] == P.MODEL_REV and P.MODEL_ID in lic["source"]


def test_depth_cache_sha_keyed(tmp_path):
    img, _ = _scene()
    f = _img_file(tmp_path, img)
    calls = []

    def est(rgb):
        calls.append(rgb.shape)
        return rgb[:, :, 0].astype(np.float32)  # mock: brighter = nearer

    d1, i1 = P.depth_for(f, est, tmp_path / "cache")
    d2, i2 = P.depth_for(f, est, tmp_path / "cache")
    assert len(calls) == 1 and i1["cache"] == "miss" and i2["cache"] == "hit"
    assert i1["image_sha256"] == P.sha256_bytes(f) and Path(i1["cache_file"]).name.startswith(i1["image_sha256"])
    assert d1.dtype == np.float32 and 0.0 <= d1.min() and d1.max() <= 1.0 and max(d1.shape) == P.DEPTH_LONG_SIDE
    assert np.allclose(d1, d2, atol=1e-3)


def test_zero_strength_equals_plain_crop():
    img, depth = _scene()
    wp = P.Warper(img, depth, 640, 360, "pan", strength=0.0)
    flat = P.Warper(img, np.full_like(depth, 0.5), 640, 360, "pan", strength=0.0, focus=0.5)
    assert np.abs(wp.frame(0.3).astype(int) - flat.frame(0.3).astype(int)).max() <= 1


def test_near_layer_moves_more_than_far():
    img, depth = _scene()
    wp = P.Warper(img, depth, 960, 540, "pan", strength=1.0, soften=False)
    mx0, _, _ = wp.maps(0.0)
    mx1, _, _ = wp.maps(1.0)
    shift = mx1 - mx0
    near = np.abs(shift[270, 470:490]).mean()  # inside the block (centre of frame)
    far = np.abs(shift[40, 20:40]).mean()
    assert near > far * 1.5


def test_gate_catches_tearing_and_feather_fixes_it():
    img, depth = _scene()
    hard = P.Warper(img, depth, 960, 540, "pan", strength=4.0, soften=False)
    g = P.geometry_check(hard)
    st, why = P.gate_status(g, {}, False)
    assert st == "FAIL" and g["fold_px"] > 0 and any("fold" in w for w in why)
    soft = P.Warper(img, depth, 960, 540, "pan", strength=0.6, edge_sigma=28.0)
    g2 = P.geometry_check(soft)
    # feathering turns a tear (fold) into a spread, milder stretch
    assert g2["fold_px"] == 0 and g2["max_dev"] < g["max_dev"]


def test_no_black_border_and_border_detector():
    img, depth = _scene()
    for mv in P.MOVES:
        wp = P.Warper(img, depth, 640, 360, mv, 1.0)
        assert P.geometry_check(wp)["oob_frac"] <= P.GATE["oob_warn"]
        for p in (0.0, 0.5, 1.0):
            assert not P.edge_black(wp.frame(p))
    fr = np.full((100, 160, 3), 128, np.uint8)
    fr[:, :4] = 0
    assert P.edge_black(fr)


def test_smoothness_and_path():
    hump = [np.sin(np.pi * (i + 0.5) / 100) * 3 + 0.2 for i in range(100)]
    s = P.smoothness(hump)
    assert s["ratio"] < 3 and s["spike"] < 1.5
    spiky = list(hump)
    spiky[50] = 30
    assert P.gate_status({"fold_px": 0, "stretch_frac": 0, "oob_frac": 0}, P.smoothness(spiky), False)[0] == "FAIL"
    assert P.smoothness([0.05, 0.5, 0.05, 0.05])["spike"] == 0.0  # sub-floor quantisation steps ignored
    for mv in P.MOVES:
        assert P.path_smoothness(mv, 1.0, 1, 200) < 0.1


def test_render_writes_mp4_with_exact_frames(tmp_path):
    img, depth = _scene()
    f = _img_file(tmp_path, img)
    r = P.render(f, tmp_path / "px.mp4", 1.0, move="dolly", w=320, h=180, depth=depth, frames=13)
    assert r["status"] in ("PASS", "WARN") and Path(r["file"]).is_file()
    from core.runs import media_summary
    ms = media_summary(r["file"])
    assert ms["width"] == 320 and abs(ms["duration"] - 13 / 25) < 0.05


def test_render_fail_writes_no_file(tmp_path, monkeypatch):
    img, depth = _scene()
    f = _img_file(tmp_path, img)
    monkeypatch.setitem(P.GATE, "stretch_fail", -1.0)  # everything fails
    r = P.render(f, tmp_path / "bad.mp4", 1.0, w=320, h=180, depth=depth, frames=5)
    assert r["status"] == "FAIL" and not (tmp_path / "bad.mp4").exists() and "file" not in r


def _rows():
    mk = lambda b, s, e, a, m, role: {"beat": b, "scene": "S01", "start": s, "end": e, "first_word_time": s, "text": "x",
                                      "asset": a, "source_dir": "assets/x", "asset_source": "v9", "match": m, "role": role,
                                      "licence": "CC BY", "title": "File:" + a}
    return [mk("S01_b01", 0.0, 4.0, "a.jpg", "exact", "v9_shot"), mk("S01_b02", 4.0, 8.0, "a.jpg", "exact", "continued_with_motion"),
            mk("S01_b03", 8.0, 11.0, "card.jpg", "text_card", "v9_shot"), mk("S01_b04", 11.0, 19.0, "card.jpg", "text_card", "card_hold"),
            mk("S01_b05", 19.0, 22.0, "c.jpg", "representative", "new_pool")]


def test_select_and_apply_keep_labels_and_no_repeat(tmp_path):
    rows = _rows()
    sel = P.select_clips(rows, 6.0)
    assert [c["first_beat"] for c in sel] == ["S01_b01"]  # card (11 s) never parallax; 3 s pool still too short
    cdir = tmp_path / "parallax_clips"
    cdir.mkdir()
    (cdir / "PX_a.mp4").write_bytes(b"x")
    rep = [{"beat": "S01_b01", "asset": "a.jpg", "status": "PASS", "parallax_clip": "PX_a.mp4", "frames": "200"},
           {"beat": "S01_b05", "asset": "c.jpg", "status": "FAIL", "parallax_clip": "", "frames": "75"}]
    new, info = P.apply_parallax(rows, rep, cdir)
    assert info["used"] == ["S01_b01"]
    px = [r for r in new if r.get("parallax_clip")]
    assert [r["beat"] for r in px] == ["S01_b01", "S01_b02"]
    assert all(r["motion"] == P.MOTION_LABEL and r["match"] == "exact" and r["asset"] == "a.jpg" for r in px)
    assert B.assign_qa(new)["pass"]
    out = B.write_assign_csv(new, tmp_path / "vb.csv")
    back = B.read_assign_csv(out)
    assert back[0]["motion"] == "parallax_2_5d" and back[0]["parallax_clip"] == "PX_a.mp4" and back[4]["parallax_clip"] == ""
    # a report whose frame count does not match the clip is not used
    rep[0]["frames"] = "150"
    assert P.apply_parallax(rows, rep, cdir)[1]["used"] == []


def test_report_roundtrip(tmp_path):
    p = P.write_report([{"clip": 1, "beat": "S01_b01", "status": "WARN", "notes": ["stretch 0.2%", "x"]}], tmp_path / "r.csv")
    r = P.read_report(p)
    assert r[0]["status"] == "WARN" and r[0]["notes"] == "stretch 0.2%; x"
