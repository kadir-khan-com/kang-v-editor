"""
Offline Unit Tests for AI Video Engine core/engine.py
Tests timestamp validation, SRT generation, Hindi punctuation handling,
word preservation, suspicious timestamp detection, and bounded targeted
re-transcription using mocked model outputs WITHOUT requiring GPU or model downloads.
"""

import sys
import os
import json
from pathlib import Path
from unittest.mock import MagicMock

sys.path.insert(0, str(Path(__file__).parent))

from core.engine import (
    format_srt_timestamp,
    validate_and_fix_timestamps,
    chunk_words,
    generate_srt,
    save_outputs,
    detect_suspicious_words,
    group_suspicious_windows,
    offset_clip_timestamps,
    is_retranscription_reliable,
    merge_targeted_retranscription,
    refine_transcript,
    transcribe,
    DEFAULT_HINDI_PROMPT,
    MAX_WORD_DURATION_THRESHOLD
)


def test_format_srt_timestamp():
    assert format_srt_timestamp(0.0) == "00:00:00,000"
    assert format_srt_timestamp(1.5) == "00:00:01,500"
    assert format_srt_timestamp(65.123) == "00:01:05,123"
    assert format_srt_timestamp(3661.045) == "01:01:01,045"
    print("[PASS] test_format_srt_timestamp")


def test_timestamp_validation_and_overlap_safety():
    min_dur = 0.05
    chunks = [
        {"start": 1.0, "end": 3.0, "text": "पहला वाक्य"},
        {"start": 2.5, "end": 4.0, "text": "दूसरा वाक्य"}
    ]
    fixed = validate_and_fix_timestamps(chunks, min_duration=min_dur)
    assert fixed[0]["start"] == 1.0
    assert fixed[0]["end"] == 2.5, f"Expected 2.5, got {fixed[0]['end']}"
    assert fixed[1]["start"] == 2.5, f"Speech onset was shifted! Got {fixed[1]['start']}"
    assert fixed[1]["end"] == 4.0
    assert fixed[0]["end"] <= fixed[1]["start"]
    print("[PASS] test_timestamp_validation_and_overlap_safety (normal overlap)")


def test_timestamp_anomalies_equal_and_inverted_starts():
    min_dur = 0.05
    equal_chunks = [
        {"start": 2.0, "end": 3.0, "text": "पहला भाग"},
        {"start": 2.0, "end": 4.0, "text": "समान टाइमस्टैम्प"}
    ]
    fixed_equal = validate_and_fix_timestamps(equal_chunks, min_duration=min_dur)
    assert fixed_equal[0]["start"] == 2.0
    assert fixed_equal[1]["start"] == 2.0
    assert fixed_equal[1].get("anomaly") == "equal_start"
    assert fixed_equal[0]["end"] > fixed_equal[0]["start"]
    assert fixed_equal[1]["end"] > fixed_equal[1]["start"]

    inverted_chunks = [
        {"start": 3.5, "end": 5.0, "text": "बाद वाला पहले आया"},
        {"start": 1.2, "end": 4.0, "text": "पहले वाला बाद में आया"}
    ]
    fixed_inv = validate_and_fix_timestamps(inverted_chunks, min_duration=min_dur)
    assert fixed_inv[0]["start"] == 3.5
    assert fixed_inv[1]["start"] == 1.2
    assert fixed_inv[1].get("anomaly") == "inverted_start"

    zero_chunk = [{"start": 5.0, "end": 5.0, "text": "शून्य अवधि"}]
    fixed_zero = validate_and_fix_timestamps(zero_chunk, min_duration=min_dur)
    assert fixed_zero[0]["end"] > fixed_zero[0]["start"]
    assert fixed_zero[0].get("anomaly") == "zero_or_negative_duration"

    short_chunks = [
        {"start": 1.0, "end": 1.02, "text": "बहुत छोटा"},
        {"start": 1.02, "end": 2.0, "text": "सामान्य भाग"}
    ]
    fixed_short = validate_and_fix_timestamps(short_chunks, min_duration=min_dur)
    assert fixed_short[0]["start"] == 1.0
    assert fixed_short[0]["end"] == 1.02
    assert fixed_short[1]["start"] == 1.02
    assert fixed_short[0]["end"] <= fixed_short[1]["start"]

    print("[PASS] test_timestamp_anomalies_equal_and_inverted_starts")


