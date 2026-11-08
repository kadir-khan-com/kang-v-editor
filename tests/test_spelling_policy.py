"""Per-video caption spelling policy is opt-in, logged, and never a global glossary rule."""
import json
from pathlib import Path

import pytest

from core.spelling_policy import apply_policy, load_policy
from core.words import apply_glossary, load_glossary

ROOT = Path(__file__).resolve().parent.parent
W = lambda s: [{"word": t, "start": i, "end": i + 1} for i, t in enumerate(s.split())]


def test_global_glossary_never_converts_between_valid_spellings():
    g = load_glossary(ROOT / "config" / "glossary.json")
    norm = lambda x: x.replace("द्वारिका", "द्वारका")
    assert not [(k, v) for k, v in g.items() if k != v and norm(k) == norm(v)]
    out, _ = apply_glossary(W("द्वारका द्वारिका द्वारकाधीश द्वारिकाधीश"), g)
    assert [w["word"] for w in out] == ["द्वारका", "द्वारिका", "द्वारकाधीश", "द्वारिकाधीश"]  # speaker spelling kept


def test_dwarika_policy_applies_only_when_passed():
    pol = load_policy(ROOT / "config" / "caption_spelling_policy.json")
    words = W("द्वारका का, द्वारकाधीश रुक्मिणी") + [{"word": "बेट द्वारका", "start": 9, "end": 10}]
    out, ch = apply_policy(words, pol)
    assert [w["word"] for w in out] == ["द्वारिका", "का,", "द्वारिकाधीश", "रुक्मिणी", "बेट द्वारिका"]
    assert len(out) == len(words) and [w["start"] for w in out] == [w["start"] for w in words]
    assert all(c["decided_by"] == "editorial-policy" for c in ch) and len(ch) == 3
    assert words[0]["word"] == "द्वारका"                                     # input untouched


def test_policy_keeps_punctuation_and_skips_substrings():
    pol = {"replace": {"द्वारका": "द्वारिका"}}
    out, _ = apply_policy(W("द्वारका। द्वारकापुरी"), pol)
    assert [w["word"] for w in out] == ["द्वारिका।", "द्वारकापुरी"]


def test_policy_that_breaks_never_rule_is_rejected(tmp_path):
    p = tmp_path / "bad.json"
    p.write_text(json.dumps({"replace": {"रुक्मिणी": "रुक्मणी"}, "never": {"रुक्मिणी": "रुक्मणी"}}, ensure_ascii=False), encoding="utf-8")
    with pytest.raises(ValueError):
        load_policy(p)


def test_fix_words_logs_policy_and_keeps_pre_policy_words(tmp_path, monkeypatch):
    from core import pipeline, runs
    monkeypatch.setenv("KANG_RUNS_DIR", str(tmp_path / "runs"))
    src = tmp_path / "w.json"
    src.write_text(json.dumps([{"word": "द्वारी", "start": 0, "end": 1}, {"word": "का", "start": 1, "end": 2}], ensure_ascii=False), encoding="utf-8")
    plain = pipeline.fix_words(str(src))
    assert [w["word"] for w in json.loads(Path(plain["words_json"]).read_text(encoding="utf-8"))] == ["द्वारका"]
    r = pipeline.fix_words(str(src), spelling_policy=str(ROOT / "config" / "caption_spelling_policy.json"))
    d = Path(r["dir"])
    assert [w["word"] for w in json.loads((d / "words.json").read_text(encoding="utf-8"))] == ["द्वारिका"]
    assert [w["word"] for w in json.loads((d / "words_pre_policy.json").read_text(encoding="utf-8"))] == ["द्वारका"]
    assert json.loads((d / "spelling_policy_changes.json").read_text(encoding="utf-8"))["changes"][0]["to"] == "द्वारिका"
