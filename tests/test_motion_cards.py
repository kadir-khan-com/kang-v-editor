"""v13 moving text cards: values from narration words, layout / safe zone, rendering (no network)."""
import json
import subprocess

import numpy as np
import pytest

cv2 = pytest.importorskip("cv2")

from core import motion_cards as MC
from core import motion_draw as D
from core import narration_values as NV
from core.runs import media_summary

SAFE = {"bottom_px": 800, "left_px": 150, "right_px": 1770, "top_px": 60}


def _words(pairs, t0=10.0, step=0.4):
    """pairs: [(hindi, hinglish)] -> (words, hwords) with increasing times."""
    w = [{"word": h, "start": round(t0 + i * step, 3), "end": round(t0 + i * step + 0.3, 3)} for i, (h, _) in enumerate(pairs)]
    hw = [{"word_id": i, "hinglish": r, "start": w[i]["start"]} for i, (_, r) in enumerate(pairs)]
    return w, hw


WORDS, HW = _words([("ऑटो", "auto"), ("वाले", "wale"), ("द्वारिका", "Dwarka"), ("500", "500"), ("से", "se"), ("600", "600"),
                    ("रुपये", "rupaye"), ("पाँच", "panch"), ("से", "se"), ("6", "6"), ("प्लेसेस", "places"),
                    ("सुबह", "subah"), ("साढ़े", "sadhe"), ("छे", "chhe"), ("बजे", "baje"), ("एक", "ek"), ("बजे", "baje"),
                    ("बारह ज्योतिर्लिंग", "barah Jyotirlinga"), ("टू", "two"), ("नौ बजे", "nau baje"), ("रात", "raat"),
                    ("700", "800")])
BEATS = {"X_b01": {"beat": "X_b01", "start": 10.0, "end": 13.2}, "X_b02": {"beat": "X_b02", "start": 13.2, "end": 16.0},
         "X_b03": {"beat": "X_b03", "start": 16.0, "end": 19.0}}


def test_number_read_from_hindi_and_hinglish_agree():
    v = NV.read_value({"ids": [3]}, WORDS, HW)
    assert v["status"] == "PASS" and v["value"] == 500 and v["display"] == "500" and v["time"] == WORDS[3]["start"]
    v = NV.read_value({"ids": [7]}, WORDS, HW)          # Hindi number word, Roman number word
    assert v["status"] == "PASS" and v["value"] == 5
    v = NV.read_value({"ids": [18]}, WORDS, HW)         # English number spoken in Devanagari ('टू' / 'two')
    assert v["status"] == "PASS" and v["value"] == 2


def test_disagreeing_or_non_numbers_are_warn_never_guessed():
    v = NV.read_value({"ids": [21]}, WORDS, HW)         # Hindi 700 vs Hinglish 800
    assert v["status"] == "WARN" and v["value"] is None and "Hinglish" in v["note"]
    v = NV.read_value({"ids": [1]}, WORDS, HW)          # 'wale' is not a number
    assert v["status"] == "WARN"
    v = NV.read_value({"ids": [999]}, WORDS, HW)
    assert v["status"] == "WARN"


def test_time_needs_spoken_part_of_day_and_merged_tokens():
    v = NV.read_value({"ids": [12, 13], "kind": "time", "meridiem_id": 11}, WORDS, HW)
    assert v["status"] == "PASS" and v["display"] == "6:30 AM"
    v = NV.read_value({"ids": [15], "kind": "time", "meridiem_id": 11, "after_hour": 7}, WORDS, HW)
    assert v["display"] == "1:00 PM" and "inferred" in v["note"]
    v = NV.read_value({"ids": [19], "kind": "time", "meridiem_id": 20}, WORDS, HW)   # 'नौ बजे' merged token
    assert v["display"] == "9:00 PM"
    v = NV.read_value({"ids": [15], "kind": "time"}, WORDS, HW)
    assert v["status"] == "WARN"
    v = NV.read_value({"ids": [17], "tok": [0, 1]}, WORDS, HW)                       # 'बारह ज्योतिर्लिंग' -> 12
    assert v["status"] == "PASS" and v["value"] == 12


def test_text_value_must_be_in_hinglish_words():
    assert NV.read_value({"ids": [2], "kind": "text", "expect": "Dwarka"}, WORDS, HW)["status"] == "PASS"
    assert NV.read_value({"ids": [2], "kind": "text", "expect": "Okha"}, WORDS, HW)["status"] == "WARN"


