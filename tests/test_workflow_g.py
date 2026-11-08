"""M3 Workflow G prototype: scenes.json, Gate 1, Premiere FCP7 XML package."""
import json
import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

from core import pipeline, premiere, scenes
from core.runs import Run


def _words(n=120, step=0.5):
    out, t = [], 0.3
    for i in range(n):
        w = f"शब्द{i}" + ("।" if i % 15 == 14 else "")
        out.append({"word": w, "start": round(t, 3), "end": round(t + 0.35, 3), "probability": 0.9})
        t += step + (0.8 if i % 15 == 14 else 0)
    return out


def test_scenes_tile_timeline_and_own_every_word():
    ws = _words()
    dur = ws[-1]["end"] + 1.0
    plan = scenes.plan_scenes(ws, dur, target_s=10, min_s=5, max_s=20)
    assert scenes.validate_scenes(plan, n_words=len(ws)) == []
    assert len(plan["scenes"]) >= 3
    for s in plan["scenes"]:  # no word is split by a boundary
        assert ws[s["first_word"]]["start"] >= s["start"] and ws[s["last_word"]]["end"] <= s["end"]


def test_scene_validator_catches_gap():
    ws = _words(40)
    plan = scenes.plan_scenes(ws, ws[-1]["end"] + 1, target_s=5, min_s=2, max_s=10)
    plan["scenes"][1]["start"] += 0.5
    assert any("gap/overlap" in e for e in scenes.validate_scenes(plan))


def test_max_scene_length_forces_split_without_punctuation():
    ws = [{"word": f"w{i}", "start": i * 0.5, "end": i * 0.5 + 0.3} for i in range(200)]
    plan = scenes.plan_scenes(ws, 100.5, target_s=30, min_s=15, max_s=45)
    assert scenes.validate_scenes(plan, n_words=200) == []
    assert all(s["end"] - s["start"] <= 46 for s in plan["scenes"][:-1])


def test_pathurl_windows_and_posix():
    assert premiere.pathurl(r"E:\kang\packages\a b\media\x.mp3") == "file://localhost/E%3a/kang/packages/a%20b/media/x.mp3"
    assert premiere.pathurl("/tmp/x y.mp3") == "file://localhost/tmp/x%20y.mp3"


def test_xmeml_cuts_are_contiguous_and_frame_exact():
    media = {"path": r"E:\k\m.mp4", "name": "m.mp4", "duration": 20.0, "has_video": True, "channels": 2}
    keep = [(0.0, 4.02), (5.0, 9.5), (12.0, 20.0)]
    xml, st = premiere.build_xmeml("t", media, keep, fps=25, markers=[{"at": 0, "name": "S01"}])
    chk = premiere.check_xmeml(xml, 25)
    assert chk["pass"], chk["problems"]
    assert st["clips"] == 3 and st["audio_tracks"] == 2 and st["video"]
    root = ET.fromstring(xml.split("\n", 2)[2])
    assert len(root.findall(".//sequence/media/video/track/clipitem")) == 3
    assert len(root.findall(".//sequence/media/audio/track/clipitem")) == 6
    assert st["sequence_frames"] == round(4.02 * 25) + round(9.5 * 25) - round(5 * 25) + 500 - 300


def test_xmeml_rejects_overlap_and_bad_fps():
    m = {"path": "/a.wav", "name": "a.wav", "duration": 10, "channels": 1}
    with pytest.raises(ValueError):
        premiere.build_xmeml("t", m, [(0, 5), (4, 8)])
    with pytest.raises(ValueError):
        premiere.build_xmeml("t", m, [(0, 5)], fps=29)


def test_to_timeline_mapping():
    keep = [[0, 4], [6, 10]]
    assert pipeline._to_timeline(2, keep) == 2
    assert pipeline._to_timeline(5, keep) == 4      # inside a cut -> next kept start
    assert pipeline._to_timeline(7, keep) == 5


def _speech_words(media):
    return [{"word": w, "start": s, "end": e, "probability": 0.9}
            for w, s, e in (("नमस्ते", 0.5, 1.0), ("दोस्तों।", 1.1, 1.6), ("द्वारका", 2.0, 2.6), ("चलिए।", 2.7, 3.2))]


def test_package_waits_at_gate1_by_default(media, tmp_path):
    wp = tmp_path / "w.json"
    wp.write_text(json.dumps(_speech_words(media), ensure_ascii=False), encoding="utf-8")
    r = pipeline.premiere_package(str(media / "speech.wav"), str(wp))
    assert r["package"] is None and "scene_plan" in r
    assert Run(r["run_id"]).manifest["approvals"]["scene_plan"] == "pending"


def test_package_built_after_approval(media, tmp_path):
    wp = tmp_path / "w.json"
    wp.write_text(json.dumps(_speech_words(media), ensure_ascii=False), encoding="utf-8")

    def human(g, i):
        return True
    human.approver_name = "cli-user"
    r = pipeline.premiere_package(str(media / "speech.wav"), str(wp), approver=human, win_root=r"E:\kang\pk")
    assert r["qa"]["pass"], r["qa"]
    pkg = Path(r["package"])
    for f in ("sequence.xml", "captions.srt", "scenes.json", "words.json", "README_IMPORT.txt", "package_manifest.json"):
        assert (pkg / f).is_file(), f
    assert "file://localhost/E%3a/kang/pk/media/speech.wav" in (pkg / "sequence.xml").read_text(encoding="utf-8")
    man = json.loads((pkg / "package_manifest.json").read_text(encoding="utf-8"))
    assert "media/speech.wav" in man["files"]
    assert r["human_approved"] is True


def test_package_refuses_unapproved_cuts(media, tmp_path):
    wp = tmp_path / "w.json"
    wp.write_text(json.dumps(_speech_words(media), ensure_ascii=False), encoding="utf-8")
    cuts = tmp_path / "cuts.json"
    cuts.write_text(json.dumps({"keep": [[0, 1.0], [2.0, 3.0]]}), encoding="utf-8")
    r = pipeline.premiere_package(str(media / "speech.wav"), str(wp), cuts_path=str(cuts),
                                  approver=lambda g, i: True)
    assert r["package"] is None and "approved" in r["error"]
