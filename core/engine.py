"""
AI Video Engine - Canonical Core Engine
Consolidated pipeline for audio processing, Hindi transcription,
timestamp validation, SRT generation, targeted re-transcription, and export.
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger("ai_video_engine")

# Configurable project base directory
DEFAULT_BASE = "/kaggle/working/ai-video-engine"
BASE = os.environ.get("ENGINE_BASE_DIR", DEFAULT_BASE)

DEFAULT_HINDI_PROMPT = (
    "राधे राधे। प्यारे भक्तों, द्वारका, द्वारकाधीश, बेट द्वारका, गोपी तालाब, "
    "रुक्मिणी माता मंदिर, नागेश्वर ज्योतिर्लिंग, सुदर्शन सेतु, चार धाम, मथुरा।"
)

# Extra faster-whisper transcribe() options (hotwords, vad_parameters, beam_size...). Empty = defaults.
# Set from code or ENGINE_ASR_OPTIONS='{"hotwords": "..."}'. Used by tools/kaggle_remote/ab_whisper.py.
ASR_OPTIONS: Dict[str, Any] = {}
# Options used ONLY by repair / gap-fill re-transcription (e.g. a short hotword list). The A/B on
# 2026-10-28 showed hotwords on the whole first pass drop ~30% of words, so they never go there.
REPAIR_ASR_OPTIONS: Dict[str, Any] = {}
# Fixed sampling seed: faster-whisper falls back to temperature sampling on hard windows, and without
# a seed two identical runs differed by 9.4% WER (Kaggle A/B 2026-10-28). ENGINE_SEED=-1 disables.
SEED: int = int(os.environ.get("ENGINE_SEED", "1234"))

MAX_WORD_DURATION_THRESHOLD = 2.5  # seconds
CONTEXT_PADDING_SECONDS = 2.0      # seconds before and after suspicious region
FALLBACK_MAX_WORD_DURATION = 1.5   # seconds for unresolved anomalous words

_cached_model = None
_cached_model_key = None


def get_audio_duration(path: str) -> float:
    """Return duration of audio file in seconds using ffprobe."""
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Audio file not found: {path}")
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=nw=1:nk=1",
        str(path)
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
    out = res.stdout.strip()
    if not out:
        raise ValueError(f"Could not determine duration for: {path}")
    return float(out)


def cut_silence(src: str, dst: str, margin: str = "0.1s") -> None:
    """Remove silence from audio using auto-editor."""
    if not os.path.isfile(src):
        raise FileNotFoundError(f"Source file not found: {src}")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    cmd = ["auto-editor", str(src), "--margin", str(margin), "--no-open", "-o", str(dst)]
    subprocess.run(cmd, check=True)
    if not os.path.isfile(dst) or os.path.getsize(dst) == 0:
        raise RuntimeError(f"Silence cutting failed to produce output at: {dst}")


def load_audio(path: str):
    """Decode audio file to 16kHz mono float32 numpy array using ffmpeg."""
    import numpy as np
    if not os.path.isfile(path):
        raise FileNotFoundError(f"Audio file not found: {path}")
    cmd = [
        "ffmpeg", "-v", "error",
        "-i", str(path),
        "-f", "f32le",
        "-ar", "16000",
        "-ac", "1",
        "-"
    ]
    res = subprocess.run(cmd, capture_output=True, check=True)
    audio = np.frombuffer(res.stdout, dtype=np.float32)
    if audio.size == 0:
        raise RuntimeError(f"Audio decoding produced 0 samples for: {path}")
    return audio


def get_model(
    model_size: str = "large-v3-turbo",
    device: Optional[str] = None,
    compute_type: Optional[str] = None
):
    """
    Load and cache WhisperModel by model/device/compute configuration.
    GPU is preferred by default. Set ENGINE_DEVICE=cpu or pass device="cpu" for testing.
    """
    global _cached_model, _cached_model_key

    from faster_whisper import WhisperModel

    if device is None:
        device = os.environ.get("ENGINE_DEVICE", "cuda").strip().lower()
    else:
        device = device.strip().lower()

    if device not in {"cuda", "cpu"}:
        raise ValueError(f"Unsupported device {device!r}; choose 'cuda' or 'cpu'.")

    if device == "cuda":
        try:
            import torch
        except Exception as exc:
            raise RuntimeError(
                "CUDA was requested but PyTorch could not be imported. "
                "Use a Kaggle GPU runtime or explicitly set ENGINE_DEVICE=cpu for CPU testing."
            ) from exc
        if not torch.cuda.is_available():
            raise RuntimeError(
                "CUDA was requested, but torch.cuda.is_available() is False. "
                "Enable a GPU accelerator in Kaggle. For intentional CPU testing only, "
                "set ENGINE_DEVICE=cpu or pass device='cpu'."
            )

    if compute_type is None:
        compute_type = os.environ.get("ENGINE_COMPUTE_TYPE") or ("float16" if device == "cuda" else "int8")

    cache_key = (model_size, device, compute_type)
    if _cached_model is not None and _cached_model_key == cache_key:
        return _cached_model

    _cached_model = WhisperModel(model_size, device=device, compute_type=compute_type)
    _cached_model_key = cache_key
    return _cached_model


def transcribe(
    audio: Any,
    language: str = "hi",
    initial_prompt: Optional[str] = None,
    model_size: str = "large-v3-turbo",
    vad_filter: bool = True,
    model: Any = None,
    extra_opts: Optional[Dict[str, Any]] = None
) -> Tuple[List[Dict[str, Any]], Any]:
    """
    Transcribe audio with faster-whisper.
    Preserves exact spoken Hindi words and timestamps without alteration.
    Uses default Hindi domain prompt if none supplied.
    """
    if model is None:
        model = get_model(model_size=model_size)

    prompt = initial_prompt if initial_prompt is not None else (
        DEFAULT_HINDI_PROMPT if language == "hi" else None
    )

    kwargs: Dict[str, Any] = {
        "language": language,
        "vad_filter": vad_filter,
        "word_timestamps": True,
        "condition_on_previous_text": False
    }
    if prompt:
        kwargs["initial_prompt"] = prompt
    env_opts = os.environ.get("ENGINE_ASR_OPTIONS")
    kwargs.update(json.loads(env_opts) if env_opts else {})
    kwargs.update(ASR_OPTIONS)
    kwargs.update(extra_opts or {})

    if SEED >= 0:
        try:
            import ctranslate2
            ctranslate2.set_random_seed(SEED)
        except Exception:  # older ctranslate2 / mocked engine: run unseeded
            pass

    segments, info = model.transcribe(audio, **kwargs)

    rows = []
    for s in segments:
        words = []
        for w in (s.words or []):
            clean_word = w.word.replace("\ufffd", "").strip()
            if clean_word:
                words.append({
                    "w": clean_word,
                    "start": round(float(w.start), 2),
                    "end": round(float(w.end), 2),
                    "p": round(float(getattr(w, "probability", 1.0) or 0.0), 3)
                })

        clean_text = s.text.replace("\ufffd", "").strip()
        rows.append({
            "start": round(float(s.start), 2),
            "end": round(float(s.end), 2),
            "text": clean_text,
            "words": words
        })

    return rows, info


# ==============================================================================
# Suspicious Timestamp Detection & Bounded Targeted Re-transcription
# ==============================================================================

def detect_suspicious_words(
    rows: List[Dict[str, Any]],
    max_duration: float = MAX_WORD_DURATION_THRESHOLD
) -> List[Dict[str, Any]]:
    """
    Scan transcript rows and flag:
    1. Word timestamps longer than max_duration (default 2.5s)
    2. Clearly invalid timestamps (end <= start, negative timestamps)
    """
    suspicious = []
    for s_idx, row in enumerate(rows):
        words = row.get("words", [])
        for w_idx, w in enumerate(words):
            start = float(w.get("start", 0.0))
            end = float(w.get("end", 0.0))
            dur = end - start
            reasons = []

            if start < 0 or end < 0:
                reasons.append("negative_timestamp")
            if end <= start:
                reasons.append("non_positive_duration")
            elif dur > max_duration:
                reasons.append("duration_exceeds_threshold")

            if reasons:
                suspicious.append({
                    "segment_idx": s_idx,
                    "word_idx": w_idx,
                    "word": w.get("w", ""),
                    "start": round(start, 2),
                    "end": round(end, 2),
                    "duration": round(dur, 2),
                    "reasons": reasons
                })
    return suspicious


def group_suspicious_windows(
    suspicious_items: List[Dict[str, Any]],
    total_audio_duration: float,
    context_padding: float = CONTEXT_PADDING_SECONDS,
    max_window_duration: float = 35.0
) -> List[Dict[str, Any]]:
    """
    Group clustered suspicious words into bounded [clip_start, clip_end] windows
    with context padding before and after.
    """
    if not suspicious_items:
        return []

    sorted_items = sorted(suspicious_items, key=lambda x: (x["start"], x["end"]))
    windows = []

    cur_start = sorted_items[0]["start"]
    cur_end = sorted_items[0]["end"]
    cur_items = [sorted_items[0]]

    for item in sorted_items[1:]:
        if item["start"] <= cur_end + (context_padding * 2):
            cur_end = max(cur_end, item["end"])
            cur_items.append(item)
        else:
            clip_start = max(0.0, cur_start - context_padding)
            clip_end = min(total_audio_duration, cur_end + context_padding)
            if clip_end - clip_start > max_window_duration:
                clip_end = clip_start + max_window_duration
            windows.append({
                "clip_start": round(clip_start, 2),
                "clip_end": round(clip_end, 2),
                "suspicious_items": cur_items
            })
            cur_start = item["start"]
            cur_end = item["end"]
            cur_items = [item]

    clip_start = max(0.0, cur_start - context_padding)
    clip_end = min(total_audio_duration, cur_end + context_padding)
    if clip_end - clip_start > max_window_duration:
        clip_end = clip_start + max_window_duration
    windows.append({
        "clip_start": round(clip_start, 2),
        "clip_end": round(clip_end, 2),
        "suspicious_items": cur_items
    })
    return windows


def offset_clip_timestamps(
    clip_rows: List[Dict[str, Any]],
    offset_seconds: float
) -> List[Dict[str, Any]]:
    """
    Offset all segment and word timestamps in clip_rows by offset_seconds.
    """
    offset_rows = []
    for r in clip_rows:
        new_row = {
            "start": round(float(r["start"]) + offset_seconds, 2),
            "end": round(float(r["end"]) + offset_seconds, 2),
            "text": r.get("text", ""),
            "words": []
        }
        for w in r.get("words", []):
            new_row["words"].append({
                "w": w["w"],
                "start": round(float(w["start"]) + offset_seconds, 2),
                "end": round(float(w["end"]) + offset_seconds, 2)
            })
        offset_rows.append(new_row)
    return offset_rows


def is_retranscription_reliable(
    clip_rows: List[Dict[str, Any]],
    max_word_duration: float = MAX_WORD_DURATION_THRESHOLD
) -> Tuple[bool, Optional[str]]:
    """
    Verify whether re-transcription output is reliable:
    - Must contain at least one valid word.
    - Must NOT contain any word with duration > max_word_duration.
    - All word start/end times must be non-negative and positive duration.
    """
    words = [w for r in clip_rows for w in r.get("words", [])]
    if not words:
        return False, "retranscription_produced_no_words"

    for w in words:
        dur = w["end"] - w["start"]
        if dur <= 0:
            return False, f"retranscription_has_non_positive_duration_word: {w['w']}"
        if dur > max_word_duration:
            return False, f"retranscription_still_contains_long_word ({w['w']}: {dur:.2f}s)"

    return True, None


def clean_hindi_token(t: str) -> str:
    """Normalize Hindi token for matching by stripping punctuation and whitespace."""
    return re.sub(r"[।?!.,\s\-]", "", t)


def merge_targeted_retranscription(
    all_words: List[Dict[str, Any]],
    clip_words: List[Dict[str, Any]],
    suspicious_items: List[Dict[str, Any]],
    clip_start: float,
    clip_end: float
) -> Tuple[List[Dict[str, Any]], bool, str]:
    """
    Merge retranscribed clip_words into all_words, replacing the suspicious region
    without duplicating boundary words, dropping valid words, or creating timestamp overlaps.
    """
    if not clip_words:
        return all_words, False, "no_clip_words"

    # Identify the index range of suspicious items in all_words
    susp_ids = set()
    for s in suspicious_items:
        for idx, w in enumerate(all_words):
            if (round(float(w["start"]), 2) == round(float(s["start"]), 2) and
                round(float(w["end"]), 2) == round(float(s["end"]), 2) and
                w.get("w", "").strip() == s.get("word", "").strip()):
                susp_ids.add(idx)

    if not susp_ids:
        susp_start = min(s["start"] for s in suspicious_items)
        susp_end = max(s["end"] for s in suspicious_items)
        first_susp_idx = None
        last_susp_idx = None
        for idx, w in enumerate(all_words):
            if w["start"] >= susp_start - 0.05 and w["end"] <= susp_end + 0.05:
                if first_susp_idx is None:
                    first_susp_idx = idx
                last_susp_idx = idx
    else:
        first_susp_idx = min(susp_ids)
        last_susp_idx = max(susp_ids)

    if first_susp_idx is None:
        return all_words, False, "could_not_locate_suspicious_words_in_transcript"

    # Guaranteed preservation of all valid words before and after
    prefix_words = all_words[:first_susp_idx]
    suffix_words = all_words[last_susp_idx + 1:]

    # Deduplicate boundary context from clip_words
    replacement_words = clip_words[:]

    # Deduplicate against prefix_words
    if prefix_words:
        last_pref = prefix_words[-1]
        last_pref_norm = clean_hindi_token(last_pref["w"])
        trim_prefix_count = 0
        for i, cw in enumerate(replacement_words):
            cw_norm = clean_hindi_token(cw["w"])
            if cw["end"] <= last_pref["end"] + 0.05:
                trim_prefix_count = i + 1
            elif cw["start"] < last_pref["end"] and cw_norm == last_pref_norm:
                trim_prefix_count = i + 1
            else:
                break
        replacement_words = replacement_words[trim_prefix_count:]

    # Deduplicate against suffix_words
    if suffix_words:
        first_suff = suffix_words[0]
        first_suff_norm = clean_hindi_token(first_suff["w"])
        trim_suffix_count = 0
        for i in range(len(replacement_words) - 1, -1, -1):
            cw = replacement_words[i]
            cw_norm = clean_hindi_token(cw["w"])
            if cw["start"] >= first_suff["start"] - 0.05:
                trim_suffix_count += 1
            elif cw["end"] > first_suff["start"] and cw_norm == first_suff_norm:
                trim_suffix_count += 1
            else:
                break
        if trim_suffix_count > 0:
            replacement_words = replacement_words[:-trim_suffix_count]

    if not replacement_words:
        return all_words, False, "no_replacement_words_remaining_after_dedup"

    # Assemble complete merged words
    merged = prefix_words + replacement_words + suffix_words

    # Timestamp continuity validation: ensure non-overlapping, strictly increasing
    for i in range(len(merged) - 1):
        cur = merged[i]
        nxt = merged[i + 1]
        if cur["end"] > nxt["start"]:
            if nxt["start"] > cur["start"]:
                cur["end"] = nxt["start"]
            else:
                cur["end"] = round(cur["start"] + 0.05, 2)
                nxt["start"] = cur["end"]
                if nxt["end"] <= nxt["start"]:
                    nxt["end"] = round(nxt["start"] + 0.05, 2)

    return merged, True, "success"


def clamp_unresolved_word_durations(
    rows: List[Dict[str, Any]],
    max_duration: float = MAX_WORD_DURATION_THRESHOLD,
    fallback_duration: float = FALLBACK_MAX_WORD_DURATION,
    min_duration: float = 0.05
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Safely clamp any remaining word durations that exceed max_duration after refinement.
    Guarantees:
    1. Validates non-positive duration (dur <= 0) first; reports anomaly without fabricating timestamps.
    2. Validates the affected word and neighboring timestamps before clamping.
    3. Never creates an end timestamp <= start, and never creates a new overlap.
    4. If space is insufficient or neighbor timestamps are out-of-order, logs a warning
       and preserves original timestamps without fabricating invalid timings.
    5. Preserves all original words, metadata, and word order.
    6. Re-syncs row boundaries using validated chronological bounds (min start, max end)
       when valid; if word bounds are invalid, reports anomaly without inventing timestamps.
    """
    all_words = [w for r in rows for w in r.get("words", [])]
    clamped_count = 0
    anomalies: List[str] = []

    for i, w in enumerate(all_words):
        start = float(w.get("start", 0.0))
        end = float(w.get("end", 0.0))
        dur = end - start

        # 1. Validate word's own timestamps: zero or negative duration
        if dur <= 0:
            msg = (
                f"Word '{w.get('w')}' has non-positive duration [{start}s -> {end}s]. "
                "Preserving original timestamps without fabricating duration."
            )
            logger.warning(f"[Clamp Anomaly] {msg}")
            anomalies.append(msg)
            w["warning"] = msg
            w["anomaly"] = "non_positive_word_duration"
            continue

        # 2. Only process words that exceed max_duration
        if dur <= max_duration:
            continue

        # Validate preceding neighbor if present
        if i > 0:
            prev = all_words[i - 1]
            prev_end = float(prev.get("end", 0.0))
            if prev_end > start:
                msg = (
                    f"Word '{w.get('w')}' at {start}s overlaps preceding word '{prev.get('w')}' "
                    f"(ends at {prev_end}s). Proceeding with cautious clamp."
                )
                logger.info(f"[Clamp Note] {msg}")

        target_end = round(start + fallback_duration, 2)
        has_next = (i + 1 < len(all_words))

        if has_next:
            nxt = all_words[i + 1]
            nxt_start = float(nxt.get("start", 0.0))

            if nxt_start <= start:
                msg = (
                    f"Word '{w.get('w')}' [{start}s -> {end}s] cannot be clamped: next word '{nxt.get('w')}' "
                    f"starts at or before it ({nxt_start}s <= {start}s). Preserving original duration with warning."
                )
                logger.warning(f"[Clamp Anomaly] {msg}")
                anomalies.append(msg)
                w["warning"] = msg
                w["anomaly"] = "cannot_clamp_inverted_or_equal_next_start"
                continue

            available = nxt_start - start
            if available < min_duration:
                msg = (
                    f"Word '{w.get('w')}' [{start}s -> {end}s] cannot be clamped: insufficient space before "
                    f"next word '{nxt.get('w')}' at {nxt_start}s ({available:.3f}s < {min_duration}s). Preserving original duration."
                )
                logger.warning(f"[Clamp Anomaly] {msg}")
                anomalies.append(msg)
                w["warning"] = msg
                w["anomaly"] = "cannot_clamp_insufficient_space_before_next_word"
                continue

            safe_end = min(end, target_end, nxt_start)
            if safe_end - start < min_duration:
                safe_end = round(start + min_duration, 3)
                if safe_end > nxt_start:
                    safe_end = nxt_start
        else:
            safe_end = min(end, target_end)
            if safe_end - start < min_duration:
                safe_end = round(start + min_duration, 3)

        if safe_end - start >= min_duration and safe_end < end:
            w["end"] = round(safe_end, 2)
            clamped_count += 1
            logger.info(f"[Clamp Applied] Clamped word '{w.get('w')}' from {dur:.2f}s to {w['end'] - start:.2f}s.")
        else:
            msg = f"Word '{w.get('w')}' [{start}s -> {end}s] cannot be safely clamped to positive duration without overlap. Preserving original timestamps."
            logger.warning(f"[Clamp Anomaly] {msg}")
            anomalies.append(msg)
            w["warning"] = msg

    # Re-sync row boundaries using validated chronological bounds without fabricating timestamps
    if clamped_count > 0:
        for r in rows:
            words = r.get("words", [])
            if words:
                w_starts = [float(x["start"]) for x in words if "start" in x]
                w_ends = [float(x["end"]) for x in words if "end" in x]
                if w_starts and w_ends:
                    min_s = round(min(w_starts), 2)
                    max_e = round(max(w_ends), 2)
                    if max_e <= min_s:
                        msg = (
                            f"Row '{r.get('text', '')}' has invalid word boundaries "
                            f"(min start {min_s}s >= max end {max_e}s). "
                            "Preserving original row bounds without fabricating timestamps."
                        )
                        logger.warning(f"[Row Anomaly] {msg}")
                        anomalies.append(msg)
                        r["warning"] = msg
                        r["anomaly"] = "invalid_word_boundaries_reported"
                    else:
                        r["start"] = min_s
                        r["end"] = max_e

    info = {
        "clamped_count": clamped_count,
        "anomalies": anomalies
    }
    return rows, info


