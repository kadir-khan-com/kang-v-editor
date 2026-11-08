"""Shared drawing helpers for v13 motion graphics (text cards + map route): own code, numpy / Pillow / OpenCV.

Frames are float32 RGB arrays (0..255). Text is rendered once per string into an RGBA sprite (Pillow, fonts from
the repo fonts/ folder, all SIL OFL) and composited at sub-pixel positions (cv2.warpAffine on the sprite only), so
slow slides never step by whole pixels. Frames are piped as rawvideo to FFmpeg (libx264, yuv420p, no audio).
"""
from __future__ import annotations

import math
import subprocess
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
FONTS = {"title": "Mukta-ExtraBold.ttf", "body": "Mukta-ExtraBold.ttf", "number": "Montserrat-Black.ttf"}
NAVY_TOP, NAVY_BOT = (18, 44, 72), (6, 14, 26)  # matches the v9 static cards
GOLD, WHITE, SOFT, BLUE = (250, 204, 21), (255, 255, 255), (203, 213, 225), (96, 165, 250)


# --------------------------------------------------------------------------- easing
def clamp01(x: float) -> float:
    return 0.0 if x <= 0 else 1.0 if x >= 1 else x


def ease_out_cubic(x: float) -> float:
    x = clamp01(x)
    return 1 - (1 - x) ** 3


def ease_in_out(x: float) -> float:
    x = clamp01(x)
    return x * x * (3 - 2 * x)


def ease_out_back(x: float, s: float = 1.6) -> float:
    x = clamp01(x)
    return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


# --------------------------------------------------------------------------- text sprites
@lru_cache(maxsize=64)
def font(kind: str, size: int):
    from PIL import ImageFont
    return ImageFont.truetype(str(ROOT / "fonts" / FONTS.get(kind, kind)), int(size))


def text_size(text: str, kind: str, size: int) -> Tuple[int, int]:
    f = font(kind, size)
    l, t, r, b = f.getbbox(text)
    return r - l, b - t


