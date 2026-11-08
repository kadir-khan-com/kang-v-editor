from core.words import apply_glossary, load_glossary
from core import pipeline
from pathlib import Path
import json

W = [{"word": "धाम,", "start": 0.0, "end": 0.4, "probability": 0.9},
     {"word": "द्वारी", "start": 0.5, "end": 0.8, "probability": 0.7},
     {"word": "का,", "start": 0.8, "end": 1.0, "probability": 0.6},
     {"word": "कृष्णे", "start": 1.1, "end": 1.5, "probability": 0.8},
     {"word": "का", "start": 1.5, "end": 1.6, "probability": 0.9}]


def test_multi_token_merge_keeps_timing_and_punct():
    out, ch = apply_glossary(W, {"द्वारी का": "द्वारका", "द्वारी": "द्वारका", "कृष्णे": "कृष्ण"})
    assert [w["word"] for w in out] == ["धाम,", "द्वारका,", "कृष्ण", "का"]
    assert out[1]["start"] == 0.5 and out[1]["end"] == 1.0 and out[1]["probability"] == 0.6
    assert len(ch) == 2 and W[1]["word"] == "द्वारी"  # input not mutated


def test_longest_match_wins_and_lone_token():
    out, _ = apply_glossary([W[1]], {"द्वारी का": "X", "द्वारी": "द्वारका"})
    assert out[0]["word"] == "द्वारका"


def test_shipped_glossary_loads():
    g = load_glossary(Path(__file__).resolve().parent.parent / "config" / "glossary.json")
    assert g["द्वारी का"] == "द्वारका" and not any(k.startswith("_") for k in g)


def test_fix_words_new_run(tmp_path):
    src = tmp_path / "w.json"; src.write_text(json.dumps(W, ensure_ascii=False), encoding="utf-8")
    r = pipeline.fix_words(str(src))
    assert len(r["fixes"]) == 2 and json.loads(src.read_text(encoding="utf-8")) == W
    assert Path(r["words_json"]).is_file()


def test_zero_duration_words_merged_not_fabricated():
    from core.words import rows_to_words
    rows = [{"words": [{"w": "गुम", "start": 1.0, "end": 1.0, "p": 0.5},
                       {"w": "बेट", "start": 1.0, "end": 1.4, "p": 0.9},
                       {"w": "द्वारका", "start": 1.4, "end": 1.4, "p": 0.9},
                       {"w": "जाएं", "start": 1.5, "end": 1.9, "p": 0.9}]}]
    w = rows_to_words(rows)
    assert [x["word"] for x in w] == ["गुम बेट द्वारका", "जाएं"]
    assert (w[0]["start"], w[0]["end"]) == (1.0, 1.4)
    assert all(x["end"] > x["start"] for x in w)


def test_brand_subtitle_font_covers_hinglish():
    from core.brand import load_brand, resolve_fonts, missing_glyphs
    root = Path(__file__).resolve().parent.parent
    fonts, warns = resolve_fonts(load_brand(root / "brand.json"), root / "fonts")
    assert not warns
    assert missing_glyphs(fonts["hindi"], "Amazing Zip line दार्जिलिंग क्षत्र ज्ञ 2026 ₹") == []


def test_sanitize_strips_foreign_script_and_drops_garbage():
    from core.words import sanitize_script, repeated_runs
    w = [{"word": "¿", "start": 0, "end": 0.2}, {"word": "neutral", "start": 0.2, "end": 0.5},
         {"word": "हैассור", "start": 0.5, "end": 0.9}, {"word": "ассор", "start": 0.9, "end": 1.0},
         {"word": "और", "start": 1.0, "end": 1.2}, {"word": "और", "start": 1.2, "end": 1.4},
         {"word": "और,", "start": 1.4, "end": 1.6}, {"word": "₹500", "start": 1.6, "end": 2.0}]
    out, log = sanitize_script(w)
    assert [x["word"] for x in out] == ["neutral", "है", "और", "और", "और,", "₹500"]
    assert {l["action"] for l in log} == {"dropped", "stripped"}
    assert repeated_runs(out)[0]["count"] == 3

