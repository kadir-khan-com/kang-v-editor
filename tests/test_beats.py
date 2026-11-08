"""Beat layer (core/beats.py, core/premiere.py motion): synthetic words/scenes, no network, no media."""
from __future__ import annotations

import json
import xml.etree.ElementTree as ET

import pytest

from core import beats as B
from core import premiere

FPS = 25


def _words_scenes():
    """Two scenes of ~20 s and ~13 s; a word every 0.4 s, commas now and then, one forced v9 cut."""
    words, t = [], 0.5
    for i in range(80):
        w = f"w{i}" + ("," if i % 9 == 8 else "")
        words.append({"word": w, "start": round(t, 3), "end": round(t + 0.32, 3)})
        t += 0.4 + (0.3 if i % 9 == 8 else 0.0)
    split = 45
    s1_end = round(words[split]["start"] - 0.05, 3)
    dur = round(words[-1]["end"] + 0.6, 3)
    plan = {"schema": "kang.scenes/1.0", "duration": dur, "scenes": [
        {"id": "S01", "start": 0.0, "end": s1_end, "first_word": 0, "last_word": split - 1, "title": "one", "text": "a"},
        {"id": "S02", "start": s1_end, "end": dur, "first_word": split, "last_word": 79, "title": "two", "text": "b"}]}
    return words, plan


RULES = {"clause_words": [], "bad_start_words": [], "places": {"nageshwar": ["nageshwar"], "bet dwarka": ["bet dwarka"],
         "beach": ["beach"]}, "reject_titles": [{"match": "surat", "reason": "wrong place"}], "eye_rejects": {},
         "area_keys": ["bet dwarka"], "focus": {}}


def _rows(plan, words):
    t2 = words[20]["start"] - 0.2
    return [
        {"scene": "S01", "asset": "a1.jpg", "shot_start": "", "notes": "match:exact", "licence": "CC BY", "brief": "x"},
        {"scene": "S01", "asset": "card.jpg", "shot_start": f"{t2:.3f}", "notes": "match:text_card", "licence": "own", "brief": "x"},
        {"scene": "S02", "asset": "b1.jpg", "shot_start": "", "notes": "match:exact", "licence": "CC BY", "brief": "x"},
    ]


def _plan_beats(anchor="lag"):
    words, plan = _words_scenes()
    forced = B.forced_from_visuals(_rows(plan, words), words)
    return words, plan, B.segment(words, plan, anchor=anchor, forced=forced, rules=RULES)


@pytest.mark.parametrize("anchor", ["lead", "lag"])
def test_segmentation_bounds_contiguous_no_scene_crossing(anchor):
    words, plan, bp = _plan_beats(anchor)
    assert B.check_beats(bp, plan) == []
    for b in bp["beats"]:
        assert 2.5 - 1e-6 <= b["duration"] <= 7.0 + 1e-6 or b["boundary"] == ["scene_start"]
    assert bp["beats"][-1]["end"] == pytest.approx(B.seq_end_of(plan["duration"], FPS))
    # forced v9 cut lands at onset + shift on a frame
    fw = 20
    want = B.frame_round(words[fw]["start"] + B.ANCHORS[anchor], FPS)
    assert any(abs(b["start"] - want) < 1e-6 and b["first_word"] == fw for b in bp["beats"])
    # scene boundary is always a beat boundary
    assert any(abs(b["start"] - B.frame_round(plan["scenes"][1]["start"], FPS)) < 1e-6 for b in bp["beats"])


def test_assign_no_repeat_labels_and_continued_with_motion():
    words, plan, bp = _plan_beats()
    rows = _rows(plan, words)
    creds = [{"file": "a1.jpg", "title": "File:A1 Nageshwar temple.jpg"}, {"file": "card.jpg", "title": "Text card"},
             {"file": "b1.jpg", "title": "File:B1 Dwarka beach.jpg"}]
    cands = {"S01": [{"title": "File:Nageshwar temple 2.jpg", "licence": "CC BY", "score": 3, "rank": 1, "pool_dir": "p",
                      "local_file": "p/n2.jpg"},
                     {"title": "File:Gopi Talav Surat.jpg", "licence": "CC BY", "score": 3, "rank": 2, "pool_dir": "p",
                      "local_file": "p/s.jpg"},
                     {"title": "File:A1 Nageshwar temple.jpg", "licence": "CC BY", "score": 3, "rank": 3, "pool_dir": "p",
                      "local_file": "p/dup.jpg"}],
             "S02": [{"title": "File:Bet Dwarka jetty.jpg", "licence": "CC BY", "score": 2, "rank": 1, "pool_dir": "p",
                      "local_file": "p/bd.jpg"}]}
    res = B.assign(bp, rows, plan, creds, cands, RULES)
    assert res["problems"] == []
    out = res["rows"]
    assert len(out) == len(bp["beats"])
    qa = B.assign_qa(out)
    assert qa["pass"] and qa["duplicates"] == []
    titles = [r["title"] for r in out if r["role"] == "new_pool"]
    assert "File:Nageshwar temple 2.jpg" in titles  # same real place as an exact shot -> exact
    assert all("Surat" not in t for t in titles)  # wrong-place reject
    assert "File:A1 Nageshwar temple.jpg" not in titles  # already on the timeline
    by_title = {r["title"]: r for r in out}
    assert by_title["File:Nageshwar temple 2.jpg"]["match"] == "exact"
    # 'bet dwarka' is not a place the beach shot shows -> rejected; S02 runs dry -> continued_with_motion
    assert "File:Bet Dwarka jetty.jpg" not in titles
    roles = {r["role"] for r in out}
    assert "continued_with_motion" in roles
    cards = [r for r in out if r["asset"] == "card.jpg"]
    assert cards and all(r["role"] in ("v9_shot", "card_hold") and r["match"] == "text_card" for r in cards)
    clips = B.merge_clips(out)
    assert len({c["asset"] for c in clips}) == len(clips)  # one clip per asset: never twice
    for c in clips:
        assert c["motion"]["s0"] != c["motion"]["s1"]