def test_hindi_chunking_and_word_preservation():
    raw_words = [
        {"w": "हेलो", "start": 0.0, "end": 0.4},
        {"w": "दोस्तों", "start": 0.45, "end": 0.8},
        {"w": "कैसे", "start": 0.85, "end": 1.1},
        {"w": "हैं", "start": 1.15, "end": 1.3},
        {"w": "आप", "start": 1.35, "end": 1.5},
        {"w": "सभी?", "start": 1.55, "end": 1.9},
        {"w": "सभी", "start": 2.2, "end": 2.5},
        {"w": "प्यारे", "start": 2.55, "end": 2.9},
        {"w": "भक्तों", "start": 2.95, "end": 3.4},
        {"w": "को", "start": 3.45, "end": 3.6},
        {"w": "राधे", "start": 3.65, "end": 4.0},
        {"w": "राधे।", "start": 4.05, "end": 4.5}
    ]
    rows = [{"start": 0.0, "end": 4.5, "text": "पूर्ण टेक्स्ट", "words": raw_words}]

    chunks = chunk_words(rows, max_words=7, max_chars=40, gap=0.6)

    output_words = [w for c in chunks for w in c["text"].split()]
    expected_words = [w["w"] for w in raw_words]
    assert output_words == expected_words

    assert chunks[0]["text"].endswith("?")
    assert chunks[-1]["text"].endswith("।")

    for c in chunks:
        assert c["start"] < c["end"]
    for i in range(len(chunks) - 1):
        assert chunks[i]["end"] <= chunks[i + 1]["start"]

    print("[PASS] test_hindi_chunking_and_word_preservation")


def test_srt_generation_and_save_outputs():
    rows = [
        {
            "start": 0.0,
            "end": 2.0,
            "text": "नमस्ते द्वारका",
            "words": [
                {"w": "नमस्ते", "start": 0.0, "end": 0.9},
                {"w": "द्वारका।", "start": 1.0, "end": 2.0}
            ]
        }
    ]

    tmpdir = os.path.join(os.path.dirname(__file__), "tmp_test_output")
    os.makedirs(tmpdir, exist_ok=True)
    try:
        srt_p, json_p = save_outputs(rows, tmpdir)
        assert os.path.isfile(srt_p)
        assert os.path.isfile(json_p)

        with open(srt_p, "r", encoding="utf-8") as f:
            srt_content = f.read()

        assert "00:00:00,000 --> 00:00:02,000" in srt_content
        assert "नमस्ते द्वारका।" in srt_content

        with open(json_p, "r", encoding="utf-8") as f:
            loaded_json = json.load(f)
        assert len(loaded_json) == 1
        assert loaded_json[0]["words"][0]["w"] == "नमस्ते"
    finally:
        import shutil
        shutil.rmtree(tmpdir, ignore_errors=True)

    print("[PASS] test_srt_generation_and_save_outputs")


# ==============================================================================
# Suspicious Timestamp Detector & Bounded Targeted Re-transcription Tests
# ==============================================================================

def test_detect_suspicious_words():
    rows = [
        {
            "start": 0.0, "end": 35.0, "text": "नमूना",
            "words": [
                {"w": "सामान्य", "start": 1.0, "end": 1.5},         # 0.5s - OK
                {"w": "सीमा", "start": 1.5, "end": 4.0},            # 2.5s - OK (not > 2.5)
                {"w": "असामान्य", "start": 4.0, "end": 18.0},        # 14.0s - SUSPICIOUS! (>2.5s)
                {"w": "उल्टा", "start": 20.0, "end": 19.5},          # End <= Start - SUSPICIOUS!
                {"w": "ऋणात्मक", "start": -1.0, "end": 0.5},        # Start < 0 - SUSPICIOUS!
                {"w": "अंतिम", "start": 22.0, "end": 22.8}          # 0.8s - OK
            ]
        }
    ]

    suspicious = detect_suspicious_words(rows, max_duration=2.5)
    assert len(suspicious) == 3, f"Expected 3 suspicious words, found {len(suspicious)}"

    dur_exceed = [s for s in suspicious if "duration_exceeds_threshold" in s["reasons"]]
    assert len(dur_exceed) == 1
    assert dur_exceed[0]["word"] == "असामान्य"
    assert dur_exceed[0]["duration"] == 14.0

    non_pos = [s for s in suspicious if "non_positive_duration" in s["reasons"]]
    assert len(non_pos) == 1
    assert non_pos[0]["word"] == "उल्टा"

    neg_ts = [s for s in suspicious if "negative_timestamp" in s["reasons"]]
    assert len(neg_ts) == 1
    assert neg_ts[0]["word"] == "ऋणात्मक"

    print("[PASS] test_detect_suspicious_words")


