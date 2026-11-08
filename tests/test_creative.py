import csv
import json
from pathlib import Path

from core import creative as cr

FIELDS = ["beat", "scene", "start", "end", "duration_s", "text", "asset", "match", "role", "motion"]


def _fixture(tmp: Path):
    rows = [
        ["S01_b01", "S01", "0.0", "4.0", "4.0", "", "a.jpg", "exact", "v9_shot", "zoom_in"],
        ["S01_b02", "S01", "4.0", "8.0", "4.0", "", "CARD_C01.mp4", "text_card", "motion_card", "video_clip"],
        ["S01_b03", "S01", "8.0", "12.0", "4.0", "", "CARD_C01.mp4", "text_card", "card_hold", "video_clip"],
        ["S01_b04", "S01", "12.0", "16.0", "4.0", "", "b.jpg", "representative", "new_pool", "zoom_out"],
    ]
    v = tmp / "visuals_beats.csv"
    with open(v, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(FIELDS); w.writerows(rows)
    words = [{"word_id": i, "hindi": "शब्द", "hinglish": f"w{i}", "start": 0.5 + i, "end": 0.9 + i} for i in range(15)]
    layer = tmp / "layer.json"
    layer.write_text(json.dumps({"words": words}, ensure_ascii=False), encoding="utf-8")
    cards = tmp / "card_values.csv"
    with open(cards, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["clip", "type", "shown_text", "shown_at"])
        w.writerow(["C01", "text_card", "5,000", "4.2"]); w.writerow(["C01", "text_card", "years ago", "9.0"])
    return v, layer


def test_build_beats_merges_card_hold_and_uses_screen_text(tmp_path):
    v, layer = _fixture(tmp_path)
    d = cr.build_beats(v, layer)
    ids = [b["id"] for b in d["beats"]]
    assert ids == ["S01_b01", "S01_b02", "S01_b04"]
    card = d["beats"][1]
    assert card["kind"] == "graphic" and card["beat_ids"] == ["S01_b02", "S01_b03"]
    assert card["text"] == "5,000 years ago"          # what the viewer reads, not narration
    assert card["narration"].startswith("w4")
    assert card["end_s"] == 12.0 and card["relevant"] is True
    assert "relevant" not in d["beats"][2]              # representative = unknown, not invented
    assert d["meta"]["wpm"] and d["meta"]["profile"] == "travel_vlog_hi"


def test_audio_rules_deferred_and_listed():
    rules = cr.load_rules()
    ids = set(cr.audio_deferred_ids(rules))
    assert "R-105" in ids and "R-102" in ids           # loudness / music level
    assert "R-111" not in ids                           # first frame w/o sound = visual rule, kept


def test_travel_profile_skips_wpm_judgement(tmp_path):
    v, layer = _fixture(tmp_path)
    rep = cr.run(cr.build_beats(v, layer))
    wpm = [r for r in rep["rule_results"] if r["rule_id"] == "R-163"]
    assert not wpm or wpm[0]["status"] == "skip"
    assert rep["summary"]["deferred_audio_rules"] > 0
    assert rep["summary"]["profile"] == "travel_vlog_hi"


def test_vendor_untouched_profiles_merge():
    p = cr.load_profiles()
    assert "hindi_hinglish" in p and "travel_vlog_hi" in p
    assert p["travel_vlog_hi"]["max_visual_gap_s"] == p["hindi_hinglish"]["max_visual_gap_s"]


def test_overlay_removes_retags_and_adds():
    rules = cr.load_rules()
    out, ch = cr.apply_overlay(rules, "travel_vlog_hi")
    ids = {r["id"] for r in out}
    assert "R-432" not in ids and "R-131" not in ids     # profile-off / superseded
    assert {"G-004", "S-021", "Q-001"} <= ids
    r088 = next(r for r in out if r["id"] == "R-088")
    assert r088["evidence"] == "🟡"
    assert all(r["check"] is None for r in out if r["id"][:2] in ("G-", "S-", "Q-"))


def test_kang_checks_on_fixture(tmp_path):
    v, layer = _fixture(tmp_path)
    srt = tmp_path / "c.srt"
    srt.write_text("1\n00:00:01,000 --> 00:00:01,200\nbahut lamba caption text\n\n", encoding="utf-8")
    res = {c["rule_id"]: c for c in cr.kang_checks(cr.build_beats(v, layer), srt)}
    assert res["G-013"]["status"] == "fail" and res["S-004"]["status"] == "fail"
    assert res["G-004"]["status"] == "pass"


# ---- 2026-11-07: card item dedupe + R-236 profile scope ----
ROOT = Path(__file__).resolve().parent.parent
V17B = ROOT / "runs" / "2026-11-05_KANG_001" / "visuals_beats_v17b.csv"
LAYER = ROOT / "runs" / "2026-11-01_KANG_001" / "words_hinglish_v1_accepted.json"


def test_card_items_dedupe_same_line_two_values(tmp_path):
    p = tmp_path / "card_values.csv"
    with open(p, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f); w.writerow(["clip", "shown_text", "shown_at"])
        w.writerow(["C01", "Shri Krishna left Mathura", "61.29"])
        w.writerow(["C01", "Shri Krishna left Mathura", "61.30"])   # 2nd value of the same line
        w.writerow(["C01", "years ago", "59.17"])
        w.writerow(["C02", "years ago", "70.0"])                    # other clip -> kept
    items = cr._card_items(p)
    assert [(i["clip"], i["text"]) for i in items] == [
        ("C01", "years ago"), ("C01", "Shri Krishna left Mathura"), ("C02", "years ago")]
    assert items[1]["t"] == 61.29                                     # earliest shown_at


def test_s03_b05_card_word_count_real_data():
    import pytest
    if not (V17B.is_file() and LAYER.is_file()):
        pytest.skip("v17b run data not present")
    d = cr.build_beats(V17B, LAYER)
    b = next(x for x in d["beats"] if "S03_b05" in x["beat_ids"])
    words = [t for t in b["text"].split() if any(ch.isalnum() for ch in t)]
    assert 7 <= len(words) <= 9, b["text"]                            # was 14 before dedupe
    assert b["text"].count("Mathura") == 1


def test_r236_off_for_travel_vlog_on_for_shorts():
    rules = cr.load_rules()
    travel, _ = cr.apply_overlay(rules, "travel_vlog_hi")
    assert "R-236" not in {r["id"] for r in travel}
    assert "shorts" in cr.load_profiles()
    shorts, ch = cr.apply_overlay(rules, "shorts")
    assert "R-236" in {r["id"] for r in shorts} and "R-236" not in ch["removed"]
