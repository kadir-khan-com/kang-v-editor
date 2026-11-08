"""M3 approved local visuals: validation, preview selection, Premiere visual track."""
import json
import subprocess
from pathlib import Path

import pytest

from core import premiere, visuals as vis

PLAN = {"schema": "kang.scenes/1.0", "duration": 30.0, "scenes": [
    {"id": "S01", "start": 0.0, "end": 10.0, "text": "a", "title": "a", "first_word": 0, "last_word": 0, "word_count": 1},
    {"id": "S02", "start": 10.0, "end": 20.0, "text": "b", "title": "b", "first_word": 1, "last_word": 1, "word_count": 1},
    {"id": "S03", "start": 20.0, "end": 30.0, "text": "c", "title": "c", "first_word": 2, "last_word": 2, "word_count": 1, "visual": {}}]}


def _row(scene, asset="", **kw):
    r = {"scene": scene, "asset": asset, "brief": "temple", "licence": "own", "fit": "cover", "asset_in_s": "0"}
    r.update(kw)
    return r


@pytest.fixture
def adir(tmp_path):
    (tmp_path / "a.png").write_bytes(b"x")
    (tmp_path / "clip.mp4").write_bytes(b"x")
    (tmp_path / "notes.txt").write_text("x", encoding="utf-8")
    return tmp_path


def probe4(_):
    return {"duration": 4.0}


def test_template_has_one_row_per_scene(tmp_path):
    p = vis.write_template(PLAN, tmp_path / "v.csv")
    rows = vis.read_csv(p)
    assert [r["scene"] for r in rows] == ["S01", "S02", "S03"] and all(r["asset"] == "" for r in rows)


def test_valid_selection_and_missing_scenes_reported(adir):
    r = vis.validate([_row("S01", "a.png"), _row("S02")], PLAN, adir, probe=probe4)
    assert r["ok"] and len(r["visuals"]["items"]) == 1
    assert r["visuals"]["items"][0]["kind"] == "still" and len(r["visuals"]["items"][0]["sha256"]) == 64
    assert r["visuals"]["scenes_without_visual"] == ["S02", "S03"]


@pytest.mark.parametrize("row, msg", [
    (_row("S01", "a.png", licence=""), "licence"),
    (_row("S01", "a.png", brief=""), "brief"),
    (_row("S01", "../escape.png"), "outside"),
    (_row("S01", "nope.png"), "not found"),
    (_row("S01", "notes.txt"), "unsupported"),
    (_row("S01", "clip.mp4"), "fit=loop"),           # 4 s clip, 10 s scene
    (_row("S01", "a.png", fit="loop"), "video clips only"),
    (_row("S09", "a.png"), "not in scenes"),
    (_row("S01", "clip.mp4", fit="loop", asset_in_s="5"), "outside clip"),
])
def test_invalid_rows_rejected(adir, row, msg):
    r = vis.validate([row], PLAN, adir, probe=probe4)
    assert not r["ok"] and any(msg in p for p in r["problems"]), r["problems"]


def test_short_clip_ok_with_loop(adir):
    assert vis.validate([_row("S01", "clip.mp4", fit="loop")], PLAN, adir, probe=probe4)["ok"]


def test_pick_needs_contiguous_scenes_with_visuals(adir):
    v = vis.validate([_row("S01", "a.png"), _row("S02", "a.png"), _row("S03", "a.png")], PLAN, adir, probe=probe4)["visuals"]
    assert [i["scene"] for i in vis.pick(v, PLAN, ["S02", "S01"])] == ["S01", "S02"]
    with pytest.raises(ValueError):
        vis.pick(v, PLAN, ["S01", "S03"])
    v2 = vis.validate([_row("S01", "a.png")], PLAN, adir, probe=probe4)["visuals"]
    with pytest.raises(ValueError):
        vis.pick(v2, PLAN, ["S01", "S02"])


MEDIA = {"path": r"E:\kang\p\media\n.mp3", "name": "n.mp3", "duration": 30.0, "has_video": False, "channels": 1}


def test_xmeml_visual_track_with_loop_and_gap():
    vc = [{"path": r"E:\kang\p\visuals\a.png", "name": "a.png", "kind": "still", "start": 0.0, "end": 10.0},
          {"path": r"E:\kang\p\visuals\c.mp4", "name": "c.mp4", "kind": "video", "start": 20.0, "end": 30.0,
           "in": 0.0, "src_duration": 4.0, "loop": True}]
    xml, st = premiere.build_xmeml("t", MEDIA, [(0, 30)], fps=25, visual_clips=vc)
    assert st["visual_clipitems"] == 1 + 3          # 10 s from a 4 s clip = 4 + 4 + 2 s
    chk = premiere.check_xmeml(xml, 25)
    assert chk["pass"], chk["problems"]
    assert "E%3a/kang/p/visuals/c.mp4" in xml and xml.count("<pathurl>") == 3


def test_check_xmeml_catches_overlapping_visuals():
    vc = [{"path": "/a.png", "name": "a.png", "kind": "still", "start": 0.0, "end": 12.0},
          {"path": "/b.png", "name": "b.png", "kind": "still", "start": 10.0, "end": 20.0}]
    xml, _ = premiere.build_xmeml("t", MEDIA, [(0, 30)], fps=25, visual_clips=vc)
    assert not premiere.check_xmeml(xml, 25)["pass"]


