"""FastAPI service for the AI Video Engine implementing the agreed API contract.

The UI source file is not included in this project archive; the public routes and
response shapes follow the contract supplied by the project owner.
"""
from __future__ import annotations

import os
import re
import secrets
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

import core.engine as engine
import core.pipeline as pipeline

app = FastAPI(title="AI Video Engine API")
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


def _require_token(x_token: str | None = Header(default=None, alias="X-Token")) -> None:
    expected = os.environ.get("ENGINE_TOKEN", "")
    if not expected or not x_token or not secrets.compare_digest(x_token, expected):
        raise HTTPException(status_code=401, detail="Invalid or missing X-Token")


def _job_worker(job_id: str, src: str, cut: bool, lang: str) -> None:
    with _jobs_lock:
        job = _jobs[job_id]
        job["status"] = "running"
        job["started_at"] = time.monotonic()
    try:
        # Same stack as kang.py (gap-fill, suspect-span repair, voter, glossary), not the old
        # engine.run_pipeline; outputs land where /file/{id}/{kind} already looks.
        out_dir = Path(engine.BASE) / "storage" / "outputs" / job_id
        res = pipeline.api_transcribe(src, str(out_dir), cut=cut, language=lang)
        with _jobs_lock:
            job["run_id"] = res["run_id"]
            # "done" = processing finished; acceptance is separate (Roadmap S4)
            job["review_required"] = res["review_required"]
            job["accepted"] = res["accepted"]
            job["warnings"] = res["warnings"]
            job["status"] = "done"
            job["secs"] = round(time.monotonic() - job["started_at"], 3)
    except Exception as exc:
        with _jobs_lock:
            job["status"] = "error"
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
):
    job_id = secrets.token_hex(4)
    base = Path(engine.BASE)
    input_dir = base / "storage" / "inputs"
    input_dir.mkdir(parents=True, exist_ok=True)

    original_name = Path(file.filename or "upload.bin").name
    # Keep a recognizable extension but avoid path traversal and empty names.
    safe_name = re.sub(r"[^A-Za-z0-9._-]", "_", original_name).strip("._") or "upload.bin"
    src_path = input_dir / f"{job_id}_{safe_name}"
    total_bytes = 0
    try:
        # Stream to disk in bounded chunks; never load the entire upload into RAM.
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
        "secs": None,
        "error": None,
        "started_at": None,
        "src": str(src_path),
    }
    with _jobs_lock:
        _jobs[job_id] = job
    _executor.submit(_job_worker, job_id, str(src_path), cut, lang)
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
            "secs": secs,
            "error": job["error"],
            # additive fields (old clients ignore them): processing done != transcript accepted
            "run_id": job.get("run_id"),
            "review_required": job.get("review_required"),
            "accepted": job.get("accepted", False),
            "warnings": job.get("warnings", []),
        }


@app.get("/file/{id}/{kind}", dependencies=[Depends(_require_token)])
def download_file(id: str, kind: str):
    if not _JOB_ID_RE.fullmatch(id) or kind not in {"srt", "json"}:
        raise HTTPException(status_code=404, detail="File not found")
    # Resolve the output directory through engine.BASE so local tests and deployments
    # can set ENGINE_BASE_DIR without changing the public API.
    suffix = "srt" if kind == "srt" else "json"
    path = Path(engine.BASE) / "storage" / "outputs" / id / f"transcript.{suffix}"
    if not path.is_file():
        raise HTTPException(status_code=404, detail="File not found")
    media_type = "application/json" if kind == "json" else "text/plain; charset=utf-8"
    return FileResponse(path, media_type=media_type, filename=path.name)
