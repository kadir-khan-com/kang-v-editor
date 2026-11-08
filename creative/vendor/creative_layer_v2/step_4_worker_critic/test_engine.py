#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Step 4 engine ke tests — stdlib unittest, asal rules.json + profiles.json par.
Chalana:  python3 test_engine.py
"""

import json
import os
import subprocess
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import engine  # noqa: E402


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


RULES = load_json(engine.DEFAULT_RULES)
PROFILES = {k: v for k, v in load_json(engine.DEFAULT_PROFILES).items()
            if not k.startswith("_")}


def run(data, profile=None):
    return engine.run_engine(data, RULES, PROFILES, profile_override=profile)


def rres(report, rid):
    for rr in report["rule_results"]:
        if rr["rule_id"] == rid:
            return rr
    return None


def beat(bid, start, end, kind="speech", **kw):
    b = {"id": bid, "start_s": start, "end_s": end, "kind": kind}
    b.update(kw)
    return b


def meta(profile="long_explainer", **kw):
    m = {"profile": profile, "platform": "youtube", "duration_s": 100}
    m.update(kw)
    return m


class TestVisualGap(unittest.TestCase):
    def test_gap_violation_pakda_jata_hai(self):
        data = {"meta": meta(duration_s=30),
                "beats": [beat("b1", 0, 5, "hook", visual_change=True,
                               text="hook ki baat yahan shuru hoti hai doston"),
                          beat("b2", 5, 30, "speech", visual_change=False,
                               text="lambi baat bina kisi badlav ke chalti rehti hai")]}
        rep = run(data)
        self.assertEqual(rres(rep, "R-160")["status"], "fail")
        self.assertTrue(any(f["rule_id"] == "R-160" and f["beat_id"] == "b2"
                            for f in rep["findings"]))

    def test_gap_nahi_to_pass(self):
        data = {"meta": meta(duration_s=10),
                "beats": [beat("b1", 0, 5, "hook", visual_change=True, text="hook baat"),
                          beat("b2", 5, 10, "speech", visual_change=True, text="baat")]}
        rep = run(data)
        self.assertEqual(rres(rep, "R-160")["status"], "pass")


class TestHookWindow(unittest.TestCase):
    def test_der_se_hook_fail(self):
        data = {"meta": meta(duration_s=30),
                "beats": [beat("s1", 0, 9, "speech", visual_change=True, text="aam baat"),
                          beat("h1", 9, 14, "hook", visual_change=True, text="asli hook der se")]}
        rep = run(data)
        self.assertEqual(rres(rep, "R-001")["status"], "fail")

    def test_samay_par_hook_pass(self):
        data = {"meta": meta(duration_s=30),
                "beats": [beat("h1", 2, 7, "hook", visual_change=True, text="hook samay par"),
                          beat("s1", 7, 30, "speech", visual_change=True, text="baat")]}
        rep = run(data)
        self.assertEqual(rres(rep, "R-001")["status"], "pass")
        self.assertEqual(rres(rep, "R-028")["status"], "pass")


class TestOpenLoops(unittest.TestCase):
    def test_loop_band_to_fail(self):
        data = {"meta": meta(duration_s=25),
                "beats": [beat("b1", 0, 5, "hook", visual_change=True, open_loop_open=True, text="sawaal"),
                          beat("b2", 5, 10, "speech", visual_change=True, open_loop_close=True, text="jawab jaldi"),
                          beat("b3", 10, 15, "speech", visual_change=True, text="aam baat"),
                          beat("b4", 15, 20, "speech", visual_change=True, text="aur aam baat"),
                          beat("b5", 20, 25, "payoff", visual_change=True, text="khatm")]}
        rep = run(data)
        self.assertEqual(rres(rep, "R-034")["status"], "fail")
        self.assertTrue(any(f["rule_id"] == "R-034" and f["beat_id"] == "b3"
                            for f in rep["findings"]))

    def test_loop_zinda_to_pass(self):
        data = {"meta": meta(duration_s=25),
                "beats": [beat("b1", 0, 5, "hook", visual_change=True, open_loop_open=True, text="sawaal"),
                          beat("b2", 5, 20, "speech", visual_change=True, text="kahani chalti hai"),
                          beat("b3", 20, 25, "payoff", visual_change=True, open_loop_close=True, text="jawab")]}
        rep = run(data)
        self.assertEqual(rres(rep, "R-034")["status"], "pass")


class TestProfileOverrides(unittest.TestCase):
    def test_caption_chars_profile_se_badte_hain(self):
        beats = [beat("s1", 0, 30, "speech", visual_change=True, caption_chars=40, text="baat")]
        rep_short = run({"meta": meta(profile="shorts", duration_s=30), "beats": beats})
        rep_long = run({"meta": meta(profile="long_explainer", duration_s=30), "beats": beats})
        self.assertEqual(rres(rep_short, "R-092")["status"], "fail")   # shorts hadd 32
        self.assertEqual(rres(rep_long, "R-092")["status"], "pass")    # long hadd 42

    def test_lufs_profile(self):
        beats = [beat("s1", 0, 30, "speech", visual_change=True, text="baat")]
        rep_pod = run({"meta": meta(profile="podcast", duration_s=30, lufs=-15.5), "beats": beats})
        rep_yt = run({"meta": meta(profile="long_explainer", duration_s=30, lufs=-15.5), "beats": beats})
        self.assertEqual(rres(rep_pod, "R-105")["status"], "pass")   # podcast target -16
        self.assertEqual(rres(rep_yt, "R-105")["status"], "fail")    # youtube target -14
        rep_pod2 = run({"meta": meta(profile="podcast", duration_s=30, lufs=-13), "beats": beats})
        rep_yt2 = run({"meta": meta(profile="long_explainer", duration_s=30, lufs=-13), "beats": beats})
        self.assertEqual(rres(rep_pod2, "R-105")["status"], "fail")
        self.assertEqual(rres(rep_yt2, "R-105")["status"], "pass")


class TestConflicts(unittest.TestCase):
    def test_relevance_gate_cadence_ko_harata_hai(self):
        data = {"meta": meta(duration_s=45),
                "beats": [beat("b1", 0, 5, "hook", visual_change=True, text="hook baat"),
                          beat("b2", 5, 40, "speech", visual_change=False, text="lambi sthir baat"),
                          beat("b3", 40, 45, "broll", visual_change=True, relevant=False,
                               text="sajawati b-roll jo bole se alag hai")]}
        rep = run(data)
        self.assertEqual(rres(rep, "R-160")["status"], "fail")
        self.assertTrue(any(f["rule_id"] == "R-088" and f["beat_id"] == "b3"
                            for f in rep["findings"]))
        res = [r for r in rep["resolutions"]
               if r["winner_rule"] == "R-088" and r["loser_rule"] == "R-160"]
        self.assertTrue(res, "resolution me R-088 winner aur R-160 loser hona chahiye")

    def test_unmotivated_punch_in_resolution(self):
        data = {"meta": meta(duration_s=45),
                "beats": [beat("b1", 0, 5, "hook", visual_change=True, text="hook baat"),
                          beat("b2", 5, 40, "speech", visual_change=False, text="sthir baat"),
                          beat("b3", 40, 45, "speech", visual_change=True,
                               punch_in=True, motivated=False, text="bina wajah zoom")]}
        rep = run(data)
        self.assertTrue(any(f["rule_id"] == "R-200" and f["beat_id"] == "b3"
                            for f in rep["findings"]))
        res = [r for r in rep["resolutions"]
               if r["winner_rule"] == "R-200" and r["loser_rule"] == "R-160"]
        self.assertTrue(res, "resolution me R-200 winner hona chahiye (ORDER #5)")


class TestHumanFlags(unittest.TestCase):
    def test_emotion_beat_sirf_flag_koi_fail_nahi(self):
        data = {"meta": meta(duration_s=100),
                "beats": [beat("b1", 0, 5, "hook", visual_change=True,
                               text="ek sawaal jo tumhe rok dega abhi"),
                          beat("e1", 78, 90, "payoff", visual_change=True, emotion_peak=True,
                               text="yahi woh pal hai jiska intezaar tha")]}
        rep = run(data)
        self.assertTrue(any(f["beat_id"] == "e1" for f in rep["human_flags"]),
                        "emotion beat par human flag hona chahiye")
        self.assertFalse(any(f["beat_id"] == "e1" for f in rep["findings"]),
                         "emotion beat par koi FAIL finding nahi honi chahiye")

    def test_dramatic_pause_flag_plain_pause_fail(self):
        base = [beat("b1", 0, 5, "hook", visual_change=True, text="hook"),
                beat("b2", 6.5, 12, "speech", visual_change=True, text="baat")]
        dram = {"meta": meta(duration_s=12),
                "beats": base[:1] + [beat("p1", 5, 6.5, "pause", dramatic_pause=True)] + base[1:]}
        rep_d = run(dram)
        self.assertEqual(rres(rep_d, "R-162")["status"], "pass")
        self.assertTrue(any(f["beat_id"] == "p1" for f in rep_d["human_flags"]))
        plain = {"meta": meta(duration_s=12),
                 "beats": base[:1] + [beat("p1", 5, 6.5, "pause", dramatic_pause=False)] + base[1:]}
        rep_p = run(plain)
        self.assertEqual(rres(rep_p, "R-162")["status"], "fail")


class TestSponsorOrder(unittest.TestCase):
    def test_sponsor_payoff_se_pehle_fail(self):
        data = {"meta": meta(duration_s=100),
                "beats": [beat("b1", 0, 5, "hook", visual_change=True, text="hook"),
                          beat("sp", 30, 40, "sponsor", visual_change=True, text="sponsor sandesh"),
                          beat("pf", 78, 90, "payoff", visual_change=True, text="asli jawab")]}
        rep = run(data)
        self.assertEqual(rres(rep, "R-038")["status"], "fail")

    def test_sponsor_payoff_ke_baad_pass(self):
        data = {"meta": meta(duration_s=100),
                "beats": [beat("b1", 0, 5, "hook", visual_change=True, text="hook"),
                          beat("pf", 30, 40, "payoff", visual_change=True, text="pehla jawab"),
                          beat("sp", 80, 90, "sponsor", visual_change=True, text="sponsor sandesh")]}
        rep = run(data)
        self.assertEqual(rres(rep, "R-038")["status"], "pass")


class TestMisc(unittest.TestCase):
    def test_data_nahi_to_skip_fail_nahi(self):
        data = {"meta": meta(duration_s=30),
                "beats": [beat("s1", 0, 30, "speech", visual_change=True, text="sirf baat")]}
        rep = run(data)
        # hook_score, retention, chapters jaise data nahi — sab skip, fail nahi
        self.assertEqual(rres(rep, "R-004")["status"], "skip")
        self.assertEqual(rres(rep, "R-087")["status"], "skip")
        self.assertEqual(rres(rep, "R-096")["status"], "skip")

    def test_cli_bina_args_usage(self):
        proc = subprocess.run([sys.executable, os.path.join(HERE, "engine.py")],
                              capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("usage", (proc.stderr + proc.stdout).lower())


class TestLoudnessDestination(unittest.TestCase):
    """ADDENDUM A7 — destination table profile defaults se upar."""

    def test_broadcast_destination_minus24(self):
        beats = [beat("s1", 0, 30, "speech", visual_change=True, text="baat")]
        rep_ok = run({"meta": meta(duration_s=30, lufs=-24, destination="broadcast"),
                      "beats": beats})
        self.assertEqual(rres(rep_ok, "R-105")["status"], "pass")   # broadcast target -24
        rep_bad = run({"meta": meta(duration_s=30, lufs=-14, destination="broadcast"),
                       "beats": beats})
        self.assertEqual(rres(rep_bad, "R-105")["status"], "fail")  # -14 broadcast par galat

    def test_netflix_destination_aur_true_peak(self):
        beats = [beat("s1", 0, 30, "speech", visual_change=True, text="baat")]
        rep_ok = run({"meta": meta(duration_s=30, lufs=-27, destination="netflix"),
                      "beats": beats})
        self.assertEqual(rres(rep_ok, "R-105")["status"], "pass")   # netflix target -27
        rep_tp = run({"meta": meta(duration_s=30, lufs=-27, destination="netflix",
                                   true_peak_db=-1),
                      "beats": beats})
        self.assertEqual(rres(rep_tp, "R-105")["status"], "fail")   # TP -1 > -2 hadd

    def test_podcast_band_rule(self):
        beats = [beat("s1", 0, 30, "speech", visual_change=True, text="baat")]
        rep_ok = run({"meta": meta(profile="podcast", duration_s=30, lufs=-18), "beats": beats})
        self.assertEqual(rres(rep_ok, "R-441")["status"], "pass")   # band -20..-16
        rep_bad = run({"meta": meta(profile="podcast", duration_s=30, lufs=-13), "beats": beats})
        self.assertEqual(rres(rep_bad, "R-441")["status"], "fail")
        rep_skip = run({"meta": meta(duration_s=30, lufs=-18), "beats": beats})
        self.assertEqual(rres(rep_skip, "R-441")["status"], "skip")  # podcast gate


class TestAlternatingPunchIn(unittest.TestCase):
    """ADDENDUM A4 — alternating 100<->112 sirf fast_talking_head me allowed."""

    def _data(self, profile):
        return {"meta": meta(profile=profile, duration_s=45),
                "beats": [beat("b1", 0, 5, "hook", visual_change=True, text="hook baat"),
                          beat("b2", 5, 40, "speech", visual_change=False, text="sthir baat"),
                          beat("b3", 40, 45, "speech", visual_change=True, punch_in=True,
                               motivated=False, scale_pct=112, text="pattern punch")]}

    def test_fast_profile_me_allowed(self):
        rep = run(self._data("fast_talking_head"))
        self.assertFalse(any(f["rule_id"] == "R-200" and f["beat_id"] == "b3"
                             for f in rep["findings"]),
                         "fast profile me alternating pattern par R-200 nahi lagna chahiye")
        self.assertEqual(rres(rep, "R-296")["status"], "pass")      # scale 112 band me

    def test_long_profile_me_resolution(self):
        rep = run(self._data("long_explainer"))
        self.assertTrue(any(f["rule_id"] == "R-200" and f["beat_id"] == "b3"
                            for f in rep["findings"]))
        res = [r for r in rep["resolutions"]
               if r["winner_rule"] == "R-200" and r["loser_rule"] == "R-160"]
        self.assertTrue(res, "long profile me R-200 resolution hona chahiye")
        self.assertEqual(rres(rep, "R-296")["status"], "skip")      # A4 gate


class TestOvershootContext(unittest.TestCase):
    """ADDENDUM A5 — overshoot ki pankti motion_class se tay hoti hai."""

    def _run_with_class(self, mclass, beats):
        profiles = dict(PROFILES)
        profiles["long_explainer"] = dict(PROFILES["long_explainer"], motion_class=mclass)
        data = {"meta": meta(duration_s=30), "beats": beats}
        return engine.run_engine(data, RULES, profiles)

    def test_premium_me_30pct_fail(self):
        beats = [beat("a1", 0, 10, "graphic", visual_change=True, overshoot_pct=30, text="anim")]
        rep = self._run_with_class("premium", beats)
        self.assertEqual(rres(rep, "R-313")["status"], "fail")      # premium band 1.5-3%
        self.assertEqual(rres(rep, "R-287")["status"], "skip")      # character pankti nahi

    def test_character_me_30pct_pass(self):
        beats = [beat("a1", 0, 10, "graphic", visual_change=True, exaggeration_pct=30, text="anim")]
        rep = self._run_with_class("character", beats)
        self.assertEqual(rres(rep, "R-287")["status"], "pass")      # character band 20-50%
        self.assertEqual(rres(rep, "R-313")["status"], "skip")

    def test_brand_follow_through_band(self):
        beats = [beat("a1", 0, 10, "graphic", visual_change=True,
                      follow_through_overshoot_pct=15, text="anim")]
        rep = self._run_with_class("brand", beats)
        self.assertEqual(rres(rep, "R-322")["status"], "pass")      # brand band 10-20%
        beats2 = [beat("a1", 0, 10, "graphic", visual_change=True,
                       follow_through_overshoot_pct=25, text="anim")]
        rep2 = self._run_with_class("brand", beats2)
        self.assertEqual(rres(rep2, "R-322")["status"], "fail")


class TestNewKinds(unittest.TestCase):
    """Editor round ke naye check kinds: min_gap_ms, frame_range, ratio_range."""

    def test_min_gap_ms_speech_cut(self):
        bad = [beat("s1", 0, 10, "speech", visual_change=True, speech_cut_distance_ms=10, text="baat")]
        rep = run({"meta": meta(duration_s=10), "beats": bad})
        self.assertEqual(rres(rep, "R-347")["status"], "fail")      # 10ms < 30ms — clipped
        ok = [beat("s1", 0, 10, "speech", visual_change=True, speech_cut_distance_ms=80, text="baat")]
        rep2 = run({"meta": meta(duration_s=10), "beats": ok})
        self.assertEqual(rres(rep2, "R-347")["status"], "pass")

    def test_frame_range_stagger(self):
        ok = [beat("a1", 0, 10, "graphic", visual_change=True, stagger_frames=3, text="anim")]
        rep = run({"meta": meta(duration_s=10), "beats": ok})
        self.assertEqual(rres(rep, "R-305")["status"], "pass")      # band 2-5 frames
        bad = [beat("a1", 0, 10, "graphic", visual_change=True, stagger_frames=9, text="anim")]
        rep2 = run({"meta": meta(duration_s=10), "beats": bad})
        self.assertEqual(rres(rep2, "R-305")["status"], "fail")

    def test_ratio_range_shots(self):
        ok = [beat("b1", 0, 2, "hook", visual_change=True, text="hook"),
              beat("b2", 2, 6, "speech", visual_change=True, text="baat"),
              beat("b3", 6, 12, "speech", visual_change=True, text="baat")]
        rep = run({"meta": meta(duration_s=12), "beats": ok})
        self.assertEqual(rres(rep, "R-338")["status"], "pass")      # ratio 3, band 2-4
        bad = [beat("b1", 0, 2, "hook", visual_change=True, text="hook"),
               beat("b2", 2, 6, "speech", visual_change=True, text="baat"),
               beat("b3", 6, 26, "speech", visual_change=True, text="bahut lambi baat")]
        rep2 = run({"meta": meta(duration_s=26), "beats": bad})
        self.assertEqual(rres(rep2, "R-338")["status"], "fail")     # ratio 10


class TestAutoFirstPass(unittest.TestCase):
    """ADDENDUM A1 — smart-cut >1s sirf auto pehle pass me."""

    def _data(self, **mkw):
        return {"meta": meta(duration_s=12, **mkw),
                "beats": [beat("b1", 0, 5, "hook", visual_change=True, text="hook"),
                          beat("p1", 5, 6.5, "pause", dramatic_pause=False),
                          beat("b2", 6.5, 12, "speech", visual_change=True, text="baat")]}

    def test_default_pass_me_skip(self):
        rep = run(self._data())
        self.assertEqual(rres(rep, "R-282")["status"], "skip")

    def test_auto_pass_me_fail(self):
        rep = run(self._data(auto_first_pass=True))
        self.assertEqual(rres(rep, "R-282")["status"], "fail")      # 1.5s plain pause > 1s


class TestAddendumAudio(unittest.TestCase):
    """ADDENDUM A8 — ducker depth cap aur SFX asset-level normalize."""

    def test_ducker_depth_cap(self):
        beats = [beat("s1", 0, 30, "speech", visual_change=True, text="baat")]
        rep_ok = run({"meta": meta(duration_s=30, ducker_depth_db=4), "beats": beats})
        self.assertEqual(rres(rep_ok, "R-440")["status"], "pass")   # band ..5 dB
        rep_bad = run({"meta": meta(duration_s=30, ducker_depth_db=8), "beats": beats})
        self.assertEqual(rres(rep_bad, "R-440")["status"], "fail")

    def test_sfx_asset_level_master_se_alag(self):
        beats = [beat("s1", 0, 30, "speech", visual_change=True, text="baat")]
        rep_ok = run({"meta": meta(duration_s=30, lufs=-14, sfx_lufs=-16), "beats": beats})
        self.assertEqual(rres(rep_ok, "R-334")["status"], "pass")   # asset -16 target par
        rep_bad = run({"meta": meta(duration_s=30, lufs=-14, sfx_lufs=-10), "beats": beats})
        self.assertEqual(rres(rep_bad, "R-334")["status"], "fail")
        rep_skip = run({"meta": meta(duration_s=30, lufs=-16), "beats": beats})
        self.assertEqual(rres(rep_skip, "R-334")["status"], "skip")  # master -16 se pass NAHI


class TestHindiHinglishFlags(unittest.TestCase):
    """Language pass: Hindi/Hinglish text se topic flags (flag andhaapan fix)."""

    def lang_flags(self, rep, bid):
        return [f for f in rep["human_flags"]
                if f["beat_id"] == bid and f["rule_id"].startswith("LANG:")]

    def test_devanagari_beat_par_flag(self):
        data = {"meta": meta(duration_s=30),
                "beats": [beat("h1", 0, 10, "speech", visual_change=True,
                               text="लेकिन सबसे ख़ास बात ये है कि यहाँ चमत्कार हुआ था"),
                          beat("s1", 10, 30, "speech", visual_change=True,
                               text="आगे का रास्ता हम धीरे धीरे तय करते हैं")]}
        rep = run(data)
        hits = self.lang_flags(rep, "h1")
        self.assertTrue(hits, "Devanagari payoff text par kam se kam ek LANG flag aana chahiye")
        self.assertTrue(any(f["rule_id"] == "LANG:payoff_bada_pal" for f in hits))

    def test_roman_hinglish_beat_par_flag(self):
        data = {"meta": meta(duration_s=30),
                "beats": [beat("h1", 0, 10, "speech", visual_change=True,
                               text="lekin sabse khaas baat ye hai, aakhirkaar wo pal aa gaya"),
                          beat("s1", 10, 30, "speech", visual_change=True,
                               text="aage ka raasta hum dheere dheere tay karte hain")]}
        rep = run(data)
        hits = self.lang_flags(rep, "h1")
        self.assertTrue(hits, "Roman Hinglish payoff text par LANG flag aana chahiye")
        self.assertTrue(any(f["rule_id"] == "LANG:payoff_bada_pal" for f in hits))

    def test_saada_hindi_beat_par_jhoota_flag_nahi(self):
        data = {"meta": meta(duration_s=30),
                "beats": [beat("s1", 0, 30, "speech", visual_change=True,
                               text="हम लोग सुबह नाश्ता करके बाज़ार गए और वहाँ से सब्ज़ी लेकर घर वापस आ गए")]}
        rep = run(data)
        self.assertEqual(self.lang_flags(rep, "s1"), [],
                         "bina sanket-shabd wale saada beat par koi LANG flag nahi hona chahiye")

    def test_english_purana_structural_flag_berkarar(self):
        # Purana behaviour: emotion_peak wala beat bina Hindi text ke bhi flag hota tha — waisa hi rahe
        data = {"meta": meta(duration_s=100),
                "beats": [beat("b1", 0, 5, "hook", visual_change=True,
                               text="a simple opening line in plain english"),
                          beat("e1", 78, 90, "payoff", visual_change=True, emotion_peak=True,
                               text="the moment everyone was waiting for")]}
        rep = run(data)
        self.assertTrue(any(f["beat_id"] == "e1" and not f["rule_id"].startswith("LANG:")
                            for f in rep["human_flags"]),
                        "purana structural (ORDER-§3 / rule-based) flag pehle jaisa aana chahiye")
        self.assertFalse(any(f["beat_id"] == "e1" for f in rep["findings"]))

    def test_dharmik_aur_cta_topics_bhi_match_hote_hain(self):
        data = {"meta": meta(duration_s=60),
                "beats": [beat("d1", 0, 30, "speech", visual_change=True,
                               text="ऐसी मान्यता है कि यहाँ दर्शन करने से मनोकामना पूरी होती है"),
                          beat("c1", 30, 60, "speech", visual_change=True,
                               text="वीडियो को अंत तक ज़रूर देखें और चैनल को सब्सक्राइब करें")]}
        rep = run(data)
        self.assertTrue(any(f["rule_id"] == "LANG:dharmik_context"
                            for f in self.lang_flags(rep, "d1")))
        self.assertTrue(any(f["rule_id"] == "LANG:cta_retention"
                            for f in self.lang_flags(rep, "c1")))


if __name__ == "__main__":
    unittest.main(verbosity=2)
