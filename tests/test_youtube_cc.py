"""v15 YouTube CC (core/youtube_cc.py): mocked yt-dlp runner, synthetic frames/video. No network."""
from __future__ import annotations

import json
import subprocess

import numpy as np
import pytest

from core import stock_common as SC
from core import youtube_cc as Y

CFG = Y.load_cfg()
SCFG = SC.load_cfg()
CC = "Creative Commons Attribution license (reuse allowed)"


def _info(vid, title, lic=CC, desc="", dur=300):
    return {"id": vid, "title": title, "channel": "Chan", "upload_date": "20240225", "license": lic,
            "description": desc, "duration": dur, "tags": [],
            "formats": [{"vcodec": "avc1", "height": 1080, "ext": "mp4", "filesize": 300_000_000, "tbr": 8000},
                        {"vcodec": "vp9", "height": 2160, "ext": "webm", "filesize": 900_000_000}]}


def make_runner(search_entries, infos, block_probe=False, calls=None):
    def run(args, timeout):
        if calls is not None:
            calls.append(args)
        url = args[-1]
        if "results?search_query" in url:
            return 0, json.dumps({"entries": search_entries}), ""
        if "--skip-download" in args:
            if block_probe:
                return 1, "", "ERROR: HTTP Error 429: Too Many Requests"
            vid = url.split("v=")[1]
            if vid not in infos:
                return 1, "", "ERROR: Video unavailable"
            return 0, json.dumps(infos[vid]), ""
        return 1, "", "ERROR: download disabled in test"
    return run


def test_licence_exact_string_only():
    assert Y.licence_ok({"license": CC}, CFG)
    assert not Y.licence_ok({"license": "Standard YouTube License"}, CFG)
    assert not Y.licence_ok({}, CFG)
    assert not Y.licence_ok({"license": "Creative Commons Attribution-NonCommercial"}, CFG)


def test_place_check_gujarat_vs_delhi():
    ok = Y.place_check(_info("a", "Aerial view of Sudarshan Setu connecting Okha mainland to Beyt Dwarka"), CFG, SCFG)
    assert ok["ok"] and "sudarshan setu" in ok["places"] and "bet dwarka" in ok["places"]
    assert Y.place_check(_info("b", "द्वारका में समुद्र का रौद्र रूप"), CFG, SCFG)["ok"]
    gu = Y.place_check(_info("b2", "દ્વારકા તાલુકાના શિવરાજપુર બીચને બ્લુ ફ્લેગ"), CFG, SCFG)
    assert gu["ok"] and "shivrajpur" in gu["places"]
    assert Y.place_check(_info("b3", "PM Modi Inaugurates India's Longest Cable-Stayed Bridge 'Sudarshan Setu'"), CFG, SCFG)["ok"]
    assert not Y.place_check(_info("c", "PM inaugurates Dwarka Expressway and UER-II"), CFG, SCFG)["ok"]
    assert not Y.place_check(_info("d", "Landing through Dwarka area - New Delhi"), CFG, SCFG)["ok"]
    assert not Y.place_check(_info("e", "Junagadh, Somnath temple, dwarka town"), CFG, SCFG)["ok"]
    assert not Y.place_check(_info("f", "Beautiful beach drone shots"), CFG, SCFG)["ok"]
    assert not Y.place_check(_info("g", "Dwarka temple tour", desc="flat for rent in Dwarka sector 12, New Delhi"),
                             CFG, SCFG)["ok"]


def test_probe_blocked_after_two_ways_then_stop():
    calls = []
    with pytest.raises(Y.Blocked) as e:
        Y.probe("x1", CFG, make_runner([], {}, block_probe=True, calls=calls))
    assert len(e.value.attempts) == 2 and all(a["blocked"] for a in e.value.attempts)
    assert len(calls) == 2
    calls = []
    info, att = Y.probe("gone", CFG, make_runner([], {}, calls=calls))
    assert info == {} and len(calls) == 1  # real error, not an IP block: no second way
    info, _ = Y.probe("ok1", CFG, make_runner([], {"ok1": _info("ok1", "Dwarka")}))
    assert info["license"] == CC