def test_fill_counts_up_numbers_only():
    vals = [NV.read_value({"ids": [3]}, WORDS, HW), NV.read_value({"ids": [5]}, WORDS, HW)]
    assert NV.fill("₹{0}–{1}", vals) == "₹500–600"
    assert NV.fill("₹{0}–{1}", vals, 0.5) == "₹250–300"
    assert NV.fill("₹{0}", [{"kind": "number", "value": 10000.0}]) == "₹10,000"


def _spec(lines, phases=None):
    return {"id": "T1", "phases": phases or [{"beats": ["X_b01", "X_b02"], "lines": lines}]}


def test_static_text_with_digits_or_unbacked_rupee_fails():
    p = MC.plan_card(_spec([{"role": "big", "fmt": "₹500"}]), BEATS, WORDS, HW, SAFE)
    assert p["rows"][0]["status"] == "FAIL" and p["problems"]
    p = MC.plan_card(_spec([{"role": "big", "fmt": "₹{0}", "values": [{"ids": [3]}]}]), BEATS, WORDS, HW, SAFE)
    assert p["rows"][0]["status"] == "FAIL"                          # no currency word named
    p = MC.plan_card(_spec([{"role": "big", "fmt": "₹{0}", "values": [{"ids": [3]}], "currency_id": 6}]), BEATS, WORDS, HW, SAFE)
    assert p["rows"][0]["status"] == "PASS" and "rupaye" in p["rows"][0]["note"]


def test_unspoken_place_in_static_text_is_warn_and_skipped():
    p = MC.plan_card(_spec([{"role": "title", "fmt": "Somnath temple"}, {"role": "title", "fmt": "Dwarka"}]), BEATS, WORDS, HW, SAFE)
    st = [r["status"] for r in p["rows"]]
    assert st == ["WARN", "PASS"]
    assert [l["text"] for l in p["phases"][0]["visible"]] == ["Dwarka"]


def test_reveal_follows_word_and_lead_is_recorded():
    p = MC.plan_card(_spec([{"role": "big", "fmt": "₹{0}–{1}", "values": [{"ids": [3]}, {"ids": [5]}], "at": 3, "currency_id": 6}]),
                     BEATS, WORDS, HW, SAFE)
    l = p["phases"][0]["visible"][0]
    assert abs(l["reveal"] - (WORDS[3]["start"] - 0.2)) < 1e-6
    assert p["rows"][0]["display_lead_s"] == pytest.approx(0.2)
    assert p["frames"] == round(16.0 * 25) - round(10.0 * 25)


def test_phases_keep_lines_and_long_phase_is_flagged():
    phases = [{"beats": ["X_b01"], "lines": [{"role": "title", "fmt": "Auto", "keep": True}, {"role": "text", "fmt": "first"}]},
              {"beats": ["X_b02", "X_b03"], "lines": [{"role": "text", "fmt": "second"}]}]
    p = MC.plan_card(_spec(None, phases), BEATS, WORDS, HW, SAFE)
    assert [l["text"] for l in p["phases"][1]["visible"]] == ["Auto", "second"]
    assert p["phases"][0]["visible"][0]["y"] == p["phases"][1]["visible"][0]["y"]      # kept line does not jump
    long = {"id": "T2", "phases": [{"beats": ["X_b01", "X_b02", "X_b03"], "lines": [{"role": "text", "fmt": "x"}]}]}
    assert any("longer than 8.5" in s for s in MC.plan_card(long, BEATS, WORDS, HW, SAFE)["problems"])


def test_layout_stays_above_caption_zone_and_long_text_shrinks():
    lines = [{"role": "kicker", "fmt": "k"}, {"role": "title", "fmt": "A very long title that goes on and on and on for ever more"},
             {"role": "big", "fmt": "{0}", "values": [{"ids": [3]}]}, {"role": "text", "fmt": "t"}, {"role": "small", "fmt": "s"}]
    p = MC.plan_card(_spec(lines), BEATS, WORDS, HW, SAFE)
    for _, (x0, y0, x1, y1) in MC.card_boxes(p):
        assert y1 <= SAFE["bottom_px"] and x1 <= SAFE["right_px"]
    assert p["phases"][0]["visible"][1]["size"] < MC.ROLE["title"][1]


