"""F03 cut, F04 audio, F05 multi-format, F19-lite, pipeline gates (real FFmpeg, offline)."""
import json
from pathlib import Path

import pytest

from core import cutter, pipeline, qa, render
from core.audio import measure_loudness
from core.brand import CANVAS
from core.runs import media_summary, sha256_file
from core.style import contrast_ratio, extract_palette, palette_to_brand_draft

ROOT = Path(__file__).resolve().parent.parent


# ---------------- F03 ----------------
def test_parse_silencedetect():
    log = ("[silencedetect @ x] silence_start: 1.5\n[silencedetect @ x] silence_end: 2.5 | silence_duration: 1\n"
           "[silencedetect @ x] silence_start: 5.1\n")
    assert cutter.parse_silencedetect(log, total=6.0) == [(1.5, 2.5), (5.1, 6.0)]


def test_detect_silence_on_real_audio(media):
    sil = cutter.detect_silence(media / "speech.wav", -34, 0.45, 5.5)
    assert len(sil) == 4
    assert abs(sil[1][0] - 1.5) < 0.05 and abs(sil[1][1] - 2.5) < 0.05


def test_tighten_words_trusts_silence():
    words = [{"word": "आप", "start": 24.02, "end": 24.8}]
    out, notes = cutter.tighten_words(words, [(24.04, 24.605)])
    assert out[0]["start"] == 24.605 and notes[0]["note"] == "tightened"


def test_plan_cuts_fillers_padding_and_no_truncation(words_speech):
    sil = [(0.0, 0.5), (1.5, 2.5), (3.5, 4.3), (5.0, 5.5)]
    fill = {"auto": ["उम्म"], "review": ["मतलब"]}
    plan = cutter.plan_cuts(words_speech, sil, 5.5, fill)
    words = plan["words_tightened"]
    assert words[0]["end"] == 1.5                     # swallowed silence trimmed
    assert cutter.check_no_word_truncated(words, plan["keep"], fill["auto"]) == []
    # filler 'उम्म' (2.5-3.5) is removed together with surrounding silence
    assert not any(s <= 3.0 <= e for s, e in plan["keep"])
    # padding: speech end 1.5 -> keep continues >= 90 ms
    assert any(abs(e - 1.59) < 1e-6 for _, e in plan["keep"])
    assert plan["flagged"][0]["action"] == "cut_proposed"


def test_review_words_never_auto_cut():
    words = [{"word": "मतलब", "start": 1.0, "end": 1.4}]
    plan = cutter.plan_cuts(words, [], 2.0, {"auto": [], "review": ["मतलब"]})
    assert plan["remove"] == [] and plan["flagged"][0]["action"] == "review_only"


def test_remap_words_to_cut_timeline():
    w = [{"word": "a", "start": 0.6, "end": 1.0}, {"word": "b", "start": 3.0, "end": 3.4}]
    out = cutter.remap_words(w, [(0.5, 1.5), (2.9, 4.0)])
    assert out[0]["start"] == 0.1 and out[1]["start"] == 1.1


def test_cut_gate_blocks_until_approved(media, words_speech, tmp_path):
    wp = tmp_path / "w.json"; wp.write_text(json.dumps(words_speech, ensure_ascii=False), encoding="utf-8")
    src_hash = sha256_file(media / "speech.wav")
    r = pipeline.plan_and_cut(str(media / "speech.wav"), str(wp))                       # default: deny
    assert r["output"] is None and r["truncated_words"] == []
    m = json.loads((Path(r["dir"]) / "manifest.json").read_text(encoding="utf-8"))
    assert m["approvals"]["cut_list"] == "pending" and m["status"] == "awaiting_cut_approval"
    assert (Path(r["dir"]) / "cut_list.txt").read_text(encoding="utf-8").startswith("KANG cut list")
    r2 = pipeline.plan_and_cut(str(media / "speech.wav"), str(wp), approver=lambda g, i: True)
    assert r2["duration_check"]["pass"]
    assert sha256_file(media / "speech.wav") == src_hash                                # original untouched
    edl = json.loads((Path(r2["dir"]) / "edl.json").read_text(encoding="utf-8"))
    assert edl["approvals"]["cut_list"] == "approved" and edl["cuts"]


def test_cut_video_keeps_av_in_sync(media, tmp_path):
    out = cutter.render_cuts(media / "video_16x9.mp4", [(0.0, 1.0), (2.0, 3.5)], tmp_path / "c.mp4")
    m = media_summary(out)
    assert abs(m["duration"] - 2.5) < 0.1 and m["has_audio"] and m["has_video"]


# ---------------- F04 ----------------
def test_audio_cleanup_hits_target_loudness(media):
    before = measure_loudness(media / "quiet.wav")
    assert before["integrated_lufs"] < -30
    r = pipeline.clean_audio(str(media / "quiet.wav"))
    a = r["report"]["after"]
    assert r["report"]["pass"], r["report"]
    assert abs(a["integrated_lufs"] + 14) <= 1.0 and a["true_peak_dbtp"] <= -1.2
    assert (Path(r["dir"]) / "loudness_report.json").is_file()