def refine_transcript(
    rows: List[Dict[str, Any]],
    audio_samples: Any,
    language: str = "hi",
    initial_prompt: Optional[str] = None,
    model_size: str = "large-v3-turbo",
    max_word_duration: float = MAX_WORD_DURATION_THRESHOLD,
    context_padding: float = CONTEXT_PADDING_SECONDS,
    model: Any = None,
    total_duration: Optional[float] = None
) -> Tuple[List[Dict[str, Any]], Dict[str, Any]]:
    """
    Detect suspicious word timestamps (>2.5s) and perform bounded targeted re-transcription.
    If correction is reliable, replaces suspicious regions without duplicate words.
    If correction is uncertain or fails, preserves existing transcript and records warnings.
    """
    suspicious_items = detect_suspicious_words(rows, max_duration=max_word_duration)
    stats: Dict[str, Any] = {
        "suspicious_count": len(suspicious_items),
        "windows_attempted": 0,
        "corrections_applied": 0,
        "warnings": []
    }

    if not suspicious_items:
        return rows, stats

    if total_duration is None:
        try:
            total_duration = float(len(audio_samples) / 16000)
        except Exception:
            total_duration = float(rows[-1]["end"]) if rows else 0.0

    windows = group_suspicious_windows(
        suspicious_items,
        total_audio_duration=total_duration,
        context_padding=context_padding
    )

    stats["windows_attempted"] = len(windows)
    current_all_words = [w for r in rows for w in r.get("words", [])]

    for win in windows:
        c_start = win["clip_start"]
        c_end = win["clip_end"]
        items = win["suspicious_items"]

        # Slice audio clip for targeted retranscription
        try:
            start_sample = max(0, int(c_start * 16000))
            end_sample = min(len(audio_samples), int(c_end * 16000))
            clip_samples = audio_samples[start_sample:end_sample]

            if len(clip_samples) == 0:
                raise ValueError("Audio clip slice produced 0 samples")

            clip_rows, _ = transcribe(
                audio=clip_samples,
                language=language,
                initial_prompt=initial_prompt,
                model_size=model_size,
                model=model
            )

            offset_rows = offset_clip_timestamps(clip_rows, offset_seconds=c_start)
            reliable, reason = is_retranscription_reliable(offset_rows, max_word_duration=max_word_duration)

            if not reliable:
                warn_msg = (
                    f"Suspicious region [{c_start}s - {c_end}s] re-transcription uncertain: {reason}. "
                    "Original transcript preserved."
                )
                logger.warning(f"[Refine Transcript] {warn_msg}")
                stats["warnings"].append(warn_msg)
                # Attach warning to affected segments
                for it in items:
                    s_idx = it["segment_idx"]
                    if s_idx < len(rows):
                        rows[s_idx]["warning"] = warn_msg
                continue

            clip_words = [w for r in offset_rows for w in r.get("words", [])]
            new_all_words, merged_ok, merge_msg = merge_targeted_retranscription(
                all_words=current_all_words,
                clip_words=clip_words,
                suspicious_items=items,
                clip_start=c_start,
                clip_end=c_end
            )

            if merged_ok:
                current_all_words = new_all_words
                stats["corrections_applied"] += 1
                logger.info(f"[Refine Transcript] Successfully corrected suspicious region [{c_start}s - {c_end}s].")
            else:
                warn_msg = (
                    f"Suspicious region [{c_start}s - {c_end}s] merge skipped: {merge_msg}. "
                    "Original transcript preserved."
                )
                logger.warning(f"[Refine Transcript] {warn_msg}")
                stats["warnings"].append(warn_msg)
                for it in items:
                    s_idx = it["segment_idx"]
                    if s_idx < len(rows):
                        rows[s_idx]["warning"] = warn_msg

        except Exception as exc:
            warn_msg = (
                f"Suspicious region [{c_start}s - {c_end}s] re-transcription encountered error: {exc}. "
                "Original transcript preserved."
            )
            logger.warning(f"[Refine Transcript] {warn_msg}")
            stats["warnings"].append(warn_msg)
            for it in items:
                s_idx = it["segment_idx"]
                if s_idx < len(rows):
                    rows[s_idx]["warning"] = warn_msg

    # If corrections were applied, rebuild rows from the updated word sequence
    if stats["corrections_applied"] > 0 and current_all_words:
        # Group words back into segments based on sentence boundaries or chunks
        updated_rows = []
        cur_words: List[Dict[str, Any]] = []

        for w in current_all_words:
            cur_words.append(w)
            is_end = w["w"] and (w["w"][-1] in "।?!.,")
            if is_end or len(cur_words) >= 14:
                seg_text = " ".join(x["w"] for x in cur_words).strip()
                updated_rows.append({
                    "start": cur_words[0]["start"],
                    "end": cur_words[-1]["end"],
                    "text": seg_text,
                    "words": cur_words[:]
                })
                cur_words.clear()

        if cur_words:
            seg_text = " ".join(x["w"] for x in cur_words).strip()
            updated_rows.append({
                "start": cur_words[0]["start"],
                "end": cur_words[-1]["end"],
                "text": seg_text,
                "words": cur_words[:]
            })

    active_rows = updated_rows if (stats["corrections_applied"] > 0 and current_all_words) else rows
    final_rows, clamp_info = clamp_unresolved_word_durations(
        active_rows,
        max_duration=max_word_duration
    )
    stats["unresolved_clamped"] = clamp_info["clamped_count"]
    if clamp_info["anomalies"]:
        stats["warnings"].extend(clamp_info["anomalies"])

    return final_rows, stats


