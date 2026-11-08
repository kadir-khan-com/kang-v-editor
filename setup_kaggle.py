"""
Kaggle Setup & Bootstrapper for AI Video Engine
Stage 1: Reproducible Environment & Recovery

This script performs an idempotent setup in Kaggle:
1. Installs Hindi Devanagari fonts (Noto Sans Devanagari) so FFmpeg renders Hindi subtitles cleanly.
2. Installs faster-whisper, auto-editor, and other required Python packages.
3. Creates the standard directory tree under /kaggle/working/ai-video-engine.
4. Recovers the voiceover file from /kaggle/input if missing post-reset.
5. Verifies GPU, dependencies, fonts, and audio file integrity.
"""
import os
import sys
import shutil
import subprocess
import platform
import urllib.request
from pathlib import Path

BASE_DIR = Path(os.environ.get("ENGINE_BASE_DIR", "/kaggle/working/ai-video-engine"))
INPUT_ROOT = Path(os.environ.get("KAGGLE_INPUT_DIR", "/kaggle/input"))

def run_cmd(cmd, desc="", check=True):
    """cmd as a list runs WITHOUT a shell (safe for 'pkg>=1.0' specifiers); a str keeps shell=True."""
    print(f"--> {desc}...")
    res = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=True, text=True, encoding="utf-8", errors="replace")
    if check and res.returncode != 0:
        print(f"ERROR: {desc} failed with code {res.returncode}")
        print(res.stderr[:2000])
        raise RuntimeError(f"Step failed: {desc}")
    return res


def install_cloudflared():
    """Install the official Cloudflare quick-tunnel binary if it is missing."""
    existing = shutil.which("cloudflared")
    if existing:
        print(f"--> cloudflared already available: {existing}")
        return existing

    machine = platform.machine().lower()
    asset_by_machine = {
        "x86_64": "cloudflared-linux-amd64",
        "amd64": "cloudflared-linux-amd64",
        "aarch64": "cloudflared-linux-arm64",
        "arm64": "cloudflared-linux-arm64",
    }
    asset = asset_by_machine.get(machine)
    if not asset:
        raise RuntimeError(f"Unsupported architecture for cloudflared: {machine}")

    install_path = Path("/usr/local/bin/cloudflared")
    if not os.access(install_path.parent, os.W_OK):
        install_path = Path.home() / ".local" / "bin" / "cloudflared"
        install_path.parent.mkdir(parents=True, exist_ok=True)

    url = f"https://github.com/cloudflare/cloudflared/releases/latest/download/{asset}"
    print(f"--> Downloading cloudflared from official release: {url}")
    try:
        urllib.request.urlretrieve(url, install_path)
        install_path.chmod(0o755)
    except Exception as exc:
        install_path.unlink(missing_ok=True)
        raise RuntimeError(f"Could not install cloudflared from {url}: {exc}") from exc

    # Ensure a user-local install is discoverable by start.py subprocesses.
    os.environ["PATH"] = f"{install_path.parent}{os.pathsep}{os.environ.get('PATH', '')}"
    print(f"--> cloudflared installed at: {install_path}")
    return str(install_path)