def test_render_card_frames_exact_no_audio(tmp_path):
    p = MC.plan_card(_spec([{"role": "title", "fmt": "Auto"}, {"role": "big", "fmt": "₹{0}", "values": [{"ids": [3]}], "at": 3,
                                                                "currency_id": 6}], [{"beats": ["X_b01"], "lines": [
        {"role": "title", "fmt": "Auto"}, {"role": "big", "fmt": "₹{0}", "values": [{"ids": [3]}], "at": 3, "currency_id": 6}]}]),
        BEATS, WORDS, HW, SAFE)
    out = tmp_path / "c.mp4"
    MC.render_card(p, out)
    info = media_summary(out)
    assert info["width"] == 1920 and info["height"] == 1080 and not info["has_audio"]
    n = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries",
                            "stream=nb_read_frames", "-of", "csv=p=0", str(out)], capture_output=True, text=True, encoding="utf-8").stdout.strip())
    assert n == p["frames"] == 80


def test_v17b_no_count_up_and_background_drift_change_frames():
    p = MC.plan_card(_spec(None, [{"beats": ["X_b01"], "lines": [{"role": "big", "fmt": "₹{0}", "values": [{"ids": [3]}], "at": 3,
                                                                    "currency_id": 6}]}]), BEATS, WORDS, HW, SAFE)
    l = p["phases"][0]["visible"][0]
    assert MC._line_text(l, l["reveal"]) == MC._line_text(l, l["reveal"] + 0.1) == MC._line_text(l, l["reveal"] + 2.0) == "₹500"
    bg = D.DriftBackground(320, 180, seed=1)
    assert np.abs(bg.frame(0.0) - bg.frame(4.0)).mean() > 0.05


def test_repo_spec_values_all_pass_against_real_words():
    """The shipped config: every value line reads PASS from the real Dwarika words (if the run files exist)."""
    from core import motion_assign as MA
    if not MA.WORDS.is_file() or not MA.HWORDS.is_file():
        pytest.skip("Dwarika words not in this checkout")
    w, hw = MA.load_words()
    spec = MC.load_spec()
    beats = {}
    import csv
    from core.motion_assign import ROOT
    v12 = ROOT / "runs" / "2026-11-03_KANG_033" / "visuals_beats_v12.csv"
    if not v12.is_file():
        pytest.skip("v12 beats CSV not present")
    with open(v12, encoding="utf-8-sig") as fh:
        beats = {r["beat"]: r for r in csv.DictReader(fh)}
    for c in spec["cards"]:
        p = MC.plan_card(c, beats, w, hw, spec["safe_zone"])
        assert not p["problems"], p["problems"]
        # v13b: a value spoken after the clip ends (C12 evening times, next beat is an exact shot) is WARN + not shown,
        # never FAIL and never shown early
        bad = [r for r in p["rows"] if r["status"] == "FAIL" or (r["status"] == "WARN" and "not shown" not in r["note"])]
        assert not bad, bad
        assert all(r["lead_s"] == "" or r["lead_s"] <= MC.MAX_LEAD_S + 1e-9 for r in p["rows"])


def test_v13b_each_value_appears_at_its_own_word_max_025s_early():
    """'₹500–600': 600 is spoken 0.8 s after 500 -> the line shows '₹500' first, '–600' only 0.2 s before its word."""
    p = MC.plan_card(_spec([{"role": "big", "fmt": "₹{0}–{1}", "values": [{"ids": [3]}, {"ids": [5]}], "at": 3, "currency_id": 6}]),
                     BEATS, WORDS, HW, SAFE)
    l = p["phases"][0]["visible"][0]
    assert l["vreveal"] == [pytest.approx(WORDS[3]["start"] - 0.2), pytest.approx(WORDS[5]["start"] - 0.2)]
    mid = MC._line_text(l, WORDS[5]["start"] - 0.3)                              # after 500 appeared, before 600
    assert mid.startswith("₹") and "–" not in mid and "600" not in mid
    assert MC._line_text(l, WORDS[5]["start"] + 1.5) == "₹500–600"
    for r in p["rows"]:
        assert r["lead_s"] == pytest.approx(0.2) and r["status"] == "PASS"


