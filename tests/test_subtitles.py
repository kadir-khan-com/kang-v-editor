"""F01 animated subtitles + F02 presets + Hindi glyph QA."""
from pathlib import Path

import pytest

from core import qa
from core.brand import CANVAS, load_brand, resolve_fonts
from core.subtitles import (ass_events, ass_word_onsets, build_ass, build_srt, chunk_timings, chunk_words,
                            list_presets, load_preset, make_layout)

ROOT = Path(__file__).resolve().parent.parent
FONT = ROOT / "fonts" / "NotoSansDevanagari-Bold.ttf"


def W(word, s, e):
    return {"word": word, "start": s, "end": e}


def test_chunk_max_words_and_chars():
    words = [W(f"शब्द{i}", i * 0.3, i * 0.3 + 0.25) for i in range(10)]
    ch = chunk_words(words, max_words=4, max_chars=32)
    assert all(2 <= len(c) <= 4 for c in ch[:-1])
    assert all(len(" ".join(w["word"] for w in c)) <= 32 for c in ch)
    assert [w for c in ch for w in c] == words  # nothing lost, order kept


def test_chunk_breaks_on_pause_sentence_and_duration():
    words = [W("एक", 0, .3), W("दो।", .35, .6), W("तीन", .65, .9), W("चार", 1.8, 2.0), W("पांच", 2.05, 4.5)]
    ch = chunk_words(words, max_words=4, max_dur=2.0, pause_break=0.35)
    texts = [" ".join(w["word"] for w in c) for c in ch]
    assert texts == ["एक दो।", "तीन", "चार", "पांच"]


def test_chunk_timings_merge_small_gap_and_trim_overlap():
    ch = [[W("a", 0, 1.0)], [W("b", 1.05, 2.0)], [W("c", 1.9, 3.0)], [W("d", 3.5, 4.0)]]
    t = chunk_timings(ch, merge_gap=0.08)
    assert t[0] == (0, 1.05)        # 50 ms gap merged
    assert t[1] == (1.05, 1.9)      # overlap trimmed
    assert t[2] == (1.9, 3.0)       # real gap kept
    assert all(a[1] <= b[0] for a, b in zip(t, t[1:]))


@pytest.fixture
def setup():
    brand = load_brand(ROOT / "brand.json")
    fonts, _ = resolve_fonts(brand, ROOT / "fonts")
    return brand, fonts


def test_option_a_kf_sync_and_colors(setup, hindi_words):
    brand, fonts = setup
    p = load_preset("vox_bold_yellow", ROOT / "presets")
    L = make_layout(brand, p, "9:16", FONT)
    ass, ev = build_ass(hindi_words, brand, p, L, FONT, option="A")
    assert "\\kf" in ass and "PlayResX: 1080" in ass and "PlayResY: 1920" in ass
    style = [l for l in ass.splitlines() if l.startswith("Style: Kang")][0].split(",")
    assert style[3] == "&H0015CCFA" and style[4] == "&H00FFFFFF"   # Primary=highlight, Secondary=white
    assert qa.check_sync(ass, hindi_words)["pass"]
    assert qa.check_no_overlap(ass)["pass"]
    assert [w for _, w in zip(range(99), (x for x, _ in ass_word_onsets(ass)))] == [w["word"] for w in hindi_words]


def test_sync_check_detects_drift(setup, hindi_words):
    brand, _ = setup
    p = load_preset("vox_bold_yellow", ROOT / "presets")
    ass, _ = build_ass(hindi_words, brand, p, make_layout(brand, p, "9:16", FONT), FONT)
    shifted = [dict(w, start=w["start"] + 0.25, end=w["end"] + 0.25) for w in hindi_words]
    assert not qa.check_sync(ass, shifted)["pass"]


