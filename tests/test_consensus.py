import copy
from core import consensus as cs


def W(text, t0=0.0):
    return [{"word": t, "start": t0 + i, "end": t0 + i + 0.8} for i, t in enumerate(text.split())]


def test_others_agree_beats_ours_and_patterns_group():
    ours = W("दोस्तो यहां नदी है और दोस्तो सुंदर है")
    timed = W("दोस्तों यहां नदी है और दोस्तों सुंदर है")
    text = "दोस्तों यहां नदी है और दोस्तों सुंदर है।"
    c = cs.consensus(ours, timed, text, [])
    rows = [r for r in c["rows"] if r["status"] == "others_agree"]
    assert len(rows) == 2 and all(r["suggestion"] == "दोस्तों" for r in rows)
    assert c["patterns"] and c["patterns"][0]["count"] == 2 and rows[0]["pattern"] == "P01"


def test_ours_majority_and_all_differ():
    ours = W("होटल कहा पर")
    c = cs.consensus(ours, W("होटल कहां पर"), "होटल कहा पर", [])
    assert c["rows"][0]["status"] == "ours_majority" and c["rows"][0]["priority"] == 3
    c = cs.consensus(W("होटल कहा पर"), W("होटल कहां पर"), "होटल यहां पर", [])
    assert c["rows"][0]["status"] == "all_differ" and c["rows"][0]["suggestion"] == ""


def test_name_hint_only_suggests():
    ours = W("फिर भेड़ द्वारिका जाएंगे")
    c = cs.consensus(ours, None, None, [{"suggest": "बेट द्वारका", "heard": ["भेड़ द्वारिका"]}])
    n = [r for r in c["rows"] if r["status"] == "name_hint"]
    assert n and n[0]["suggestion"] == "बेट द्वारका" and n[0]["first"] == 1 and n[0]["last"] == 2


def test_timed_windows_keep_hints_local():
    ours = W(" ".join(["राम"] * 40) + " बेट", 0.0)
    timed = W(" ".join(["राम"] * 40) + " भेट", 0.0)
    c = cs.consensus(ours, timed, None, [])
    assert len(c["rows"]) == 1 and c["rows"][0]["first"] == 40


def test_words_never_modified_and_review_annotation():
    ours = W("होटल कहा पर")
    before = copy.deepcopy(ours)
    c = cs.consensus(ours, W("होटल कहां पर"), "होटल कहाँ पर", [])
    assert ours == before
    rows = cs.annotate_review([{"id": "R1", "first": "1", "last": "1"}, {"id": "R2", "first": "0", "last": "0"}], c)
    assert rows[0]["consensus_status"] == "others_agree" and rows[0]["consensus_hint_PART"] == "कहा -> कहां"
    assert rows[1]["consensus_status"] == "all_agree"


def test_script_rows_are_low_priority():
    c = cs.consensus(W("railway station"), W("रेलवे स्टेशन"), "रेलवे स्टेशन", [])
    assert all(r["priority"] == 3 for r in c["rows"])


from core import hindi_numbers as hn


def test_hindi_number_values():
    assert hn.canon_numbers("एक सौ पैंतीस किलोमीटर".split()) == ["#135", "किलोमीटर"]
    assert hn.canon_numbers("पैंतीस सौ से चार हजार".split()) == ["#3500", "से", "#4000"]
    assert hn.canon_numbers("दो हजार से ढाई हजार".split()) == ["#2000", "से", "#2500"]
    assert hn.canon_numbers(["2,500,000"]) == ["#2500000"]
    assert hn.canon_numbers("साढ़े छह बजे".split()) == ["#6.5", "बजे"]


def test_digits_words_script_units_are_format_only():
    c = cs.consensus(W("स्टेशन 2 km दूर"), W("स्टेशन दो किलोमीटर दूर"), "स्टेशन 2 किलोमीटर दूर", [])
    assert all(r["status"] == "format_only" for r in c["rows"])
    c = cs.consensus(W("होटल train से"), W("होटल ट्रेन से"), "होटल train से", [])
    assert c["rows"] == [] or all(r["status"] == "format_only" for r in c["rows"])


def test_amount_value_mismatch_is_priority_zero():
    ours = W("ऑटो 2,500,000 रुपये का चार्ज")
    c = cs.consensus(ours, W("ऑटो दो हजार से ढाई हजार रुपये का चार्ज"), "ऑटो 2000 से 2500 रुपए का चार्ज", [])
    top = c["rows"][0]
    assert top["priority"] == 0 and top["kind"] == "amount" and top["status"] == "others_agree"


def test_timed_hint_does_not_spill_into_next_word():
    ours = W("वेल कनेक्टेड द्वारका का रेलवे स्टेशन")
    timed = [{"word": "वेल", "start": 0, "end": .8}, {"word": "कनेक्टेड", "start": 1, "end": 1.8},
             {"word": "द्वारिका", "start": 2.2, "end": 3.6}, {"word": "रेलवे", "start": 4, "end": 4.8},
             {"word": "स्टेशन", "start": 5, "end": 5.8}]
    c = cs.consensus(ours, timed, None, [])
    assert len(c["rows"]) == 1 and c["rows"][0]["ours"] == "द्वारका का" and c["rows"][0]["nemotron"] == "द्वारिका"


