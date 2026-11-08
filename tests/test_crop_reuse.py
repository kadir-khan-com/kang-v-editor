"""v14 crop reuse (core/crop_reuse.py): synthetic images only, no network, fake face detector."""
from __future__ import annotations

import csv

import numpy as np
import pytest
from PIL import Image

from core import beats as B
from core import crop_reuse as C

RULES = {"places": {"nageshwar": ["nageshwar"], "beach": ["beach"]}, "reject_titles": [], "eye_rejects": {},
         "area_keys": [], "focus": {},
         "crop_reuse": {"extra_places": {}, "rejects": {}, "require_face_detector": False, "step_px": 64}}


def _img(path, w, h, detail_box=None, seed=0):
    """Flat light-blue 'sky' everywhere; random high-contrast texture inside detail_box (x0, y0, x1, y1)."""
    rng = np.random.default_rng(seed)
    a = np.zeros((h, w, 3), np.uint8)
    a[...] = (200, 170, 120)  # RGB light blue, smooth
    if detail_box:
        x0, y0, x1, y1 = detail_box
        a[y0:y1, x0:x1] = rng.integers(0, 255, (y1 - y0, x1 - x0, 3), dtype=np.uint8)
    Image.fromarray(a).save(path, quality=95)
    return path


def _cfg(**kw):
    return {**C.settings(RULES), **kw}


def test_geometry_area_iou_width():
    ff = C.first_framing(1920, 2560)
    assert ff == (0, 740, 1920, 1080)
    assert C.iou(ff, ff) == pytest.approx(1.0)
    cfg = _cfg()
    boxes = C.candidate_boxes(1920, 2560, [ff], cfg)
    assert boxes
    for b in boxes:
        assert b[2] >= 1280 and b[2] * b[3] <= 0.5 * ff[2] * ff[3] + 1e-6
        assert C.iou(b, ff) <= 0.3 + 1e-9
        assert 0 <= b[0] and b[0] + b[2] <= 1920 and 0 <= b[1] and b[1] + b[3] <= 2560
    # a 16:9 1920x1080 photo has no second framing (1280 px crop = 44 % of it, IoU 0.44 > 0.3) -> skipped
    assert C.candidate_boxes(1920, 1080, [C.first_framing(1920, 1080)], cfg) == []
    # 1920x1440: only the top / bottom bands at exactly 1280 px pass (IoU 0.30)
    b1440 = C.candidate_boxes(1920, 1440, [C.first_framing(1920, 1440)], cfg)
    assert b1440 and all(b[2] == 1280 and b[1] in (0, 720) for b in b1440)


def test_best_crop_picks_detail_refuses_flat_and_faces(tmp_path):
    p = _img(tmp_path / "a.jpg", 1920, 2560, detail_box=(500, 0, 1900, 760))  # detail at the top (the 'spire')
    an = C.Analysis(p)
    ff = C.first_framing(an.iw, an.ih)
    bc = C.best_crop(an, [ff], _cfg())
    assert bc["box"] is not None
    x, y, w, h = bc["box"]
    assert y + h <= 900 and x >= 300  # lands on the textured region, not in the flat sky
    # all-flat photo: every window refused (sky / low detail)
    flat = C.Analysis(_img(tmp_path / "flat.jpg", 1920, 2560))
    r = C.best_crop(flat, [C.first_framing(1920, 2560)], _cfg())
    assert r["box"] is None and "refused" in r["reason"]
    # a face inside the detailed region -> that region is refused
    faced = C.Analysis(p, face_detector=lambda img: [(900, 100, 300, 300)])
    r2 = C.best_crop(faced, [ff], _cfg())
    assert r2["box"] is None or not faced.touches_face(r2["box"])
    # blur gate: same detail, heavily blurred -> refused as blurry / low detail
    Image.open(p).resize((96, 128)).resize((1920, 2560), Image.BILINEAR).save(tmp_path / "blur.jpg")
    rb = C.best_crop(C.Analysis(tmp_path / "blur.jpg"), [ff], _cfg())
    assert rb["box"] is None