# ==============================================================================
# Timestamp Validation, Chunking, and SRT Formatting
# ==============================================================================

def validate_and_fix_timestamps(
    chunks: List[Dict[str, Any]],
    min_duration: float = 0.05
) -> List[Dict[str, Any]]:
    """
    Validate timestamps and resolve overlaps while strictly preserving speech sync.
    Guarantees:
    1. start >= 0
    2. end > start (positive segment duration)
    3. No overlapping adjacent chunks (chunks[i]['end'] <= chunks[i+1]['start'])
    4. Speech onset (nxt['start']) is NEVER shifted forward into the future for normal speech.
    5. Anomalous timestamps (equal starts, inverted starts) are explicitly flagged with warnings.
    """
    if not chunks:
        return []

    for i, c in enumerate(chunks):
        c["start"] = max(0.0, round(float(c["start"]), 3))
        raw_end = round(float(c["end"]), 3)
        if raw_end <= c["start"]:
            c["anomaly"] = "zero_or_negative_duration"
            c["end"] = round(c["start"] + min_duration, 3)
            logger.warning(
                f"[Timestamp Warning] Chunk {i} ('{c.get('text', '')}') had non-positive duration "
                f"({c['start']} -> {raw_end}). Clamped end to {c['end']}."
            )
        else:
            c["end"] = raw_end

    for i in range(len(chunks) - 1):
        cur = chunks[i]
        nxt = chunks[i + 1]

        if nxt["start"] < cur["start"]:
            nxt["anomaly"] = "inverted_start"
            logger.warning(
                f"[Timestamp Anomaly] Chunk {i+1} starts at {nxt['start']}s before Chunk {i} starts at {cur['start']}s. "
                f"Flagged anomaly without shifting speech timing."
            )
            if cur["end"] <= cur["start"]:
                cur["end"] = round(cur["start"] + min_duration, 3)
            continue

        if nxt["start"] == cur["start"]:
            nxt["anomaly"] = "equal_start"
            logger.warning(
                f"[Timestamp Anomaly] Chunk {i} and Chunk {i+1} have identical start time ({cur['start']}s). "
                f"Flagged anomaly without shifting speech timing."
            )
            if cur["end"] <= cur["start"]:
                cur["end"] = round(cur["start"] + min_duration, 3)
            continue

        if cur["end"] > nxt["start"]:
            cur["end"] = nxt["start"]
            if cur["end"] - cur["start"] < min_duration:
                cur["warning"] = "short_duration_segment"
                logger.info(
                    f"[Timestamp Note] Chunk {i} clamped to {cur['end']}s to yield to speech onset of Chunk {i+1}. "
                    f"Duration is {round(cur['end'] - cur['start'], 3)}s."
                )

    return chunks