def _ff(*a):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *a], check=True)


def test_visual_preview_end_to_end(tmp_path, monkeypatch):
    from core import pipeline
    monkeypatch.setenv("KANG_RUNS_DIR", str(tmp_path / "runs"))
    a = tmp_path / "assets"
    a.mkdir()
    _ff("-f", "lavfi", "-i", "color=c=red:s=320x240", "-frames:v", "1", str(a / "s.png"))
    _ff("-f", "lavfi", "-i", "testsrc2=s=320x240:r=25:d=1", "-pix_fmt", "yuv420p", str(a / "c.mp4"))
    au = tmp_path / "n.wav"
    _ff("-f", "lavfi", "-i", "sine=f=300:d=4", "-ac", "1", str(au))
    words = [{"word": "राधे", "start": 0.3, "end": 0.9}, {"word": "राधे।", "start": 1.0, "end": 1.6},
             {"word": "द्वारिका", "start": 2.3, "end": 3.0}]
    wp = tmp_path / "w.json"
    wp.write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
    plan = {"schema": "kang.scenes/1.0", "duration": 4.0, "scenes": [
        {"id": "S01", "start": 0.0, "end": 1.95, "text": "राधे राधे।", "title": "राधे", "first_word": 0, "last_word": 1, "word_count": 2, "visual": {}},
        {"id": "S02", "start": 1.95, "end": 4.0, "text": "द्वारिका", "title": "द्वारिका", "first_word": 2, "last_word": 2, "word_count": 1, "visual": {}}]}
    sp = tmp_path / "scenes.json"
    sp.write_text(json.dumps(plan, ensure_ascii=False), encoding="utf-8")
    csvp = tmp_path / "v.csv"
    vis.write_template(plan, csvp)
    rows = vis.read_csv(csvp)
    rows[0].update(asset="s.png", brief="red", licence="own test")
    rows[1].update(asset="c.mp4", brief="clip", licence="own test", fit="loop")
    import csv
    with open(csvp, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    held = pipeline.visual_preview(str(au), str(wp), str(sp), str(csvp), str(a), scene_ids=["S01", "S02"])
    assert held.get("visual_selection") and not held.get("preview")          # default-deny: gate pending

    def yes(g, i):
        return True
    yes.approver_name = "auto(--yes)"
    r = pipeline.visual_preview(str(au), str(wp), str(sp), str(csvp), str(a), scene_ids=["S01", "S02"], approver=yes)
    assert r["qa"]["pass"], r["qa"]
    assert r["accepted"] is False and r["visuals_human_approved"] is False   # auto approval is not human
    assert r["package_status"] == "draft_package_ready"                     # transcript not accepted
    pv = Path(r["preview"])
    assert pv.is_file() and r["stats"]["visual_clipitems"] == 1 + 3          # 2.05 s from a 1 s clip, looped
    man = json.loads((Path(r["package"]) / "package_manifest.json").read_text(encoding="utf-8"))
    assert man["status"]["premiere_import"] == "NOT_TESTED" and "visuals/c.mp4" in man["files"]


def test_multi_shot_scene_splits_at_shot_start(adir):
    (adir / "b.png").write_bytes(b"y")
    rows = [_row("S01", "a.png"), _row("S01", "b.png", shot_start="4.0"), _row("S02", "a.png")]
    r = vis.validate(rows, PLAN, adir, probe=probe4)
    assert r["ok"], r["problems"]
    it = r["visuals"]["items"]
    assert [(i["shot"], i["start"], i["end"]) for i in it] == [("S01.1", 0.0, 4.0), ("S01.2", 4.0, 10.0), ("S02", 10.0, 20.0)]
    sel = vis.pick(r["visuals"], PLAN, ["S01", "S02"])
    assert [i["shot"] for i in sel] == ["S01.1", "S01.2", "S02"]
    assert any("more than one shot" in w for w in r["warnings"])


@pytest.mark.parametrize("ss,msg", [("", "needs shot_start"), ("0.5", "must be >="), ("9.5", "must be >=")])
def test_multi_shot_bad_shot_start(adir, ss, msg):
    r = vis.validate([_row("S01", "a.png"), _row("S01", "a.png", shot_start=ss)], PLAN, adir, probe=probe4)
    assert not r["ok"] and any(msg in p for p in r["problems"])


def test_xmeml_stats_flag_visual_track_separately_from_source_video():
    from core import premiere
    media = {"path": "a.mp3", "name": "a.mp3", "duration": 10.0, "has_video": False, "channels": 2,
             "sample_rate": 48000}
    vc = [{"path": "v.jpg", "name": "v.jpg", "width": 1920, "height": 1080, "kind": "still",
           "start": 0.0, "end": 10.0, "in": 0.0, "src_duration": 10.0, "loop": False}]
    _, st = premiere.build_xmeml("t", media, [[0.0, 10.0]], fps=25, markers=[], visual_clips=vc)
    assert st["source_has_video"] is False and st["visual_track"] is True and st["visual_clipitems"] == 1
    _, st0 = premiere.build_xmeml("t", media, [[0.0, 10.0]], fps=25, markers=[])
    assert st0["visual_track"] is False