def test_fetch_cmd_counts_and_blocked(tmp_path):
    ents = [{"id": "v1", "title": "Exclusive drone shots of the Sudarshan Setu connecting Okha & Beyt Dwarka", "channel": "N"},
            {"id": "v2", "title": "Dwarka Gujarat temple vlog", "channel": "M"},
            {"id": "v3", "title": "Dwarka Expressway inauguration", "channel": "N"},
            None]
    infos = {"v1": _info("v1", ents[0]["title"]), "v2": _info("v2", ents[1]["title"], lic="Standard YouTube License")}
    r = Y.fetch_cmd(str(tmp_path / "pool"), runner=make_runner(ents, infos))
    assert r["counts"].get("accepted") == 1 and r["counts"].get("rejected") == 2
    assert r["download_errors"] and r["shots"] == 0  # download disabled in the mock -> recorded, not faked
    rb = Y.fetch_cmd(str(tmp_path / "pool2"), runner=make_runner(ents, infos, block_probe=True))
    assert rb["status"] == "blocked" and rb["accepted"] == 0 and rb["qa"]["pass"] is False
    assert rb["counts"].get("unverified_blocked") == 2  # v1, v2: licence never read -> never accepted


def test_sections_bytes_and_args():
    s = Y.plan_sections(300, CFG)
    assert len(s) == 3 and all(b - a == pytest.approx(20) for a, b in s) and s[0][0] >= 300 * 0.12 - 1e-6
    assert Y.plan_sections(18, CFG) == [(0.0, 18.0)]
    info = _info("v", "t")
    assert Y.pick_format(info)["height"] == 1080
    est = Y.est_bytes(info, s)
    assert 50_000_000 < est < 80_000_000
    a = Y.download_args("v", s, "o.%(ext)s", CFG)
    assert a.count("--download-sections") == 3 and "height<=1080" in a[a.index("-f") + 1]
    assert "-x" not in a and "bestaudio" not in a[a.index("-f") + 1]


def test_shots_and_verdicts():
    assert Y.shots_from_cuts([5.0, 6.0, 12.0], 20.0, 2.5) == [(0.0, 4.8), (6.2, 11.8), (12.2, 20.0)]
    base = {"duration": 5.0, "height": 1080, "shake_px": 1.0, "face_area": 0.0, "static_overlay": 0.0}
    assert Y.shot_verdict(base, CFG) is None
    assert "shaky" in Y.shot_verdict({**base, "shake_px": 20}, CFG)
    assert "face" in Y.shot_verdict({**base, "face_area": 0.1}, CFG)
    assert "watermark" in Y.shot_verdict({**base, "static_overlay": 0.05}, CFG)
    assert "detector" in Y.shot_verdict({**base, "face_area": -1}, CFG)


def test_overlay_and_shake_metrics():
    rng = np.random.default_rng(1)
    base = (rng.random((180, 400)) * 255).astype(np.uint8)
    pan = np.stack([base[:, i * 4: i * 4 + 320] for i in range(10)])  # steady pan
    assert Y.shake_px(pan) < 2.0
    jit = np.stack([base[:, (i % 2) * 12 + 20: (i % 2) * 12 + 340] for i in range(10)])  # back-and-forth
    assert Y.shake_px(jit) > 6.0
    logo = pan.copy()
    logo[:, 10:40, 10:90] = 0
    for x in range(20, 80, 6):  # frozen text-like strokes = watermark / burned-in text
        logo[:, 18:32, x:x + 3] = 255
    assert Y.static_overlay_frac(logo) > Y.static_overlay_frac(pan)
    assert Y.static_overlay_frac(logo) > CFG["shots"]["static_overlay_frac"]