def setup_environment():
    print("=" * 60)
    print("AI VIDEO ENGINE - KAGGLE ENVIRONMENT SETUP (STAGE 1)")
    print("=" * 60)

    # 1. Install System Fonts for Devanagari / Hindi subtitles
    # (Prevents tofu / blank square boxes in FFmpeg subtitle rendering)
    if os.path.exists("/usr/bin/apt-get"):
        run_cmd(
            "apt-get update -qq && apt-get install -y -qq fonts-noto-core fonts-noto-extra ffmpeg",
            desc="Installing Hindi Devanagari fonts and FFmpeg"
        )
        run_cmd("fc-cache -f", desc="Refreshing font cache", check=False)
    else:
        print("--> apt-get not present (non-Debian / local environment). Skipping apt-get.")

    # 2. Install Python Dependencies
    packages = ["faster-whisper", "auto-editor", "fastapi", "uvicorn", "python-multipart",
                "numpy", "pydantic>=2.5", "pillow", "fonttools", "pytest"]
    # list form: with shell=True, "pydantic>=2.5" was parsed as a redirect to a file named "=2.5"
    run_cmd(
        [sys.executable, "-m", "pip", "install", "-q", *packages],
        desc="Installing Python dependencies (faster-whisper, auto-editor)"
    )

    # 3. Install Cloudflare quick-tunnel binary for start.py
    # cloudflared is only needed for start.py (public tunnel). Offline Kaggle sessions must still finish setup.
    try:
        install_cloudflared()
    except RuntimeError as exc:
        print(f"--> WARNING: cloudflared not installed ({exc}). start.py tunnel unavailable; engine/tests unaffected.")

    # 4. Create Project Directory Tree
    folders = [
        BASE_DIR / "core",
        BASE_DIR / "configs" / "presets",
        BASE_DIR / "storage" / "inputs",
        BASE_DIR / "storage" / "temp",
        BASE_DIR / "storage" / "outputs",
    ]
    for f in folders:
        f.mkdir(parents=True, exist_ok=True)
    print(f"--> Project directories verified under: {BASE_DIR}")

    # 5. Deterministic Audio Discovery & Recovery from /kaggle/input
    target_audio = BASE_DIR / "storage" / "inputs" / "voiceover.mp3"
    selected_source = None

    explicit = os.environ.get("KANG_INPUT_AUDIO", "").strip()
    if explicit:  # any client/audio: explicit path wins, no name guessing
        selected_source = Path(explicit)
        if not selected_source.is_file() or selected_source.stat().st_size == 0:
            raise FileNotFoundError(f"KANG_INPUT_AUDIO not found or empty: {explicit}")
        print(f"--> Using explicit KANG_INPUT_AUDIO: {selected_source}")
        target_audio.parent.mkdir(parents=True, exist_ok=True)
        if selected_source.resolve() != target_audio.resolve():  # same file: nothing to copy
            shutil.copy2(selected_source, target_audio)
    elif target_audio.is_file() and target_audio.stat().st_size > 0:
        print(f"--> Found existing voiceover in working directory: {target_audio}")
        selected_source = target_audio
    else:
        print("--> storage/inputs/voiceover.mp3 not found. Performing deterministic search in /kaggle/input...")
        input_root = INPUT_ROOT
        if not input_root.exists():
            raise FileNotFoundError("/kaggle/input directory does not exist. Are datasets mounted?")

        # Step 4a: Exact match for known Dwarika audio
        exact_matches = list(input_root.rglob("6 Dwarika enhanced.mp3"))
        if exact_matches:
            selected_source = exact_matches[0]
            print(f"--> Unambiguous exact match found: {selected_source}")
        else:
            # Step 4b: Search for Dwarika / voiceover candidates
            all_audios = [
                p for p in input_root.rglob("*")
                if p.is_file() and p.suffix.lower() in [".mp3", ".wav", ".m4a", ".aac"]
            ]
            dwarika_candidates = [
                p for p in all_audios
                if "dwarika" in p.name.lower() or "voiceover" in p.name.lower()
            ]

            if len(dwarika_candidates) == 1:
                selected_source = dwarika_candidates[0]
                print(f"--> Unambiguous Dwarika candidate found: {selected_source}")
            elif len(dwarika_candidates) > 1:
                cand_list = "\n  - ".join(f"{p} ({round(p.stat().st_size/(1024*1024), 2)} MB)" for p in dwarika_candidates)
                raise RuntimeError(
                    f"AMBIGUOUS AUDIO: Multiple Dwarika/voiceover candidates found in /kaggle/input:\n  - {cand_list}\n"
                    f"Stopping automatically. Please specify which file to use rather than guessing."
                )
            else:
                other_list = "\n  - ".join(f"{p} ({round(p.stat().st_size/(1024*1024), 2)} MB)" for p in all_audios[:5])
                raise FileNotFoundError(
                    f"Expected '6 Dwarika enhanced.mp3' not found in /kaggle/input.\n"
                    f"Other files found:\n  - {other_list if other_list else 'None'}\n"
                    f"Please attach the Dwarika voiceover dataset to your Kaggle session."
                )

        print(f"--> Copying {selected_source} -> {target_audio}...")
        shutil.copy2(selected_source, target_audio)

    # 6. Verify Environment
    print("\n" + "=" * 60)
    print("STAGE 1 VERIFICATION REPORT")
    print("=" * 60)
    # Check PyTorch & GPU
    try:
        import torch
        cuda_ok = torch.cuda.is_available()
        gpu_name = torch.cuda.get_device_name(0) if cuda_ok else "None (CPU only)"
        print(f"CUDA Available: {cuda_ok} | Device: {gpu_name}")
    except Exception as e:
        print(f"PyTorch Check: {e}")

    # Check faster-whisper
    try:
        import faster_whisper
        print(f"faster-whisper: Installed (v{faster_whisper.__version__})")
    except Exception as e:
        print(f"faster-whisper: FAILED ({e})")

    # Check auto-editor
    ae = shutil.which("auto-editor")
    print(f"auto-editor: {'Available at ' + ae if ae else 'NOT FOUND'}")

    # Check ffmpeg
    ff = shutil.which("ffmpeg")
    print(f"ffmpeg: {'Available at ' + ff if ff else 'NOT FOUND'}")

    # Check cloudflared
    cf = shutil.which("cloudflared")
    print(f"cloudflared: {'Available at ' + cf if cf else 'NOT FOUND'}")

    # Check Hindi font
    font_res = subprocess.run("fc-match 'Noto Sans Devanagari'", shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    out_font = font_res.stdout.strip()
    print(f"Devanagari Font: {out_font if out_font else 'NOT FOUND'}")

    # Check Voiceover Audio
    if target_audio.is_file():
        size_bytes = target_audio.stat().st_size
        size_mb = round(size_bytes / (1024 * 1024), 2)
        dur_sec = "Unknown"
        dur_min = "Unknown"
        if shutil.which("ffprobe"):
            dur_res = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(target_audio)],
                capture_output=True, text=True, encoding="utf-8", errors="replace"
            )
            dur_str = dur_res.stdout.strip()
            if dur_str:
                total_s = float(dur_str)
                dur_sec = round(total_s, 2)
                dur_min = round(total_s / 60, 2)

        print("\n--- DETERMINISTIC AUDIO INSPECTION ---")
        print(f"Selected Audio Path: {target_audio}")
        print(f"File Size          : {size_mb} MB ({size_bytes} bytes)")
        print(f"Audio Duration     : {dur_min} min ({dur_sec} seconds)")
        print(f"Expected Reference : ~11.54 min (~692s) | ~10.57 MB")
        if dur_min != "Unknown":
            match_ok = 11.0 <= float(dur_min) <= 12.0
            print(f"Integrity Check    : {'PASS (Duration matches Dwarika voiceover)' if match_ok else 'WARNING (Duration differs from ~11.54 min)'}")
        print("---------------------------------------")
    else:
        print("Audio File: Pending (not yet present in storage/inputs/voiceover.mp3)")
    print("=" * 60)

if __name__ == "__main__":
    setup_environment()