def test_pool_pick_is_representative_unless_same_place():
    words, plan, bp = _plan_beats()
    rows = _rows(plan, words)
    rows[0]["notes"] = "match:exact"
    creds = [{"file": "a1.jpg", "title": "File:Dwarkadhish view.jpg"}, {"file": "card.jpg", "title": "card"},
             {"file": "b1.jpg", "title": "File:b1.jpg"}]
    cands = {"S01": [{"title": "File:Dwaraka and around (5).jpg", "licence": "CC BY-SA", "score": 1, "rank": 1,
                      "pool_dir": "p", "local_file": "p/g.jpg"}]}
    res = B.assign(bp, rows, plan, creds, cands, RULES)
    pick = [r for r in res["rows"] if r["role"] == "new_pool"]
    assert pick and pick[0]["match"] == "representative"


def _xml(motion=True):
    vis = [{"path": "C:/k/visuals/a.jpg", "name": "a.jpg", "kind": "still", "start": 0.0, "end": 4.0, "in": 0.0,
            "src_duration": 4.0, "width": 1280, "height": 960,
            "motion": B.motion_for(0, "exact") if motion else None},
           {"path": "C:/k/visuals/b.jpg", "name": "b.jpg", "kind": "still", "start": 4.0, "end": 9.0, "in": 0.0,
            "src_duration": 5.0, "width": 1920, "height": 1080,
            "motion": dict(B.motion_for(1, "text_card"), focus=[0.8, 0.5])}]
    markers = [{"at": 0.0, "name": "S01 one", "comment": "scene"}, {"at": 0.0, "name": "S01_b01", "comment": "w0 w1"},
               {"at": 4.0, "name": "S01_b02", "comment": "w9"}]
    return premiere.build_xmeml("t", {"path": "C:/k/media/n.mp3", "name": "n.mp3", "duration": 9.0, "has_video": False,
                                      "channels": 1, "sample_rate": 48000}, [[0.0, 9.0]], fps=FPS, markers=markers,
                                visual_clips=vis)


def test_xml_motion_keyframes_and_beat_markers_check_pass():
    xml, stats = _xml()
    chk = premiere.check_xmeml(xml, FPS)
    assert chk["pass"], chk["problems"]
    assert stats["motion_clipitems"] == 2 and stats["markers"] == 3
    root = ET.fromstring(xml.split("\n", 2)[2])
    names = [m.findtext("name") for m in root.find("sequence").findall("marker")]
    assert "S01_b02" in names
    ci = [c for c in root.iter("clipitem") if c.get("id", "").startswith("visual-")][0]
    sc = [p for p in ci.findall("filter/effect/parameter") if p.findtext("parameterid") == "scale"][0]
    vals = [float(k.findtext("value")) for k in sc.findall("keyframe")]
    cover = max(1920 / 1280, 1080 / 960) * 100
    assert vals[0] == pytest.approx(cover * 1.0, rel=1e-3) and vals[1] == pytest.approx(cover * 1.08, rel=1e-3)
    assert int(sc.findall("keyframe")[-1].findtext("when")) == 4 * FPS - 1


def test_check_xmeml_catches_bad_keyframe():
    xml, _ = _xml()
    bad = xml.replace("<when>99</when>", "<when>500</when>", 1)
    assert bad != xml
    assert not premiere.check_xmeml(bad, FPS)["pass"]


def test_motion_never_reveals_edges_and_is_subpixel(tmp_path):
    from PIL import Image
    src = Image.new("RGB", (1600, 900), (200, 50, 50))
    for k, match in enumerate(["exact", "exact", "text_card", "archival"]):
        m = B.motion_for(k, match)
        for p in (0.0, 0.37, 1.0):
            s, ox, oy = B.motion_at(m, p)
            assert abs(ox) * 2 <= (s - 1.0) + 1e-9 and abs(oy) * 2 <= (s - 1.0) + 1e-9
            fr = B.frame_at(src, m, p, 320, 180)
            px = fr.load()
            assert px[0, 0] == (200, 50, 50) and px[319, 179] == (200, 50, 50)  # no black edge
    # sub-pixel: a zoom far slower than 1 px/frame still changes EVERY frame (integer crop would repeat frames)
    import numpy as np
    from PIL import ImageFilter
    rng = np.random.default_rng(1)
    tex = Image.fromarray((rng.random((900, 1600, 3)) * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(3))
    tex.save(tmp_path / "tex.png")
    src2 = B._cover_source(tmp_path / "tex.png", 320, 180, 1.08)  # same pre-scale as the preview renderer
    m = B.motion_for(0, "exact")
    frames = [np.asarray(B.frame_at(src2, m, 0.3 + i / 2000, 320, 180), dtype=np.int16) for i in range(10)]
    diffs = [int(np.abs(a - b).sum()) for a, b in zip(frames, frames[1:])]
    assert all(d > 0 for d in diffs)
    assert max(diffs) / max(1, min(diffs)) < 3  # even steps, no jumps


def test_shift_srt():
    srt = "1\n00:03:29,000 --> 00:03:31,000\nHello\n\n2\n00:05:00,000 --> 00:05:01,500\nBye\n\n3\n00:06:00,000 --> 00:06:01,000\nOut\n"
    out = B.shift_srt(srt, 210.0, 340.0)
    assert "00:00:00,000 --> 00:00:01,000\nHello" in out and "00:01:30,000 --> 00:01:31,500\nBye" in out
    assert "Out" not in out
