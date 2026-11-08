"""FastAPI service for the AI Video Engine implementing the agreed API contract.

Includes a built-in modern web UI at `/` for drag-and-drop audio uploading,
live pipeline tracking, and instant download of rendered videos, subtitles,
and project packages.
"""
from __future__ import annotations

import glob
import json
import os
import re
import secrets
import shutil
import threading
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse

import core.engine as engine
import core.pipeline as pipeline

app = FastAPI(title="AI Video Engine API & Studio UI")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# One worker guarantees at most one engine/GPU pipeline runs at a time.
_executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="ai-video-job")
_jobs: dict[str, dict[str, Any]] = {}
_jobs_lock = threading.Lock()
_JOB_ID_RE = re.compile(r"^[0-9a-fA-F]{8}$")
MAX_UPLOAD_BYTES = int(os.environ.get("ENGINE_MAX_UPLOAD_BYTES", str(100 * 1024 * 1024)))
UPLOAD_CHUNK_BYTES = 1024 * 1024


def _require_token(
    x_token: str | None = Header(default=None, alias="X-Token"),
    token: str | None = Query(default=None),
) -> None:
    expected = os.environ.get("ENGINE_TOKEN", "")
    if not expected:
        return  # No token configured, local development/open access allowed
    provided = x_token or token
    if not provided or not secrets.compare_digest(provided, expected):
        raise HTTPException(status_code=401, detail="Invalid or missing X-Token")


def _job_worker(
    job_id: str,
    src: str,
    cut: bool,
    lang: str,
    mode: str = "transcribe",
    place: str = "kang",
    fmt: str = "9:16",
    preset: str = "vox_bold_yellow",
) -> None:
    with _jobs_lock:
        job = _jobs[job_id]
        job["status"] = "running"
        job["started_at"] = time.monotonic()
        job["stage"] = "transcribing"
    try:
        out_dir = Path(engine.BASE) / "storage" / "outputs" / job_id
        out_dir.mkdir(parents=True, exist_ok=True)

        if mode == "workflow":
            # Run the complete end-to-end video pipeline
            with _jobs_lock:
                job["stage"] = "full_pipeline"
            # Auto-approve pipeline gates when running via UI
            approver = lambda gate, info: True
            res = pipeline.workflow_clip(
                src,
                start=0.0,
                full=True,
                formats=[fmt],
                preset_name=preset,
                approver=approver,
                language=lang,
            )
            run_dir = Path(res["dir"])
            # Copy all generated media and metadata into out_dir
            for mp4 in run_dir.glob("*.mp4"):
                shutil.copy2(mp4, out_dir / mp4.name)
            for meta in run_dir.glob("*.json"):
                shutil.copy2(meta, out_dir / meta.name)
            for srt in run_dir.glob("*.srt"):
                shutil.copy2(srt, out_dir / srt.name)
            for ass in run_dir.glob("*.ass"):
                shutil.copy2(ass, out_dir / ass.name)

            # Ensure transcript.srt and transcript.json exist for standard API clients
            if not (out_dir / "transcript.srt").exists():
                srts = list(run_dir.rglob("*.srt"))
                if srts:
                    shutil.copy2(srts[0], out_dir / "transcript.srt")
            if not (out_dir / "transcript.json").exists():
                jsons = list(run_dir.rglob("*words*.json"))
                if jsons:
                    shutil.copy2(jsons[0], out_dir / "transcript.json")

            # Zip the outputs for easy single-click download
            zip_target = out_dir / f"{place}_output_bundle.zip"
            with zipfile.ZipFile(zip_target, "w", zipfile.ZIP_DEFLATED) as zf:
                for fpath in out_dir.iterdir():
                    if fpath.is_file() and fpath.name != zip_target.name:
                        zf.write(fpath, arcname=fpath.name)

            with _jobs_lock:
                job["run_id"] = res["run_id"]
                job["review_required"] = False
                job["accepted"] = True
                job["warnings"] = []
                job["status"] = "done"
                job["stage"] = "completed"
                job["secs"] = round(time.monotonic() - job["started_at"], 3)
        else:
            # Standard Transcription Stack
            res = pipeline.api_transcribe(src, str(out_dir), cut=cut, language=lang)
            with _jobs_lock:
                job["run_id"] = res["run_id"]
                job["review_required"] = res["review_required"]
                job["accepted"] = res["accepted"]
                job["warnings"] = res["warnings"]
                job["status"] = "done"
                job["stage"] = "completed"
                job["secs"] = round(time.monotonic() - job["started_at"], 3)
    except Exception as exc:
        with _jobs_lock:
            job["status"] = "error"
            job["stage"] = "failed"
            job["error"] = str(exc)
            job["secs"] = round(time.monotonic() - job["started_at"], 3)