def chunk_words(
    rows: List[Dict[str, Any]],
    max_words: int = 7,
    max_chars: int = 40,
    gap: float = 0.6,
    min_duration: float = 0.05
) -> List[Dict[str, Any]]:
    """
    Group words into subtitle lines adhering to Hindi punctuation (।?!.,)
    and word limits without altering spoken words.
    Validates timestamps to guarantee positive duration.
    """
    words = [w for r in rows for w in r.get("words", [])]
    if not words:
        fallback = [
            {"start": r["start"], "end": r["end"], "text": r["text"]}
            for r in rows if r.get("text", "").strip()
        ]
        return validate_and_fix_timestamps(fallback, min_duration=min_duration)

    chunks: List[Dict[str, Any]] = []
    cur: List[Dict[str, Any]] = []

    def flush():
        if cur:
            chunk_text = " ".join(w["w"] for w in cur).strip()
            if chunk_text:
                chunks.append({
                    "start": cur[0]["start"],
                    "end": cur[-1]["end"],
                    "text": chunk_text
                })
            cur.clear()

    for w in words:
        if cur and (w["start"] - cur[-1]["end"]) > gap:
            flush()

        cur.append(w)
        current_text = " ".join(x["w"] for x in cur)

        is_punct = w["w"] and (w["w"][-1] in "।?!.,")
        if len(cur) >= max_words or len(current_text) >= max_chars or (is_punct and len(cur) >= 3):
            flush()

    flush()
    return validate_and_fix_timestamps(chunks, min_duration=min_duration)