def test_scene_cuts_synthetic(tmp_path):
    p = tmp_path / "two.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc=size=320x180:rate=25:duration=3",
                    "-f", "lavfi", "-i", "color=c=red:size=320x180:rate=25:duration=3", "-filter_complex",
                    "[0:v][1:v]concat=n=2:v=1[v]", "-map", "[v]", str(p)], check=True)
    cuts = Y.scene_cuts(p, 0.3)
    assert any(abs(c - 3.0) < 0.1 for c in cuts)


def _row(beat, start, end, asset, match, role, src="pool", title=""):
    return {"beat": beat, "scene": beat.split("_")[0], "start": start, "end": end, "asset": asset, "match": match,
            "role": role, "asset_source": src, "title": title, "source_dir": "x", "licence": "", "notes": ""}


def test_plan_youtube_rules():
    rows = [_row("S01_b01", 0, 4, "temple.jpg", "exact", "v9_shot", title="Dwarkadhish temple"),
            _row("S01_b02", 4, 8, "temple.jpg", "exact", "continued_with_motion", title="Dwarkadhish temple"),
            _row("S02_b01", 8, 12, "STK_a.mp4", "representative", "new_stock", src="pixabay"),
            _row("S02_b02", 12, 16, "CARD_C1.mp4", "text_card", "motion_card", src="kang_motion"),
            _row("S03_b01", 16, 20, "STK_b.mp4", "representative", "new_stock", src="pixabay"),
            _row("S04_b01", 20, 24, "STK_c.mp4", "representative", "new_stock", src="pixabay")]
    pool = [{"key": "yt:1", "file": "YT_1.mp4", "dir": "d", "place": "sudarshan setu", "label": "representative",
             "duration": 10, "title": "T1", "channel": "C", "url": "u1", "credit": "T1 — C (YouTube), CC BY 3.0"},
            {"key": "yt:2", "file": "YT_2.mp4", "dir": "d", "place": "dwarkadhish", "label": "representative",
             "duration": 10, "title": "T2", "channel": "C", "url": "u2", "credit": "c2"},
            {"key": "yt:3", "file": "YT_3.mp4", "dir": "d", "place": "dwarkadhish", "label": "exact",
             "duration": 2, "title": "T3", "channel": "C", "url": "u3", "credit": "c3"}]
    places = {"S02_b01": {"sudarshan setu"}, "S03_b01": {"sudarshan setu"}, "S02_b02": {"sudarshan setu"},
              "S04_b01": set()}
    new, dec = Y.plan_youtube(rows, pool, places, lambda r: {"dwarkadhish"} if "temple" in r["asset"] else set())
    by = {r["beat"]: r for r in new}
    assert by["S01_b01"]["asset"] == "temple.jpg"  # exact shot never replaced
    assert by["S01_b02"]["asset"] == "temple.jpg"  # continued of an exact hold: only an exact clip (yt:3 too short)
    assert by["S02_b01"]["asset"] == "YT_1.mp4" and by["S02_b01"]["match"] == "representative"
    assert by["S02_b02"]["asset"] == "CARD_C1.mp4"  # card untouched
    assert by["S03_b01"]["asset"] == "STK_b.mp4"  # yt:1 already used -> no repeat
    assert by["S04_b01"]["asset"] == "STK_c.mp4"  # narration names no place -> keep stock
    assert by["S02_b01"]["licence"].endswith("CC BY 3.0")
    pool[2]["duration"] = 10
    new2, _ = Y.plan_youtube(rows, pool, places, lambda r: {"dwarkadhish"} if "temple" in r["asset"] else set())
    assert {r["beat"]: r for r in new2}["S01_b02"]["asset"] == "YT_3.mp4"


def test_credit_line():
    assert Y.credit_line({"title": "Aerial view", "channel": "Narendra Modi"}, CFG) == \
        "Aerial view — Narendra Modi (YouTube), CC BY 3.0"


