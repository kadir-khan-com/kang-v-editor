"""Download the open-licensed fonts Kang needs into ./fonts (idempotent).

Mukta ExtraBold (OFL, Devanagari + Latin) for Hinglish subtitles, Noto Sans Devanagari (OFL) fallback, Montserrat Black (OFL) for headings.
"""
from __future__ import annotations

import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FONTS = {
    "Mukta-ExtraBold.ttf":
        "https://github.com/google/fonts/raw/main/ofl/mukta/Mukta-ExtraBold.ttf",
    "NotoSansDevanagari-Bold.ttf":
        "https://github.com/notofonts/notofonts.github.io/raw/main/fonts/NotoSansDevanagari/hinted/ttf/NotoSansDevanagari-Bold.ttf",
    "Montserrat-Black.ttf":
        "https://github.com/JulietaUla/Montserrat/raw/master/fonts/ttf/Montserrat-Black.ttf",
}
# Roadmap v2 §11.2: licence file per font family (tests/test_licences.py checks they exist)
LICENCES = {
    "OFL-Mukta.txt": "https://raw.githubusercontent.com/google/fonts/main/ofl/mukta/OFL.txt",
    "OFL-Noto.txt": "https://raw.githubusercontent.com/notofonts/devanagari/main/OFL.txt",
    "OFL-Montserrat.txt": "https://raw.githubusercontent.com/JulietaUla/Montserrat/master/OFL.txt",
}


def fetch(dest: Path = ROOT / "fonts") -> int:
    dest.mkdir(parents=True, exist_ok=True)
    rc = 0
    for name, url in {**FONTS, **LICENCES}.items():
        p = dest / name
        if p.is_file() and p.stat().st_size > (1000 if name.endswith('.txt') else 10000):
            print(f"[fonts] ok  {name}")
            continue
        try:
            urllib.request.urlretrieve(url, p)
            print(f"[fonts] got {name} ({p.stat().st_size} bytes)")
        except Exception as exc:  # pragma: no cover
            print(f"[fonts] FAILED {name}: {exc}", file=sys.stderr)
            rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(fetch())