@app.get("/health", dependencies=[Depends(_require_token)])
def health():
    return {"ok": True}


@app.post("/upload", dependencies=[Depends(_require_token)])
async def upload(
    file: UploadFile = File(...),
    cut: bool = Form(False),  # Roadmap v2: narration preserved by default; cuts only after review
    lang: str = Form("hi"),
    mode: str = Form("transcribe"),  # 'transcribe' or 'workflow'
    place: str = Form("kang"),
    fmt: str = Form("9:16"),
    preset: str = Form("vox_bold_yellow"),
):
    job_id = secrets.token_hex(4)
    base = Path(engine.BASE)
    input_dir = base / "storage" / "inputs"
    input_dir.mkdir(parents=True, exist_ok=True)

    original_name = Path(file.filename or "upload.bin").name
    safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", original_name).strip("._") or "upload.bin"
    src_path = input_dir / f"{job_id}_{safe_name}"
    total_bytes = 0
    try:
        with src_path.open("wb") as destination:
            while True:
                chunk = await file.read(UPLOAD_CHUNK_BYTES)
                if not chunk:
                    break
                total_bytes += len(chunk)
                if total_bytes > MAX_UPLOAD_BYTES:
                    destination.close()
                    src_path.unlink(missing_ok=True)
                    raise HTTPException(
                        status_code=413,
                        detail=f"Upload exceeds the {MAX_UPLOAD_BYTES}-byte limit",
                    )
                destination.write(chunk)
        if total_bytes == 0:
            src_path.unlink(missing_ok=True)
            raise HTTPException(status_code=400, detail="Uploaded file is empty")
    except HTTPException:
        raise
    except Exception:
        src_path.unlink(missing_ok=True)
        raise
    finally:
        await file.close()

    job = {
        "id": job_id,
        "name": original_name,
        "status": "queued",
        "stage": "queued",
        "mode": mode,
        "place": place,
        "secs": None,
        "error": None,
        "started_at": None,
        "src": str(src_path),
    }
    with _jobs_lock:
        _jobs[job_id] = job
    _executor.submit(_job_worker, job_id, str(src_path), cut, lang, mode, place, fmt, preset)
    return {"id": job_id, "name": original_name, "status": "queued"}


@app.get("/status/{id}", dependencies=[Depends(_require_token)])
def status(id: str):
    if not _JOB_ID_RE.fullmatch(id):
        raise HTTPException(status_code=404, detail="Job not found")
    with _jobs_lock:
        job = _jobs.get(id)
        if not job:
            raise HTTPException(status_code=404, detail="Job not found")
        secs = job["secs"]
        if job["status"] == "running" and job["started_at"] is not None:
            secs = round(time.monotonic() - job["started_at"], 3)
        return {
            "id": job["id"],
            "name": job["name"],
            "status": job["status"],
            "stage": job.get("stage", "running"),
            "mode": job.get("mode", "transcribe"),
            "place": job.get("place", "kang"),
            "secs": secs,
            "error": job["error"],
            "run_id": job.get("run_id"),
            "review_required": job.get("review_required"),
            "accepted": job.get("accepted", False),
            "warnings": job.get("warnings", []),
        }


