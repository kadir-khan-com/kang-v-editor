"""Shared helpers for external free sources (Openverse, Pixabay): config, on-disk response cache (24 h),
rate limiter, wrong-place / people / landmark text checks, perceptual hash (dHash) for near-duplicate checks.
No network here; callers pass a `get(url) -> bytes` function so tests can mock HTTP."""
from __future__ import annotations

import hashlib
import json
import re
import time
from collections import deque
from pathlib import Path
from typing import Any, Callable, Deque, Dict, Iterable, List, Optional, Sequence

ROOT = Path(__file__).resolve().parent.parent
UA = "KANG-asset-fetch/0.7 (personal video editing tool; API terms followed: cache 24 h, rate-limited, no mass download)"


def load_cfg(path: Optional[str | Path] = None) -> Dict[str, Any]:
    return json.loads(Path(path or ROOT / "config" / "stock_sources.json").read_text(encoding="utf-8"))


def norm_text(s: str) -> str:
    s = (s or "").lower()
    s = re.sub(r"[_\-/|,.;:()\[\]\"']+", " ", s)
    return " " + re.sub(r"\s+", " ", re.sub(r"[^a-z0-9\u0900-\u097f ]+", " ", s)).strip() + " "


def find_terms(text: str, terms: Iterable[str]) -> List[str]:
    t = norm_text(text)
    return [w for w in terms if f" {norm_text(w).strip()} " in t]


def text_reject(text: str, cfg: Dict[str, Any], *, people: bool = True, landmarks: bool = True) -> Optional[str]:
    """Wrong place first (named other place), then landmark / identifiable-person cues."""
    wp = find_terms(text, cfg.get("wrong_places", []))
    if wp:
        return f"wrong place: mentions {', '.join(wp[:3])}"
    if landmarks:
        lm = find_terms(text, cfg.get("landmark_words", []))
        if lm:
            return f"recognisable landmark / foreign cue: {', '.join(lm[:3])}"
    if people:
        pp = find_terms(text, cfg.get("people_words", []))
        if pp:
            return f"identifiable-person cue: {', '.join(pp[:3])}"
    return None


class RateLimiter:
    """At most `n` calls per `window` seconds (sliding window). `clock`/`sleep` injectable for tests."""

    def __init__(self, n: int, window: float = 60.0, clock: Callable[[], float] = time.monotonic,
                 sleep: Callable[[float], None] = time.sleep):
        self.n, self.window, self.clock, self.sleep = n, window, clock, sleep
        self.calls: Deque[float] = deque()
        self.waited = 0.0

    def wait(self) -> None:
        now = self.clock()
        while self.calls and now - self.calls[0] >= self.window:
            self.calls.popleft()
        if len(self.calls) >= self.n:
            dt = self.window - (now - self.calls[0]) + 0.01
            self.sleep(dt)
            self.waited += dt
            now = self.clock()
            while self.calls and now - self.calls[0] >= self.window:
                self.calls.popleft()
        self.calls.append(now)


class JsonCache:
    """API responses on disk, keyed by the request URL (with the key PLACEHOLDER, never a real key)."""

    def __init__(self, folder: str | Path, ttl_s: float = 86400, clock: Callable[[], float] = time.time):
        self.dir = Path(folder)
        self.ttl, self.clock = ttl_s, clock
        self.hits = self.misses = 0

    def _p(self, url: str) -> Path:
        return self.dir / (hashlib.sha1(url.encode("utf-8")).hexdigest() + ".json")

    def get(self, url: str) -> Optional[Any]:
        p = self._p(url)
        if p.is_file():
            rec = json.loads(p.read_text(encoding="utf-8"))
            if self.clock() - rec.get("fetched_at", 0) < self.ttl:
                self.hits += 1
                return rec["data"]
        self.misses += 1
        return None

    def put(self, url: str, data: Any) -> None:
        self.dir.mkdir(parents=True, exist_ok=True)
        self._p(url).write_text(json.dumps({"url": url, "fetched_at": self.clock(), "data": data}, ensure_ascii=False),
                                encoding="utf-8")


