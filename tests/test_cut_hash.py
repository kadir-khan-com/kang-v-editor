import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import pytest
from core import cutter, pipeline
from core.runs import Run


def _media(tmp_path):
    import subprocess
    (tmp_path / "runs").mkdir(exist_ok=True)
    m = tmp_path / "a.wav"
    subprocess.run(["ffmpeg", "-hide_banner", "-y", "-f", "lavfi", "-i", "sine=f=440:d=4", str(m)],
                   check=True, capture_output=True)
    return m


def _approved_cuts(tmp_path, media):
    src = Run(root=tmp_path / "runs")
    src.add_input(media, "A1")
    plan = {"keep": [[0.0, 1.5], [2.0, 4.0]], "remove": [[1.5, 2.0]], "flagged": [],
            "stats": {"source_dur": 4.0, "kept_dur": 3.5, "removed_dur": 0.5, "cut_count": 1}}
    cp = pipeline.write_json(src.path("cuts.json"), plan)
    h = pipeline.plan_hash(cutter.cut_list_text(plan), [cp])
    src.set_approval("cut_list", "approved", plan_hash=h, approver="cli-user")
    return cp


def _words(tmp_path):
    w = [{"word": "एक", "start": 0.2, "end": 0.6, "probability": 0.9},
         {"word": "दो।", "start": 2.2, "end": 2.6, "probability": 0.9}]
    return pipeline.write_json(tmp_path / "w.json", w)


def test_cuts_edited_after_approval_are_rejected(tmp_path):
    media = _media(tmp_path)
    cp = _approved_cuts(tmp_path, media)
    plan = json.loads(cp.read_text(encoding="utf-8"))
    plan["keep"] = [[0.0, 4.0]]
    plan["remove"] = []
    cp.write_text(json.dumps(plan), encoding="utf-8")
    r = pipeline.premiere_package(str(media), str(_words(tmp_path)), run=Run(root=tmp_path / "runs"),
                                  approver=lambda g, i: True,
                                  cuts_path=str(cp))
    assert "plan hash mismatch" in r.get("error", "")


def test_cuts_for_other_media_are_rejected(tmp_path):
    media = _media(tmp_path)
    cp = _approved_cuts(tmp_path, media)
    import subprocess
    other = tmp_path / "b.wav"
    subprocess.run(["ffmpeg", "-hide_banner", "-y", "-f", "lavfi", "-i", "sine=f=220:d=4", str(other)],
                   check=True, capture_output=True)
    r = pipeline.premiere_package(str(other), str(_words(tmp_path)), run=Run(root=tmp_path / "runs"),
                                  approver=lambda g, i: True, cuts_path=str(cp))
    assert "different source media" in r.get("error", "")


def test_unchanged_approved_cuts_pass_gate(tmp_path):
    media = _media(tmp_path)
    cp = _approved_cuts(tmp_path, media)
    r = pipeline.premiere_package(str(media), str(_words(tmp_path)), run=Run(root=tmp_path / "runs"),
                                  approver=lambda g, i: True, cuts_path=str(cp))
    assert "error" not in r and r["cuts_human_approved"] is True
