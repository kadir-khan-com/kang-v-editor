from core.voter import load_wordlist, spelling_vote, split_core

VOCAB = {"ज्योतिर्लिंग", "किलोमीटर", "मंदिर", "द्वारका", "है"}


def W(word, s, e):
    return {"word": word, "start": s, "end": e}


def test_fixes_oov_word_from_alt_at_same_time():
    base = [W("ज्योतिरलिंग,", 1.0, 1.6), W("है", 1.6, 1.8)]
    alt = {"vaani": [W("ज्योतिर्लिंग", 1.05, 1.62)]}
    out, ch = spelling_vote(base, alt, VOCAB)
    assert out[0]["word"] == "ज्योतिर्लिंग,"  # punctuation kept
    assert out[0]["start"] == 1.0 and out[1]["word"] == "है"
    assert ch[0]["by"] == ["vaani"]


def test_never_adds_or_drops_words():
    base = [W("द्वारका", 0, 0.5)]
    alt = {"vaani": [W("द्वारका", 0, 0.5), W("मंदिर", 0.5, 1.0)]}
    out, ch = spelling_vote(base, alt, VOCAB)
    assert [w["word"] for w in out] == ["द्वारका"] and ch == []


def test_keeps_in_vocab_numbers_and_inflections():
    base = [W("मंदिरों", 0, 0.5), W("12", 0.5, 0.8), W("किलोमिटर", 0.8, 1.3)]
    alt = {"vaani": [W("मंदिर", 0, 0.5), W("बारह", 0.5, 0.8), W("किलोमीटर", 2.0, 2.5)]}
    out, ch = spelling_vote(base, alt, VOCAB)
    # inflection not trimmed, number untouched, no time overlap -> no change
    assert [w["word"] for w in out] == ["मंदिरों", "12", "किलोमिटर"] and ch == []


def test_dissimilar_alt_is_ignored():
    out, ch = spelling_vote([W("गोपी", 0, 0.5)], {"a": [W("मंदिर", 0, 0.5)]}, VOCAB)
    assert ch == []


def test_require_agree_needs_both_models():
    base = [W("किलोमिटर", 0, 0.5)]
    one = {"a": [W("किलोमीटर", 0, 0.5)], "b": [W("किलोमिटर", 0, 0.5)]}
    assert spelling_vote(base, one, VOCAB, require_agree=True)[1] == []
    both = {"a": [W("किलोमीटर", 0, 0.5)], "b": [W("किलोमीटर", 0.02, 0.5)]}
    out, ch = spelling_vote(base, both, VOCAB, require_agree=True)
    assert out[0]["word"] == "किलोमीटर" and ch[0]["by"] == ["a", "b"]


def test_wordlist_loader(tmp_path):
    p = tmp_path / "hi.dic"
    p.write_text("3\nमंदिर/12\nहै\n", encoding="utf-8")
    v = load_wordlist(p, extra=["द्वारकाधीश मंदिर,"])
    assert {"मंदिर", "है", "द्वारकाधीश"} <= v and "3" not in v
    assert split_core("«मंदिर»,") == ("«", "मंदिर", "»,")


def test_engine_passes_repair_opts_and_seed(monkeypatch):
    import sys, types
    from core import engine
    calls = {}
    fake_ct2 = types.SimpleNamespace(set_random_seed=lambda s: calls.setdefault("seed", s))
    monkeypatch.setitem(sys.modules, "ctranslate2", fake_ct2)

    class M:
        def transcribe(self, audio, **kw):
            calls["kw"] = kw
            return iter([]), None

    monkeypatch.setattr(engine, "SEED", 7)
    engine.transcribe([0.0], model=M(), extra_opts={"hotwords": "द्वारका"})
    assert calls["seed"] == 7 and calls["kw"]["hotwords"] == "द्वारका"
    assert calls["kw"]["condition_on_previous_text"] is False
    engine.transcribe([0.0], model=M())
    assert "hotwords" not in calls["kw"]


