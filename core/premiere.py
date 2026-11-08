"""M3 Workflow G, F12: Premiere Pro package as Final Cut Pro 7 XML (xmeml v4).

Premiere Pro 24.x opens xmeml via File > Open Project (Ctrl+O, "All Files") - verified on the user's PC 2026-10-31.
Element layout mirrors the H1-H6 diagnostic files that Premiere accepted (GUID uuid, media before timecode/markers,
track enabled/locked, sequence audio format, file timecode + video width/height, masterclipid, alphatype); the
previous layout (non-GUID uuid, markers before media, bare tracks) was rejected with "project could not be loaded". The sequence references the ORIGINAL
media (non-destructive): every kept range is one clipitem, so jump cuts stay editable in Premiere.
Scenes become sequence markers. Captions travel as an SRT sidecar (File > Import -> caption track).
Integer timebase only (25 / 30 / 50 / 60 fps, ntsc FALSE) so frame maths is exact.
"""
from __future__ import annotations

import uuid as _uuid
import xml.etree.ElementTree as ET
from pathlib import Path, PureWindowsPath
from typing import Any, Dict, List, Optional, Sequence, Tuple
from urllib.parse import quote

Range = Tuple[float, float]


def frames(t: float, fps: int) -> int:
    return int(round(t * fps))


def pathurl(path: str) -> str:
    """file://localhost/E%3a/kang/x.mp3 style URL (what Premiere itself writes) for Windows or POSIX paths."""
    if len(path) > 1 and path[1] == ":":  # Windows drive path
        p = PureWindowsPath(path).as_posix()
        drive, rest = p[0], p[2:]
        return "file://localhost/" + drive + "%3a" + quote(rest, safe="/")
    return "file://localhost" + quote(str(Path(path).as_posix()), safe="/")


def _rate(parent: ET.Element, fps: int) -> None:
    r = ET.SubElement(parent, "rate")
    ET.SubElement(r, "timebase").text = str(fps)
    ET.SubElement(r, "ntsc").text = "FALSE"


def _timecode(parent: ET.Element, fps: int) -> None:
    tc = ET.SubElement(parent, "timecode")
    _rate(tc, fps)
    _txt(tc, "string", "00:00:00:00")
    _txt(tc, "frame", 0)
    _txt(tc, "displayformat", "NDF")


def _video_chars(parent: ET.Element, fps: int, width: int, height: int) -> None:
    sc = ET.SubElement(parent, "samplecharacteristics")
    _rate(sc, fps)
    _txt(sc, "width", width)
    _txt(sc, "height", height)
    _txt(sc, "anamorphic", "FALSE")
    _txt(sc, "pixelaspectratio", "square")
    _txt(sc, "fielddominance", "none")


def _close_track(track: ET.Element) -> None:
    _txt(track, "enabled", "TRUE")
    _txt(track, "locked", "FALSE")


def sequence_uuid(name: str) -> str:
    """Deterministic RFC-4122 GUID per sequence name (Premiere expects a GUID, not free text)."""
    return str(_uuid.uuid5(_uuid.NAMESPACE_URL, "kang-sequence:" + name))


def _txt(parent: ET.Element, tag: str, value: Any) -> ET.Element:
    e = ET.SubElement(parent, tag)
    e.text = str(value)
    return e


