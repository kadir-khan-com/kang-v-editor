"""Layer 1 (Intake) + Layer 7 (Archive).

- Unique run IDs (YYYY-MM-DD_KANG_NNN), one run = one folder.
- Media integrity: sha256 + ffprobe.
- manifest.json written for every run.
- Originals are never overwritten: every write goes inside the run folder.
"""
from __future__ import annotations

import datetime as _dt
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path
from typing import Any, Dict, List, Optional

RUN_ID_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})_KANG_(\d{3,})$")


def runs_root() -> Path:
    root = Path(os.environ.get("KANG_RUNS_DIR", Path(__file__).resolve().parent.parent / "runs"))
    root.mkdir(parents=True, exist_ok=True)
    return root


def sha256_file(path: str | Path, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def ffprobe(path: str | Path) -> Dict[str, Any]:
    """Return ffprobe JSON (format + streams). Raises RuntimeError on unreadable media."""
    p = Path(path)
    if not p.is_file() or p.stat().st_size == 0:
        raise FileNotFoundError(f"Media missing or empty: {p}")
    cmd = ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(p)]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if res.returncode != 0:
        raise RuntimeError(f"ffprobe failed for {p}: {res.stderr.strip()}")
    return json.loads(res.stdout)


def media_summary(path: str | Path) -> Dict[str, Any]:
    info = ffprobe(path)
    v = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)
    a = next((s for s in info.get("streams", []) if s.get("codec_type") == "audio"), None)
    out: Dict[str, Any] = {
        "duration": float(info.get("format", {}).get("duration", 0.0) or 0.0),
        "has_video": v is not None,
        "has_audio": a is not None,
    }
    if v:
        out["width"] = int(v.get("width", 0))
        out["height"] = int(v.get("height", 0))
        num, _, den = str(v.get("avg_frame_rate", "0/1")).partition("/")
        try:
            out["fps"] = round(float(num) / float(den or 1), 3)
        except ZeroDivisionError:
            out["fps"] = 0.0
        out["vcodec"] = v.get("codec_name")
        if v.get("nb_frames"):
            out["nb_frames"] = int(v["nb_frames"])
    if a:
        out["acodec"] = a.get("codec_name")
        out["sample_rate"] = int(a.get("sample_rate", 0) or 0)
        out["channels"] = int(a.get("channels", 0) or 0)
    return out


def new_run_id(date: Optional[_dt.date] = None, root: Optional[Path] = None) -> str:
    date = date or _dt.date.today()
    root = root or runs_root()
    prefix = date.isoformat()
    nums = [int(m.group(2)) for d in root.iterdir() if (m := RUN_ID_RE.match(d.name)) and m.group(1) == prefix]
    return f"{prefix}_KANG_{(max(nums) + 1 if nums else 1):03d}"


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _rel_to_project(p: Path) -> str:
    """Path relative to the KANG project root (portable manifests, 2026-11-07); absolute if outside."""
    try:
        return Path(p).resolve().relative_to(PROJECT_ROOT).as_posix()
    except ValueError:
        return str(p)