def test_group_suspicious_windows():
    suspicious_items = [
        {"start": 15.0, "end": 18.0, "word": "द"},
        {"start": 19.0, "end": 22.0, "word": "ब"},      # Clustered within padding
        {"start": 50.0, "end": 55.0, "word": "ना"}      # Distant window
    ]

    windows = group_suspicious_windows(suspicious_items, total_audio_duration=100.0, context_padding=2.0)
    assert len(windows) == 2, f"Expected 2 windows, got {len(windows)}"

    # Window 1: merges items at 15.0 and 19.0
    w1 = windows[0]
    assert w1["clip_start"] == 13.0  # 15.0 - 2.0
    assert w1["clip_end"] == 24.0    # 22.0 + 2.0
    assert len(w1["suspicious_items"]) == 2

    # Window 2: distant item at 50.0
    w2 = windows[1]
    assert w2["clip_start"] == 48.0  # 50.0 - 2.0
    assert w2["clip_end"] == 57.0    # 55.0 + 2.0
    assert len(w2["suspicious_items"]) == 1

    print("[PASS] test_group_suspicious_windows")


def test_offset_clip_timestamps():
    clip_rows = [
        {
            "start": 0.0,
            "end": 2.5,
            "text": "पूरी जानकारी",
            "words": [
                {"w": "पूरी", "start": 0.0, "end": 0.8},
                {"w": "जानकारी", "start": 0.8, "end": 2.5}
            ]
        }
    ]

    offset_res = offset_clip_timestamps(clip_rows, offset_seconds=15.0)
    assert offset_res[0]["start"] == 15.0
    assert offset_res[0]["end"] == 17.5
    assert offset_res[0]["words"][0]["start"] == 15.0
    assert offset_res[0]["words"][0]["end"] == 15.8
    assert offset_res[0]["words"][1]["start"] == 15.8
    assert offset_res[0]["words"][1]["end"] == 17.5

    print("[PASS] test_offset_clip_timestamps")


def test_is_retranscription_reliable():
    # 1. Valid rows
    valid_rows = [{
        "start": 0.0, "end": 2.0, "text": "सही",
        "words": [{"w": "सही", "start": 0.0, "end": 0.8}, {"w": "शब्द", "start": 0.8, "end": 1.8}]
    }]
    ok, reason = is_retranscription_reliable(valid_rows)
    assert ok is True
    assert reason is None

    # 2. Empty rows
    empty_rows = [{"start": 0.0, "end": 2.0, "text": "", "words": []}]
    ok, reason = is_retranscription_reliable(empty_rows)
    assert ok is False
    assert "produced_no_words" in reason

    # 3. Still contains frozen/long word > 2.5s
    bad_rows = [{
        "start": 0.0, "end": 5.0, "text": "खराब",
        "words": [{"w": "खराब", "start": 0.0, "end": 4.5}]
    }]
    ok, reason = is_retranscription_reliable(bad_rows)
    assert ok is False
    assert "contains_long_word" in reason

    # 4. Zero/negative duration word
    zero_rows = [{
        "start": 0.0, "end": 1.0, "text": "शून्य",
        "words": [{"w": "शून्य", "start": 0.5, "end": 0.5}]
    }]
    ok, reason = is_retranscription_reliable(zero_rows)
    assert ok is False
    assert "non_positive_duration" in reason

    print("[PASS] test_is_retranscription_reliable")