def _motion_filter(ci: ET.Element, m: Dict[str, Any], length: int, iw: int, ih: int, sw: int, sh: int) -> None:
    """Basic Motion (FCP7 xmeml) Ken Burns on a still: scale keyframes from cover-fit * s0 to cover-fit * s1
    (cover-fit = the scale at which the image fills the sequence frame) and a small centre drift.
    keyframe <when> is clip-relative (stills start at in=0). Units of centre = fraction of the frame
    (0,0 = centred); drift is tiny (<=0.015) and tied to the zoom, so no edge shows either way."""
    cover = max(sw / max(1, iw), sh / max(1, ih)) * 100.0
    eff = ET.SubElement(ET.SubElement(ci, "filter"), "effect")
    _txt(eff, "name", "Basic Motion")
    _txt(eff, "effectid", "basic")
    _txt(eff, "effectcategory", "motion")
    _txt(eff, "effecttype", "motion")
    _txt(eff, "mediatype", "video")
    sc = ET.SubElement(eff, "parameter", authoringApp="PremierePro")
    _txt(sc, "parameterid", "scale")
    _txt(sc, "name", "Scale")
    _txt(sc, "valuemin", 0)
    _txt(sc, "valuemax", 1000)
    _txt(sc, "value", f"{cover * m['s0']:.3f}")
    last = max(1, length - 1)
    for when, s in ((0, m["s0"]), (last, m["s1"])):
        kf = ET.SubElement(sc, "keyframe")
        _txt(kf, "when", when)
        _txt(kf, "value", f"{cover * s:.3f}")
    ce = ET.SubElement(eff, "parameter", authoringApp="PremierePro")
    _txt(ce, "parameterid", "center")
    _txt(ce, "name", "Center")
    smax = m.get("smax", max(m["s0"], m["s1"]))

    def off(s: float) -> Tuple[float, float]:
        if m.get("focus"):  # off-centre subject: same clamped offset as the preview, no drift (fraction of frame)
            k0 = max(sw / max(1, iw), sh / max(1, ih)) * s
            slx, sly = (k0 * iw - sw) / 2, (k0 * ih - sh) / 2
            return (max(-slx, min(slx, -(m["focus"][0] - 0.5) * k0 * iw)) / sw,
                    max(-sly, min(sly, -(m["focus"][1] - 0.5) * k0 * ih)) / sh)
        f = (s - 1.0) / (smax - 1.0) if smax > 1.0 else 0.0
        return m.get("dx", 0.0) * f, m.get("dy", 0.0) * f
    v0 = ET.SubElement(ce, "value")
    x0, y0 = off(m["s0"])
    _txt(v0, "horiz", f"{x0:.4f}")
    _txt(v0, "vert", f"{y0:.4f}")
    for when, s in ((0, m["s0"]), (last, m["s1"])):
        kf = ET.SubElement(ce, "keyframe")
        _txt(kf, "when", when)
        vv = ET.SubElement(kf, "value")
        x, y = off(s)
        _txt(vv, "horiz", f"{x:.4f}")
        _txt(vv, "vert", f"{y:.4f}")