class Run:
    """One run = one folder with manifest.json, logs and all outputs."""

    def __init__(self, run_id: Optional[str] = None, root: Optional[Path] = None):
        self.root = root or runs_root()
        if run_id is None:
            # create atomically (retry on race)
            for _ in range(50):
                rid = new_run_id(root=self.root)
                try:
                    (self.root / rid).mkdir(parents=False, exist_ok=False)
                    run_id = rid
                    break
                except FileExistsError:
                    continue
            else:  # pragma: no cover
                raise RuntimeError("Could not allocate a unique run id")
        if not RUN_ID_RE.match(run_id):
            raise ValueError(f"Invalid run id: {run_id}")
        self.run_id = run_id
        self.dir = self.root / run_id
        self.dir.mkdir(parents=True, exist_ok=True)
        self.manifest_path = self.dir / "manifest.json"
        if self.manifest_path.is_file():
            self.manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        else:
            self.manifest = {
                "run_id": run_id,
                "created_at": _dt.datetime.now().isoformat(timespec="seconds"),
                "inputs": [],
                "outputs": [],
                "steps": [],
                "warnings": [],
                "approvals": {},
                "status": "created",
            }
            self.save()

    # ---- helpers -------------------------------------------------------
    def path(self, name: str) -> Path:
        p = (self.dir / name).resolve()
        if self.dir.resolve() not in p.parents and p != self.dir.resolve():
            raise ValueError(f"Refusing to write outside run folder: {name}")
        p.parent.mkdir(parents=True, exist_ok=True)
        return p

    def add_input(self, path: str | Path, input_id: str = "A1") -> Dict[str, Any]:
        p = Path(path).resolve()
        entry = {"id": input_id, "path": str(p), "rel_path": _rel_to_project(p), "sha256": sha256_file(p)}
        try:
            entry["media"] = media_summary(p)
        except Exception as exc:  # non-media inputs (json, png) are fine
            entry["media_error"] = str(exc)
        self.manifest["inputs"] = [i for i in self.manifest["inputs"] if i["id"] != input_id] + [entry]
        self.save()
        return entry

    def add_output(self, path: str | Path, kind: str) -> Dict[str, Any]:
        p = Path(path).resolve()
        try:
            rel = str(p.relative_to(self.dir.resolve()))
        except ValueError:
            rel = str(p)
        entry = {"kind": kind, "path": rel, "rel_path": _rel_to_project(p), "sha256": sha256_file(p)}
        self.manifest["outputs"] = [o for o in self.manifest["outputs"] if o["path"] != entry["path"]] + [entry]
        self.save()
        return entry

    def log_step(self, name: str, **data: Any) -> None:
        self.manifest["steps"].append({"step": name, "at": _dt.datetime.now().isoformat(timespec="seconds"), **data})
        self.save()

    def warn(self, msg: str) -> None:
        self.manifest["warnings"].append(msg)
        self.save()

    def set_approval(self, gate: str, value: str, plan_hash: Optional[str] = None,
                     approver: Optional[str] = None) -> None:
        """manifest.approvals[gate] = value (old contract) + an append-only record in approvals.json
        binding the decision to the exact plan it saw (sha256), who/what approved it, and when."""
        if value not in {"pending", "approved", "rejected", "n/a"}:
            raise ValueError(value)
        self.manifest["approvals"][gate] = value
        if plan_hash is not None:
            p = self.path("approvals.json")
            recs = json.loads(p.read_text(encoding="utf-8")) if p.exists() else []
            recs.append({"gate": gate, "value": value, "plan_hash": plan_hash, "approver": approver or "unknown",
                         "at": _dt.datetime.now().astimezone().isoformat(timespec="seconds")})
            p.write_text(json.dumps(recs, ensure_ascii=False, indent=2), encoding="utf-8")
        self.save()

    def approval_valid(self, gate: str, plan_hash: str) -> bool:
        """True only if the LAST record for gate is 'approved' for this exact plan hash."""
        p = self.path("approvals.json")
        recs = [r for r in (json.loads(p.read_text(encoding="utf-8")) if p.exists() else []) if r["gate"] == gate]
        return bool(recs) and recs[-1]["value"] == "approved" and recs[-1]["plan_hash"] == plan_hash

    def set_status(self, status: str) -> None:
        self.manifest["status"] = status
        self.save()

    def save(self) -> None:
        tmp = self.manifest_path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.manifest_path)


def write_json(path: str | Path, data: Any) -> Path:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


_FF_MAJOR: Optional[int] = None


def ffmpeg_major() -> int:
    """Major version of the ffmpeg on PATH (git/nightly builds count as new). Cached."""
    global _FF_MAJOR
    if _FF_MAJOR is None:
        try:
            out = subprocess.run(["ffmpeg", "-hide_banner", "-version"], capture_output=True,
                                 text=True, encoding="utf-8", errors="replace").stdout
            m = re.search(r"ffmpeg version n?(\d+)\.", out)
            _FF_MAJOR = int(m.group(1)) if m else 99
        except OSError:
            _FF_MAJOR = 99
    return _FF_MAJOR


def filter_script_args(script: Path) -> List[str]:
    """FFmpeg 9 removed -filter_complex_script; 7.x+ reads an option from a file with -/filter_complex."""
    return ["-/filter_complex", str(script)] if ffmpeg_major() >= 7 else ["-filter_complex_script", str(script)]


def run_ffmpeg(args: List[str], log_path: Optional[Path] = None) -> None:
    cmd = ["ffmpeg", "-hide_banner", "-nostdin", "-y", *args]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if log_path:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write("$ " + " ".join(cmd) + "\n" + res.stderr[-20000:] + "\n")
    if res.returncode != 0:
        raise RuntimeError(f"ffmpeg failed ({res.returncode}): {res.stderr.strip()[-2000:]}")