def test_merge_targeted_retranscription_deduplication():
    # Simulates the actual Kaggle freeze on 'द' (15.75s to 30.11s)
    orig_words = [
        {"w": "दर्शन", "start": 12.0, "end": 13.0},
        {"w": "की", "start": 13.0, "end": 13.5},
        {"w": "पूरी", "start": 13.5, "end": 14.5},
        {"w": "जानकारी", "start": 14.5, "end": 15.75},
        {"w": "द", "start": 15.75, "end": 30.11},  # Anomaly to be replaced!
        {"w": "हो", "start": 30.5, "end": 31.0},
        {"w": "जाती", "start": 31.0, "end": 31.5},
        {"w": "है", "start": 31.5, "end": 32.0}
    ]
    suspicious = [{"start": 15.75, "end": 30.11, "word": "द"}]

    # Clip starting at 13.75s (2s context before 15.75s)
    # Clip retranscribes the context words 'पूरी', 'जानकारी' as well as the missing words
    clip_offset_words = [
        {"w": "पूरी", "start": 13.75, "end": 14.5},      # Overlaps prefix
        {"w": "जानकारी", "start": 14.5, "end": 15.75},   # Matches last prefix word
        {"w": "दूंगा।", "start": 15.75, "end": 16.35},   # New corrected word!
        {"w": "अगर", "start": 16.35, "end": 16.85},     # New corrected word!
        {"w": "आप", "start": 16.85, "end": 17.15},       # New corrected word!
        {"w": "हो", "start": 30.5, "end": 31.0}          # Overlaps suffix
    ]

    merged_words, success, msg = merge_targeted_retranscription(
        all_words=orig_words,
        clip_words=clip_offset_words,
        suspicious_items=suspicious,
        clip_start=13.75,
        clip_end=32.11
    )

    assert success is True
    merged_texts = [w["w"] for w in merged_words]

    # Verify suspicious word 'द' was eliminated
    assert "द" not in merged_texts

    # Verify newly recovered words are present
    assert "दूंगा।" in merged_texts
    assert "अगर" in merged_texts
    assert "आप" in merged_texts

    # Verify context boundary words are NOT duplicated
    assert merged_texts.count("जानकारी") == 1
    assert merged_texts.count("पूरी") == 1
    assert merged_texts.count("हो") == 1

    # Verify timestamps are strictly sequential and non-overlapping
    for i in range(len(merged_words) - 1):
        assert merged_words[i]["start"] < merged_words[i + 1]["start"]
        assert merged_words[i]["end"] <= merged_words[i + 1]["start"]

    print("[PASS] test_merge_targeted_retranscription_deduplication")


def test_refine_transcript_with_mock_model():
    """Test full refine_transcript workflow using a mocked model."""
    orig_rows = [
        {
            "start": 0.0,
            "end": 32.0,
            "text": "दर्शन की पूरी जानकारी द हो जाती है",
            "words": [
                {"w": "दर्शन", "start": 12.0, "end": 13.0},
                {"w": "की", "start": 13.0, "end": 13.5},
                {"w": "पूरी", "start": 13.5, "end": 14.5},
                {"w": "जानकारी", "start": 14.5, "end": 15.75},
                {"w": "द", "start": 15.75, "end": 30.11},  # 14.36s anomaly!
                {"w": "हो", "start": 30.5, "end": 31.0},
                {"w": "जाती", "start": 31.0, "end": 31.5},
                {"w": "है", "start": 31.5, "end": 32.0}
            ]
        }
    ]

    # Mock audio array (e.g. 40 seconds of 16kHz silence)
    mock_audio = [0.0] * (40 * 16000)

    # Create mock WhisperModel
    mock_model = MagicMock()

    class MockWord:
        def __init__(self, w, s, e):
            self.word = w
            self.start = s
            self.end = e

    class MockSegment:
        def __init__(self, text, words):
            self.text = text
            self.start = words[0].start if words else 0.0
            self.end = words[-1].end if words else 0.0
            self.words = words

    # Mock transcribe returning corrected clip words
    def mock_transcribe(audio, **kwargs):
        # Clip relative words (relative to 0.0)
        corrected_words = [
            MockWord("पूरी", 0.0, 0.75),
            MockWord("जानकारी", 0.75, 2.0),
            MockWord("दूंगा।", 2.0, 2.6),
            MockWord("अगर", 2.6, 3.1),
            MockWord("आप", 3.1, 3.4),
            MockWord("हो", 16.75, 17.25)
        ]
        return [MockSegment("पूरी जानकारी दूंगा। अगर आप हो", corrected_words)], MagicMock()

    mock_model.transcribe.side_effect = mock_transcribe

    refined_rows, stats = refine_transcript(
        rows=orig_rows,
        audio_samples=mock_audio,
        language="hi",
        model=mock_model
    )

    assert stats["suspicious_count"] == 1
    assert stats["corrections_applied"] == 1
    assert len(stats["warnings"]) == 0

    refined_words = [w["w"] for r in refined_rows for w in r.get("words", [])]
    assert "द" not in refined_words
    assert "दूंगा।" in refined_words
    assert "अगर" in refined_words
    assert "आप" in refined_words

    print("[PASS] test_refine_transcript_with_mock_model")


