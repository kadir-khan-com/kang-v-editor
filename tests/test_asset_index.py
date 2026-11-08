import json
from pathlib import Path

from PIL import Image

from core import asset_index as ai


def _lib(tmp_path):
    d = tmp_path / "lib"
    d.mkdir()
    Image.new("RGB", (1920, 1080), "red").save(d / "S13_1_nageshwar_shiva_statue.jpg")
    Image.new("RGB", (800, 600), "blue").save(d / "S06_1_gomti_ghat_holy_bath.jpg")
    Image.new("RGB", (100, 100), "green").save(d / "own_photo.png")
    sha = ai._sha(d / "S13_1_nageshwar_shiva_statue.jpg")
    (d / "CREDITS.json").write_text(json.dumps([
        {"file": "S13_1_nageshwar_shiva_statue.jpg", "title": "File:Nageshwar Shiva.jpg", "author": "A",
         "licence": "CC BY-SA 4.0", "source_page": "https://x", "sha256": sha},
        {"file": "S06_1_gomti_ghat_holy_bath.jpg", "title": "File:Gomti Ghat.jpg", "author": "B", "licence": "CC0"},
        {"file": "gone.jpg", "licence": "CC BY 2.0"}]), encoding="utf-8")
    return d


def test_ingest_records_licence_dims_tags_and_warnings(tmp_path):
    d = _lib(tmp_path)
    r = ai.ingest(d)
    assert r["ok"] and r["count"] == 3
    idx = json.loads(Path(r["index"]).read_text(encoding="utf-8"))
    assert idx["schema"] == ai.SCHEMA
    by = {Path(i["path"]).name: i for i in idx["items"]}
    n = by["S13_1_nageshwar_shiva_statue.jpg"]
    assert (n["width"], n["height"]) == (1920, 1080) and n["licence_info"]["sharealike"]
    assert "nageshwar" in n["tags"] and "shiva" in n["tags"] and n["embedding_ref"] is None
    assert by["own_photo.png"]["rights_status"] == "unknown"
    assert idx["licence_summary"] == {"CC BY-SA": 1, "CC0": 1, "UNKNOWN": 1}
    assert any("no licence" in w for w in r["warnings"]) and any("gone.jpg" in w for w in r["warnings"])


def test_ingest_flags_file_changed_after_crediting(tmp_path):
    d = _lib(tmp_path)
    Image.new("RGB", (1920, 1080), "black").save(d / "S13_1_nageshwar_shiva_statue.jpg")
    r = ai.ingest(d)
    assert not r["ok"] and "sha256 differs" in r["problems"][0]


def test_search_hindi_alias_and_sharealike_filter(tmp_path):
    d = _lib(tmp_path)
    idx = json.loads(Path(ai.ingest(d)["index"]).read_text(encoding="utf-8"))
    top = ai.search(idx, "नागेश्वर शिव")
    assert top[0]["path"].startswith("S13_1") and top[0]["score"] == 1.0
    assert ai.search(idx, "गोमती घाट")[0]["path"].startswith("S06_1")
    assert ai.search(idx, "nageshwar", exclude_sharealike=True) == []
    assert ai.search(idx, "") == []


def test_licence_family():
    assert ai.licence_family("CC BY 2.0")["family"] == "CC BY"
    assert ai.licence_family("Public domain")["family"] == "PD"
    assert ai.licence_family("")["commercial_ok"] is None