def build_xmeml(name: str, media: Dict[str, Any], keep: Sequence[Range], fps: int = 25,
                width: int = 1920, height: int = 1080, markers: Sequence[Dict[str, Any]] = (),
                visual_clips: Sequence[Dict[str, Any]] = ()) -> Tuple[str, Dict[str, Any]]:
    """media: {path (as Premiere should see it), name, duration, has_video, channels, sample_rate}.
    keep: source ranges in seconds, in order.
    visual_clips: scene visuals [{path, name, kind still|video, start, end (timeline s), in (s), src_duration (s,
    video), loop}] placed on their own video track (V1 when the narration has no picture, else V2).
    Returns (xml text, stats)."""
    if fps not in (24, 25, 30, 50, 60):
        raise ValueError("fps must be an integer timebase (24/25/30/50/60)")
    keep = [(float(a), float(b)) for a, b in keep if b > a]
    if not keep:
        raise ValueError("nothing to place on the timeline")
    for (a1, b1), (a2, b2) in zip(keep, keep[1:]):
        if a2 < b1:
            raise ValueError(f"keep ranges overlap: {a1}-{b1} / {a2}-{b2}")
    src_frames = frames(media["duration"], fps)
    channels = 1 if int(media.get("channels", 2)) == 1 else 2
    has_video = bool(media.get("has_video"))

    # timeline positions in whole frames; each clip's length = its source length in frames
    clips, pos = [], 0
    for a, b in keep:
        i_, o_ = frames(a, fps), min(frames(b, fps), src_frames)
        if o_ <= i_:
            continue
        clips.append({"in": i_, "out": o_, "start": pos, "end": pos + (o_ - i_)})
        pos += o_ - i_
    seq_frames = pos

    root = ET.Element("xmeml", version="4")
    seq = ET.SubElement(root, "sequence", id="sequence-1")
    _txt(seq, "uuid", sequence_uuid(name))
    _txt(seq, "duration", seq_frames)
    _rate(seq, fps)
    _txt(seq, "name", name)
    mt = ET.SubElement(seq, "media")
    vid = ET.SubElement(mt, "video")
    _video_chars(ET.SubElement(vid, "format"), fps, width, height)
    vtrack = ET.SubElement(vid, "track")
    aud = ET.SubElement(mt, "audio")
    _txt(aud, "numOutputChannels", 2)
    afs = ET.SubElement(ET.SubElement(aud, "format"), "samplecharacteristics")
    _txt(afs, "depth", 16)
    _txt(afs, "samplerate", int(media.get("sample_rate", 48000)))
    atracks = [ET.SubElement(aud, "track") for _ in range(channels)]

    file_written = False

    def file_el(parent: ET.Element) -> None:
        nonlocal file_written
        if file_written:
            ET.SubElement(parent, "file", id="file-1")
            return
        file_written = True
        f = ET.SubElement(parent, "file", id="file-1")
        _txt(f, "name", media["name"])
        _txt(f, "pathurl", pathurl(media["path"]))
        _rate(f, fps)
        _txt(f, "duration", src_frames)
        _timecode(f, fps)
        fm = ET.SubElement(f, "media")
        if has_video:
            _video_chars(ET.SubElement(fm, "video"), fps, int(media.get("width") or width),
                         int(media.get("height") or height))
        fa = ET.SubElement(fm, "audio")
        sa = ET.SubElement(fa, "samplecharacteristics")
        _txt(sa, "depth", 16)
        _txt(sa, "samplerate", int(media.get("sample_rate", 48000)))
        _txt(fa, "channelcount", channels)

    def clipitem(track: ET.Element, cid: str, c: Dict[str, int], kind: str, tindex: int) -> None:
        ci = ET.SubElement(track, "clipitem", id=cid)
        _txt(ci, "masterclipid", "masterclip-1")
        _txt(ci, "name", media["name"])
        _txt(ci, "enabled", "TRUE")
        _txt(ci, "duration", src_frames)
        _rate(ci, fps)
        _txt(ci, "start", c["start"])
        _txt(ci, "end", c["end"])
        _txt(ci, "in", c["in"])
        _txt(ci, "out", c["out"])
        if kind == "video":
            _txt(ci, "alphatype", "none")
        file_el(ci)
        if kind == "audio":
            st = ET.SubElement(ci, "sourcetrack")
            _txt(st, "mediatype", "audio")
            _txt(st, "trackindex", tindex)

    for n, c in enumerate(clips, 1):
        if has_video:
            clipitem(vtrack, f"clipitem-v{n}", c, "video", 1)
        for t, tr in enumerate(atracks, 1):
            clipitem(tr, f"clipitem-a{t}-{n}", c, "audio", t)

    n_visual = 0
    n_motion = 0
    if visual_clips:
        vis_track = ET.SubElement(vid, "track") if has_video else vtrack
        files_done: Dict[str, str] = {}
        for k, v in enumerate(sorted(visual_clips, key=lambda x: x["start"]), 1):
            s0, s1 = frames(v["start"], fps), min(frames(v["end"], fps), seq_frames)
            if s1 <= s0:
                continue
            still = v["kind"] == "still"
            fdur = (s1 - s0) if still else frames(v["src_duration"], fps)
            a_in = 0 if still else frames(v.get("in", 0.0), fps)
            pieces, pos_ = [], s0
            while pos_ < s1:  # a looped video repeats as consecutive clipitems
                ln = min(s1 - pos_, fdur - a_in)
                if ln <= 0:
                    break
                pieces.append((pos_, pos_ + ln, a_in, a_in + ln))
                pos_ += ln
                if not v.get("loop"):
                    break
                a_in = 0
            for j, (st, en, i_, o_) in enumerate(pieces, 1):
                ci = ET.SubElement(vis_track, "clipitem", id=f"visual-{k}-{j}")
                vkey = files_done.get(v["path"]) or f"file-v{len(files_done) + 1}"
                _txt(ci, "masterclipid", "masterclip-" + vkey)
                _txt(ci, "name", v["name"])
                _txt(ci, "enabled", "TRUE")
                _txt(ci, "duration", fdur)
                _rate(ci, fps)
                for tag, val in (("start", st), ("end", en), ("in", i_), ("out", o_)):
                    _txt(ci, tag, val)
                _txt(ci, "alphatype", "none")
                fid = files_done.get(v["path"])
                if fid:
                    ET.SubElement(ci, "file", id=fid)
                else:
                    fid = f"file-v{len(files_done) + 1}"
                    files_done[v["path"]] = fid
                    f = ET.SubElement(ci, "file", id=fid)
                    _txt(f, "name", v["name"])
                    _txt(f, "pathurl", pathurl(v["path"]))
                    _rate(f, fps)
                    _txt(f, "duration", fdur)
                    _timecode(f, fps)
                    _video_chars(ET.SubElement(ET.SubElement(f, "media"), "video"), fps,
                                 int(v.get("width") or width), int(v.get("height") or height))
                if still and v.get("motion"):
                    _motion_filter(ci, v["motion"], en - st, int(v.get("width") or width),
                                   int(v.get("height") or height), width, height)
                    n_motion += 1
                n_visual += 1
    for tr in [t for t in vid.findall("track")] + atracks:
        _close_track(tr)
    _timecode(seq, fps)  # after <media>, then markers (Premiere-accepted order)
    for m in markers:
        mk = ET.SubElement(seq, "marker")
        _txt(mk, "comment", m.get("comment", ""))
        _txt(mk, "name", m["name"])
        _txt(mk, "in", frames(m["at"], fps))
        _txt(mk, "out", -1)
    ET.indent(root, space="  ")
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n' + ET.tostring(root, encoding="unicode") + "\n"
    stats = {"fps": fps, "clips": len(clips), "sequence_frames": seq_frames, "sequence_s": round(seq_frames / fps, 3),
             "source_frames": src_frames, "audio_tracks": channels, "video": has_video, "source_has_video": has_video,
             "visual_track": n_visual > 0, "markers": len(markers), "visual_clipitems": n_visual,
             "motion_clipitems": n_motion}
    return xml, stats