def test_option_b_scale_pop(setup, hindi_words):
    brand, _ = setup
    p = load_preset("promo", ROOT / "presets")
    ass, ev = build_ass(hindi_words, brand, p, make_layout(brand, p, "9:16", FONT), FONT)
    assert "\\fscx108\\fscy108" in ass and "\\t(" in ass
    assert len(ass_events(ass)) >= len(hindi_words) - 1
    assert qa.check_no_overlap(ass)["pass"]


def test_srt_format(hindi_words, setup):
    brand, _ = setup
    p = load_preset("vox_bold_yellow", ROOT / "presets")
    _, ev = build_ass(hindi_words, brand, p, make_layout(brand, p, "9:16", FONT), FONT)
    srt = build_srt(ev)
    assert srt.startswith("1\n00:00:00,300 --> ") and "दार्जिलिंग।" in srt


def test_long_word_chunks_fit_safe_width(setup):
    brand, _ = setup
    p = load_preset("promo", ROOT / "presets")
    L = make_layout(brand, p, "9:16", FONT)
    long = [W("त्र्यंबकेश्वरमहादेवमंदिरपरिसर", i, i + 0.5) for i in range(4)]
    _, ev = build_ass(long, brand, p, L, FONT)
    assert all(len(e["words"]) == 1 for e in ev)  # pixel-width checker forced one word per line


# ---------------- F02: presets via JSON only ----------------
def test_all_presets_validate_and_render_three_lines(setup, tmp_path):
    brand, fonts = setup
    names = list_presets(ROOT / "presets")
    assert {"vox_bold_yellow", "travel", "educational", "promo"} <= set(names)
    lines = [W("पहली", 0.2, 0.6), W("लाइन", 0.65, 1.0), W("दूसरी", 1.6, 2.0), W("लाइन", 2.05, 2.4),
             W("तीसरी", 3.0, 3.4), W("लाइन।", 3.45, 3.8)]
    for n in names:
        p = load_preset(n, ROOT / "presets")
        for fmt in ("9:16", "16:9", "1:1"):
            L = make_layout(brand, p, fmt, fonts[p.font_role])
            ass, ev = build_ass(lines, brand, p, L, fonts[p.font_role])
            assert len(ev) == 3
            f = tmp_path / f"{n}_{fmt.replace(':', 'x')}.ass"
            f.write_text(ass, encoding="utf-8")
            png = qa.render_ass_on_black(f, ROOT / "fonts", CANVAS[fmt], 0.4, tmp_path / f"{f.stem}.png")
            res = qa.check_safe_zone(png, CANVAS[fmt], L.margin_lr, L.margin_v)
            assert res["pass"], (n, fmt, res)


def test_new_preset_is_json_only(tmp_path, setup):
    import json, shutil
    shutil.copytree(ROOT / "presets", tmp_path / "presets")
    d = json.loads((tmp_path / "presets" / "travel.json").read_text(encoding="utf-8"))
    d.update(name="custom_red", size_pct=5.0, uppercase=True)
    (tmp_path / "presets" / "custom_red.json").write_text(json.dumps(d), encoding="utf-8")
    assert load_preset("custom_red", tmp_path / "presets").size_pct == 5.0


# ---------------- glyph / shaping (F01 QA) ----------------
def test_glyph_coverage_of_test_sentences():
    assert qa.check_glyphs(FONT, qa.GLYPH_TEST_SENTENCES)["pass"]


def test_hindi_shaping_complex_not_broken(setup, tmp_path):
    """Regression for the real bug found: default libass shaping breaks द्वा / क्ष / श्री."""
    brand, _ = setup
    p = load_preset("vox_bold_yellow", ROOT / "presets")
    words = [W(w, 0.1 + i * 0.3, 0.35 + i * 0.3) for i, w in enumerate("द्वारका क्षत्रिय श्री".split())]
    ass, _ = build_ass(words, brand, p, make_layout(brand, p, "9:16", FONT), FONT)
    f = tmp_path / "g.ass"; f.write_text(ass, encoding="utf-8")
    res = qa.check_shaping(f, ROOT / "fonts", (1080, 1920), 0.8, tmp_path)
    assert res["pass"], res