def http_get(url: str, *, retries: int = 3, timeout: float = 60.0, backoff: float = 8.0,
             headers: Optional[Dict[str, str]] = None, direct: bool = False) -> bytes:
    """GET with UA; backoff on 429/503. Raises urllib HTTPError with .code on other failures.
    direct=True bypasses the HTTP(S)_PROXY (used for cdn.pixabay.com media: the credential proxy only accepts the
    connected API URL for the whole pixabay.com host, and CDN files need no key)."""
    import urllib.error
    import urllib.request
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({})) if direct else None
    delay = backoff
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, headers={"User-Agent": UA, **(headers or {})})
        try:
            with (opener.open(req, timeout=timeout) if opener else urllib.request.urlopen(req, timeout=timeout)) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < retries:
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise RuntimeError("unreachable")


# ------------------------------------------------------------------ perceptual hash (dHash, 64 bit)
def dhash_image(im) -> int:
    """64-bit difference hash of a PIL image (grey, 9x8). Robust to resize/recompress."""
    from PIL import Image
    g = im.convert("L").resize((9, 8), Image.LANCZOS)
    px = list(g.tobytes())  # mode L: one byte per pixel
    bits = 0
    for y in range(8):
        for x in range(8):
            bits = (bits << 1) | (1 if px[y * 9 + x] > px[y * 9 + x + 1] else 0)
    return bits


def dhash_file(path: str | Path) -> Optional[int]:
    from PIL import Image
    p = Path(path)
    if p.suffix.lower() in (".mp4", ".mov", ".webm", ".mkv", ".m4v"):
        fr = video_frame(p, 0.5)
        return dhash_image(fr) if fr is not None else None
    try:
        with Image.open(p) as im:
            return dhash_image(im)
    except Exception:
        return None


def hamming(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def near_duplicate(h: int, pool: Dict[str, int], max_dist: int = 8) -> Optional[str]:
    best = None
    for k, v in pool.items():
        d = hamming(h, v)
        if d <= max_dist and (best is None or d < best[1]):
            best = (k, d)
    return f"{best[0]} (dHash distance {best[1]})" if best else None


def video_frame(path: str | Path, frac: float = 0.5):
    """PIL frame at frac of the video duration (ffmpeg)."""
    import subprocess
    import tempfile
    from PIL import Image
    from .runs import media_summary
    try:
        d = float(media_summary(path).get("duration") or 0)
    except Exception:
        d = 0.0
    tmp = Path(tempfile.mkdtemp(prefix="kang_vf_")) / "f.jpg"
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{max(0.0, d * frac):.3f}", "-i", str(path),
                        "-frames:v", "1", str(tmp)], capture_output=True)
    if r.returncode != 0 or not tmp.is_file():
        return None
    return Image.open(tmp).convert("RGB")


def pool_hashes(dirs: Sequence[str | Path], cache_file: Optional[str | Path] = None) -> Dict[str, int]:
    """dHash of every image in the given asset folders (recursive), cached by sha256 of the file."""
    from .asset_index import IMG, _sha
    cache: Dict[str, int] = {}
    cf = Path(cache_file) if cache_file else None
    if cf and cf.is_file():
        cache = {k: int(v) for k, v in json.loads(cf.read_text(encoding="utf-8")).items()}
    out: Dict[str, int] = {}
    for d in map(Path, dirs):
        if not d.is_dir():
            continue
        for p in sorted(d.rglob("*")):
            if p.is_file() and p.suffix.lower() in IMG and "depth_cache" not in p.parts:
                sha = _sha(p)
                if sha not in cache:
                    h = dhash_file(p)
                    if h is None:
                        continue
                    cache[sha] = h
                out[f"{d.name}/{p.relative_to(d).as_posix()}"] = cache[sha]
    if cf:
        cf.parent.mkdir(parents=True, exist_ok=True)
        cf.write_text(json.dumps({k: str(v) for k, v in cache.items()}), encoding="utf-8")
    return out


def pool_shas(dirs: Sequence[str | Path]) -> Dict[str, str]:
    from .asset_index import IMG, VID, _sha
    out = {}
    for d in map(Path, dirs):
        if d.is_dir():
            for p in d.rglob("*"):
                if p.is_file() and p.suffix.lower() in IMG | VID:
                    out[_sha(p)] = f"{d.name}/{p.relative_to(d).as_posix()}"
    return out


def slug(s: str, n: int = 36) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (s or "").lower()).strip("_")[:n] or "item"