# ---------------- F05 ----------------
def test_reframe_filter_math():
    assert render.reframe_filter(1920, 1080, "9:16", 0.5) == "crop=608:1080:656:0,scale=1080:1920"
    assert render.reframe_filter(1920, 1080, "9:16", 0.0).startswith("crop=608:1080:0:0")
    assert render.reframe_filter(1920, 1080, "9:16", 1.0).startswith("crop=608:1080:1312:0")
    assert render.reframe_filter(1080, 1920, "16:9").startswith("crop=1080:")
    assert render.reframe_filter(1920, 1080, "16:9") == "scale=1920:1080"


def test_multi_format_exact_sizes_and_duration(media, hindi_words, tmp_path):
    wp = tmp_path / "w.json"; wp.write_text(json.dumps(hindi_words[:12], ensure_ascii=False), encoding="utf-8")
    r = pipeline.multi_format(str(media / "video_16x9.mp4"), str(wp), ["9:16", "16:9", "1:1"])
    assert r["qa"]["pass"], r["qa"]
    for fmt, p in r["outputs"].items():
        m = media_summary(p)
        assert (m["width"], m["height"]) == CANVAS[fmt]


# ---------------- F01 pipeline + gates ----------------
def test_subtitle_video_preview_gate(media, hindi_words, tmp_path):
    wp = tmp_path / "w.json"; wp.write_text(json.dumps(hindi_words[:10], ensure_ascii=False), encoding="utf-8")
    r = pipeline.subtitle_video(str(media / "video_16x9.mp4"), str(wp))
    assert r["qa"]["pass"], r["qa"]["failed"]
    assert r["final"] is None and Path(r["preview"]).is_file()
    prev = media_summary(r["preview"])
    assert prev["height"] == 960 and prev["duration"] <= 6.1
    r2 = pipeline.subtitle_video(str(media / "video_16x9.mp4"), str(wp), approver=lambda g, i: True)
    assert r2["final"] and r2["qa"]["pass"]
    d = Path(r2["dir"])
    for f in ("subs_9x16.ass", "subs.srt", "preview_10s.mp4", "final.mp4", "render_settings.json", "manifest.json"):
        assert (d / f).is_file(), f


def test_promo_clip_from_voiceover(media, tmp_path):
    words = [{"word": w, "start": 0.5 + i * 0.5, "end": 0.9 + i * 0.5} for i, w in enumerate("नमस्ते दोस्तों आज बात करेंगे".split())]
    wp = tmp_path / "w.json"; wp.write_text(json.dumps(words, ensure_ascii=False), encoding="utf-8")
    r = pipeline.promo_clip(str(media / "speech.wav"), str(wp), start=0.0, duration=5.0, approver=lambda g, i: True)
    assert r["qa"]["pass"], r["qa"]
    m = media_summary(r["final"])
    assert (m["width"], m["height"]) == (1080, 1920) and abs(m["duration"] - 5.0) < 0.1


def test_transcribe_to_words_with_mock(media):
    def fake(samples):
        return [{"start": 0.5, "end": 1.5, "text": "नमस्ते", "words": [{"w": "नमस्ते", "start": 0.5, "end": 1.5, "p": 0.9}]}]
    r = pipeline.transcribe_to_words(str(media / "speech.wav"), transcriber=fake)
    d = Path(r["dir"])
    assert r["words"] >= 1  # tones after 1.5 s have no words -> gap re-transcribed
    assert r["speech_gaps"] and (d / "speech_gaps.json").is_file()
    for f in ("words.json", "words_raw.json", "transcript.srt", "transcript.json", "anomaly_audit.json", "review_sample.txt"):
        assert (d / f).is_file(), f


# ---------------- F19-lite ----------------
def test_contrast_ratio_known_values():
    assert contrast_ratio("#FFFFFF", "#000000") == 21.0
    assert contrast_ratio("#777777", "#777777") == 1.0
    assert not qa.check_contrast("#777777", "#888888")["pass"]


def test_palette_from_screenshot(tmp_path):
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (400, 300), "#0F172A")
    d = ImageDraw.Draw(img)
    d.rectangle([20, 20, 200, 120], fill="#FACC15")
    d.rectangle([220, 150, 380, 280], fill="#2563EB")
    p = tmp_path / "shot.png"; img.save(p)
    pal = extract_palette(p, k=3)
    assert pal[0]["hex"] == "#0F172A"
    draft = palette_to_brand_draft(pal)
    assert draft["colors"]["primary"] == "#0F172A"
    assert {draft["colors"]["accent"], draft["colors"]["highlight"]} == {"#FACC15", "#2563EB"}
    assert draft["colors"]["text"] == "#FFFFFF" and draft["contrast_ok"]
    r = pipeline.palette_from_screenshot(str(p), k=3)
    assert (Path(r["dir"]) / "brand_draft.json").is_file()