def format_srt_timestamp(seconds: float) -> str:
    """Format float seconds into SRT timestamp string HH:MM:SS,mmm."""
    ms = round(seconds * 1000)
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def generate_srt(chunks: List[Dict[str, Any]]) -> str:
    """Generate SRT formatted string from subtitle chunks."""
    blocks = []
    for i, c in enumerate(chunks, 1):
        start_ts = format_srt_timestamp(c["start"])
        end_ts = format_srt_timestamp(c["end"])
        blocks.append(f"{i}\n{start_ts} --> {end_ts}\n{c['text']}\n")
    return "\n".join(blocks)


def save_outputs(
    rows: List[Dict[str, Any]],
    folder: str,
    min_duration: float = 0.05
) -> Tuple[str, str]:
    """Save transcripts as transcript.srt and transcript.json."""
    os.makedirs(folder, exist_ok=True)
    chunks = chunk_words(rows, min_duration=min_duration)
    srt_content = generate_srt(chunks)

    srt_path = os.path.join(folder, "transcript.srt")
    json_path = os.path.join(folder, "transcript.json")

    with open(srt_path, "w", encoding="utf-8") as f:
        f.write(srt_content)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    return srt_path, json_path


def run_pipeline(
    src: str,
    job_name: str,
    cut: bool = False,
    language: str = "hi",
    initial_prompt: Optional[str] = None,
    model_size: str = "large-v3-turbo",
    max_word_duration: float = MAX_WORD_DURATION_THRESHOLD
) -> Dict[str, Any]:
    """Execute transcription and subtitle pipeline for an audio source."""
    if not os.path.isfile(src):
        raise FileNotFoundError(f"Input audio file not found: {src}")

    out_dir = os.path.join(BASE, "storage", "outputs", job_name)
    os.makedirs(out_dir, exist_ok=True)

    audio_path = src
    if cut:
        temp_dir = os.path.join(BASE, "storage", "temp")
        os.makedirs(temp_dir, exist_ok=True)
        work = os.path.join(temp_dir, f"{job_name}_cut.mp3")
        cut_silence(src, work)
        audio_path = work

    shutil.copy2(audio_path, os.path.join(out_dir, "audio_used.mp3"))

    audio_samples = load_audio(audio_path)
    prompt = initial_prompt if initial_prompt is not None else DEFAULT_HINDI_PROMPT

    rows, info = transcribe(
        audio=audio_samples,
        language=language,
        initial_prompt=prompt,
        model_size=model_size
    )

    # Apply suspicious timestamp detector and targeted re-transcription
    rows, refine_stats = refine_transcript(
        rows=rows,
        audio_samples=audio_samples,
        language=language,
        initial_prompt=prompt,
        model_size=model_size,
        max_word_duration=max_word_duration
    )

    srt_path, json_path = save_outputs(rows, out_dir)
    chunks = chunk_words(rows)

    return {
        "job_name": job_name,
        "audio_used": os.path.join(out_dir, "audio_used.mp3"),
        "srt_path": srt_path,
        "json_path": json_path,
        "segment_count": len(rows),
        "subtitle_line_count": len(chunks),
        "refine_stats": refine_stats
    }
