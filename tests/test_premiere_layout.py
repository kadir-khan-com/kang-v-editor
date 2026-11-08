"""Regression: xmeml layout that Premiere 24.6.1 accepted on the user's PC (H1-H6, 2026-10-31)."""
import re
import uuid
import xml.etree.ElementTree as ET

from core import premiere

MEDIA = {"path": "E:/kang/p/media/a.mp3", "name": "a.mp3", "duration": 100.0, "has_video": False,
         "channels": 1, "sample_rate": 48000}
VIS = [{"path": "E:/kang/p/visuals/s1.png", "name": "s1.png", "kind": "still", "start": 0, "end": 10, "in": 0,
        "width": 1600, "height": 1200},
       {"path": "E:/kang/p/visuals/c.mp4", "name": "c.mp4", "kind": "video", "start": 10, "end": 25, "in": 0,
        "src_duration": 6, "loop": True, "width": 1280, "height": 720}]


def _build():
    xml, st = premiere.build_xmeml("KANG test", MEDIA, [[0, 100]], fps=25,
                                   markers=[{"at": 0, "name": "S01 हेलो", "comment": "द्वारिका"}], visual_clips=VIS)
    return xml, st, ET.fromstring(xml.split("\n", 2)[2])


def test_uuid_is_guid_and_deterministic():
    xml, _, root = _build()
    u = root.find("sequence/uuid").text
    uuid.UUID(u)
    assert u == premiere.sequence_uuid("KANG test")
    assert "kang-" not in u


def test_child_order_media_then_timecode_then_markers():
    _, _, root = _build()
    tags = [c.tag for c in root.find("sequence")]
    assert tags[:5] == ["uuid", "duration", "rate", "name", "media"]
    assert tags.index("timecode") > tags.index("media")
    assert all(i > tags.index("timecode") for i, t in enumerate(tags) if t == "marker")


def test_tracks_closed_and_audio_format():
    _, _, root = _build()
    tracks = root.findall(".//media/video/track") + root.findall(".//media/audio/track")
    assert tracks
    for t in tracks:
        kids = [c.tag for c in t]
        assert kids[-2:] == ["enabled", "locked"]
    assert root.find("sequence/media/audio/format/samplecharacteristics/samplerate").text == "48000"


def test_files_have_timecode_dims_and_clips_masterclip():
    _, st, root = _build()
    for f in root.iter("file"):
        if f.find("name") is None:
            continue  # reference
        assert f.find("timecode") is not None
    dims = {f.find("name").text: (f.find(".//video/samplecharacteristics/width").text,
                                  f.find(".//video/samplecharacteristics/height").text)
            for f in root.iter("file") if f.find("name") is not None and f.find(".//video") is not None}
    assert dims == {"s1.png": ("1600", "1200"), "c.mp4": ("1280", "720")}
    for ci in root.iter("clipitem"):
        assert ci.find("masterclipid") is not None
    vis = [ci for ci in root.iter("clipitem") if ci.get("id", "").startswith("visual-")]
    assert all(ci.find("alphatype").text == "none" for ci in vis)
    assert st["visual_clipitems"] == 1 + 3  # still + 15 s of a 6 s loop
    assert {ci.find("masterclipid").text for ci in vis if ci.find("name").text == "c.mp4"} == {"masterclip-file-v2"}


def test_check_xmeml_still_passes():
    xml, _, _ = _build()
    assert premiere.check_xmeml(xml, 25)["pass"] is True


def test_check_xmeml_flags_old_layout():
    xml, _, root = _build()
    bad = xml.replace(premiere.sequence_uuid("KANG test"), "kang-KANG test")
    probs = premiere.check_xmeml(bad, 25)["problems"]
    assert "sequence uuid is not a GUID" in probs


def test_fix_paths_regex_and_files(tmp_path):
    xml, _, _ = _build()
    m = re.search(premiere.PATH_PREFIX_RE, xml)
    assert m and m.group(1) == "file://localhost/E%3a/kang/p/"
    premiere.write_fix_paths(tmp_path)
    ps = (tmp_path / "fix_paths.ps1").read_bytes()
    bat = (tmp_path / "FIX_PATHS.bat").read_bytes()
    ps.decode("ascii"); bat.decode("ascii")
    assert b"\r\n" in ps and b"fix_paths.ps1" in bat
    assert premiere.PATH_PREFIX_RE.replace("<pathurl>", "").split("(?:")[0][:10] in ps.decode()