def test_danda_phrase_compound_and_nasal_guards():
    v = VOCAB | {"द्वारिका", "धाम", "यहां", "दूँगा"}
    base = [W("द्वारका।", 0, 0.5), W("बेट द्वारका", 0.5, 1.0), W("पावनधाम", 1.0, 1.5), W("यहाँ", 1.5, 2.0)]
    alt = {"a": [W("द्वारिका", 0, 0.5), W("द्वारिका", 0.5, 1.0), W("धाम", 1.0, 1.5), W("यहां", 1.5, 2.0)]}
    out, ch = spelling_vote(base, alt, v | {"द्वारका"})
    assert ch == []  # द्वारका in vocab once the danda is split off; phrase, compound half, nasal variant kept
    out, ch = spelling_vote([W("दूंगा।", 0, 0.5)], {"a": [W("दूँगा", 0, 0.5)]}, v)
    assert ch == []  # nasal variant
    assert split_core("द्वारका।") == ("", "द्वारका", "।")


def test_pipeline_voter_stage_offline(tmp_path, monkeypatch):
    """Voter on: spelling borrowed from 2 agreeing second models, word count/timing untouched."""
    import json, wave
    import numpy as np
    from core import pipeline
    from core.runs import Run
    sr = 16000
    t = np.arange(int(sr * 2.0)) / sr
    sig = (0.3 * np.sin(2 * np.pi * 220 * t) * 32767).astype("<i2")
    wav = tmp_path / "a.wav"
    with wave.open(str(wav), "wb") as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(sr); f.writeframes(sig.tobytes())
    words = [("नमस्ते", 0.0, 0.5), ("दोपर", 0.5, 1.0), ("में", 1.0, 1.4), ("आए", 1.4, 1.9)]
    row = lambda ws: [{"start": ws[0][1], "end": ws[-1][2], "text": " ".join(w for w, _, _ in ws),
                       "words": [{"w": w, "start": a, "end": b, "p": 0.9} for w, a, b in ws]}]
    base = lambda s: row(words)
    alt = lambda s: row([("दोपहर", 0.5, 1.0)])
    dic = tmp_path / "hi.dic"
    dic.write_text("2\nदोपहर\nनमस्ते\n", encoding="utf-8")
    from pathlib import Path
    runs_dir = tmp_path / "runs"
    runs_dir.mkdir()
    monkeypatch.setattr(pipeline, "find_speech_gaps", lambda *a, **k: [])
    monkeypatch.setattr(pipeline, "repair_suspect_spans", lambda w, *a, **k: (w, []))
    r = pipeline.transcribe_to_words(str(wav), run=Run(root=runs_dir), transcriber=base,
                                     voters={"a": alt, "b": alt}, wordlist=str(dic))
    out = json.loads((Path(r["dir"]) / "words.json").read_text(encoding="utf-8"))
    assert [w["word"] for w in out][1] == "दोपहर" and len(out) == 4
    assert r["vote_changes"][0]["from"] == "दोपर"
    r2 = pipeline.transcribe_to_words(str(wav), run=Run(root=runs_dir), transcriber=base)
    assert r2["vote_changes"] is None  # default off


def test_default_voters_from_config(tmp_path, monkeypatch):
    from core import pipeline
    d = tmp_path / "v"
    for n in ("vaani", "indic"):
        (d / n).mkdir(parents=True); (d / n / "model.bin").write_bytes(b"x")
    monkeypatch.setenv("KANG_VOTER_DIR", str(d))
    monkeypatch.delenv("ENGINE_WORDLIST", raising=False)
    found, wl = pipeline._default_voters()
    assert set(found) == {"vaani", "indic"} and wl.endswith("hi_IN.dic")
    monkeypatch.setenv("KANG_VOTER_DIR", str(tmp_path / "none"))
    assert pipeline._default_voters()[0] == {}