def test_analyse_and_cut_shot_synthetic(tmp_path):
    p = tmp_path / "pan.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "testsrc2=size=1280x720:rate=25:duration=4",
                    str(p)], check=True)
    m = Y.analyse_shot(p, 0.2, 3.8, CFG, detector=lambda img: [], height=720)
    assert m["duration"] == pytest.approx(3.6) and m["face_area"] == 0.0 and "shake_px" in m
    o = Y.cut_shot(p, 0.2, 3.8, tmp_path / "YT_x_01.mp4")
    assert not o.get("has_audio") and abs(float(o["duration"]) - 3.6) < 0.1


def test_shot_key_and_apply_eye():
    assert Y.shot_key("YT_ab_c-1_D_03.mp4") == "ab_c-1_D@3"
    cfg = {"eye_rejects": {"vid1@2": "wrong place"}, "eye_exact": {"vid1@1": "gomti"}}
    cr = [{"file": "YT_vid1_01.mp4", "label": "representative", "place": "dwarkadhish"},
          {"file": "YT_vid1_02.mp4", "label": "representative", "place": "dwarkadhish"},
          {"file": "YT_vid1_03.mp4", "label": "representative", "place": "dwarkadhish"}]
    sk = []
    out = Y.apply_eye(cr, cfg, sk)
    assert [c["file"] for c in out] == ["YT_vid1_01.mp4", "YT_vid1_03.mp4"]
    assert out[0]["label"] == "exact" and out[0]["place"] == "gomti"
    assert out[1]["label"] == "representative"
    assert sk[0]["key"] == "vid1@2" and cr[0]["label"] == "representative"  # input not mutated


def _yt(key, place, label, dur):
    return {"key": key, "file": key.split(":")[1] + ".mp4", "dir": "d", "place": place, "label": label,
            "duration": dur, "title": "T", "channel": "C", "url": "u", "credit": "T — C (YouTube), CC BY 3.0"}


def test_plan_youtube_v16_rule_a_archival_and_named_representative():
    rows = [_row("S17_b03", 0, 3, "S17_bridge_archival_label.jpg", "archival", "v9_shot"),
            _row("S17_b04", 3, 6, "S17_bridge_archival_label.jpg", "archival", "card_hold"),
            _row("S07_b05", 6, 9, "B10_dwarkadhish_rep.jpg", "representative", "new_pool", src="pool"),
            _row("S07_b06", 9, 12, "B10_other_rep.jpg", "representative", "new_pool", src="pool"),
            _row("S07_b07", 12, 15, "exact_temple.jpg", "exact", "v9_shot"),
            _row("S07_b08", 15, 18, "MAP_M4.mp4", "map", "motion_map", src="kang_motion"),
            _row("S07_b09", 18, 21, "B10_gomti_rep.jpg", "representative", "new_pool", src="pool")]
    places = {"S17_b03": {"sudarshan setu"}, "S07_b05": {"dwarkadhish"}, "S07_b07": {"dwarkadhish"},
              "S07_b08": {"sudarshan setu"}, "S07_b09": {"gomti"}}
    pool = [_yt("yt:setu_long", "sudarshan setu", "exact", 12), _yt("yt:setu_rep", "sudarshan setu", "representative", 30),
            _yt("yt:dw_exact", "dwarkadhish", "exact", 5), _yt("yt:dw_rep", "dwarkadhish", "representative", 9),
            _yt("yt:gomti_rep", "gomti", "representative", 9), _yt("yt:setu_2", "sudarshan setu", "exact", 8)]
    vr = {"archival_replace_places": ["sudarshan setu"], "named_representative": True}
    # v15 behaviour (no vrules): archival + representative stills untouched
    old, _ = Y.plan_youtube(rows, pool, places, lambda r: set())
    assert [r["asset"] for r in old] == [r["asset"] for r in rows]
    new, dec = Y.plan_youtube(rows, pool, places, lambda r: set(), vr)
    by = {r["beat"]: r for r in new}
    # (1) whole archival hold -> one EXACT Setu clip (representative 30 s clip refused), no archival still left
    assert by["S17_b03"]["asset"] == by["S17_b04"]["asset"] == "setu_long.mp4"
    assert by["S17_b03"]["match"] == "exact" and all("archival" not in r["asset"] for r in new)
    # (2) representative still whose narration names the place -> exact clip; representative clip never used
    assert by["S07_b05"]["asset"] == "dw_exact.mp4" and by["S07_b05"]["match"] == "exact"
    assert by["S07_b09"]["asset"] == "B10_gomti_rep.jpg"  # only a representative Gomti clip -> kept
    assert by["S07_b06"]["asset"] == "B10_other_rep.jpg"  # narration names no place -> kept
    assert by["S07_b07"]["asset"] == "exact_temple.jpg" and by["S07_b08"]["asset"] == "MAP_M4.mp4"  # protected
    # no repeat: each pool clip on one unit only
    clips = [d["item"] for d in dec if d["action"] == "replaced"]
    assert len(clips) == len(set(clips)) == 2
    kinds = {d["unit"] for d in dec if d["action"] == "replaced"}
    assert kinds == {"archival", "named_representative"}
    # archival whose narration names no listed place stays
    new2, _ = Y.plan_youtube(rows, pool, {**places, "S17_b03": set()}, lambda r: set(), vr)
    assert new2[0]["asset"] == "S17_bridge_archival_label.jpg"