def test_refine_transcript_uncertain_preserves_original():
    """Test that if targeted re-transcription fails or is uncertain, original is preserved with warning."""
    orig_rows = [
        {
            "start": 0.0,
            "end": 20.0,
            "text": "असामान्य भाग",
            "words": [
                {"w": "शुरुआत", "start": 0.0, "end": 1.0},
                {"w": "अटका", "start": 1.0, "end": 10.0},  # 9.0s anomaly!
                {"w": "समाप्त", "start": 10.0, "end": 11.0}
            ]
        }
    ]

    mock_audio = [0.0] * (25 * 16000)
    mock_model = MagicMock()

    class MockWord:
        def __init__(self, w, s, e):
            self.word = w
            self.start = s
            self.end = e

    class MockSegment:
        def __init__(self, text, words):
            self.text = text
            self.start = words[0].start if words else 0.0
            self.end = words[-1].end if words else 0.0
            self.words = words

    # Mock retranscription that STILL produces a frozen 6-second word
    def mock_bad_transcribe(audio, **kwargs):
        bad_words = [
            MockWord("अटका", 0.0, 6.0)  # Still > 2.5s!
        ]
        return [MockSegment("अटका", bad_words)], MagicMock()

    mock_model.transcribe.side_effect = mock_bad_transcribe

    refined_rows, stats = refine_transcript(
        rows=orig_rows,
        audio_samples=mock_audio,
        language="hi",
        model=mock_model
    )

    assert stats["suspicious_count"] == 1
    assert stats["corrections_applied"] == 0
    assert len(stats["warnings"]) == 1
    assert "uncertain" in stats["warnings"][0]

    # Verify original rows are completely preserved
    assert len(refined_rows) == 1
    orig_words_text = [w["w"] for w in refined_rows[0]["words"]]
    assert orig_words_text == ["शुरुआत", "अटका", "समाप्त"]
    assert "warning" in refined_rows[0]
    assert "uncertain" in refined_rows[0]["warning"]

    print("[PASS] test_refine_transcript_uncertain_preserves_original")


def test_configurable_initial_prompt():
    """Test that default Hindi prompt is used when None is passed, but can be overridden."""
    mock_model = MagicMock()
    mock_model.transcribe.return_value = ([], MagicMock(language="hi", language_probability=1.0))

    # 1. Default prompt test
    transcribe(audio=[], language="hi", initial_prompt=None, model=mock_model)
    _, kwargs = mock_model.transcribe.call_args
    assert kwargs.get("initial_prompt") == DEFAULT_HINDI_PROMPT

    # 2. Custom prompt test
    custom_prompt = "कस्टम द्वारकाधीश मंदिर"
    transcribe(audio=[], language="hi", initial_prompt=custom_prompt, model=mock_model)
    _, kwargs = mock_model.transcribe.call_args
    assert kwargs.get("initial_prompt") == custom_prompt

    print("[PASS] test_configurable_initial_prompt")


# ==============================================================================
# Fallback Clamping & Overlap / Out-of-Order Safety Tests
# ==============================================================================

from core.engine import clamp_unresolved_word_durations, FALLBACK_MAX_WORD_DURATION


