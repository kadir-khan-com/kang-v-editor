"""Fixes from the 2026-10-29 external code review (API cut default, approvals, pip shell bug, coverage, overlap)."""
import inspect
import json
from pathlib import Path

import numpy as np

from core import gapfill, pipeline
from core.runs import Run

ROOT = Path(__file__).resolve().parent.parent


def test_api_cut_default_off():
    src = (ROOT / "app.py").read_text(encoding="utf-8")
    assert "cut: bool = Form(False)" in src


def test_setup_pip_uses_arg_list_not_shell():
    src = (ROOT / "setup_kaggle.py").read_text(encoding="utf-8")
    assert '[sys.executable, "-m", "pip", "install", "-q", *packages]' in src
    assert "shell=isinstance(cmd, str)" in src
    assert "KANG_INPUT_AUDIO" in src


def test_coverage_threshold_is_2s_and_blocking_3s():
    assert gapfill.COVERAGE_GAP_S == 2.0 and gapfill.BLOCKING_GAP_S == 3.0
    assert inspect.signature(gapfill.find_speech_gaps).parameters["min_gap"].default == 2.0


def test_find_speech_gaps_sees_2_5s_voiced_gap():
    sr = gapfill.SR
    t = np.arange(int(6 * sr)) / sr
    samples = (0.3 * np.sin(2 * np.pi * 220 * t)).astype("float32")  # 'voiced' throughout
    words = [{"word": "a", "start": 0.0, "end": 1.0}, {"word": "b", "start": 3.5, "end": 6.0}]
    gaps = gapfill.find_speech_gaps(words, samples)
    assert [(g["start"], g["end"]) for g in gaps] == [(1.0, 3.5)]


def test_no_overlap_close_starts_never_overlap_and_keep_text():
    ws = [{"word": "पहला", "start": 1.00, "end": 1.30}, {"word": "दूसरा", "start": 1.02, "end": 1.40},
          {"word": "तीसरा", "start": 1.40, "end": 1.80}]
    out = gapfill.no_overlap(ws)
    for a, b in zip(out, out[1:]):
        assert a["end"] <= b["start"]
    assert " ".join(w["word"] for w in out).split() == ["पहला", "दूसरा", "तीसरा"]  # nothing dropped
    assert out[0].get("timing_squeezed")


def test_no_overlap_equal_starts_merge_text_not_drop():
    ws = [{"word": "क", "start": 0.0, "end": 0.5}, {"word": "ख", "start": 1.0, "end": 1.2},
          {"word": "ग", "start": 1.0, "end": 1.5}]
    out = gapfill.no_overlap(ws)
    assert all(w["end"] > w["start"] for w in out)
    assert " ".join(w["word"] for w in out).split() == ["क", "ख", "ग"]
    for a, b in zip(out, out[1:]):
        assert a["end"] <= b["start"]


def test_gate_records_hash_bound_approval():
    run = Run()

    def auto(g, i):
        return True
    auto.approver_name = "auto(--yes)"
    assert pipeline._gate(run, "cut_list", "plan A", auto)
    recs = json.loads(run.path("approvals.json").read_text(encoding="utf-8"))
    assert recs[-1]["approver"] == "auto(--yes)" and recs[-1]["plan_hash"] == pipeline.plan_hash("plan A")
    assert run.approval_valid("cut_list", pipeline.plan_hash("plan A"))
    assert not run.approval_valid("cut_list", pipeline.plan_hash("plan B"))  # changed plan = not approved
    assert run.manifest["approvals"]["cut_list"] == "approved"                  # old contract kept


# ---- third review (2026-10-29 20:00) -------------------------------------------------------
def _fake(samples):
    ws = [("नमस्ते", 0.5, 1.6), ("द्वारी", 2.5, 3.0), ("का", 3.0, 3.5), ("दोस्तों।", 4.25, 5.0)]
    return [{"start": 0.5, "end": 5.0, "text": " ".join(w for w, _, _ in ws),
             "words": [{"w": w, "start": s, "end": e, "p": 0.9} for w, s, e in ws]}]


def test_standalone_transcript_srt_matches_final_words(media, monkeypatch):
    monkeypatch.setenv("ENGINE_VOTE", "0")
    r = pipeline.transcribe_to_words(str(media / "speech.wav"), transcriber=_fake)
    d = Path(r["dir"])
    final_words = [w["word"] for w in json.loads((d / "words.json").read_text(encoding="utf-8"))]
    rows = json.loads((d / "transcript.json").read_text(encoding="utf-8"))
    assert [w["w"] for row in rows for w in row["words"]] == final_words
    srt = (d / "transcript.srt").read_text(encoding="utf-8")
    assert "द्वारका" in srt and "द्वारी" not in srt                 # glossary reached the SRT
    assert "द्वारी" in (d / "raw" / "transcript.srt").read_text(encoding="utf-8")  # raw layer kept


def test_api_reports_review_and_acceptance_separately(media, tmp_path, monkeypatch):
    monkeypatch.setenv("ENGINE_VOTE", "0")
    r = pipeline.api_transcribe(str(media / "speech.wav"), str(tmp_path / "o"), transcriber=_fake)
    assert r["processing_complete"] is True and r["accepted"] is False
    assert "review_required" in r and isinstance(r["warnings"], list)
    src = (ROOT / "app.py").read_text(encoding="utf-8")
    assert '"review_required": job.get("review_required")' in src


def test_plan_hash_changes_with_artifact_content(tmp_path):
    f = tmp_path / "preview.mp4"
    f.write_bytes(b"A")
    h1 = pipeline.plan_hash("Preview: x", [f], {"crf": 20})
    f.write_bytes(b"B")                                         # same path, new content
    assert pipeline.plan_hash("Preview: x", [f], {"crf": 20}) != h1
    f.write_bytes(b"A")
    assert pipeline.plan_hash("Preview: x", [f], {"crf": 21}) != h1   # settings change


def test_gate_no_is_rejected_default_deny_is_pending():
    run = Run()

    def human_no(g, i):
        return False
    human_no.approver_name = "cli-user"
    pipeline._gate(run, "preview", "p", human_no)
    assert run.manifest["approvals"]["preview"] == "rejected"
    pipeline._gate(run, "cut_list", "c", pipeline._deny)
    assert run.manifest["approvals"]["cut_list"] == "pending"


def test_auto_yes_is_not_human_approved():
    run = Run()

    def auto(g, i):
        return True
    auto.approver_name = "auto(--yes)"
    pipeline._gate(run, "preview", "p", auto)
    assert run.manifest["human_approved"]["preview"] is False


def test_cli_exit_codes():
    import kang
    assert kang.exit_code("audio", {"report": {"pass": False}}) == 1
    assert kang.exit_code("audio", {"report": {"pass": True}}) == 0
    assert kang.exit_code("cut", {"output": None, "truncated_words": []}) == 2
    assert kang.exit_code("cut", {"output": None, "truncated_words": [1]}) == 1
    assert kang.exit_code("cut", {"output": "x", "truncated_words": [], "duration_check": {"pass": True}}) == 0
    assert kang.exit_code("subs", {"qa": {"pass": True}, "final": None}) == 2


def test_setup_same_file_guard():
    src = (ROOT / "setup_kaggle.py").read_text(encoding="utf-8")
    assert "selected_source.resolve() != target_audio.resolve()" in src
