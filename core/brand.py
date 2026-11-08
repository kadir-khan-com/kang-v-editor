"""F16 Brand kit engine: brand.json = single source of truth (video + design).

Rules from the roadmap:
- Validate before every run.
- Missing font -> fallback font + VISIBLE warning (never a silent fail).
- Safe margin per format: max(brand.safe_margin_px, format safe zone).
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from pydantic import BaseModel, Field, field_validator

HEX_RE = re.compile(r"^#[0-9A-Fa-f]{6}$")

# Format-level minimums (roadmap F15: never below 40px). Values are px on the canvas.
FORMAT_MIN_MARGIN = {"9:16": 40, "16:9": 40, "1:1": 40, "4:5": 40}

CANVAS = {"9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080), "4:5": (1080, 1350)}


class SafeZone(BaseModel):
    subtitle_bottom_px: int = Field(ge=0, le=1000)


class Colors(BaseModel):
    primary: str
    accent: str
    highlight: str
    text: str = "#FFFFFF"
    outline: str = "#000000"

    @field_validator("*")
    @classmethod
    def _hex(cls, v: str) -> str:
        if not HEX_RE.match(v):
            raise ValueError(f"color must be #RRGGBB, got {v!r}")
        return v.upper()


class Fonts(BaseModel):
    heading: str
    body: str
    hindi: str


class Brand(BaseModel):
    client: str = Field(min_length=1)
    colors: Colors
    fonts: Fonts
    logo_path: Optional[str] = None
    safe_margin_px: int = Field(ge=0, le=400)
    safe_zones: Dict[str, SafeZone]

    @field_validator("safe_zones")
    @classmethod
    def _formats(cls, v: Dict[str, SafeZone]) -> Dict[str, SafeZone]:
        bad = [k for k in v if k not in CANVAS]
        if bad:
            raise ValueError(f"unknown format(s) in safe_zones: {bad}; allowed {list(CANVAS)}")
        if "9:16" not in v:
            raise ValueError("safe_zones must define 9:16 (Workflow A)")
        return v

    # ---- derived ----------------------------------------------------------
    def margin_for(self, fmt: str) -> int:
        """Rule: max(brand.safe_margin_px, format safe zone minimum)."""
        return max(self.safe_margin_px, FORMAT_MIN_MARGIN.get(fmt, 40))

    def subtitle_bottom_for(self, fmt: str) -> int:
        zone = self.safe_zones.get(fmt)
        base = zone.subtitle_bottom_px if zone else 0
        return max(base, self.margin_for(fmt))


def load_brand(path: str | Path) -> Brand:
    p = Path(path)
    data = json.loads(p.read_text(encoding="utf-8"))
    return Brand.model_validate(data)


def resolve_fonts(brand: Brand, fonts_dir: str | Path, fallback: str = "NotoSansDevanagari-Bold.ttf") -> Tuple[Dict[str, Path], List[str]]:
    """Return {role: font path} and a list of visible warnings for missing fonts."""
    fonts_dir = Path(fonts_dir)
    resolved: Dict[str, Path] = {}
    warnings: List[str] = []
    fb = fonts_dir / fallback
    for role, name in brand.fonts.model_dump().items():
        p = fonts_dir / name
        if p.is_file():
            resolved[role] = p
        elif fb.is_file():
            resolved[role] = fb
            warnings.append(f"FONT MISSING: '{name}' ({role}) not in {fonts_dir}; using fallback '{fallback}'.")
        else:
            raise FileNotFoundError(f"Font '{name}' and fallback '{fallback}' both missing in {fonts_dir}")
    return resolved, warnings


def font_family_name(font_path: str | Path) -> str:
    """Family name as libass will see it (name ID 1 first, then 16)."""
    from fontTools.ttLib import TTFont
    f = TTFont(str(font_path), lazy=True)
    name = f["name"]
    for nid in (1, 16):  # libass matches the legacy family (ID1), e.g. "Mukta ExtraBold"
        rec = name.getName(nid, 3, 1) or name.getName(nid, 1, 0)
        if rec:
            return str(rec)
    return Path(font_path).stem


def missing_glyphs(font_path: str | Path, text: str) -> List[str]:
    """Characters in `text` that the font cannot render (tofu risk)."""
    from fontTools.ttLib import TTFont
    cmap = TTFont(str(font_path), lazy=True).getBestCmap()
    skip = {" ", "\n", "\u200c", "\u200d"}
    return sorted({ch for ch in text if ch not in skip and ord(ch) not in cmap})


def hex_to_rgb(h: str) -> Tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def hex_to_ass(h: str, alpha: int = 0) -> str:
    """#RRGGBB -> ASS &HAABBGGRR."""
    r, g, b = hex_to_rgb(h)
    return f"&H{alpha:02X}{b:02X}{g:02X}{r:02X}"