def test_fallback_clamp_long_unresolved_word():
    """Test that a long unresolved word followed by normal silence gap is safely clamped to 1.5s."""
    rows = [
        {
            "start": 277.63,
            "end": 291.37,
            "text": "स्वय",
            "words": [{"w": "स्वय", "start": 277.63, "end": 291.37}]
        },
        {
            "start": 291.37,
            "end": 293.00,
            "text": "भगवान श्री कृष्ण",
            "words": [
                {"w": "भगवान", "start": 291.37, "end": 291.80},
                {"w": "श्री", "start": 291.80, "end": 292.20},
                {"w": "कृष्ण", "start": 292.20, "end": 293.00}
            ]
        }
    ]
    res, info = clamp_unresolved_word_durations(rows)
    w = res[0]["words"][0]
    assert info["clamped_count"] == 1
    assert w["end"] == 279.13, f"Expected 279.13, got {w['end']}"
    assert w["end"] <= 291.37, "Clamped end must not overlap next word onset"
    assert res[0]["end"] == 279.13, "Row end boundary must update to match clamped word"
    print("[PASS] test_fallback_clamp_long_unresolved_word")


def test_fallback_clamp_adjacent_overlapping_and_out_of_order_words():
    """Test safety handling when next word has out-of-order start, equal start, or overlapping start."""
    # Subtest A: Out-of-order / inverted start (nxt_start < start)
    rows_inverted = [
        {
            "start": 10.0,
            "end": 20.0,
            "text": "पहला",
            "words": [{"w": "पहला", "start": 10.0, "end": 20.0}]
        },
        {
            "start": 8.0,
            "end": 9.0,
            "text": "उल्टा",
            "words": [{"w": "उल्टा", "start": 8.0, "end": 9.0}]
        }
    ]
    res_a, info_a = clamp_unresolved_word_durations(rows_inverted)
    w_a = res_a[0]["words"][0]
    assert info_a["clamped_count"] == 0, "Must not clamp when next start is before cur start"
    assert w_a["end"] == 20.0, "Original positive duration must be preserved"
    assert len(info_a["anomalies"]) == 1, "Anomaly must be reported"
    assert "starts at or before it" in info_a["anomalies"][0]
    assert "warning" in w_a

    # Subtest B: Equal start (nxt_start == start)
    rows_equal = [
        {
            "start": 15.0,
            "end": 25.0,
            "text": "समान",
            "words": [{"w": "समान", "start": 15.0, "end": 25.0}]
        },
        {
            "start": 15.0,
            "end": 16.0,
            "text": "शब्द",
            "words": [{"w": "शब्द", "start": 15.0, "end": 16.0}]
        }
    ]
    res_b, info_b = clamp_unresolved_word_durations(rows_equal)
    w_b = res_b[0]["words"][0]
    assert info_b["clamped_count"] == 0
    assert w_b["end"] == 25.0
    assert len(info_b["anomalies"]) == 1

    # Subtest C: Insufficient gap (nxt_start - start < 0.05s)
    rows_tight = [
        {
            "start": 30.0,
            "end": 40.0,
            "text": "अतिनिकट",
            "words": [{"w": "अतिनिकट", "start": 30.0, "end": 40.0}]
        },
        {
            "start": 30.02,
            "end": 31.0,
            "text": "शब्द",
            "words": [{"w": "शब्द", "start": 30.02, "end": 31.0}]
        }
    ]
    res_c, info_c = clamp_unresolved_word_durations(rows_tight)
    w_c = res_c[0]["words"][0]
    assert info_c["clamped_count"] == 0
    assert w_c["end"] == 40.0
    assert "insufficient space" in info_c["anomalies"][0]

    print("[PASS] test_fallback_clamp_adjacent_overlapping_and_out_of_order_words")


def test_fallback_clamp_final_word():
    """Test that a long unresolved word at the very end of recording is clamped to fallback limit."""
    rows = [
        {
            "start": 600.0,
            "end": 614.76,
            "text": "समाप्ति",
            "words": [{"w": "समाप्ति", "start": 600.0, "end": 614.76}]
        }
    ]
    res, info = clamp_unresolved_word_durations(rows)
    w = res[0]["words"][0]
    assert info["clamped_count"] == 1
    assert w["end"] == 601.50, f"Expected 601.50, got {w['end']}"
    assert res[0]["end"] == 601.50
    print("[PASS] test_fallback_clamp_final_word")


