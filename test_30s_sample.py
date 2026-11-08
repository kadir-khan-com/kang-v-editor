"""
AI Video Engine - 30-Second Audio Slice Test (Stage 4)
This script verifies Hindi transcription accuracy and SRT generation
on only the first 30 seconds of the voiceover audio.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.engine import (
    load_audio,
    transcribe,
    refine_transcript,
    chunk_words,
    generate_srt,
    save_outputs,
    BASE,
    DEFAULT_HINDI_PROMPT
)

SAMPLE_DURATION_SEC = 30
TEST_OUTPUT_DIR = os.path.join(BASE, "storage", "outputs", "test_30s")
HINDI_PROMPT = DEFAULT_HINDI_PROMPT


def find_voiceover_audio() -> str:
    """
    Deterministically locate the Dwarika voiceover audio.
    Stops with clear error if ambiguous or missing.
    """
    # Priority 1: Check storage/inputs/voiceover.mp3
    target = os.path.join(BASE, "storage", "inputs", "voiceover.mp3")
    if os.path.isfile(target) and os.path.getsize(target) > 0:
        return target

    # Priority 2: Check storage/inputs/voice.mp3
    legacy_target = os.path.join(BASE, "storage", "inputs", "voice.mp3")
    if os.path.isfile(legacy_target) and os.path.getsize(legacy_target) > 0:
        return legacy_target

    # Priority 3: Search /kaggle/input deterministically
    input_path = Path(os.environ.get("KAGGLE_INPUT_DIR", "/kaggle/input"))
    if not input_path.exists():
        raise FileNotFoundError(
            f"Voiceover not found in storage/inputs/voiceover.mp3 and /kaggle/input does not exist."
        )

    # 3a. Exact filename match for '6 Dwarika enhanced.mp3'
    exact = list(input_path.rglob("6 Dwarika enhanced.mp3"))
    if exact:
        return str(exact[0])

    # 3b. Search for dwarika / voiceover candidates
    all_audios = [
        p for p in input_path.rglob("*")
        if p.is_file() and p.suffix.lower() in [".mp3", ".wav", ".m4a", ".aac"]
    ]
    dwarika_cand = [
        p for p in all_audios
        if "dwarika" in p.name.lower() or "voiceover" in p.name.lower()
    ]

    if len(dwarika_cand) == 1:
        return str(dwarika_cand[0])
    elif len(dwarika_cand) > 1:
        cand_list = "\n  - ".join(f"{p} ({round(p.stat().st_size/(1024*1024), 2)} MB)" for p in dwarika_cand)
        raise RuntimeError(
            f"AMBIGUOUS AUDIO: Multiple Dwarika/voiceover candidates found in /kaggle/input:\n  - {cand_list}\n"
            f"Please specify the exact file path to proceed."
        )
    else:
        other_list = "\n  - ".join(f"{p} ({round(p.stat().st_size/(1024*1024), 2)} MB)" for p in all_audios[:5])
        raise FileNotFoundError(
            f"Voiceover audio not found in storage/inputs/voiceover.mp3 or /kaggle/input.\n"
            f"Other audio files found:\n  - {other_list if other_list else 'None'}\n"
            f"Please mount the Dwarika voiceover dataset."
        )


def extract_30s_slice(source_audio: str, slice_path: str, duration: int = 30) -> str:
    """Extract first N seconds of audio using ffmpeg."""
    os.makedirs(os.path.dirname(slice_path), exist_ok=True)
    cmd = [
        "ffmpeg", "-y", "-v", "error",
        "-i", str(source_audio),
        "-t", str(duration),
        "-c:a", "libmp3lame", "-q:a", "2",
        str(slice_path)
    ]
    subprocess.run(cmd, check=True)
    return slice_path


def run_30s_test(model_size: str = "large-v3-turbo"):
    print("=" * 60)
    print(f"RUNNING 30-SECOND HINDI TRANSCRIPTION TEST (Stage 4)")
    print("=" * 60)

    # 1. Deterministically Locate Audio
    source_audio = find_voiceover_audio()
    sz_bytes = os.path.getsize(source_audio)
    sz_mb = round(sz_bytes / (1024 * 1024), 2)
    dur_str, dur_min, dur_sec = "Unknown", "Unknown", "Unknown"
    if shutil.which("ffprobe"):
        d_res = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(source_audio)],
            capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        if d_res.stdout.strip():
            t_s = float(d_res.stdout.strip())
            dur_sec = round(t_s, 2)
            dur_min = round(t_s / 60, 2)

    print("\n--- DETERMINISTIC AUDIO SELECTION ---")
    print(f"Selected Audio Path: {source_audio}")
    print(f"File Size          : {sz_mb} MB ({sz_bytes} bytes)")
    print(f"Total Duration     : {dur_min} min ({dur_sec} seconds)")
    print(f"Expected Reference : ~11.54 min (~692s) | ~10.57 MB")
    print("-------------------------------------")

    # 2. Extract 30s slice
    slice_path = os.path.join(BASE, "storage", "temp", "voiceover_30s_test.mp3")
    print(f"Extracting {SAMPLE_DURATION_SEC}s test sample to: {slice_path}...")
    extract_30s_slice(source_audio, slice_path, duration=SAMPLE_DURATION_SEC)
    print(f"Sample created successfully ({round(os.path.getsize(slice_path) / 1024, 1)} KB)")

    # 3. Transcribe only the sample
    print(f"\nTranscribing 30s sample using {model_size}...")
    audio_data = load_audio(slice_path)
    rows, info = transcribe(
        audio=audio_data,
        language="hi",
        initial_prompt=HINDI_PROMPT,
        model_size=model_size
    )

    # 3b. Detect and refine suspicious timestamps (>2.5s)
    rows, refine_stats = refine_transcript(
        rows=rows,
        audio_samples=audio_data,
        language="hi",
        initial_prompt=HINDI_PROMPT,
        model_size=model_size
    )
    if refine_stats.get("suspicious_count", 0) > 0:
        print(f"Refinement: {refine_stats['suspicious_count']} suspicious words detected, "
              f"{refine_stats['corrections_applied']} corrections applied.")
        if refine_stats.get("warnings"):
            for w in refine_stats["warnings"]:
                print(f"  [Warning] {w}")

    # 4. Generate Subtitles
    chunks = chunk_words(rows)
    srt_p, json_p = save_outputs(rows, TEST_OUTPUT_DIR)

    print("\n" + "=" * 60)
    print("30-SECOND TEST RESULTS FOR ACCURACY VERIFICATION")
    print("=" * 60)
    print(f"Detected Language: {info.language} (probability: {info.language_probability:.2f})")
    print(f"Total Segments: {len(rows)} | Total Subtitle Lines: {len(chunks)}")
    print(f"SRT saved at: {srt_p}")
    print(f"JSON saved at: {json_p}\n")

    print("--- RAW SPOKEN TEXT EXTRACTED ---")
    full_text = " ".join(r["text"] for r in rows)
    print(full_text)

    print("\n--- FIRST 8 SUBTITLE LINES (TIMED) ---")
    for i, c in enumerate(chunks[:8], 1):
        print(f"[{c['start']:.2f}s -> {c['end']:.2f}s]: {c['text']}")

    print("=" * 60)
    print("Test completed. Please review transcribed text against your audio.")
    print("=" * 60)
    return rows, chunks


if __name__ == "__main__":
    run_30s_test()