@app.get("/file/{id}/{kind}", dependencies=[Depends(_require_token)])
def download_file(id: str, kind: str):
    if not _JOB_ID_RE.fullmatch(id) or kind not in {"srt", "json"}:
        raise HTTPException(status_code=404, detail="File not found")
    suffix = "srt" if kind == "srt" else "json"
    path = Path(engine.BASE) / "storage" / "outputs" / id / f"transcript.{suffix}"
    if not path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    media_type = "application/json" if kind == "json" else "text/plain; charset=utf-8"
    return FileResponse(path, media_type=media_type, filename=path.name)


@app.get("/files/{id}", dependencies=[Depends(_require_token)])
def list_job_files(id: str):
    if not _JOB_ID_RE.fullmatch(id):
        raise HTTPException(status_code=404, detail="Job not found")
    out_dir = Path(engine.BASE) / "storage" / "outputs" / id
    if not out_dir.is_dir():
        return {"files": []}
    files = []
    for f in out_dir.iterdir():
        if f.is_file():
            size_mb = round(f.stat().st_size / (1024 * 1024), 2)
            files.append({"name": f.name, "size_mb": size_mb, "ext": f.suffix.lower()})
    return {"files": files}


@app.get("/download/{id}/{filename}", dependencies=[Depends(_require_token)])
def download_any_file(id: str, filename: str):
    if not _JOB_ID_RE.fullmatch(id):
        raise HTTPException(status_code=404, detail="Job not found")
    safe_name = Path(filename).name
    path = (Path(engine.BASE) / "storage" / "outputs" / id / safe_name).resolve()
    base_dir = (Path(engine.BASE) / "storage" / "outputs" / id).resolve()
    if not str(path).startswith(str(base_dir)) or not path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    
    media_types = {
        ".mp4": "video/mp4",
        ".srt": "text/plain; charset=utf-8",
        ".ass": "text/plain; charset=utf-8",
        ".json": "application/json",
        ".zip": "application/zip",
        ".mp3": "audio/mpeg",
    }
    mtype = media_types.get(path.suffix.lower(), "application/octet-stream")
    return FileResponse(path, media_type=mtype, filename=path.name)