def test_full_span_keeps_rest_of_row_and_digits_for_amounts():
    ours = W("वही टैक्सी वाले 35,000 से 4,000 रुपये का चार्ज")
    c = cs.consensus(ours, W("वही टैक्सी वाले पैंतीस सौ से चार हजार रुपये का चार्ज"), "वही टैक्सी वाले 3500 से 4000 रुपए का चार्ज", [])
    row = cs.annotate_review([{"id": "R038", "first": "3", "last": "6"}], c, ours)[0]
    assert row["consensus_hint_PART"] == "35,000 -> पैंतीस सौ"
    assert row["consensus_full_span_UNVERIFIED"] == "3500 से 4000 रुपये"


def test_full_span_blank_when_part_needs_listen():
    ours = W("होटल कहा पर")
    c = cs.consensus(ours, W("होटल कहां पर"), "होटल यहां पर", [])
    row = cs.annotate_review([{"id": "R1", "first": "0", "last": "2"}], c, ours)[0]
    assert row["consensus_full_span_UNVERIFIED"] == "" and row["consensus_note"].startswith("needs_listen")


def test_patterns_never_group_proper_names():
    ours = W("भेट द्वारिका और भेट द्वारिका")
    other = W("बेट द्वारका और बेट द्वारका")
    names = [{"suggest": "बेट द्वारका", "heard": ["भेट द्वारिका"]}]
    c = cs.consensus(ours, other, "बेट द्वारका और बेट द्वारका", names)
    assert c["patterns"] == []


def test_apply_review_refuses_pasted_partial_hint():
    from core import review as rv
    ours = W("वही 35,000 से 4,000 रुपये")
    row = {"id": "R038", "first": "1", "last": "4", "asr_text": "35,000 से 4,000 रुपये", "action": "fix",
           "correct_text": "पैंतीस सौ", "consensus_hint_PART": "35,000 -> पैंतीस सौ"}
    r = rv.apply_review(ours, [row])
    assert not r["ok"] and "partial hint" in r["problems"][0]
    row["correct_text"] = "3500 से 4000 रुपये"
    assert rv.apply_review(ours, [row])["ok"]


def test_full_span_keeps_number_words_when_row_had_no_digits():
    ours = W("सुबह साथ बजे से एक बजे तक")
    c = cs.consensus(ours, W("सुबह सात बजे से एक बजे तक"), "सुबह 7 बजे से 1 बजे तक", [])
    row = cs.annotate_review([{"id": "R045", "first": "1", "last": "5"}], c, ours)[0]
    assert row["consensus_full_span_UNVERIFIED"] == "सात बजे से एक बजे"


def test_protected_name_rukmini_never_bulk_pattern():
    ours = W("रुक्मिणी जी और रुक्मिणी मंदिर")
    c = cs.consensus(ours, W("रुक्मणी जी और रुक्मणी मंदिर"), "रुक्मणी जी और रुक्मणी मंदिर", [])
    assert c["patterns"] == []


def test_apply_review_rejects_stale_span():
    from core import review as rv
    r = rv.apply_review(W("वही 3500 से 4000 रुपये"), [{"id": "R038", "first": "1", "last": "4",
        "asr_text": "35,000 से 4,000 रुपये", "action": "fix", "correct_text": "3500 से 4000 रुपये"}])
    assert not r["ok"] and "changed since" in r["problems"][0]


def test_apply_review_allows_shorter_duplicate_removal():
    from core import review as rv
    r = rv.apply_review(W("भगवान विराजमान विराजमान हैं"), [{"id": "R031", "first": "1", "last": "2",
        "asr_text": "विराजमान विराजमान", "action": "fix", "correct_text": "विराजमान", "consensus_hint_PART": ""}])
    assert r["ok"] and [w["word"] for w in r["words"]] == ["भगवान", "विराजमान", "हैं"]


def test_auto_extraction_source_is_draft_never_accepted(tmp_path):
    import csv, json
    from core import pipeline
    from core.runs import Run
    wp = tmp_path / "w.json"
    wp.write_text(json.dumps(W("सुबह साथ बजे")), encoding="utf-8")
    cp = tmp_path / "r.csv"
    with cp.open("w", encoding="utf-8", newline="") as fh:
        wr = csv.DictWriter(fh, ["id", "priority", "first", "last", "asr_text", "action", "correct_text"])
        wr.writeheader(); wr.writerow({"id": "C006", "priority": "0", "first": "1", "last": "1", "asr_text": "साथ",
                                       "action": "fix", "correct_text": "सात"})
    (tmp_path / "runs").mkdir()
    r = pipeline.apply_transcript_review(str(wp), str(cp), run=Run(root=tmp_path / "runs"), approver=lambda *a, **k: True,
                                         source="auto-extraction")
    assert r["ok"] and not r["transcript_accepted"] and r["status"] == "draft_corrected_not_accepted"
    out = json.loads(open(r["words"], encoding="utf-8").read())
    assert out[1]["word"] == "सात" and out[1]["text_status"] == "auto_extraction_recommended"


def test_decided_by_per_row_and_policy_rows_keep_draft():
    from core import review as rv
    ours = W("द्वारका में साथ बजे")
    rows = [{"id": "N1", "first": "0", "last": "0", "asr_text": "द्वारका", "action": "fix", "correct_text": "द्वारिका",
             "decided_by": "editorial-policy", "content_review": "pending"},
            {"id": "N2", "first": "2", "last": "2", "asr_text": "साथ", "action": "fix", "correct_text": "सात",
             "decided_by": "listened"}]
    r = rv.apply_review(ours, rows)
    assert r["ok"]
    assert r["words"][0]["text_status"] == "editorial_policy" and r["words"][0]["content_review_pending"]
    assert r["words"][2]["text_status"] == "human_reviewed"
    rows[1]["decided_by"] = "guess"
    assert not rv.apply_review(ours, rows)["ok"]