def check_xmeml(xml: str, fps: int) -> Dict[str, Any]:
    """Structural QA: parses, clips contiguous on the timeline (no gap/overlap), in<out, one full file element,
    sequence duration = sum of clip lengths. Returns {pass, problems}."""
    problems: List[str] = []
    root = ET.fromstring(xml.split("\n", 2)[2] if xml.startswith("<?xml") else xml)
    seq = root.find("sequence")
    dur = int(seq.findtext("duration"))
    if int(seq.findtext("rate/timebase")) != fps:
        problems.append("sequence timebase mismatch")
    full_files = [f for f in root.iter("file") if f.find("pathurl") is not None]
    ids = {f.get("id") for f in root.iter("file")}
    if len(full_files) != len(ids) or len({f.get("id") for f in full_files}) != len(full_files):
        problems.append(f"every <file> id needs exactly one full definition ({len(full_files)} full, {len(ids)} ids)")
    # Premiere-accepted layout (2026-10-31 H1-H6): GUID uuid, media before timecode/markers, closed tracks
    try:
        _uuid.UUID(seq.findtext("uuid") or "")
    except ValueError:
        problems.append("sequence uuid is not a GUID")
    tags = [c.tag for c in seq]
    if "media" not in tags or "timecode" not in tags or tags.index("timecode") < tags.index("media"):
        problems.append("sequence <timecode> must follow <media>")
    elif any(t == "marker" and i < tags.index("media") for i, t in enumerate(tags)):
        problems.append("markers must follow <media>")
    for tr in seq.findall("media/video/track") + seq.findall("media/audio/track"):
        if [c.tag for c in tr][-2:] != ["enabled", "locked"]:
            problems.append("track missing trailing <enabled>/<locked>")
            break
    if "file-1" not in {f.get("id") for f in full_files}:
        problems.append("narration media file-1 missing")
    for kind in ("video", "audio"):
        for ti, tr in enumerate(seq.findall(f"media/{kind}/track"), 1):
            vis = [ci for ci in tr.findall("clipitem") if ci.get("id", "").startswith("visual-")]
            if vis:  # scene visuals: ordered, no overlap, inside the sequence (gaps allowed = scene without visual)
                end_prev = 0
                for ci in vis:
                    s, e, i, o = (int(ci.findtext(k)) for k in ("start", "end", "in", "out"))
                    if s < end_prev or e > dur or o <= i or e - s != o - i:
                        problems.append(f"{kind} track {ti} {ci.get('id')}: overlap/length/out of sequence")
                    end_prev = e
                if len(vis) != len(tr.findall("clipitem")):
                    problems.append(f"{kind} track {ti}: visuals mixed with narration clips")
                continue
            pos = 0
            for ci in tr.findall("clipitem"):
                s, e, i, o = (int(ci.findtext(k)) for k in ("start", "end", "in", "out"))
                if s != pos:
                    problems.append(f"{kind} track {ti} {ci.get('id')}: starts {s}, expected {pos}")
                if o <= i or e - s != o - i:
                    problems.append(f"{kind} track {ti} {ci.get('id')}: length mismatch")
                pos = e
            if tr.findall("clipitem") and pos != dur:
                problems.append(f"{kind} track {ti}: ends {pos}, sequence {dur}")
    for ci in root.iter("clipitem"):  # Ken Burns filters (beat layer): keyframes inside the clip, scale > 0
        for prm in ci.findall("filter/effect/parameter"):
            ln = int(ci.findtext("end")) - int(ci.findtext("start"))
            for kf in prm.findall("keyframe"):
                w = int(kf.findtext("when"))
                if not 0 <= w <= max(0, ln - 1) + 1:
                    problems.append(f"{ci.get('id')}: keyframe at {w} outside clip length {ln}")
                if prm.findtext("parameterid") == "scale" and float(kf.findtext("value")) <= 0:
                    problems.append(f"{ci.get('id')}: scale keyframe <= 0")
    return {"name": "premiere_xml", "pass": not problems, "problems": problems}


