import csv
import json

import pytest

from core.hinglish import DictBackend
from core.hinglish_review import (apply_block, apply_hinglish_review, hinglish_layer_run, make_blocks, read_rows,
                                  spelling_issues, write_rows)
from core.runs import Run

MAP = {"यह": "yah", "मंदिर": "mandir", "है": "hai", "दोस्तों": "doston", "प्रशित": "prashit", "दमंदीर": "damandir",
       "बहुत": "bahut", "पुराना": "purana"}
TABLE = {"version": "t", "decided_by": "test", "phrases": {}, "names": {"द्वारिका": "Dwarka", "कृष्ण": "Krishna"},
         "words": {}, "suspect": {"words": ["दमंदीर"]}}


def _w(words, t0=0.0, step=0.5):
    return [{"word": w, "start": round(t0 + i * step, 3), "end": round(t0 + i * step + 0.4, 3), "probability": 0.9}
            for i, w in enumerate(words)]


@pytest.fixture
def layer(tmp_path):
    wp = tmp_path / "words.json"
    words = _w(["दोस्तों", "यह", "प्रशित", "दमंदीर", "है।", "द्वारिका", "बहुत", "पुराना", "है।"], step=1.0)
    wp.write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
    tp = tmp_path / "t.json"
    tp.write_text(json.dumps(TABLE, ensure_ascii=False), encoding="utf-8")
    runs = tmp_path / "runs"
    runs.mkdir()
    r = hinglish_layer_run(str(wp), backend=DictBackend(MAP), table_path=str(tp), block_s=5.0, clips=False,
                           run=Run(root=runs))
    return r, wp, words


def test_layer_schema_and_master_untouched(layer):
    r, wp, words = layer
    doc = json.loads(open(r["files"]["layer"], encoding="utf-8").read())
    assert doc["schema"] == "kang.hinglish_words/1" and doc["status"] == "draft"
    e = doc["words"][5]
    assert e["hindi"] == "द्वारिका" and e["hinglish"] == "Dwarka" and e["word_id"] == 5
    assert e["timing_method"] == "inherited_from_hindi" and e["timing_status"] == "verified_pending"
    assert e["start"] == words[5]["start"] and e["source_words_sha256"] == doc["source_words_sha256"]
    assert json.loads(wp.read_text(encoding="utf-8")) == words
    assert r["accepted"] is False and r["blocks"] >= 2
    for k in ("srt_hinglish", "srt_hindi", "review_csv", "review_html"):
        assert open(r["files"][k], encoding="utf-8").read()


def _fill(path, decisions):
    rows = read_rows(path)
    for row in rows:
        d = decisions.get(row["block"], {})
        row.update(d)
    with open(path, encoding="utf-8-sig") as f:
        fields = next(csv.reader(f))
    write_rows(path, rows, fields)


def test_apply_refuses_undecided_and_bad_decider(layer):
    r, _, _ = layer
    res = apply_hinglish_review(r["files"]["layer"], r["files"]["review_csv"])
    assert not res["ok"] and "without a decision" in res["problems"][0]
    _fill(r["files"]["review_csv"], {"H001": {"action": "ok", "decided_by": "agent"}})
    res = apply_hinglish_review(r["files"]["layer"], r["files"]["review_csv"], allow_partial=True)
    assert not res["ok"] and "decided_by" in res["problems"][0]


def test_apply_accept_spelling_keeps_timing_merge_unverified(layer):
    r, _, words = layer
    rows = read_rows(r["files"]["review_csv"])
    blk1 = rows[0]
    assert "prashit damandir" in blk1["hinglish"]
    fixed = blk1["hinglish"].replace("prashit damandir", "prasiddh-mandir").replace("doston", "Doston")
    dec = {row["block"]: {"action": "ok", "decided_by": "listened"} for row in rows}
    dec["H001"] = {"action": "fix", "corrected_hinglish": fixed, "decided_by": "listened"}
    _fill(r["files"]["review_csv"], dec)
    res = apply_hinglish_review(r["files"]["layer"], r["files"]["review_csv"])
    assert res["ok"] and res["accepted"] and res["status"] == "PASS"
    out = json.loads(open(res["files"]["layer"], encoding="utf-8").read())
    assert out["status"] == "accepted_text"
    ws = out["words"]
    assert ws[0]["hinglish"] == "Doston" and ws[0]["start"] == words[0]["start"]  # case only -> timing kept
    m = next(w for w in ws if w["hinglish"] == "prasiddh-mandir")
    assert m["timing_status"] == "unverified" and m["timing_method"] == "merged_after_review"
    assert m["start"] == words[2]["start"] and m["end"] == words[3]["end"] and m["from_word_ids"] == [2, 3]
    assert res["words_out"] == res["words_in"] - 1
    assert open(res["files"]["srt"], encoding="utf-8").read().count("prasiddh-mandir") == 1


