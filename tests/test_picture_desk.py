"""v18 picture desk + cold open row logic (synthetic rows, no media; parallax lengths via the cache)."""
import json
from pathlib import Path

import pytest

from core import picture_desk as pd
from core import cold_open as co
from core import creative as cr


def row(beat, s, e, asset, match="representative", motion="zoom_in", role="new_pool", scene="S01", **kw):
    r = {"beat": beat, "scene": scene, "start": s, "end": e, "asset": asset, "match": match, "motion": motion,
         "role": role, "source_dir": "x", "title": asset, "parallax_clip": "", "parallax_dir": ""}
    r.update(kw)
    return r


def px(r, clip, d="px"):
    r.update(parallax_clip=clip, parallax_dir=d, parallax_status="PASS", motion="parallax_2_5d")
    return r


def test_short_still_borrows_on_lead_rule_cut():
    rows = [row("b1", 0.0, 4.0, "a.jpg", motion="zoom_in"), row("b2", 4.0, 6.6, "b.jpg", motion="zoom_out"),
            row("b3", 6.6, 11.0, "c.jpg", motion="zoom_in")]
    onsets = [7.1, 7.92]                     # -> candidate cuts 6.88 (too short), 7.72
    res = pd.plan(rows, onsets)
    assert res["after"]["stills_outside_3_10s"] == []
    assert rows[1]["end"] == pytest.approx(7.72) and rows[2]["start"] == pytest.approx(7.72)
    d = res["decisions"][0]
    assert d["rule"] == "G-004" and "lead rule" in d["reason"] and d["cut_at"] == pytest.approx(7.72)


def test_cards_never_donate_and_merge_fallback():
    rows = [row("b1", 0.0, 4.0, "a.jpg", match="exact"), row("b2", 4.0, 6.5, "b.jpg"),
            row("b3", 6.5, 11.0, "CARD.mp4", match="text_card", motion="video_clip", role="motion_card")]
    res = pd.plan(rows, [1.0, 2.0])          # no cut point inside b1 that leaves it >= 3 s and b2 >= 3 s
    assert rows[2]["start"] == 6.5           # card untouched
    assert rows[1]["asset"] == "a.jpg" and rows[1]["role"] == "desk_hold"
    assert any(x["rule"] == "G-004" and "merge" in x["action"] for x in res["decisions"])
    assert res["after"]["stills_outside_3_10s"] == []


def test_unresolved_short_still_is_warn():
    rows = [row("b1", 0.0, 4.0, "C1.mp4", match="text_card", motion="video_clip"),
            row("b2", 4.0, 6.0, "b.jpg"), row("b3", 6.0, 10.0, "M.mp4", match="map", motion="video_clip")]
    res = pd.plan(rows, [])
    assert res["decisions"][-1]["status"] == "WARN"


def test_continued_parallax_hold_is_one_shot_when_clip_covers():
    rows = [px(row("b1", 0.0, 3.0, "p.jpg", match="exact"), "PX_p.mp4"),
            px(row("b2", 3.0, 7.0, "p.jpg", match="exact", role="continued_with_motion"), "PX_p.mp4")]
    cache = {str(pd.ROOT / "px" / "PX_p.mp4"): 8.0}
    res = pd.plan(rows, [], px_cache=cache)
    assert res["decisions"][0]["rule"] == "G-008" and res["decisions"][0]["action"].startswith("merge")
    assert rows[0]["parallax_clip"] == "PX_p.mp4"


def test_continued_parallax_hold_too_long_for_clip_becomes_zoom():
    rows = [px(row("b1", 0.0, 3.0, "p.jpg"), "PX_p.mp4"),
            px(row("b2", 3.0, 7.0, "p.jpg", role="continued_with_motion"), "PX_p.mp4")]
    res = pd.plan(rows, [], px_cache={str(pd.ROOT / "px" / "PX_p.mp4"): 5.0})
    assert rows[0]["parallax_clip"] == "" and rows[0]["desk_motion"] in ("zoom_in", "zoom_out")
    assert res["decisions"][0]["rule"] == "G-008"


def test_back_to_back_parallax_and_accent_budget():
    cache = {}
    rows = []
    t = 0.0
    for k, (scene, isp) in enumerate([("S1", True), ("S1", True), ("S1", False), ("S1", True), ("S2", True)]):
        r = row(f"b{k}", t, t + 4.0, f"{k}.jpg", scene=scene)
        if isp:
            px(r, f"PX_{k}.mp4")
            cache[str(pd.ROOT / "px" / f"PX_{k}.mp4")] = 9.0
        rows.append(r)
        t += 4.0
    res = pd.plan(rows, [], px_cache=cache)
    a = res["after"]
    assert a["parallax_back_to_back"] == [] and a["accents_closer_than_3"] == []
    kept = [r["beat"] for r in rows if r["parallax_clip"]]
    assert "b0" in kept and "b4" in kept      # scene openers win
    assert {x["rule"] for x in res["decisions"]} >= {"G-008"}


def test_no_three_identical_moves():
    rows = [row(f"b{k}", 4.0 * k, 4.0 * k + 4.0, f"{k}.jpg", motion="zoom_in") for k in range(4)]
    res = pd.plan(rows, [])
    assert res["after"]["three_same_moves"] == []
    assert [r["desk_motion"] for r in rows] == ["zoom_in", "zoom_in", "zoom_out", "zoom_in"]
    assert all(x["rule"] == "G-006" for x in res["decisions"])


