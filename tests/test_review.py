import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from core import review as rv
from core.scenes import plan_scenes, validate_scenes


def W(text, t0=0.0, step=0.4, p=0.9):
    return [{"word": w, "start": round(t0 + i * step, 3), "end": round(t0 + i * step + 0.3, 3), "probability": p}
            for i, w in enumerate(text.split())]


def test_flags_amounts_fragments_and_repeats():
    w = W("टिकट 35,000 से 4,000 रुपये है वहाँ पर द्वारिकाधीश दीश मंदिर में फिर बरकेश्वर पेश्वर और फिर दूर दूर से वह बनाया गया")
    sp = rv.review_spans(w)
    txt = {s["asr_text"]: s for s in sp}
    assert any("35,000" in t for t in txt) and all(s["priority"] == 1 for s in sp if "35,000" in s["asr_text"])
    assert txt["द्वारिकाधीश दीश"]["reasons"] == ["fragment"] and txt["द्वारिकाधीश दीश"]["priority"] == 2
    assert "बरकेश्वर पेश्वर" in txt
    assert txt["दूर दूर"]["priority"] == 3  # may be intentional Hindi reduplication
    assert not any("गया" in t for t in txt)  # auxiliary is not a stutter


def test_manual_phrase_and_csv_roundtrip(tmp_path):
    w = W("यह विश्वा प्रशित दमंदीर ढाई हजार साल पुराना है")
    m = rv.find_phrase(w, "विश्वा प्रशित दमंदीर")
    assert m and (m["first"], m["last"]) == (1, 3)
    spans = rv.merge_manual(rv.review_spans(w), [m], w)
    p = rv.write_review_csv(tmp_path / "r.csv", spans)
    assert p.read_bytes().startswith(b"\xef\xbb\xbf")  # BOM: Excel shows Devanagari
    rows = rv.read_review_csv(p)
    assert {r["asr_text"] for r in rows} >= {"विश्वा प्रशित दमंदीर"}
    assert all(r["action"] == "" and r["correct_text"] == "" for r in rows)


def test_apply_review_only_changes_human_rows():
    w = W("मंदिर द्वारिकाधीश दीश में 2,500,000 रुपये लगते")
    rows = [{"id": "R1", "first": "1", "last": "2", "asr_text": "द्वारिकाधीश दीश", "action": "fix",
             "correct_text": "द्वारकाधीश"},
            {"id": "R2", "first": "4", "last": "5", "asr_text": "2,500,000 रुपये", "action": "", "correct_text": ""}]
    r = rv.apply_review(w, rows)
    assert r["ok"]
    out = [x["word"] for x in r["words"]]
    assert out == ["मंदिर", "द्वारकाधीश", "में", "2,500,000", "रुपये", "लगते"]
    fixed = r["words"][1]
    assert fixed["start"] == w[1]["start"] and fixed["end"] == w[2]["end"] and fixed["reviewed"] == "R1"
    for a, b in zip(r["words"], r["words"][1:]):
        assert a["end"] <= b["start"] + 1e-6


def test_apply_review_guards():
    w = W("एक दो तीन चार")
    stale = [{"id": "R1", "first": "1", "last": "1", "asr_text": "पाँच", "action": "fix", "correct_text": "x"}]
    assert not rv.apply_review(w, stale)["ok"]
    empty = [{"id": "R1", "first": "1", "last": "1", "asr_text": "दो", "action": "fix", "correct_text": ""}]
    assert not rv.apply_review(w, empty)["ok"]
    overlap = [{"id": "R1", "first": "0", "last": "1", "asr_text": "एक दो", "action": "delete", "correct_text": ""},
               {"id": "R2", "first": "1", "last": "2", "asr_text": "दो तीन", "action": "fix", "correct_text": "x"}]
    assert not rv.apply_review(w, overlap)["ok"]
    dele = [{"id": "R1", "first": "1", "last": "1", "asr_text": "दो", "action": "delete", "correct_text": ""}]
    assert [x["word"] for x in rv.apply_review(w, dele)["words"]] == ["एक", "तीन", "चार"]


def test_scene_boundary_not_mid_phrase():
    # pause after "शुरुआत" but next word "से" continues the phrase -> must not split there
    words = W("आज हम यात्रा की एकदम शुरुआत", 0, 5.0) + W("से शुरू करते हैं। अब मंदिर चलते हैं।", 31.0, 2.0)
    plan = plan_scenes(words, 50.0, target_s=20.0, min_s=10.0, max_s=60.0)
    assert validate_scenes(plan, len(words)) == []
    for s in plan["scenes"][:-1]:
        nxt = words[s["last_word"] + 1]["word"]
        assert nxt != "से"


def test_review_timing_marked_not_faked():
    w = W("मंदिर द्वारिकाधीश दीश में")
    one = [{"id": "R1", "first": "1", "last": "2", "asr_text": "द्वारिकाधीश दीश", "action": "fix",
            "correct_text": "द्वारकाधीश"}]
    r = rv.apply_review(w, one)
    x = r["words"][1]
    assert "probability" not in x and x["text_status"] == "human_reviewed"
    assert x["timing_method"] == "interpolated_after_review" and x["timing_status"] == "unverified"
    assert r["timing_unverified"] == [{"id": "R1", "start": w[1]["start"], "end": w[2]["end"], "old_words": 2, "new_words": 1}]
    same = [{"id": "R1", "first": "1", "last": "2", "asr_text": "द्वारिकाधीश दीश", "action": "fix",
             "correct_text": "द्वारकाधीश जी"}]
    r2 = rv.apply_review(w, same)
    assert r2["timing_unverified"] == []
    assert r2["words"][2]["start"] == w[2]["start"] and r2["words"][2]["timing_method"] == "asr_after_review"


def test_scene_breaks_before_dosto_not_before_predicate():
    words = (W("आज हम यात्रा करेंगे और यहाँ नागेश्वर ज्योतिर्लिंग भी", 0, 3.0)
             + W("स्थापित है फिर हम चलेंगे", 28.0, 1.0) + W("दोस्तो अब मंदिर चलते हैं", 34.0, 1.0))
    plan = plan_scenes(words, 40.0, target_s=20.0, min_s=8.0, max_s=60.0)
    assert validate_scenes(plan, len(words)) == []
    starts = [words[s["first_word"]]["word"] for s in plan["scenes"]]
    assert "स्थापित" not in starts and "दोस्तो" in starts


def test_scene_never_ends_on_dangling_to_or_before_jo():
    words = (W("हम मंदिर देखेंगे और वहाँ की भव्यता में चार चाँद लगाते हैं,", 0, 4.0)
             + W("तो दोस्तों अब हम शिवराजपुर बीच, जो द्वारका से दूर है।", 44.0, 1.0)
             + W("वहाँ पानी साफ है।", 60.0, 1.0))
    plan = plan_scenes(words, 70.0, target_s=30.0, min_s=15.0, max_s=45.0)
    assert validate_scenes(plan, len(words)) == []
    for s in plan["scenes"][:-1]:
        last = words[s["last_word"]]["word"].strip(",।")
        nxt = words[s["last_word"] + 1]["word"]
        assert last != "तो" and nxt != "जो"