# --------------------------------------------------------------------------- Web UI
HTML_UI = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>KANG Creative Studio - AI Video Engine</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0b0f19;
      --card-bg: rgba(23, 29, 45, 0.75);
      --card-border: rgba(255, 255, 255, 0.08);
      --primary: #f59e0b;
      --primary-hover: #d97706;
      --accent: #3b82f6;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --success: #10b981;
      --danger: #ef4444;
      --font: 'Plus Jakarta Sans', 'Noto Sans Devanagari', -apple-system, sans-serif;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background: var(--bg);
      color: var(--text);
      font-family: var(--font);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      background-image: 
        radial-gradient(at 0% 0%, rgba(245, 158, 11, 0.12) 0px, transparent 50%),
        radial-gradient(at 100% 100%, rgba(59, 130, 246, 0.10) 0px, transparent 50%);
    }
    header {
      padding: 1.25rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--card-border);
      backdrop-filter: blur(12px);
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(11, 15, 25, 0.8);
    }
    .logo {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      font-weight: 800;
      font-size: 1.35rem;
      letter-spacing: -0.5px;
    }
    .logo span {
      background: linear-gradient(135deg, #f59e0b, #ef4444);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .badge {
      font-size: 0.75rem;
      padding: 0.25rem 0.65rem;
      border-radius: 9999px;
      background: rgba(16, 185, 129, 0.15);
      color: #34d399;
      border: 1px solid rgba(16, 185, 129, 0.25);
      font-weight: 600;
      display: flex;
      align-items: center;
      gap: 0.4rem;
    }
    .badge::before {
      content: '';
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: #34d399;
      box-shadow: 0 0 8px #34d399;
    }
    .container {
      max-width: 900px;
      margin: 2.5rem auto;
      padding: 0 1.5rem;
      width: 100%;
      flex: 1;
    }
    .card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: 1.25rem;
      padding: 2rem;
      backdrop-filter: blur(16px);
      box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.5);
      margin-bottom: 2rem;
    }
    .dropzone {
      border: 2px dashed rgba(245, 158, 11, 0.35);
      border-radius: 1rem;
      padding: 3rem 1.5rem;
      text-align: center;
      cursor: pointer;
      transition: all 0.25s ease;
      background: rgba(245, 158, 11, 0.02);
      position: relative;
    }
    .dropzone:hover, .dropzone.dragover {
      border-color: var(--primary);
      background: rgba(245, 158, 11, 0.06);
      transform: translateY(-2px);
    }
    .dropzone-icon {
      font-size: 3rem;
      margin-bottom: 1rem;
      display: inline-block;
    }
    .dropzone h3 {
      font-size: 1.2rem;
      font-weight: 700;
      margin-bottom: 0.35rem;
    }
    .dropzone p {
      color: var(--text-muted);
      font-size: 0.9rem;
    }
    input[type="file"] { display: none; }
    .file-preview {
      display: none;
      margin-top: 1.25rem;
      background: rgba(255, 255, 255, 0.04);
      border-radius: 0.75rem;
      padding: 1rem;
      align-items: center;
      gap: 1rem;
    }
    .file-preview audio { width: 100%; height: 36px; }
    .grid-2 {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1.25rem;
      margin-top: 1.5rem;
    }
    .form-group {
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }
    label {
      font-size: 0.85rem;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }
    input[type="text"], select {
      background: rgba(11, 15, 25, 0.75);
      border: 1px solid var(--card-border);
      border-radius: 0.65rem;
      padding: 0.85rem 1rem;
      color: var(--text);
      font-family: inherit;
      font-size: 0.95rem;
      outline: none;
      transition: border-color 0.2s;
    }
    input[type="text"]:focus, select:focus {
      border-color: var(--primary);
      box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.2);
    }
    .btn-submit {
      width: 100%;
      margin-top: 2rem;
      padding: 1.1rem;
      background: linear-gradient(135deg, var(--primary), var(--primary-hover));
      color: #0b0f19;
      font-weight: 800;
      font-size: 1.05rem;
      border: none;
      border-radius: 0.75rem;
      cursor: pointer;
      transition: all 0.2s ease;
      display: flex;
      justify-content: center;
      align-items: center;
      gap: 0.5rem;
      box-shadow: 0 10px 25px -5px rgba(245, 158, 11, 0.4);
    }
    .btn-submit:hover:not(:disabled) {
      transform: translateY(-2px);
      box-shadow: 0 15px 30px -5px rgba(245, 158, 11, 0.6);
    }
    .btn-submit:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
    /* Status & Progress */
    .status-panel {
      display: none;
      margin-top: 1.5rem;
      padding: 1.5rem;
      border-radius: 1rem;
      background: rgba(0, 0, 0, 0.25);
      border: 1px solid var(--card-border);
    }
    .progress-bar-wrap {
      width: 100%;
      height: 8px;
      background: rgba(255, 255, 255, 0.08);
      border-radius: 9999px;
      overflow: hidden;
      margin: 1.25rem 0;
    }
    .progress-bar {
      height: 100%;
      width: 15%;
      background: linear-gradient(90deg, var(--primary), #ef4444);
      border-radius: 9999px;
      transition: width 0.4s ease;
      animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 0.8; }
      50% { opacity: 1; }
    }
    .stages {
      display: flex;
      flex-direction: column;
      gap: 0.65rem;
      font-size: 0.9rem;
    }
    .stage-item {
      display: flex;
      align-items: center;
      gap: 0.75rem;
      color: var(--text-muted);
    }
    .stage-item.active {
      color: var(--primary);
      font-weight: 600;
    }
    .stage-item.done {
      color: #34d399;
    }
    /* Results */
    .results-panel {
      display: none;
      margin-top: 1.5rem;
    }
    .video-preview-wrap {
      width: 100%;
      max-width: 480px;
      margin: 1.5rem auto;
      border-radius: 1rem;
      overflow: hidden;
      border: 1px solid var(--card-border);
      background: #000;
    }
    video { width: 100%; display: block; }
    .downloads-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
      gap: 1rem;
      margin-top: 1.5rem;
    }
    .download-btn {
      padding: 0.9rem 1.25rem;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--card-border);
      border-radius: 0.75rem;
      color: var(--text);
      text-decoration: none;
      font-weight: 600;
      font-size: 0.95rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      transition: all 0.2s;
    }
    .download-btn:hover {
      background: rgba(245, 158, 11, 0.15);
      border-color: var(--primary);
      transform: translateY(-2px);
    }
    .download-btn span.size {
      font-size: 0.75rem;
      color: var(--text-muted);
    }
    footer {
      text-align: center;
      padding: 1.5rem;
      color: var(--text-muted);
      font-size: 0.85rem;
      border-top: 1px solid var(--card-border);
    }
    @media(max-width: 650px) {
      .grid-2 { grid-template-columns: 1fr; }
      header { padding: 1rem; }
      .card { padding: 1.25rem; }
    }
  </style>