def test_fallback_clamp_normal_words_untouched():
    """Test that words with duration <= 2.5s are never clamped."""
    rows = [
        {
            "start": 5.0,
            "end": 5.8,
            "text": "सामान्य",
            "words": [{"w": "सामान्य", "start": 5.0, "end": 5.8}]
        }
    ]
    res, info = clamp_unresolved_word_durations(rows)
    w = res[0]["words"][0]
    assert info["clamped_count"] == 0
    assert w["end"] == 5.8
    print("[PASS] test_fallback_clamp_normal_words_untouched")


def test_fallback_clamp_preserves_word_count_order_and_row_metadata():
    """Test that word count, word order, and row metadata are strictly preserved."""
    rows = [
        {
            "start": 1.0,
            "end": 15.0,
            "text": "पहला वाक्य जिसमें लंबा शब्द है",
            "custom_id": "job_123",
            "words": [
                {"w": "पहला", "start": 1.0, "end": 1.4},
                {"w": "वाक्य", "start": 1.4, "end": 1.8},
                {"w": "लंबा", "start": 1.8, "end": 15.0}
            ]
        },
        {
            "start": 20.0,
            "end": 21.0,
            "text": "दूसरा वाक्य",
            "custom_id": "job_124",
            "words": [
                {"w": "दूसरा", "start": 20.0, "end": 20.5},
                {"w": "वाक्य", "start": 20.5, "end": 21.0}
            ]
        }
    ]
    orig_words = [w["w"] for r in rows for w in r["words"]]
    res, info = clamp_unresolved_word_durations(rows)
    final_words = [w["w"] for r in res for w in r["words"]]

    assert orig_words == final_words, "Word order and text must be 100% preserved"
    assert len(final_words) == 5, "Word count must remain 5"
    assert res[0]["custom_id"] == "job_123", "Metadata preserved"
    assert res[0]["words"][2]["end"] == 3.30, f"Expected 3.30, got {res[0]['words'][2]['end']}"
    assert res[0]["end"] == 3.30, "Row end updated to match chronological max word end"
    print("[PASS] test_fallback_clamp_preserves_word_count_order_and_row_metadata")


def test_refine_transcript_integration_updated_rows_vs_rows():
    """Test that updated_rows vs rows selection preserves applied corrections and clamps unresolved words."""
    current_all_words = [
        {"w": "सुधरा", "start": 10.0, "end": 10.5},
        {"w": "शब्द", "start": 10.5, "end": 11.0},
        {"w": "अटका", "start": 50.0, "end": 64.0}
    ]
    updated_rows = [{
        "start": 10.0,
        "end": 64.0,
        "text": "सुधरा शब्द अटका",
        "words": current_all_words[:]
    }]
    stats = {"corrections_applied": 1, "warnings": []}

    target_rows = updated_rows if (stats["corrections_applied"] > 0 and current_all_words) else []
    final_rows, info = clamp_unresolved_word_durations(target_rows)
    stats["unresolved_clamped"] = info["clamped_count"]

    assert stats["corrections_applied"] == 1
    assert stats["unresolved_clamped"] == 1
    assert final_rows[0]["words"][0]["w"] == "सुधरा"
    assert final_rows[0]["words"][1]["w"] == "शब्द"
    assert final_rows[0]["words"][2]["w"] == "अटका"
    assert final_rows[0]["words"][2]["end"] == 51.5
    assert final_rows[0]["end"] == 51.5
    print("[PASS] test_refine_transcript_integration_updated_rows_vs_rows")


