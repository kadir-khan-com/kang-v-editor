"""Phase 0/1 + F16 + EDL: runs, manifest, brand, schema, words."""
import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from core import runs
from core.brand import Brand, load_brand, resolve_fonts, hex_to_ass, missing_glyphs, font_family_name
from core.edl import EDL, save_edl, load_edl
from core.words import rows_to_words, audit_words, validate_words, review_sample

ROOT = Path(__file__).resolve().parent.parent


# ---------------- runs / manifest ----------------
def test_run_ids_unique_and_sequential(tmp_path):
    r1, r2 = runs.Run(root=tmp_path), runs.Run(root=tmp_path)
    assert r1.run_id != r2.run_id
    assert runs.RUN_ID_RE.match(r1.run_id) and r1.run_id.endswith("_KANG_001") and r2.run_id.endswith("_KANG_002")
    assert (r1.dir / "manifest.json").is_file()


def test_run_refuses_writes_outside_folder(tmp_path):
    r = runs.Run(root=tmp_path)
    with pytest.raises(ValueError):
        r.path("../escape.txt")


def test_manifest_records_inputs_outputs_hash(tmp_path, media):
    r = runs.Run(root=tmp_path)
    src = media / "speech.wav"
    before = runs.sha256_file(src)
    e = r.add_input(src)
    assert e["sha256"] == before and e["media"]["has_audio"]
    out = r.path("x.txt"); out.write_text("hi", encoding="utf-8")
    r.add_output(out, "note")
    m = json.loads((r.dir / "manifest.json").read_text(encoding="utf-8"))
    assert m["outputs"][0]["path"] == "x.txt" and len(m["outputs"][0]["sha256"]) == 64
    assert runs.sha256_file(src) == before  # original untouched


def test_ffprobe_rejects_missing_and_corrupt(tmp_path):
    with pytest.raises(FileNotFoundError):
        runs.ffprobe(tmp_path / "nope.mp4")
    bad = tmp_path / "bad.mp4"; bad.write_bytes(b"not a video at all" * 100)
    with pytest.raises(RuntimeError):
        runs.ffprobe(bad)


# ---------------- brand (F16) ----------------
def test_brand_json_valid_and_margin_rule():
    b = load_brand(ROOT / "brand.json")
    assert b.margin_for("9:16") == 60                  # max(60, 40)
    assert b.subtitle_bottom_for("9:16") == 480
    b2 = b.model_copy(update={"safe_margin_px": 10})
    assert b2.margin_for("9:16") == 40                 # format minimum wins


@pytest.mark.parametrize("patch", [
    {"colors": {"primary": "blue", "accent": "#2563EB", "highlight": "#FACC15"}},
    {"safe_zones": {"16:9": {"subtitle_bottom_px": 60}}},          # 9:16 required
    {"safe_zones": {"9:16": {"subtitle_bottom_px": 120}, "7:3": {"subtitle_bottom_px": 1}}},
    {"client": ""},
])
def test_brand_schema_rejects_bad(patch):
    data = json.loads((ROOT / "brand.json").read_text(encoding="utf-8"))
    data.update(patch)
    with pytest.raises(ValidationError):
        Brand.model_validate(data)


def test_missing_font_gives_visible_warning():
    data = json.loads((ROOT / "brand.json").read_text(encoding="utf-8"))
    data["fonts"]["heading"] = "DoesNotExist.ttf"
    fonts, warns = resolve_fonts(Brand.model_validate(data), ROOT / "fonts")
    assert fonts["heading"].name == "NotoSansDevanagari-Bold.ttf"
    assert warns and "DoesNotExist.ttf" in warns[0]


def test_font_helpers():
    f = ROOT / "fonts" / "NotoSansDevanagari-Bold.ttf"
    assert "Noto Sans Devanagari" in font_family_name(f)
    assert missing_glyphs(f, "द्वारका क्षत्रिय श्री") == []
    assert hex_to_ass("#FACC15") == "&H0015CCFA"


# ---------------- EDL ----------------
def _edl(**kw):
    base = {"run_id": "2026-10-28_KANG_001", "inputs": [{"id": "A1", "path": "raw.mp4", "sha256": "a" * 64}],
            "cuts": [{"src": "A1", "in": 0.0, "out": 2.0}, {"src": "A1", "in": 2.5, "out": 4.0}]}
    base.update(kw)
    return EDL.model_validate(base)


def test_edl_roundtrip(tmp_path):
    e = _edl()
    assert e.kept_duration() == 3.5
    p = save_edl(e, tmp_path / "edl.json")
    d = json.loads(p.read_text(encoding="utf-8"))
    assert d["schema"] == "kang.edl/1.0" and d["cuts"][0]["in"] == 0.0
    assert load_edl(p).kept_duration() == 3.5


@pytest.mark.parametrize("cuts", [
    [{"src": "A1", "in": 2.0, "out": 1.0}],                                  # out <= in
    [{"src": "B9", "in": 0.0, "out": 1.0}],                                  # unknown input
    [{"src": "A1", "in": 0.0, "out": 3.0}, {"src": "A1", "in": 2.0, "out": 4.0}],  # overlap
])
def test_edl_rejects_bad_cuts(cuts):
    with pytest.raises(ValidationError):
        _edl(cuts=cuts)


def test_edl_broll_requires_license():
    with pytest.raises(ValidationError):
        _edl(b_roll=[{"src": "x.png", "t_in": 1, "dur": 2, "license": ""}])


# ---------------- words.json (Phase 1) ----------------
def test_rows_to_words_and_audit():
    rows = [{"start": 0, "end": 2, "text": "a b", "words": [
        {"w": "राधे", "start": 0.0, "end": 0.4, "p": 0.9},
        {"w": " ", "start": 0.4, "end": 0.5},
        {"w": "राधे।", "start": 0.3, "end": 3.5, "p": 0.2}]}]
    w = rows_to_words(rows)
    assert [x["word"] for x in w] == ["राधे", "राधे।"]
    a = audit_words(w)
    kinds = {i["issue"] for i in a["issues"]}
    assert {"too_long", "overlaps_previous", "low_confidence"} <= kinds and not a["ok"]
    assert "राधे" in review_sample(w)


def test_validate_words_rejects_bad():
    with pytest.raises(ValueError):
        validate_words([])
    with pytest.raises(ValueError):
        validate_words([{"word": "x", "start": 1.0, "end": 1.0}])