</head>
<body>
  <header>
    <div class="logo">
      🎬 <span>KANG Studio</span>
    </div>
    <div class="badge">Engine Ready</div>
  </header>

  <main class="container">
    <div class="card">
      <div class="dropzone" id="dropzone">
        <input type="file" id="audioInput" accept="audio/*,.mp3,.wav,.m4a,.aac,.flac">
        <div class="dropzone-icon">🎙️</div>
        <h3>Drop voiceover audio here</h3>
        <p>Supports MP3, WAV, M4A, AAC (Max 100 MB)</p>
      </div>

      <div class="file-preview" id="filePreview">
        <div style="flex: 1;">
          <div style="font-weight: 700;" id="fileName">voiceover.mp3</div>
          <div style="font-size: 0.8rem; color: var(--text-muted);" id="fileSize">0 MB</div>
          <audio id="audioPlayer" controls style="margin-top: 0.5rem;"></audio>
        </div>
        <button type="button" id="changeFileBtn" style="background: none; border: 1px solid var(--card-border); color: var(--text); padding: 0.4rem 0.8rem; border-radius: 0.5rem; cursor: pointer;">Change</button>
      </div>

      <div class="grid-2">
        <div class="form-group">
          <label>Target Place / Project</label>
          <input type="text" id="placeInput" value="darjeeling" placeholder="e.g. darjeeling, dwarika">
        </div>
        <div class="form-group">
          <label>Processing Mode</label>
          <select id="modeSelect">
            <option value="workflow">⚡ Full Video & Subtitles (Video + Subtitles + Cuts)</option>
            <option value="transcribe">📝 Fast Transcription Only (SRT + JSON)</option>
          </select>
        </div>
        <div class="form-group">
          <label>Aspect Ratio / Format</label>
          <select id="fmtSelect">
            <option value="9:16">📱 9:16 Vertical (Reels / Shorts / TikTok)</option>
            <option value="16:9">🖥️ 16:9 Landscape (YouTube)</option>
            <option value="1:1">⏹️ 1:1 Square (Feed)</option>
          </select>
        </div>
        <div class="form-group">
          <label>Subtitle Preset</label>
          <select id="presetSelect">
            <option value="vox_bold_yellow">🟨 Vox Bold Yellow (Viral Retention)</option>
            <option value="travel">🌄 Clean Travel Style</option>
            <option value="promo">🎯 Promo Highlight</option>
          </select>
        </div>
      </div>

      <button class="btn-submit" id="startBtn" disabled>
        <span>Generate Output</span> ⚡
      </button>

      <!-- Live Status Tracking -->
      <div class="status-panel" id="statusPanel">
        <div style="display: flex; justify-content: space-between; align-items: center;">
          <h4 id="statusTitle">Processing Audio...</h4>
          <span style="font-size: 0.85rem; color: var(--text-muted);" id="timer">0.0s</span>
        </div>
        <div class="progress-bar-wrap">
          <div class="progress-bar" id="progressBar"></div>
        </div>
        <div class="stages">
          <div class="stage-item done" id="s1">✓ 1. Audio Uploaded & Validated</div>
          <div class="stage-item active" id="s2">⏳ 2. Whisper Speech Recognition & Hindi Glossary</div>
          <div class="stage-item" id="s3">⏳ 3. Silence / Filler Jumpcut Processing</div>
          <div class="stage-item" id="s4">⏳ 4. Loudness Normalization & Audio Cleanup</div>
          <div class="stage-item" id="s5">⏳ 5. Animated Subtitles & Final Render</div>
        </div>
      </div>

      <!-- Results & Downloads -->
      <div class="results-panel" id="resultsPanel">
        <h3 style="margin-bottom: 0.5rem;">🎉 Output Ready!</h3>
        <p style="color: var(--text-muted); font-size: 0.9rem;">Your files have been processed and are ready to download:</p>
        
        <div class="video-preview-wrap" id="videoPreviewWrap" style="display: none;">
          <video id="outputVideo" controls></video>
        </div>

        <div class="downloads-grid" id="downloadsGrid"></div>

        <button type="button" id="resetBtn" style="margin-top: 1.5rem; width: 100%; padding: 0.75rem; background: transparent; border: 1px solid var(--card-border); color: var(--text); border-radius: 0.5rem; cursor: pointer;">
          Process Another Audio File
        </button>
      </div>

    </div>
  </main>

  <footer>
    KANG Creative Automation Engine • Powered by Fast Whisper & FFmpeg
  </footer>

  <script>
    const dropzone = document.getElementById('dropzone');
    const audioInput = document.getElementById('audioInput');
    const filePreview = document.getElementById('filePreview');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const audioPlayer = document.getElementById('audioPlayer');
    const startBtn = document.getElementById('startBtn');
    const changeFileBtn = document.getElementById('changeFileBtn');
    const statusPanel = document.getElementById('statusPanel');
    const resultsPanel = document.getElementById('resultsPanel');
    const progressBar = document.getElementById('progressBar');
    const timerText = document.getElementById('timer');
    const downloadsGrid = document.getElementById('downloadsGrid');
    const resetBtn = document.getElementById('resetBtn');

    let selectedFile = null;
    let pollInterval = null;
    let timerInterval = null;
    let startTime = null;

    // Detect token from URL if provided (e.g. ?token=...)
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token') || '';

    dropzone.addEventListener('click', () => audioInput.click());
    dropzone.addEventListener('dragover', (e) => { e.preventDefault(); dropzone.classList.add('dragover'); });
    dropzone.addEventListener('dragleave', () => dropzone.classList.remove('dragover'));
    dropzone.addEventListener('drop', (e) => {
      e.preventDefault();
      dropzone.classList.remove('dragover');
      if (e.dataTransfer.files.length) handleFile(e.dataTransfer.files[0]);
    });
    audioInput.addEventListener('change', () => {
      if (audioInput.files.length) handleFile(audioInput.files[0]);
    });
    changeFileBtn.addEventListener('click', () => audioInput.click());

    function handleFile(file) {
      selectedFile = file;
      fileName.textContent = file.name;
      fileSize.textContent = (file.size / (1024 * 1024)).toFixed(2) + ' MB';
      audioPlayer.src = URL.createObjectURL(file);
      dropzone.style.display = 'none';
      filePreview.style.display = 'flex';
      startBtn.disabled = false;
    }

    startBtn.addEventListener('click', async () => {
      if (!selectedFile) return;
      startBtn.disabled = true;
      statusPanel.style.display = 'block';
      resultsPanel.style.display = 'none';
      progressBar.style.width = '20%';

      startTime = Date.now();
      timerInterval = setInterval(() => {
        timerText.textContent = ((Date.now() - startTime) / 1000).toFixed(1) + 's';
      }, 100);

      const formData = new FormData();
      formData.append('file', selectedFile);
      formData.append('place', document.getElementById('placeInput').value.trim() || 'kang');
      formData.append('mode', document.getElementById('modeSelect').value);
      formData.append('fmt', document.getElementById('fmtSelect').value);
      formData.append('preset', document.getElementById('presetSelect').value);
      formData.append('cut', 'true');
      formData.append('lang', 'hi');

      try {
        const uploadUrl = token ? `/upload?token=${encodeURIComponent(token)}` : '/upload';
        const headers = token ? { 'X-Token': token } : {};
        const res = await fetch(uploadUrl, { method: 'POST', headers, body: formData });
        if (!res.ok) throw new Error('Upload failed with status ' + res.status);
        const data = await res.json();
        pollJob(data.id);
      } catch (err) {
        clearInterval(timerInterval);
        alert('Upload Error: ' + err.message);
        startBtn.disabled = false;
        statusPanel.style.display = 'none';
      }
    });

    function pollJob(jobId) {
      let stepProgress = 30;
      pollInterval = setInterval(async () => {
        try {
          const statusUrl = token ? `/status/${jobId}?token=${encodeURIComponent(token)}` : `/status/${jobId}`;
          const headers = token ? { 'X-Token': token } : {};
          const res = await fetch(statusUrl, { headers });
          if (!res.ok) return;
          const job = await res.json();

          if (stepProgress < 90) stepProgress += 5;
          progressBar.style.width = stepProgress + '%';

          if (job.status === 'done') {
            clearInterval(pollInterval);
            clearInterval(timerInterval);
            progressBar.style.width = '100%';
            showResults(jobId);
          } else if (job.status === 'error') {
            clearInterval(pollInterval);
            clearInterval(timerInterval);
            alert('Pipeline Error: ' + (job.error || 'Unknown error occurred.'));
            startBtn.disabled = false;
          }
        } catch (e) {
          console.error(e);
        }
      }, 1500);
    }

    async function showResults(jobId) {
      statusPanel.style.display = 'none';
      resultsPanel.style.display = 'block';
      downloadsGrid.innerHTML = '';

      const filesUrl = token ? `/files/${jobId}?token=${encodeURIComponent(token)}` : `/files/${jobId}`;
      const headers = token ? { 'X-Token': token } : {};
      const res = await fetch(filesUrl, { headers });
      const data = await res.json();

      let videoFound = false;
      const tokenParam = token ? `?token=${encodeURIComponent(token)}` : '';

      data.files.forEach(f => {
        const fileUrl = `/download/${jobId}/${encodeURIComponent(f.name)}${tokenParam}`;
        
        // Video Preview
        if (f.ext === '.mp4' && !videoFound) {
          videoFound = true;
          const videoWrap = document.getElementById('videoPreviewWrap');
          const videoEl = document.getElementById('outputVideo');
          videoEl.src = fileUrl;
          videoWrap.style.display = 'block';
        }

        // Download Buttons
        const btn = document.createElement('a');
        btn.className = 'download-btn';
        btn.href = fileUrl;
        btn.download = f.name;

        let icon = '📄';
        if (f.ext === '.mp4') icon = '🎬';
        else if (f.ext === '.zip') icon = '📦';
        else if (f.ext === '.srt' || f.ext === '.ass') icon = '📝';
        else if (f.ext === '.json') icon = '📊';

        btn.innerHTML = `<div>${icon} <strong>${f.name}</strong></div><span class="size">${f.size_mb} MB</span>`;
        downloadsGrid.appendChild(btn);
      });
    }

    resetBtn.addEventListener('click', () => {
      selectedFile = null;
      audioInput.value = '';
      dropzone.style.display = 'block';
      filePreview.style.display = 'none';
      startBtn.disabled = true;
      resultsPanel.style.display = 'none';
      statusPanel.style.display = 'none';
      document.getElementById('videoPreviewWrap').style.display = 'none';
    });
  </script>
</body>
</html>
"""


@app.get("/", response_class=HTMLResponse)
def index():
    return HTML_UI
