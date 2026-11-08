"""F19-lite Screenshot style cloner (Phase 3): K-Means palette -> brand_draft.json.

Output is a DRAFT. It is merged into brand.json only after user approval.
Label: 'close, identical nahi'.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List, Tuple

import numpy as np


def _hex(rgb) -> str:
    return "#{:02X}{:02X}{:02X}".format(*[int(round(c)) for c in rgb])


def rel_luminance(hex_color: str) -> float:
    h = hex_color.lstrip("#")
    rgb = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
    return 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]


def contrast_ratio(a: str, b: str) -> float:
    """WCAG 2.x contrast ratio."""
    la, lb = sorted((rel_luminance(a), rel_luminance(b)), reverse=True)
    return round((la + 0.05) / (lb + 0.05), 2)


def kmeans(pixels: np.ndarray, k: int = 5, iters: int = 25, seed: int = 0) -> Tuple[np.ndarray, np.ndarray]:
    """Deterministic k-means (k-means++ init, fixed seed)."""
    rng = np.random.default_rng(seed)
    X = pixels.astype(np.float64)
    centers = [X[rng.integers(len(X))]]
    for _ in range(1, k):
        d = np.min(((X[:, None, :] - np.array(centers)[None]) ** 2).sum(-1), axis=1)
        if d.sum() == 0:
            centers.append(X[rng.integers(len(X))])
        else:
            centers.append(X[rng.choice(len(X), p=d / d.sum())])
    C = np.array(centers)
    for _ in range(iters):
        labels = np.argmin(((X[:, None, :] - C[None]) ** 2).sum(-1), axis=1)
        newC = np.array([X[labels == j].mean(0) if np.any(labels == j) else C[j] for j in range(k)])
        if np.allclose(newC, C):
            break
        C = newC
    labels = np.argmin(((X[:, None, :] - C[None]) ** 2).sum(-1), axis=1)
    return C, np.bincount(labels, minlength=k)


def _saturation(rgb) -> float:
    mx, mn = max(rgb) / 255, min(rgb) / 255
    return 0.0 if mx == 0 else (mx - mn) / mx


def extract_palette(image_path: str | Path, k: int = 5, sample: int = 20000) -> List[Dict[str, Any]]:
    from PIL import Image
    img = Image.open(image_path).convert("RGB")
    img.thumbnail((400, 400))
    px = np.asarray(img).reshape(-1, 3)
    if len(px) > sample:
        px = px[np.random.default_rng(0).choice(len(px), sample, replace=False)]
    C, counts = kmeans(px, k=min(k, len(np.unique(px, axis=0))))
    total = counts.sum()
    pal = [{"hex": _hex(c), "share": round(float(n) / total, 4), "saturation": round(_saturation(c), 3),
            "luminance": round(rel_luminance(_hex(c)), 4)} for c, n in zip(C, counts) if n > 0]
    return sorted(pal, key=lambda p: -p["share"])


def palette_to_brand_draft(palette: List[Dict[str, Any]], client: str = "draft") -> Dict[str, Any]:
    """background = most common; accent = most saturated of the rest; highlight = the
    remaining color with best contrast against background. Text = white/black by contrast."""
    bg = palette[0]["hex"]
    rest = palette[1:] or palette
    accent = max(rest, key=lambda p: (p["saturation"], p["share"]))["hex"]
    others = [p for p in rest if p["hex"] != accent] or rest
    highlight = max(others, key=lambda p: contrast_ratio(p["hex"], bg))["hex"]
    text = "#FFFFFF" if contrast_ratio("#FFFFFF", bg) >= contrast_ratio("#000000", bg) else "#000000"
    checks = {
        "text_vs_background": contrast_ratio(text, bg),
        "highlight_vs_background": contrast_ratio(highlight, bg),
        "accent_vs_background": contrast_ratio(accent, bg),
    }
    return {
        "status": "draft (approve before merging into brand.json)",
        "label": "close, identical nahi",
        "client": client,
        "colors": {"primary": bg, "accent": accent, "highlight": highlight, "text": text,
                   "outline": "#000000" if text == "#FFFFFF" else "#FFFFFF"},
        "palette": palette,
        "contrast": checks,
        "contrast_ok": checks["text_vs_background"] >= 4.5,
    }


def merge_brand_draft(brand: Dict[str, Any], draft: Dict[str, Any]) -> Dict[str, Any]:
    """Return a new brand dict with draft colors (only after user approval)."""
    out = dict(brand)
    out["colors"] = {**brand.get("colors", {}), **draft["colors"]}
    return out
