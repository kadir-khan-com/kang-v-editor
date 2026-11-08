import json

from core.hinglish import (DictBackend, build_hinglish_srt, diff_hints, load_table, mark_pending_spans,
                           phon_key, romanize_words, run_hinglish, skeleton, split_token)

TABLE = {"version": "t", "decided_by": "test",
         "phrases": {"बेट द्वारिका": "Bet Dwarka"},
         "names": {"द्वारिका": "Dwarka", "कृष्ण": "Krishna"},
         "words": {"मे": "mein"},
         "suspect": {"words": ["दमंदीर"]}}
MAP = {"हेलो": "hello", "दोस्तों": "doston", "चलेंगे": "chalenge", "है": "hai", "यह": "yah", "मंदिर": "mandir",
       "श्री": "shri"}


def _w(words, t0=0.0, step=0.5):
    return [{"word": w, "start": round(t0 + i * step, 3), "end": round(t0 + i * step + 0.4, 3), "probability": 0.9}
            for i, w in enumerate(words)]


def _table(tmp_path):
    p = tmp_path / "t.json"
    p.write_text(json.dumps(TABLE, ensure_ascii=False), encoding="utf-8")
    return load_table(p)


def test_split_token_danda_and_punct():
    assert split_token("द्वारिका।") == ("", "द्वारिका", ".")
    assert split_token("(हेलो,") == ("(", "हेलो", ",")


def test_romanize_keeps_timings_and_sources(tmp_path):
    words = _w(["हेलो", "दोस्तों,", "चलेंगे", "बेट", "द्वारिका।", "मे", "km", "दमंदीर", "अज्ञात"])
    rw = romanize_words(words, DictBackend(MAP), _table(tmp_path))
    assert [w["start"] for w in rw] == [w["start"] for w in words]
    assert [w["end"] for w in rw] == [w["end"] for w in words]
    assert [w["devanagari"] for w in rw] == [w["word"] for w in words]  # master text carried, not changed
    got = {w["devanagari"]: (w["roman"], w["roman_source"]) for w in rw}
    assert got["दोस्तों,"] == ("doston,", "xlit_map")
    assert got["बेट"] == ("Bet", "phrase") and got["द्वारिका।"] == ("Dwarka.", "phrase")
    assert got["मे"] == ("mein", "word_fix")
    assert got["km"] == ("km", "passthrough")
    unk = next(w for w in rw if w["devanagari"] == "अज्ञात")
    assert unk["roman_source"] == "xlit_model" and unk["needs_review"] and "model_guess" in unk["review_reasons"]
    sus = next(w for w in rw if w["devanagari"] == "दमंदीर")
    assert "suspect_asr_word" in sus["review_reasons"]
    assert not next(w for w in rw if w["devanagari"] == "हेलो")["needs_review"]


def test_multiword_token_and_name(tmp_path):
    rw = romanize_words(_w(["श्री कृष्ण", "द्वारिका"]), DictBackend(MAP), _table(tmp_path))
    assert rw[0]["roman"] == "shri Krishna" and rw[1]["roman"] == "Dwarka"


def test_pending_spans_by_time():
    words = _w(["हेलो", "दोस्तों", "चलेंगे"])
    rows = [{"action": "", "start": "0.45", "end": "0.95", "first": "99", "last": "99"},
            {"action": "fix", "start": "0", "end": "2"}]
    out = mark_pending_spans(words, rows)
    assert [bool(w.get("pending_listen")) for w in out] == [False, True, False]
    assert "pending_listen" not in words[1]  # input untouched


def test_srt_capitalizes_and_keeps_times(tmp_path):
    rw = romanize_words(_w(["हेलो", "दोस्तों।", "यह", "मंदिर", "है"]), DictBackend(MAP), _table(tmp_path))
    srt, ev = build_hinglish_srt(rw)
    assert ev[0]["text"].startswith("Hello") and ev[0]["start"] == 0.0
    assert any(e["text"].startswith("Yah") for e in ev)  # new sentence after danda
    assert "-->" in srt


def test_skeleton_spelling_noise():
    assert skeleton("Krishna") == skeleton("krshn")
    assert skeleton("Dwarka") == skeleton("dvaari ka")
    assert skeleton("liye") == skeleton("lie")
    assert skeleton("sunset") != skeleton("sansad")
    assert skeleton("snan") != skeleton("sthaan")
    assert phon_key("Dosto") == phon_key("dosto")


def test_diff_hints_only_real_differences(tmp_path):
    rw = romanize_words(_w(["यह", "मंदिर", "है"]), DictBackend(MAP), _table(tmp_path))
    chunks = [{"start": 0.0, "end": 2.0, "text": "Yah mandir hain"}]
    assert diff_hints(rw, chunks) == []  # hai/hain = nasal noise
    chunks = [{"start": 0.0, "end": 2.0, "text": "Yah sansad hai"}]
    h = diff_hints(rw, chunks)
    assert len(h) == 1 and h[0]["ours"] == "mandir" and h[0]["other_asr"] == "sansad"


def test_run_hinglish_writes_new_files_only(tmp_path):
    wp = tmp_path / "words.json"
    words = _w(["हेलो", "दोस्तों", "यह", "मंदिर", "है"])
    wp.write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
    before = wp.read_bytes()
    tp = tmp_path / "t.json"
    tp.write_text(json.dumps(TABLE, ensure_ascii=False), encoding="utf-8")
    other = tmp_path / "o.json"
    other.write_text(json.dumps({"model": "x", "chunks": [{"start": 0, "end": 3, "text": "hello doston yah mandir hai"}]}),
                     encoding="utf-8")
    rep = run_hinglish(wp, tmp_path / "out" / "h", backend=DictBackend(MAP), table_path=tp, other_asr=str(other))
    assert rep["status"] == "WARN" and rep["stats"]["words"] == 5
    assert rep["vs_other"]["mean_agreement"] == 1.0 and rep["vs_other"]["word_diff_hints"] == 0
    for k in ("words", "srt", "review", "report", "text", "vs_other", "diff_hints"):
        assert (tmp_path / "out").joinpath(rep["files"][k].split("/")[-1]).exists()
    assert wp.read_bytes() == before  # master untouched
    srt = (tmp_path / "out" / "h.srt").read_text(encoding="utf-8")
    assert "Hello doston" in srt


def test_repo_table_loads():
    t = load_table("config/hinglish_names.json")
    assert t["names"]["द्वारिका"] and t["phrases"]["बेट द्वारिका"]
    assert "दीश" in t["suspect"] and "दीश" not in t["words"]  # ASR errors are flagged, never hidden