def _rows(tmp_path):
    d = tmp_path / "assets"
    d.mkdir()
    _img(d / "nageshwar_exact.jpg", 1920, 2560, detail_box=(0, 0, 1920, 2560), seed=1)  # textured everywhere
    _img(d / "rep1.jpg", 1920, 1080, detail_box=(0, 0, 1920, 1080), seed=2)
    rel = d.relative_to(tmp_path).as_posix()
    spec = [  # beat, asset, match, role, narration (Hinglish)
        ("S01_b01", "nageshwar_exact.jpg", "exact", "v9_shot", "yeh hai Nageshwar"),
        ("S01_b02", "rep1.jpg", "representative", "v9_shot", "Nageshwar mandir"),           # 1 beat away -> too close
        ("S01_b03", "CARD_C01.mp4", "text_card", "motion_card", "Nageshwar"),              # card: never
        ("S01_b04", "STK_a.mp4", "representative", "new_stock", "Nageshwar jyotirling"),  # 3 away -> too close
        ("S01_b05", "STK_b.mp4", "representative", "new_stock", "Nageshwar ke darshan"),  # 4 away -> reuse 1
        ("S01_b06", "STK_c.mp4", "representative", "new_stock", "kuch aur"),              # names no place -> untouched
        ("S01_b07", "STK_d.mp4", "representative", "new_stock", "kuch aur"),
        ("S01_b08", "STK_e.mp4", "representative", "new_stock", "kuch aur"),
        ("S01_b09", "STK_f.mp4", "representative", "new_stock", "Nageshwar"),            # 4 after reuse 1 -> reuse 2
        ("S01_b10", "STK_g.mp4", "representative", "new_stock", "kuch aur"),
        ("S01_b11", "STK_h.mp4", "representative", "new_stock", "kuch aur"),
        ("S01_b12", "STK_i.mp4", "representative", "new_stock", "kuch aur"),
        ("S01_b13", "STK_j.mp4", "representative", "new_stock", "Nageshwar"),            # max 2 reuses -> skipped
    ]
    rows, beats, hw = [], [], []
    for k, (b, a, m, role, txt) in enumerate(spec):
        rows.append({"beat": b, "scene": "S01", "start": k * 4.0, "end": k * 4.0 + 4.0, "first_word_time": k * 4.0 + 0.2,
                     "text": txt, "asset": a, "source_dir": rel, "asset_source": "x", "match": m, "role": role, "v9_shot": "S01.1",
                     "licence": "CC BY 4.0", "title": f"File:{a}", "source_page": "", "notes": ""})
        beats.append({"id": b, "first_word": len(hw), "last_word": len(hw) + len(txt.split()) - 1})
        hw += [{"hinglish": w} for w in txt.split()]
    return rows, {"beats": beats}, hw


def test_plan_rules_end_to_end(tmp_path):
    rows, bp, hw = _rows(tmp_path)
    res = C.plan_crop_reuse(rows, bp, hw, RULES, root=tmp_path, face_detector=lambda img: [])
    used = [u["beat"] for u in res["reuses"]]
    assert used == ["S01_b05", "S01_b09"]
    assert all(u["asset"] == "nageshwar_exact.jpg" and u["match"] == "exact" for u in res["reuses"])
    skipped = {s["beat"]: s["reason"] for s in res["skipped"]}
    assert "< 4 beats" in skipped["S01_b02"] and "< 4 beats" in skipped["S01_b04"]
    assert "already 2 reuses" in skipped["S01_b13"]
    assert "S01_b03" not in used and "S01_b01" not in used  # card / exact never replaced
    # second crop is distinct from the first framing AND the first crop
    a, b = res["reuses"]
    assert C.iou(tuple(a["box"]), tuple(b["box"])) <= 0.3 + 1e-9
    assert b["iou_max"] <= 0.3 and b["area_ratio"] <= 0.5
    # files, rows, QA, CSV columns
    cdir = tmp_path / "crop"
    creds = C.write_crops(res["reuses"], cdir, root=tmp_path)
    assert all("modification" in c["modified"] and c["reuse"] == "crop_reuse" for c in creds)
    for u in res["reuses"]:
        assert Image.open(cdir / u["file"]).size == (u["box"][2], u["box"][3])
    new = C.apply_reuses(rows, res["reuses"], "crop")
    assert C.crop_qa(new, res["reuses"], RULES) == []
    qa = B.assign_qa(new)
    assert qa["pass"] and qa["crop_reuses"] == 2 and qa["roles"]["crop_reuse"] == 2
    out = B.write_assign_csv(new, tmp_path / "v.csv")
    with open(out, encoding="utf-8-sig") as fh:
        got = list(csv.DictReader(fh))
    r5 = next(r for r in got if r["beat"] == "S01_b05")
    assert r5["reuse"] == "crop_reuse" and r5["reuse_of"] == "nageshwar_exact.jpg" and r5["crop_box"].endswith("of 1920x2560")
    assert r5["match"] == "exact"


def test_rejects_and_qa_catch_violations(tmp_path):
    rows, bp, hw = _rows(tmp_path)
    rules = {**RULES, "crop_reuse": {**RULES["crop_reuse"], "rejects": {"nageshwar_exact.jpg@S01_b05": "eye: wall"}}}
    res = C.plan_crop_reuse(rows, bp, hw, rules, root=tmp_path, face_detector=lambda img: [])
    assert "S01_b05" not in [u["beat"] for u in res["reuses"]]
    assert "rejected by eye" in next(s["reason"] for s in res["skipped"] if s["beat"] == "S01_b05")
    # crop_qa flags a reuse placed too close and one too small
    bad = [{"beat": "S01_b02", "kind": "representative", "asset": "nageshwar_exact.jpg", "box": [0, 0, 1000, 562], "image": [1920, 2560],
            "first_framing": [0, 740, 1920, 1080], "iou_max": 0.0, "area_ratio": 0.27, "match": "exact", "places": ["nageshwar"],
            "file": "x.jpg"}]
    new = [dict(r) for r in rows]
    new[1].update(asset="x.jpg", reuse="crop_reuse", reuse_of="nageshwar_exact.jpg")
    probs = C.crop_qa(new, bad, rules)
    assert any("1280" in p for p in probs) and any("beats apart" in p for p in probs)


def test_no_face_detector_refuses_by_default(tmp_path, monkeypatch):
    rows, bp, hw = _rows(tmp_path)
    monkeypatch.setattr(C, "yunet_detector", lambda **kw: None)
    rules = {**RULES, "crop_reuse": {**RULES["crop_reuse"], "require_face_detector": True}}
    res = C.plan_crop_reuse(rows, bp, hw, rules, root=tmp_path)
    assert res["reuses"] == [] and "face detector" in res["skipped"][0]["reason"]