def test_plan_youtube_v16_forced_outro_and_prefer():
    rows = [_row("S22_b05", 0, 3, "STK_x.mp4", "representative", "new_stock", src="pixabay"),
            _row("S22_b06", 3, 6, "STK_subscribe.mp4", "representative", "new_stock", src="pixabay")]
    pool = [_yt("yt:a", "dwarkadhish", "exact", 6), _yt("yt:b", "shivrajpur", "representative", 8)]
    vr = {"force": {"S22_b06": {"reason": "decision C"}}, "prefer": {"S22_b06": "yt:b"}}
    new, dec = Y.plan_youtube(rows, pool, {}, lambda r: set(), vr)
    by = {r["beat"]: r for r in new}
    assert by["S22_b05"]["asset"] == "STK_x.mp4"  # not forced, narration names no place
    assert by["S22_b06"]["asset"] == "b.mp4" and by["S22_b06"]["match"] == "representative"  # eye-preferred
    d = [d for d in dec if d["action"] == "replaced"][0]
    assert d["unit"] == "forced" and d["eye_preferred"] and d["before"] == "STK_subscribe.mp4"
    new2, _ = Y.plan_youtube(rows, pool, {}, lambda r: set(), {"force": {"S22_b06": {}}})
    assert {r["beat"]: r for r in new2}["S22_b06"]["asset"] == "a.mp4"  # no preference -> exact first
    # a clip already on the timeline from an earlier pass (YTC_<beat>_<stem>.mp4) is never used again
    rows3 = [dict(rows[0], asset="YTC_S22_b05_a.mp4", asset_source="youtube_cc", match="exact", role="new_youtube_cc"),
             rows[1]]
    new3, _ = Y.plan_youtube(rows3, pool, {}, lambda r: set(), {"force": {"S22_b06": {}}})
    assert {r["beat"]: r for r in new3}["S22_b06"]["asset"] == "b.mp4"


def test_fetch_cmd_skip_video_ids(tmp_path):
    ents = [{"id": "v1", "title": "Sudarshan Setu Okha Bet Dwarka drone", "channel": "N"},
            {"id": "v2", "title": "Shivrajpur beach Dwarka", "channel": "M"}]
    infos = {"v1": _info("v1", ents[0]["title"]), "v2": _info("v2", ents[1]["title"])}
    cfg = json.loads(json.dumps(CFG))
    cfg["skip_video_ids"] = ["v1"]
    cp = tmp_path / "cfg.json"
    cp.write_text(json.dumps(cfg), encoding="utf-8")
    calls = []
    r = Y.fetch_cmd(str(tmp_path / "pool"), runner=make_runner(ents, infos, calls=calls), cfg_path=str(cp))
    assert r["counts"].get("skipped") == 1 and r["counts"].get("accepted") == 1
    assert not any("watch?v=v1" in " ".join(c) for c in calls if "--skip-download" in c)