@lru_cache(maxsize=512)
def text_sprite(text: str, kind: str, size: int, color: Tuple[int, int, int], shadow: bool = True) -> np.ndarray:
    """RGBA float32 sprite (premultiplied not used; alpha 0..1), tight box + 6 px pad, soft drop shadow."""
    from PIL import Image, ImageDraw, ImageFilter
    f = font(kind, size)
    l, t, r, b = f.getbbox(text)
    pad = max(6, size // 10)
    w, h = r - l + 2 * pad, b - t + 2 * pad
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    if shadow:
        sh = Image.new("L", (w, h), 0)
        ImageDraw.Draw(sh).text((pad - l + 2, pad - t + 3), text, font=f, fill=150)
        sh = sh.filter(ImageFilter.GaussianBlur(max(2, size // 22)))
        im.putalpha(sh)
        im = Image.composite(Image.new("RGBA", (w, h), (0, 0, 0, 255)), im, sh)
        im.putalpha(sh)
    ImageDraw.Draw(im).text((pad - l, pad - t), text, font=f, fill=tuple(color) + (255,))
    a = np.asarray(im, dtype=np.float32)
    a[..., 3] /= 255.0
    return a


def pill_sprite(w: int, h: int, color: Tuple[int, int, int], alpha: float = 0.85, radius: Optional[int] = None,
                border: Optional[Tuple[int, int, int]] = None) -> np.ndarray:
    from PIL import Image, ImageDraw
    im = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = radius if radius is not None else h // 2
    d.rounded_rectangle((0, 0, int(w) - 1, int(h) - 1), radius=r, fill=tuple(color) + (int(255 * alpha),),
                        outline=(tuple(border) + (255,)) if border else None, width=3 if border else 0)
    a = np.asarray(im, dtype=np.float32)
    a[..., 3] /= 255.0
    return a


def blit(dst: np.ndarray, spr: np.ndarray, x: float, y: float, alpha: float = 1.0) -> Optional[Tuple[int, int, int, int]]:
    """Alpha-composite RGBA sprite onto float RGB frame at float (x, y) = top-left. Returns the drawn box."""
    if alpha <= 0.003:
        return None
    H, W = dst.shape[:2]
    ix, iy = int(math.floor(x)), int(math.floor(y))
    fx, fy = x - ix, y - iy
    h, w = spr.shape[:2]
    if fx > 1e-3 or fy > 1e-3:
        import cv2
        M = np.float32([[1, 0, fx], [0, 1, fy]])
        spr = cv2.warpAffine(spr, M, (w + 1, h + 1), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        h, w = spr.shape[:2]
    x0, y0, x1, y1 = max(0, ix), max(0, iy), min(W, ix + w), min(H, iy + h)
    if x0 >= x1 or y0 >= y1:
        return None
    s = spr[y0 - iy:y1 - iy, x0 - ix:x1 - ix]
    a = s[..., 3:4] * alpha
    region = dst[y0:y1, x0:x1]
    region *= (1 - a)
    region += s[..., :3] * a
    return x0, y0, x1, y1


# --------------------------------------------------------------------------- backgrounds
def gradient(w: int, h: int, top=NAVY_TOP, bot=NAVY_BOT) -> np.ndarray:
    t = np.linspace(0, 1, h, dtype=np.float32)[:, None, None]
    g = np.array(top, np.float32) * (1 - t) + np.array(bot, np.float32) * t
    return np.repeat(g, w, axis=1)


class DriftBackground:
    """Navy gradient + 3 soft glows drifting slowly (computed at 1/4 size, upscaled = smooth, cheap)."""

    def __init__(self, w: int, h: int, seed: int = 0):
        self.w, self.h = w, h
        self.lw, self.lh = w // 4, h // 4
        self.base = gradient(self.lw, self.lh)
        rng = np.random.default_rng(seed)
        self.glows = [(rng.uniform(0.1, 0.9), rng.uniform(0.15, 0.85), rng.uniform(0.18, 0.32), c, rng.uniform(0, 6.28))
                      for c in ((37, 99, 235), (250, 204, 21), (14, 116, 144))]
        yy, xx = np.mgrid[0:self.lh, 0:self.lw].astype(np.float32)
        self.xx, self.yy = xx / self.lw, yy / self.lh

    def frame(self, t: float) -> np.ndarray:
        import cv2
        img = self.base.copy()
        for k, (cx, cy, r, col, ph) in enumerate(self.glows):
            x = cx + 0.06 * math.sin(0.11 * t + ph)  # ~1 cycle per minute: drift, not motion sickness
            y = cy + 0.05 * math.cos(0.09 * t + ph * 1.3)
            d2 = ((self.xx - x) * 1.78) ** 2 + (self.yy - y) ** 2
            g = np.exp(-d2 / (2 * r * r))[..., None] * (0.16 if k == 1 else 0.24)
            img = img * (1 - g) + np.array(col, np.float32) * g
        return cv2.resize(img, (self.w, self.h), interpolation=cv2.INTER_CUBIC)


# --------------------------------------------------------------------------- encoding
class FrameWriter:
    def __init__(self, out: str | Path, w: int, h: int, fps: int = 25, crf: int = 18):
        self.out = Path(out)
        self.n = 0
        self.proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                                      "-s", f"{w}x{h}", "-r", str(fps), "-i", "-", "-an", "-c:v", "libx264",
                                      "-preset", "fast", "-crf", str(crf), "-pix_fmt", "yuv420p",
                                      "-movflags", "+faststart", str(self.out)], stdin=subprocess.PIPE)

    def write(self, frame: np.ndarray) -> None:
        self.proc.stdin.write(np.clip(frame, 0, 255).astype(np.uint8).tobytes())
        self.n += 1

    def close(self) -> int:
        self.proc.stdin.close()
        rc = self.proc.wait()
        if rc != 0:
            raise RuntimeError(f"ffmpeg encode failed ({rc}) for {self.out}")
        return self.n


# --------------------------------------------------------------------------- numbers
def fmt_int(v: float) -> str:
    """Indian-style grouping is the same as western below 1 lakh: 1,500 / 10,000 / 12,000."""
    v = int(round(v))
    return f"{v:,}"


def fmt_time(h: float, meridiem: str) -> str:
    hh = int(h)
    mm = int(round((h - hh) * 60))
    return f"{hh}:{mm:02d} {meridiem}"
