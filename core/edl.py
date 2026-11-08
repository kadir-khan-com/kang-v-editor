"""Master EDL (kang.edl/1.0): the one brain both engines read.

Schema follows roadmap Section 3. Validated with Pydantic before any render.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, model_validator

Approval = Literal["pending", "approved", "rejected", "n/a"]


class Input(BaseModel):
    id: str
    path: str
    sha256: str = Field(min_length=64, max_length=64)


class Cut(BaseModel):
    src: str
    in_: float = Field(alias="in", ge=0)
    out: float = Field(gt=0)
    type: Literal["keep", "jumpcut"] = "keep"
    reframe_x: float = Field(0.5, ge=0, le=1)

    model_config = {"populate_by_name": True}

    @model_validator(mode="after")
    def _order(self):
        if self.out <= self.in_:
            raise ValueError(f"cut out ({self.out}) must be > in ({self.in_})")
        return self


class Subtitles(BaseModel):
    preset: str
    font: str
    ass: str
    option: Literal["A", "B"] = "A"


class BRoll(BaseModel):
    src: str
    t_in: float = Field(ge=0)
    dur: float = Field(gt=0)
    anim: str = "slide_up"
    status: Literal["suggested", "approved", "rejected"] = "suggested"
    license: str = Field(min_length=1)


class Motion(BaseModel):
    template: str
    params: Dict[str, Any] = {}
    t_in: float = Field(ge=0)
    dur: float = Field(gt=0)


class Audio(BaseModel):
    denoise: bool = True
    target_lufs: float = Field(-14.0, ge=-30, le=-5)
    true_peak_db: float = Field(-1.5, ge=-9, le=0)
    music: Optional[str] = None
    duck_db: float = -18


class Export(BaseModel):
    ratio: Literal["9:16", "16:9", "1:1", "4:5"]
    codec: Literal["h264"] = "h264"
    crf: int = Field(20, ge=0, le=51)


class Approvals(BaseModel):
    cut_list: Approval = "pending"
    preview: Approval = "pending"
    paid_api: Approval = "n/a"


class EDL(BaseModel):
    schema_: Literal["kang.edl/1.0"] = Field("kang.edl/1.0", alias="schema")
    run_id: str
    brand: str = "brand.json"
    canvas: List[int] = Field(default=[1080, 1920], min_length=2, max_length=2)
    fps: int = Field(30, ge=1, le=120)
    inputs: List[Input]
    cuts: List[Cut] = []
    subtitles: Optional[Subtitles] = None
    b_roll: List[BRoll] = []
    motion: List[Motion] = []
    audio: Audio = Audio()
    export: List[Export] = [Export(ratio="9:16")]
    approvals: Approvals = Approvals()
    status: Literal["planned", "approved", "rendered", "failed"] = "planned"

    model_config = {"populate_by_name": True}

    @model_validator(mode="after")
    def _refs(self):
        ids = {i.id for i in self.inputs}
        for c in self.cuts:
            if c.src not in ids:
                raise ValueError(f"cut references unknown input {c.src!r}")
        # cuts per source must not overlap and must be ordered
        last: Dict[str, float] = {}
        for c in self.cuts:
            if c.in_ < last.get(c.src, -1.0) - 1e-6:
                raise ValueError(f"cuts overlap / out of order at {c.in_}")
            last[c.src] = c.out
        return self

    def kept_duration(self) -> float:
        return round(sum(c.out - c.in_ for c in self.cuts), 3)

    def dump(self) -> Dict[str, Any]:
        return self.model_dump(by_alias=True, mode="json")


def load_edl(path: str | Path) -> EDL:
    return EDL.model_validate(json.loads(Path(path).read_text(encoding="utf-8")))


def save_edl(edl: EDL, path: str | Path) -> Path:
    p = Path(path)
    p.write_text(json.dumps(edl.dump(), ensure_ascii=False, indent=2), encoding="utf-8")
    return p