def test_invalid_row_boundaries_reported_without_fabrication():
    """Test that rows with invalid word boundaries (min start >= max end) report an anomaly without fabricating timestamps."""
    rows = [
        {
            "start": 1.0,
            "end": 15.0,
            "text": "सामान्य पंक्ति",
            "words": [{"w": "लंबा", "start": 1.0, "end": 15.0}]
        },
        {
            "start": 40.0,
            "end": 50.0,
            "text": "अवैध सीमा पंक्ति",
            "words": [{"w": "उल्टा", "start": 45.0, "end": 42.0}]
        }
    ]
    res, info = clamp_unresolved_word_durations(rows)
    assert info["clamped_count"] == 1
    # Row 0 clamped to 2.50s (start 1.0 + fallback 1.5)
    assert res[0]["end"] == 2.50
    # Row 1 has invalid word boundaries (min_start 45.0 >= max_end 42.0):
    # Must preserve original row bounds without fabricating invented timestamps
    assert res[1]["start"] == 40.0, f"Expected 40.0, got {res[1]['start']}"
    assert res[1]["end"] == 50.0, f"Expected 50.0, got {res[1]['end']}"
    assert res[1].get("anomaly") == "invalid_word_boundaries_reported"
    assert any("invalid word boundaries" in a for a in info["anomalies"])
    print("[PASS] test_invalid_row_boundaries_reported_without_fabrication")


def test_zero_and_negative_word_durations_reported_without_changes():
    """Test that words with zero or negative durations are reported without changing their timestamps."""
    rows = [
        {
            "start": 5.0,
            "end": 15.0,
            "text": "शून्य और ऋणात्मक अवधि परीक्षण",
            "words": [
                {"w": "शून्य", "start": 5.0, "end": 5.0},    # dur == 0.0
                {"w": "ऋणात्मक", "start": 8.0, "end": 6.0},  # dur == -2.0
                {"w": "सामान्य", "start": 10.0, "end": 10.8} # dur == 0.8 (normal)
            ]
        }
    ]
    res, info = clamp_unresolved_word_durations(rows)
    words = res[0]["words"]

    # 1. Zero duration word
    assert words[0]["start"] == 5.0, "Zero-duration word start must be preserved"
    assert words[0]["end"] == 5.0, "Zero-duration word end must be preserved without fabrication"
    assert words[0].get("anomaly") == "non_positive_word_duration"
    assert "non-positive duration" in words[0].get("warning", "")

    # 2. Negative duration word
    assert words[1]["start"] == 8.0, "Negative-duration word start must be preserved"
    assert words[1]["end"] == 6.0, "Negative-duration word end must be preserved without fabrication"
    assert words[1].get("anomaly") == "non_positive_word_duration"
    assert "non-positive duration" in words[1].get("warning", "")

    # 3. Normal word
    assert words[2]["start"] == 10.0
    assert words[2]["end"] == 10.8
    assert "warning" not in words[2]

    # Overall stats
    assert info["clamped_count"] == 0, "No clamps should occur on invalid or normal words"
    assert len(info["anomalies"]) == 2, "Both invalid duration words must be recorded in anomalies"
    print("[PASS] test_zero_and_negative_word_durations_reported_without_changes")


if __name__ == "__main__":
    print("=" * 60)
    print("RUNNING OFFLINE ENGINE UNIT TESTS (ENHANCED SUITE)")
    print("=" * 60)
    test_format_srt_timestamp()
    test_timestamp_validation_and_overlap_safety()
    test_timestamp_anomalies_equal_and_inverted_starts()
    test_hindi_chunking_and_word_preservation()
    test_srt_generation_and_save_outputs()
    test_detect_suspicious_words()
    test_group_suspicious_windows()
    test_offset_clip_timestamps()
    test_is_retranscription_reliable()
    test_merge_targeted_retranscription_deduplication()
    test_refine_transcript_with_mock_model()
    test_refine_transcript_uncertain_preserves_original()
    test_configurable_initial_prompt()
    test_fallback_clamp_long_unresolved_word()
    test_fallback_clamp_adjacent_overlapping_and_out_of_order_words()
    test_fallback_clamp_final_word()
    test_fallback_clamp_normal_words_untouched()
    test_fallback_clamp_preserves_word_count_order_and_row_metadata()
    test_refine_transcript_integration_updated_rows_vs_rows()
    test_invalid_row_boundaries_reported_without_fabrication()
    test_zero_and_negative_word_durations_reported_without_changes()
    print("=" * 60)
    print("ALL 21 OFFLINE UNIT TESTS PASSED SUCCESSFULLY!")
    print("=" * 60)