def test_v13b_value_spoken_after_clip_end_is_warn_not_early():
    beats = {"X_b01": {"beat": "X_b01", "start": 10.0, "end": 12.0}}              # '600' (word 5) at 12.0 = clip end
    p = MC.plan_card({"id": "T3", "phases": [{"beats": ["X_b01"], "lines": [
        {"role": "title", "fmt": "Auto"},
        {"role": "big", "fmt": "₹{0}–{1}", "values": [{"ids": [3]}, {"ids": [5]}], "at": 3, "currency_id": 6}]}]}, beats, WORDS, HW, SAFE)
    rows = [r for r in p["rows"] if r["item"] == "big"]
    assert all(r["status"] == "WARN" and r["lead_s"] == "" for r in rows) and "not shown" in rows[0]["note"]
    assert [l["text"] for l in p["phases"][0]["visible"]] == ["Auto"]


# --------------------------------------------------------------------------- v17b: values never shown in-between
def _range_card():
    return MC.plan_card(_spec([{"role": "value", "fmt": "{0} places · ₹{1}–{2}", "values": [{"ids": [9]}, {"ids": [3]}, {"ids": [5]}],
                                "at": 3, "currency_id": 6}]), BEATS, WORDS, HW, SAFE)


def test_v17b_every_frame_shows_only_final_values():
    """User bug (C17): '2 people · 0 days' / '₹9,990–5,056' while counting. Now each frame of a multi-value line
    shows a prefix of the final text with final numbers only (or nothing), never an in-between value."""
    p = _range_card()
    l = p["phases"][0]["visible"][0]
    assert MC.displayed_value_problems(p) == []
    fin = MC.NUM_RE.findall(l["text"])
    n0 = round(p["start"] * MC.FPS)
    seen = set()
    for n in range(p["frames"]):
        T = (n0 + n + 0.5) / MC.FPS
        if T < l["reveal"]:
            continue
        got = MC.NUM_RE.findall(MC._line_text(l, T))
        assert got == fin[:len(got)], (T, got)
        seen.add(len(got))
    assert max(seen) == len(fin)


def test_v17b_qa_fails_an_old_style_count_up(monkeypatch):
    p = _range_card()

    def old(l, T):  # v13b behaviour: numbers counted up from 0 over 0.9 s
        vrev = l.get("vreveal") or [l["reveal"]] * len(l["vals"])
        return NV.fill(l["fmt"], l["vals"], [D.ease_out_cubic((T - r) / 0.9) for r in vrev])
    monkeypatch.setattr(MC, "_line_text", old)
    probs = MC.displayed_value_problems(p)
    assert probs and "final" in probs[0]


def test_v17b_count_up_only_when_opted_in_single_big_number():
    one = MC.plan_card(_spec(None, [{"beats": ["X_b01"], "lines": [{"role": "big", "fmt": "₹{0}", "currency_id": 6, "at": 3,
                                                                     "values": [{"ids": [3], "count_up": True}]}]}]), BEATS, WORDS, HW, SAFE)
    l = one["phases"][0]["visible"][0]
    assert MC.count_up_allowed(l, 0)
    mid = MC._line_text(l, l["vreveal"][0] + 0.2)
    v = int(mid.strip("₹").replace(",", ""))
    assert 0 <= v < 500 and v % MC.count_up_step(500) == 0          # rounded step, never above final
    assert MC._line_text(l, l["vreveal"][0] + 1.0) == "₹500"
    assert MC.displayed_value_problems(one) == []
    small = MC.plan_card(_spec([{"role": "big", "fmt": "{0} places", "at": 9, "values": [{"ids": [9], "count_up": True}]}]),
                         BEATS, WORDS, HW, SAFE)
    ls = small["phases"][0]["visible"][0]
    assert not MC.count_up_allowed(ls, 0) and MC._line_text(ls, ls["reveal"]) == "6 places"   # < 100: no count-up
    multi = MC.plan_card(_spec([{"role": "big", "fmt": "₹{0}–{1}", "at": 3, "currency_id": 6,
                                 "values": [{"ids": [3], "count_up": True}, {"ids": [5], "count_up": True}]}]), BEATS, WORDS, HW, SAFE)
    lm = multi["phases"][0]["visible"][0]
    assert not MC.count_up_allowed(lm, 0) and not MC.count_up_allowed(lm, 1)                  # range: no count-up


def test_v17b_value_line_enters_within_03s():
    p = _range_card()
    l = p["phases"][0]["visible"][0]
    assert MC.enter_s(l) <= 0.3
    assert MC.enter_s({"vals": []}) == MC.ENTER_S


def test_v17b_repo_spec_has_no_count_up_opt_in():
    spec = MC.load_spec()
    assert not any(v.get("count_up") for c in spec["cards"] for ph in c["phases"] for ln in ph["lines"] for v in ln.get("values", []))
