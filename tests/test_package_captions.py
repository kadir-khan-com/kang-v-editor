import json

from core.package_captions import repackage_captions
from core.runs import Run, sha256_file


def test_repackage_keeps_original_and_rehashes(tmp_path):
    pkg = tmp_path / "pkg"
    (pkg / "media").mkdir(parents=True)
    (pkg / "sequence.xml").write_text("<xmeml/>", encoding="utf-8")
    (pkg / "captions.srt").write_text("1\n00:00:00,000 --> 00:00:01,000\nहेलो\n", encoding="utf-8")
    (pkg / "media" / "a.mp3").write_bytes(b"x")
    (pkg / "README_IMPORT.txt").write_text("old readme", encoding="utf-8")
    (pkg / "package_manifest.json").write_text(json.dumps({"run_id": "R0", "files": {}}), encoding="utf-8")
    new = tmp_path / "h.srt"
    new.write_text("1\n00:00:00,000 --> 00:00:01,000\nHello\n", encoding="utf-8")
    (tmp_path / "runs").mkdir()
    r = repackage_captions(str(pkg), str(new), extras=[str(new)], caption_note="Hinglish", run=Run(root=tmp_path / "runs"))
    d = tmp_path / "runs" / r["run_id"] / "premiere_package"
    assert "Hello" in (d / "captions.srt").read_text(encoding="utf-8")
    assert "हेलो" in (d / "captions_hindi.srt").read_text(encoding="utf-8")
    assert "हेलो" in (pkg / "captions.srt").read_text(encoding="utf-8")  # original untouched
    pm = json.loads((d / "package_manifest.json").read_text(encoding="utf-8"))
    assert pm["parent_package_run"] == "R0" and pm["files"]["captions.srt"] == sha256_file(d / "captions.srt")
    assert (d / "README_IMPORT.txt").read_text(encoding="utf-8").startswith("CAPTIONS CHANGED")


def test_rejects_non_package(tmp_path):
    (tmp_path / "runs").mkdir()
    assert "error" in repackage_captions(str(tmp_path), str(tmp_path / "x.srt"), run=Run(root=tmp_path / "runs"))