def test_apply_detects_changed_layer(layer):
    r, _, _ = layer
    rows = read_rows(r["files"]["review_csv"])
    rows[0]["hinglish"] = "something else"
    for row in rows:
        row.update({"action": "ok", "decided_by": "read"})
    write_rows(r["files"]["review_csv"], rows, list(rows[0].keys()))
    res = apply_hinglish_review(r["files"]["layer"], r["files"]["review_csv"])
    assert not res["ok"] and "changed" in res["problems"][0]


def test_apply_block_split_and_insert():
    blk = [{"word_id": 0, "hindi": "क", "hinglish": "bahuthi", "start": 1.0, "end": 2.0, "timing_method": "inherited_from_hindi",
            "timing_status": "verified_pending", "source_words_sha256": "x"}]
    out = apply_block(blk, "bahut hi", 0.0, 3.0, "H1")
    assert [w["hinglish"] for w in out] == ["bahut", "hi"]
    assert out[0]["start"] == 1.0 and out[1]["end"] == 2.0 and all(w["timing_status"] == "unverified" for w in out)


def test_spelling_issues():
    ents = [{"word_id": i, "hinglish": t} for i, t in enumerate(["dwarika", "Dwarka", "matra", "krishna", "dwar"])]
    sp = spelling_issues(ents, ["Dwarka", "Krishna", "Mathura", "Dwar"])
    assert set(sp) == {0, 3}


def test_make_blocks_cover_all():
    ents = [{"word_id": i, "hinglish": "a.", "start": i * 1.0, "end": i * 1.0 + 0.5} for i in range(40)]
    bl = make_blocks(ents, 6.0)
    assert sum(len(b) for b in bl) == 40 and all((b[-1]["end"] - b[0]["start"]) <= 9.5 for b in bl)


def test_apply_out_and_acceptance_file(layer, tmp_path):
    r, _, _ = layer
    rows = read_rows(r["files"]["review_csv"])
    for row in rows:
        row.update({"action": "ok", "decided_by": "listened"})
    write_rows(r["files"]["review_csv"], rows, list(rows[0].keys()))
    out = tmp_path / "words_hinglish_v1_accepted.json"
    res = apply_hinglish_review(r["files"]["layer"], r["files"]["review_csv"], out=str(out))
    assert res["accepted"] and out.exists()
    acc = json.loads(open(res["files"]["acceptance"], encoding="utf-8").read())
    assert acc["accepted"] and acc["timing_verified"] is False and acc["decided_by"] == {"listened": len(rows)}


def test_bulk_ok_csv_keeps_original_and_user_rows(tmp_path):
    import csv
    from core.hinglish_review import BLOCK_FIELDS, bulk_ok_csv, read_rows
    src = tmp_path / "r.csv"
    with open(src, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=BLOCK_FIELDS)
        w.writeheader()
        w.writerow({"block": "H001", "words": "0-1", "hinglish": "a b"})
        w.writerow({"block": "H002", "words": "2-2", "hinglish": "c", "action": "fix", "corrected_hinglish": "C",
                    "decided_by": "listened"})
    out = bulk_ok_csv(str(src), "user chat 2026-11-01 21:12: proceed")
    rows = read_rows(out)
    assert rows[0]["action"] == "ok" and rows[0]["decided_by"] == "user_bulk" and "proceed" in rows[0]["note"]
    assert rows[1]["action"] == "fix" and rows[1]["decided_by"] == "listened"
    assert read_rows(src)[0]["action"] == ""
    import pytest
    with pytest.raises(ValueError):
        bulk_ok_csv(str(src), "  ")