def test_q002_avoids_equal_length_triple():
    rows = [row("b0", 0.0, 3.04, "z.jpg", motion="zoom_out"), row("b1", 3.04, 6.08, "a.jpg"),
            row("b2", 6.08, 8.88, "b.jpg", motion="zoom_out"), row("b3", 8.88, 14.0, "c.jpg")]
    res = pd.plan(rows, [9.32, 9.92])        # cuts 9.12 (-> 3.04 = triple with 3.04,3.04) or 9.72
    assert rows[2]["end"] == pytest.approx(9.72)
    assert "Q-002" in res["decisions"][0]["reason"]


def test_deterministic():
    def mk():
        return [row("b1", 0.0, 4.0, "a.jpg"), row("b2", 4.0, 6.6, "b.jpg"), row("b3", 6.6, 11.0, "c.jpg")]
    r1, r2 = mk(), mk()
    assert pd.plan(r1, [7.1, 7.9])["decisions"] == pd.plan(r2, [7.1, 7.9])["decisions"]
    assert r1 == r2


# ------------------------------------------------------------- cold open ----
def test_cold_open_rows_drop_and_straddle():
    rows = [row("S01_b01", 0.0, 4.92, "s1.jpg", match="exact"), row("S01_b02", 4.92, 8.40, "s2.jpg"),
            px(row("S01_b03", 8.40, 12.32, "s3.jpg", match="exact"), "PX_s3.mp4")]
    spec = {"title": {"kicker": "DWARKA · GUJARAT", "title": "Shri Krishna ki nagri"},
            "shots": [{"id": "S01_t01", "file": "TSR_01.mp4", "src": "a.mp4", "frames": 80, "label": "exact", "why": "x"},
                      {"id": "S01_t02", "file": "TSR_02.mp4", "src": "b.mp4", "frames": 78, "label": "exact", "why": "y"}]}
    creds = {"TSR_01.mp4": {"licence": "CC BY 3.0", "title": "A"}, "TSR_02.mp4": {"licence": "CC BY 3.0", "title": "B"}}
    words = [{"word": "w", "start": 0.9}, {"word": "v", "start": 5.1}, {"word": "u", "start": 6.51}]
    out, info = co.build_rows(rows, spec, 6.32, "runs/x/teaser_clips", creds, words)
    assert [r["beat"] for r in out] == ["S01_t01", "S01_t02", "S01_b02", "S01_b03"]
    assert info["dropped_beats"] == ["S01_b01"] and info["straddle_asset_dropped"] == "s2.jpg"
    assert out[2]["asset"] == "s3.jpg" and out[2]["start"] == 6.32 and out[2]["parallax_clip"] == "PX_s3.mp4"
    assert out[0]["role"] == "teaser" and out[0]["reuse"] == "teaser" and out[1]["end"] == pytest.approx(6.32)
    assert out[0]["first_word_time"] and float(out[0]["first_word_time"]) == pytest.approx(0.9)


def test_cold_open_shots_must_fill_teaser():
    spec = {"title": {"kicker": "K", "title": "T"},
            "shots": [{"id": "t1", "file": "f.mp4", "src": "a", "frames": 50, "label": "exact", "why": ""}]}
    with pytest.raises(ValueError):
        co.build_rows([row("b1", 0.0, 9.0, "a.jpg")], spec, 6.32, "d", {"f.mp4": {}}, [])


def test_teaser_end_uses_lead_rule():
    sp = co.load_spec()
    assert co.teaser_end(sp) == pytest.approx(6.32)            # 'bhagwan' 6.51 - 0.2, frame aligned
    assert sum(s["frames"] for s in sp["shots"]) == round(6.32 * 25)


def test_critic_teaser_is_one_hook_beat_exempt_from_g004(tmp_path):
    import csv
    fields = ["beat", "scene", "start", "end", "asset", "match", "role", "motion", "overlay_text", "source_dir"]
    rows = [["S01_t01", "S01", "0.0", "1.6", "TSR_01.mp4", "exact", "teaser", "video_clip", "DWARKA · GUJARAT | Shri Krishna ki nagri", ""],
            ["S01_t02", "S01", "1.6", "3.2", "TSR_02.mp4", "exact", "teaser", "video_clip", "DWARKA · GUJARAT | Shri Krishna ki nagri", ""],
            ["S01_b02", "S01", "3.2", "8.0", "a.jpg", "exact", "v9_shot", "zoom_in", "", ""]]
    v = tmp_path / "v.csv"
    with open(v, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(fields); w.writerows(rows)
    layer = tmp_path / "l.json"
    layer.write_text(json.dumps({"words": [{"hindi": "x", "hinglish": "x", "start": 0.5 + i, "end": 0.8 + i}
                                           for i in range(7)]}), encoding="utf-8")
    d = cr.build_beats(v, layer)
    hook = d["beats"][0]
    assert hook["kind"] == "hook" and hook["tease"] and hook["overlay"] and hook["end_s"] == 3.2
    assert hook["beat_ids"] == ["S01_t01", "S01_t02"] and hook["teaser_cuts"] == [1.6]
    assert hook["text"].split()[0] == "DWARKA"
    kc = {c["rule_id"]: c for c in cr.kang_checks(d)}
    assert kc["G-004"]["status"] == "pass"