# --- "extract anywhere" relink helper (2026-10-31: user hit Link Media after extracting to Downloads) ---
PATH_PREFIX_RE = r"<pathurl>(file://localhost/[^<]*?/)(?:media|visuals)/[^/<]+</pathurl>"

FIX_PATHS_PS1 = r"""# KANG: point sequence.xml at THIS folder (wherever you extracted it). Safe to run again.
$ErrorActionPreference = 'Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$p = Join-Path $here 'sequence.xml'
$x = [IO.File]::ReadAllText($p, [Text.Encoding]::UTF8)
$m = [regex]::Match($x, '<pathurl>(file://localhost/[^<]*?/)(?:media|visuals)/[^/<]+</pathurl>')
if (-not $m.Success) { Write-Host 'FAIL: no media path found in sequence.xml'; exit 1 }
$cur = $m.Groups[1].Value
$segs = ($here -replace '\\', '/').Split('/') | Where-Object { $_ -ne '' }
if ($segs[0] -notmatch '^[A-Za-z]:$') { Write-Host "FAIL: folder must be on a drive letter (got $here)"; exit 1 }
$drive = $segs[0].Substring(0, 1)
$rest = ($segs | Select-Object -Skip 1 | ForEach-Object { [uri]::EscapeDataString($_) }) -join '/'
$new = if ($rest) { "file://localhost/$drive%3a/$rest/" } else { "file://localhost/$drive%3a/" }
$x = $x.Replace($cur, $new)
[IO.File]::WriteAllText($p, $x, (New-Object Text.UTF8Encoding($false)))
$missing = @()
foreach ($u in [regex]::Matches($x, '<pathurl>file://localhost/([^<]+)</pathurl>')) {
  $f = [uri]::UnescapeDataString($u.Groups[1].Value) -replace '/', '\'
  if (-not (Test-Path -LiteralPath $f)) { $missing += $f }
}
if ($missing.Count) { Write-Host 'WARN: missing files:'; $missing | Sort-Object -Unique | ForEach-Object { Write-Host "  $_" } }
else { Write-Host "PASS: sequence.xml now points to $here" }
"""

FIX_PATHS_BAT = ('@echo off\r\npowershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0fix_paths.ps1"\r\n'
                 'echo.\r\necho Ab Premiere mein Ctrl+O se sequence.xml kholo.\r\npause\r\n')


def write_fix_paths(pkg_dir: Path) -> None:
    """Drop FIX_PATHS.bat + fix_paths.ps1 next to sequence.xml (Windows, ASCII, CRLF)."""
    (Path(pkg_dir) / "fix_paths.ps1").write_bytes(FIX_PATHS_PS1.replace("\r\n", "\n").replace("\n", "\r\n").encode("ascii"))
    (Path(pkg_dir) / "FIX_PATHS.bat").write_bytes(FIX_PATHS_BAT.encode("ascii"))
