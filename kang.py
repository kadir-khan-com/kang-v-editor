"""Kang AI CLI. One run = one folder under runs/ (or $KANG_RUNS_DIR).

Approval gates (cut list, preview) ask y/n in the terminal. Pass --yes only when you
have already reviewed what will be produced.

Examples
  python kang.py check                                   # Phase 0: PASS/FAIL report
  python kang.py transcribe voice.mp3 --device cpu       # Phase 1: words.json + audit
  python kang.py workflow voice.mp3 --start 0 --dur 60   # Phase 3: 1 command, 3 formats
  python kang.py workflow voice.mp3 --full --yes          # whole file -> 16:9 long video
  python kang.py fix-words runs/<id>/words.json          # glossary: द्वारी का -> द्वारका  [--spelling-policy config/caption_spelling_policy.json]
  python kang.py subs video.mp4 runs/<id>/words.json     # F01: preview -> approve -> final
  python kang.py promo voice.mp3 words.json --start 0 --dur 20   # Phase 2 exit proof
  python kang.py cut raw.mp4 words.json                  # F03: cut list -> approve -> cut
  python kang.py audio raw.mp4                           # F04: -14 LUFS / -1.5 dBTP
  python kang.py formats final.mp4 --words words.json --to 9:16 16:9 1:1   # F05
  python kang.py palette screenshot.png                  # F19-lite: brand_draft.json
  python kang.py presets                                 # F02: list presets
  python kang.py review voice.mp3 words.json --phrase "बेड द्वारका"   # review.csv + clips (no edits)
  python kang.py apply-review words.json review.csv      # your fixes -> new words.json + accept gate
  python kang.py package voice.mp3 words.json --win-root E:/kang/packages/x  # M3 Premiere package
  python kang.py beats words.json scenes.json --out beats_lag --anchor lag --visuals v9.csv   # beat layer
  python kang.py parallax photo.jpg --out px.mp4 --dur 8 --move dolly          # 2.5D parallax (CPU)
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))


def _approver(args):
    from core.pipeline import cli_approver
    if not args.yes:
        return cli_approver

    def auto(g, i):  # dev/automation only: recorded as auto(--yes) in approvals.json, never as a human review
        return True
    auto.approver_name = "auto(--yes)"
    return auto


def _print(obj):
    print(json.dumps(obj, ensure_ascii=False, indent=2, default=str))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="kang", description="Kang AI Creative Automation (Phase 0-3)")
    _vf = Path(__file__).resolve().parent / "VERSION"
    ap.add_argument("--version", action="version",
                    version="kang " + (_vf.read_text(encoding="utf-8").strip() if _vf.exists() else "unknown"))
    sub = ap.add_subparsers(dest="cmd", required=True)

    sub.add_parser("check", help="Phase 0 build & environment check")
    sub.add_parser("presets", help="List subtitle presets (F02)")

    p = sub.add_parser("transcribe", help="Phase 1: audio -> words.json (cut=False)")
    p.add_argument("audio"); p.add_argument("--lang", default="hi"); p.add_argument("--model", default="large-v3-turbo")
    p.add_argument("--device", choices=["cuda", "cpu"]); p.add_argument("--prompt")
    p.add_argument("--voters", help="spelling voter: name=ct2_dir,... (default: config/voters.json models)"); p.add_argument("--wordlist")
    p.add_argument("--no-vote", action="store_true", help="turn the spelling voter off")
    p.add_argument("--spelling-policy", help="per-video caption spelling json (opt-in, e.g. config/caption_spelling_policy.json)")

    for name, hlp in (("subs", "F01 animated subtitles"), ("promo", "Phase 2 promo clip from voiceover")):
        p = sub.add_parser(name, help=hlp)
        p.add_argument("media"); p.add_argument("words")
        p.add_argument("--fmt", default="9:16", choices=["9:16", "16:9", "1:1", "4:5"])
        p.add_argument("--preset", default="vox_bold_yellow")
        p.add_argument("--yes", action="store_true", help="approve the preview gate non-interactively")
        if name == "subs":
            p.add_argument("--preview-start", type=float, default=0.0)
            p.add_argument("--option", choices=["A", "B"])
        else:
            p.add_argument("--start", type=float, default=0.0); p.add_argument("--dur", type=float, default=20.0)

    p = sub.add_parser("workflow", help="Phase 3: audio/video -> cut -> clean -> subtitles in all formats")
    p.add_argument("source"); p.add_argument("--start", type=float, default=0.0); p.add_argument("--dur", type=float, default=60.0)
    p.add_argument("--to", nargs="+", default=None, help="formats (default: 9:16 16:9 1:1; --full: 16:9)")
    p.add_argument("--full", action="store_true", help="whole file from --start (max 1 h), --dur ignored")
    p.add_argument("--preset", default="vox_bold_yellow")
    p.add_argument("--lang", default="hi"); p.add_argument("--device", choices=["cuda", "cpu"]); p.add_argument("--prompt")
    p.add_argument("--model", default="large-v3-turbo"); p.add_argument("--yes", action="store_true")
    p.add_argument("--voters", help="spelling voter: name=ct2_dir,... (default: config/voters.json models)"); p.add_argument("--wordlist")
    p.add_argument("--no-vote", action="store_true", help="turn the spelling voter off")
    p.add_argument("--spelling-policy", help="per-video caption spelling json (opt-in, e.g. config/caption_spelling_policy.json)")

    p = sub.add_parser("fix-words", help="Apply config/glossary.json to words.json (new run)")
    p.add_argument("words"); p.add_argument("--glossary")
    p.add_argument("--spelling-policy", help="per-video caption spelling json (opt-in)")

    p = sub.add_parser("cut", help="F03 silence + filler cut")
    p.add_argument("media"); p.add_argument("words"); p.add_argument("--noise-db", type=float, default=-34.0)
    p.add_argument("--min-silence", type=float, default=0.45); p.add_argument("--yes", action="store_true")

    p = sub.add_parser("audio", help="F04 cleanup + loudness")
    p.add_argument("media"); p.add_argument("--lufs", type=float, default=-14.0); p.add_argument("--tp", type=float, default=-1.5)
    p.add_argument("--rnnoise-model")

    p = sub.add_parser("formats", help="F05 multi-format render")
    p.add_argument("video"); p.add_argument("--words"); p.add_argument("--to", nargs="+", default=["9:16", "16:9", "1:1"])
    p.add_argument("--preset", default="vox_bold_yellow"); p.add_argument("--reframe-x", type=float, default=0.5)

    p = sub.add_parser("visuals-template", help="scenes.json -> visuals.csv (brief/asset/licence per scene)")
    p.add_argument("scenes"); p.add_argument("--out")
    p = sub.add_parser("visuals", help="approved local visuals -> preview mp4 (chosen scenes) + Premiere package with visual track")
    p.add_argument("media"); p.add_argument("words"); p.add_argument("scenes"); p.add_argument("visuals_csv")
    p.add_argument("--assets", required=True, help="folder holding your images/clips (asset paths are relative to it)")
    p.add_argument("--preview", help="contiguous scenes for the integration preview, e.g. S01,S02,S03")
    p.add_argument("--fps", type=int, default=25); p.add_argument("--win-root"); p.add_argument("--yes", action="store_true")
    p.add_argument("--selected-by", default="user", help="who picked the visuals (user / agent_under_user_delegation ...); recorded in README + manifest")

    p = sub.add_parser("ingest", help="Asset Brain v0: scan assets dir -> index.json (tags, licence, sha256) [+ contact sheet]")
    p.add_argument("assets"); p.add_argument("--briefs", nargs="*", default=[], help="visuals CSV(s) whose brief column adds tags")
    p.add_argument("--out"); p.add_argument("--sheet", help="write a labelled contact sheet (jpg) here")
    p = sub.add_parser("asset-search", help="Tag search in index.json (Hindi/English aliases); hints only, selects nothing")
    p.add_argument("index"); p.add_argument("query"); p.add_argument("--top", type=int, default=3)
    p.add_argument("--no-sharealike", action="store_true", help="skip CC BY-SA assets")
    p = sub.add_parser("match", help="Asset Brain Phase 2: scenes + index.json -> broll_suggestions.json/.csv (hints, top-3 per scene)")
    p.add_argument("scenes"); p.add_argument("index"); p.add_argument("--words"); p.add_argument("--top", type=int, default=3)
    p.add_argument("--out", required=True, help="output prefix, writes <out>.json and <out>.csv")
    p.add_argument("--no-sharealike", action="store_true"); p.add_argument("--eval-csv", help="visuals CSV actually used -> hit@k")
    p = sub.add_parser("match-approve", help="your choices in broll_suggestions.csv (choose=1) -> visuals.csv for `visuals`")
    p.add_argument("suggestions_csv"); p.add_argument("index"); p.add_argument("scenes"); p.add_argument("--out", required=True)
    p.add_argument("--allow-missing", action="store_true")
    p = sub.add_parser("match-check", help="structural QA of broll_suggestions.json (coverage, 3/scene, duplicates, reasons)")
    p.add_argument("suggestions"); p.add_argument("--scenes", help="scenes.json for expected scene ids")
    p.add_argument("--sheet", help="also write a spot-check image (narration + A/B/C thumbs); needs --scenes and --assets")
    p.add_argument("--assets"); p.add_argument("--only", help="scene ids for the sheet, e.g. S04,S09,S13")
    p = sub.add_parser("approve-broll", help="choose A/B/C per scene (prompt, or --choices S01=A,S02=AB,S22=skip) -> approved_broll.json + visuals.csv")
    p.add_argument("suggestions"); p.add_argument("index"); p.add_argument("scenes")
    p.add_argument("--out", required=True, help="visuals.csv to write"); p.add_argument("--approved", help="approved_broll.json (default next to --out)")
    p.add_argument("--choices"); p.add_argument("--allow-missing", action="store_true")
    p = sub.add_parser("package", help="M3 Workflow G: words -> scenes.json -> Gate 1 -> Premiere package (FCP7 XML)")
    p.add_argument("media")
    p.add_argument("words")
    p.add_argument("--scenes", help="your edited scenes.json (default: generate)")
    p.add_argument("--cuts", help="cuts.json from a run whose cut_list gate is approved (default: no cuts)")
    p.add_argument("--fps", type=int, default=25)
    p.add_argument("--win-root", help=r"Windows folder the package will live in, e.g. E:\kang\packages\dwarika")
    p.add_argument("--english-script", choices=["asr", "latin", "devanagari"], default="asr",
                   help="captions only: English words as transcribed (asr), in Latin, or in Devanagari")
    p.add_argument("--yes", action="store_true")
    p = sub.add_parser("review", help="Transcript review sheet: review.csv + audio clips (changes no words)")
    p.add_argument("media"); p.add_argument("words")
    p.add_argument("--phrase", action="append", default=[], help="extra suspicious phrase to add (repeatable)")
    p.add_argument("--no-clips", action="store_true")
    p = sub.add_parser("apply-review", help="Apply your filled review.csv -> new words.json (+ accept gate)")
    p.add_argument("words"); p.add_argument("review_csv"); p.add_argument("--yes", action="store_true")
    p.add_argument("--source", choices=["human", "auto-extraction"], default="human",
                   help="who decided the fixes: human listening (can be accepted) or automatic audio extraction (draft only)")
    p = sub.add_parser("second-opinion", help="2nd ASR (e.g. Nemotron chunks.json) -> hint columns in review.csv (changes no words)")
    p.add_argument("words"); p.add_argument("chunks"); p.add_argument("--review-csv")
    p = sub.add_parser("consensus", help="3-model consensus hints (ours + timed ASR json + untimed text) -> consensus.csv (changes no words)")
    p.add_argument("words"); p.add_argument("--timed", help="2nd ASR with word timestamps (NeMo-Speech.cpp json)")
    p.add_argument("--text", help="untimed transcript text (e.g. MAI)"); p.add_argument("--review-csv")
    p.add_argument("--names", help="name_suggestions.json (default config/)")
    p.add_argument("--audio", help="source audio -> one mp3 clip per row to listen to")
    p = sub.add_parser("hinglish", help="Devanagari words.json -> Hinglish (Roman) words/SRT/review sheet, same timings (master untouched)")
    p.add_argument("words"); p.add_argument("--out", required=True, help="output prefix")
    p.add_argument("--yapper-dir", help="clone of github.com/ABHISHEKgauti25/yapper_transliterator (romanizer)")
    p.add_argument("--table", default=str(ROOT / "config" / "hinglish_names.json"))
    p.add_argument("--review-csv", help="master review.csv: undecided rows flagged for listening")
    p.add_argument("--apply-review-fixes", action="store_true", help="apply decided review.csv fixes in memory first (draft)")
    p.add_argument("--other-asr", help="untimed Hinglish ASR chunks.json to compare against (hints only)")
    p = sub.add_parser("hinglish-layer", help="Hinglish Transcript Layer v0: Hindi words.json -> new run with words_hinglish_v1.json, both SRTs, review CSV/HTML (+clips)")
    p.add_argument("words"); p.add_argument("--media", help="audio for per-block review clips")
    p.add_argument("--yapper-dir", required=True); p.add_argument("--table", default=str(ROOT / "config" / "hinglish_names.json"))
    p.add_argument("--master-review-csv"); p.add_argument("--block-s", type=float, default=12.0)
    p.add_argument("--no-clips", action="store_true"); p.add_argument("--version", default="v1")
    p.add_argument("--other-asr", help="untimed Hinglish ASR chunks.json -> per-block hints (never applied)")
    p = sub.add_parser("review-hinglish", help="Hinglish Review Assistant v0: layer -> review blocks CSV/HTML with audio clips (changes no words)")
    p.add_argument("media"); p.add_argument("layer"); p.add_argument("--table", default=str(ROOT / "config" / "hinglish_names.json"))
    p.add_argument("--block-s", type=float, default=12.0); p.add_argument("--other-asr")
    p = sub.add_parser("apply-hinglish-review", help="your filled review_hinglish CSV -> words_hinglish_*_accepted.json + SRT (only if every block decided)")
    p.add_argument("layer"); p.add_argument("review_csv"); p.add_argument("--partial", action="store_true", help="undecided blocks allowed -> draft_reviewed, NOT accepted")
    p.add_argument("--out", help="output layer path (default <layer>_accepted.json)")
    p.add_argument("--bulk-ok-by-user", metavar="STATEMENT", help="user explicitly approved ALL undecided blocks: writes a filled copy *_user_bulk_ok.csv (decided_by=user_bulk) and applies it")
    p = sub.add_parser("fetch-plan", help="scenes.json -> editable scene,query CSV for kang.py fetch (from asset_aliases tags)")
    p.add_argument("scenes"); p.add_argument("--out", required=True); p.add_argument("--place", default="", help="e.g. Dwarka (prefixed to every query)")
    p = sub.add_parser("fetch", help="Wikimedia Commons stills + licence -> assets folder + CREDITS.json/.txt (free licences only; nothing approved)")
    p.add_argument("--out", required=True, help="assets folder to fill"); p.add_argument("--queries", nargs="*", default=[])
    p.add_argument("--queries-csv", help="CSV scene,query[,count] (from fetch-plan, edited)")
    p.add_argument("--per-query", type=int, default=3); p.add_argument("--no-sharealike", action="store_true")
    p.add_argument("--min-width", type=int, default=1280); p.add_argument("--dry-run", action="store_true")
    p = sub.add_parser("fetch-pool", help="Commons category pool (e.g. deepcat:\"Dwarka\") ranked per scene -> assets + CREDITS + pool_ranking.csv")
    p.add_argument("scenes"); p.add_argument("--pool", required=True, help='Commons search expr, e.g. deepcat:"Dwarka"')
    p.add_argument("--out", required=True); p.add_argument("--per-scene", type=int, default=2)
    p.add_argument("--max-pool", type=int, default=800); p.add_argument("--min-score", type=float, default=1.0)
    p.add_argument("--no-sharealike", action="store_true"); p.add_argument("--min-width", type=int, default=1280)
    p.add_argument("--dry-run", action="store_true"); p.add_argument("--pool-cache", help="reuse a saved pool.json")
    p = sub.add_parser("package-captions", help="copy a Premiere package into a new run with new captions.srt (old kept as captions_<tag>.srt)")
    p.add_argument("package"); p.add_argument("srt"); p.add_argument("--old-tag", default="hindi")
    p.add_argument("--extra", nargs="*", default=[], help="files to add to the package (layer json, acceptance json)")
    p.add_argument("--note", default="")
    p = sub.add_parser("reels", help="KANG Caption Adapter v0: Hinglish layer -> karaoke ASS (karaoke-subs, MIT) + 9:16 preview + qa_report")
    p.add_argument("audio"); p.add_argument("layer"); p.add_argument("--style", default="karaoke_yellow")
    p.add_argument("--format", default="9:16", choices=["9:16", "1:1", "16:9"]); p.add_argument("--start", type=float, default=0.0)
    p.add_argument("--dur", type=float, default=30.0); p.add_argument("--visuals", help="approved visuals.json for the background")
    p.add_argument("--allow-draft", action="store_true", help="render a non-accepted layer, outputs labelled DRAFT_")
    p.add_argument("--no-render", action="store_true", help="ASS + QA only")
    p = sub.add_parser("beats", help="Beat layer: words + scenes -> beats (2.5-7 s, never across a scene) PREFIX.json/.csv")
    p.add_argument("words"); p.add_argument("scenes"); p.add_argument("--out", required=True, help="output prefix")
    p.add_argument("--min", type=float, default=2.5); p.add_argument("--target", type=float, default=4.5)
    p.add_argument("--max", type=float, default=7.0); p.add_argument("--anchor", choices=["lead", "lag"], default="lag")
    p.add_argument("--fps", type=int, default=25)
    p.add_argument("--visuals", help="current visuals CSV: its shot starts become forced beat cuts (cards keep their beats)")
    p = sub.add_parser("beats-assign", help="beats + visual plan CSV + Commons pool(s) -> visuals_beats.csv (no repeats, labels kept)")
    p.add_argument("beats"); p.add_argument("visuals_csv"); p.add_argument("--pool", nargs="+", default=[])
    p.add_argument("--assets", required=True, help="assets folder of the visual plan (with CREDITS.json)")
    p.add_argument("--scenes", required=True); p.add_argument("--download-to", help="new folder for pool stills not downloaded yet")
    p.add_argument("--top-n", type=int, default=40); p.add_argument("--out", required=True)
    p.add_argument("--no-new-downloads", action="store_true", help="use only pool stills already in --download-to (eye-checked)")
    p.add_argument("--parallax", help="parallax_report.csv (parallax-batch): gate-passed clips replace the Ken Burns of the same photo")
    p.add_argument("--allow-crop-reuse", action="store_true",
                   help="v14: a still may come back as a distinctly different crop (beat_rules.json crop_reuse)")
    p.add_argument("--hinglish-words", help="Hinglish words json (narration place names for crop reuse)")
    p = sub.add_parser("beats-crop-reuse", help="v14: crop-reuse pass on an existing visuals_beats CSV (keeps parallax/stock/cards/maps)")
    p.add_argument("visuals_beats"); p.add_argument("--beats", required=True); p.add_argument("--out", required=True)
    p.add_argument("--hinglish-words"); p.add_argument("--grid", help="first framing vs crop grid JPEG")
    p = sub.add_parser("beats-package", help="beats + visuals_beats.csv -> Premiere package (beat markers, Ken Burns) [+ zip]")
    p.add_argument("media"); p.add_argument("words"); p.add_argument("scenes"); p.add_argument("beats"); p.add_argument("visuals_beats")
    p.add_argument("--captions", required=True); p.add_argument("--win-root"); p.add_argument("--fps", type=int, default=25)
    p.add_argument("--extra", nargs="*", default=[]); p.add_argument("--zip")
    p.add_argument("--selected-by", default="agent_under_user_delegation")
    p = sub.add_parser("beats-preview", help="smooth Ken Burns preview of a range with burned captions (resumable, --run)")
    p.add_argument("media"); p.add_argument("visuals_beats"); p.add_argument("--captions", required=True)
    p.add_argument("--range", required=True, help="START-END seconds, e.g. 210-340"); p.add_argument("--out", required=True)
    p.add_argument("--run"); p.add_argument("--width", type=int, default=1280); p.add_argument("--crf", type=int, default=26)
    p.add_argument("--budget", type=float, default=80.0)
    p = sub.add_parser("beats-grid", help="frame grid at beat midpoints of a preview (+ black-frame / jitter check)")
    p.add_argument("preview"); p.add_argument("visuals_beats"); p.add_argument("--start", type=float, required=True)
    p.add_argument("--scenes", required=True); p.add_argument("--out", required=True); p.add_argument("--jitter-at", type=float)
    p = sub.add_parser("parallax", help="2.5D parallax: one still -> depth (DA-V2 Small, cached) -> MP4 + quality gate")
    p.add_argument("image"); p.add_argument("--out", required=True); p.add_argument("--dur", type=float, required=True)
    p.add_argument("--move", choices=["dolly", "pan", "zoom"], default="dolly"); p.add_argument("--strength", type=float, default=1.0)
    p.add_argument("--width", type=int, default=1920); p.add_argument("--fps", type=int, default=25)
    p = sub.add_parser("parallax-batch", help="parallax clips for long holds / continued_with_motion clips of a visuals_beats.csv (resumable, --run)")
    p.add_argument("visuals_beats"); p.add_argument("--run"); p.add_argument("--beats", help="only these first-beat ids, comma separated")
    p.add_argument("--min-hold", type=float, default=6.0); p.add_argument("--width", type=int, default=1920)
    p.add_argument("--strength", type=float, default=1.0); p.add_argument("--budget", type=float, default=90.0)
    p = sub.add_parser("parallax-apply", help="visuals_beats.csv + parallax_report.csv -> visuals_beats CSV using gate-passed parallax clips")
    p.add_argument("visuals_beats"); p.add_argument("report"); p.add_argument("--out", required=True)
    p = sub.add_parser("ai-motion-plan", help="v17: AI motion candidates (real stills with sea/sky/flag/water, no faces) -> Kaggle jobs + inputs")
    p.add_argument("visuals_beats"); p.add_argument("--beats", help="only these first-beat ids, comma separated (test set)")
    p.add_argument("--max-clips", type=int); p.add_argument("--run")
    p = sub.add_parser("ai-motion-apply", help="v17: Kaggle raw I2V clips -> gate + masked composite + eye_pass -> visuals_beats CSV")
    p.add_argument("visuals_beats"); p.add_argument("--jobs", required=True, help="jobs.json from ai-motion-plan")
    p.add_argument("--raw", required=True, help="folder with raw AI_<beat>.mp4 from the Kaggle kernel")
    p.add_argument("--kernel-report"); p.add_argument("--out", required=True); p.add_argument("--run")
    p = sub.add_parser("fetch-openverse", help="Openverse CC images (by/by-sa/cc0/pdm, no key) -> assets + CREDITS (place check, sha256+dHash dedupe)")
    p.add_argument("--out", default="assets/dwarika_openverse_v1"); p.add_argument("--min-width", type=int)
    p.add_argument("--queries", help="JSON list [{scene, query, count}] (default: config/stock_sources.json)")
    p = sub.add_parser("fetch-pixabay", help="Pixabay videos/images (Pixabay Content License, representative only) -> assets + CREDITS")
    p.add_argument("--out", default="assets/dwarika_pixabay_v1"); p.add_argument("--verify-auth", action="store_true")
    p.add_argument("--thumbs-only", action="store_true", help="list candidates + thumbnails for the eye check, no media download")
    p.add_argument("--kind", nargs="+", default=["video"], choices=["video", "image"]); p.add_argument("--per-query", type=int)
    p = sub.add_parser("asset-index-all", help="ONE asset index over several asset folders (Commons + Openverse + Pixabay)")
    p.add_argument("dirs", nargs="+"); p.add_argument("--out", default="assets/asset_index.json")
    p = sub.add_parser("beats-stock", help="visuals_beats CSV + Openverse/Pixabay folders -> new CSV (stock only on continued_with_motion / long holds)")
    p.add_argument("visuals_beats"); p.add_argument("--stock", nargs="+", required=True); p.add_argument("--out", required=True)
    p.add_argument("--run", help="continue a partial beats-stock run (resumable trimming)")
    p = sub.add_parser("stock-grid", help="grid of every newly used Openverse/Pixabay asset (label + source)")
    p.add_argument("visuals_beats"); p.add_argument("--out", required=True)
    p = sub.add_parser("motion-build", help="v13: moving text cards + map routes (config/motion_cards.json) into a visuals_beats CSV (resumable)")
    p.add_argument("visuals_beats"); p.add_argument("--out", default="visuals_beats_v13.csv")
    p.add_argument("--spec"); p.add_argument("--run", help="continue a partial motion-build run"); p.add_argument("--budget", type=float, default=95.0)
    p = sub.add_parser("motion-fix", help="v13b: re-plan cards/maps, re-render only changed clips of a motion-build run into a new run (resumable)")
    p.add_argument("base_run"); p.add_argument("--out", default="visuals_beats_v13b.csv"); p.add_argument("--force", nargs="*", default=[])
    p.add_argument("--run"); p.add_argument("--budget", type=float, default=60.0)
    p.add_argument("--base-csv", help="v17b: visuals CSV to patch (default <base_run>/visuals_beats_v13.csv)")
    p.add_argument("--base-values", help="v17b: card_values.csv to diff against (default <base_run>/card_values.csv)")
    p = sub.add_parser("motion-grid", help="v13: grid of every card/map phase from a motion-build run")
    p.add_argument("build_run"); p.add_argument("--out", required=True)
    p = sub.add_parser("motion-preview", help="v13: only the card/map beats back to back, captions burned (resumable)")
    p.add_argument("build_run"); p.add_argument("media"); p.add_argument("captions"); p.add_argument("--out", required=True)
    p.add_argument("--run"); p.add_argument("--width", type=int, default=1280)
    p = sub.add_parser("fetch-youtube-cc", help="v15: YouTube CC BY clips of Dwarka (yt-dlp; licence field + place check, sections, shot checks)")
    p.add_argument("--out", required=True, help="pool folder for accepted shots (YT_*.mp4 + CREDITS.json)")
    p.add_argument("--config", help="default config/youtube_cc.json")
    p.add_argument("--search-only", action="store_true", help="search + title place check only (no watch-page probe)")
    p.add_argument("--max-probe", type=int, default=40); p.add_argument("--run")
    p = sub.add_parser("beats-youtube-cc", help="v15: visuals_beats CSV + YouTube CC pool -> new CSV (replaces representative Pixabay / continued_with_motion only)")
    p.add_argument("visuals_beats"); p.add_argument("--beats", required=True); p.add_argument("--pool", nargs="+", required=True)
    p.add_argument("--out", required=True); p.add_argument("--hinglish-words")
    p.add_argument("--v16-rules", action="store_true", help="v16 rule A/C from config/youtube_cc.json v16_rules: EXACT clip may replace the Sudarshan Setu archival hold and representative shots whose narration names the clip's place; `force` beats (outro stock) take any eye-passed clip")
    p = sub.add_parser("creative-check", help="Creative Office critic: visuals_beats CSV + Hinglish layer -> rules-engine report (vendor creative_layer_v2, audio rules deferred)")
    p.add_argument("visuals_beats"); p.add_argument("layer"); p.add_argument("--profile", default="travel_vlog_hi")
    p.add_argument("--run"); p.add_argument("--with-audio", action="store_true", help="also evaluate audio rules (deferred by default)")
    p.add_argument("--captions", help="captions SRT for caption-speed checks (default: captions_hinglish_v1_accepted.srt next to layer)")
    p = sub.add_parser("plan-pictures", help="v18 picture desk: visuals_beats CSV -> rule-based shot plan (G-004/G-008/Q-006/G-006) + new visuals CSV")
    p.add_argument("visuals_beats"); p.add_argument("--out", required=True); p.add_argument("--words", help="words.json for lead-rule cut points (default runs/2026-10-31_KANG_004/words.json)")
    p.add_argument("--run")
    p = sub.add_parser("cold-open", help="v18: visual-only teaser over the opening narration (clips + title overlay) -> new visuals CSV")
    p.add_argument("visuals_beats"); p.add_argument("--out", required=True); p.add_argument("--spec", help="default config/cold_open.json")
    p.add_argument("--run")
    p = sub.add_parser("palette", help="F19-lite screenshot -> brand_draft.json")
    p.add_argument("image"); p.add_argument("-k", type=int, default=5)

    args = ap.parse_args(argv)
    import os
    if getattr(args, "voters", None):  # read by pipeline.transcribe_to_words (also inside workflow)
        os.environ["ENGINE_VOTERS"] = args.voters
    if getattr(args, "no_vote", False):
        os.environ["ENGINE_VOTE"] = "0"
    if getattr(args, "wordlist", None):
        os.environ["ENGINE_WORDLIST"] = args.wordlist
    from core import pipeline

    if args.cmd == "check":
        import build_and_check
        return build_and_check.main([])
    if args.cmd == "presets":
        from core.subtitles import list_presets, load_preset
        for n in list_presets(ROOT / "presets"):
            print(f"{n:18s} {load_preset(n, ROOT / 'presets').description}")
        return 0
    if args.cmd == "transcribe":
        r = pipeline.transcribe_to_words(args.audio, language=args.lang, model_size=args.model,
                                         initial_prompt=args.prompt, device=args.device,
                                         spelling_policy=args.spelling_policy)
        _print({k: r[k] for k in ("run_id", "dir", "words")} | {"audit_issues": r["audit"]["issue_count"]})
        return 0
    if args.cmd == "fix-words":
        _print(pipeline.fix_words(args.words, glossary_path=args.glossary, spelling_policy=args.spelling_policy))
        return 0
    if args.cmd == "workflow":
        r = pipeline.workflow_clip(args.source, args.start, args.dur, formats=args.to, preset_name=args.preset,
                                   approver=_approver(args), language=args.lang, device=args.device,
                                   model_size=args.model, initial_prompt=args.prompt, full=args.full,
                                   spelling_policy=args.spelling_policy)
        _print(r)
        return 0 if r["pass"] else 1
    if args.cmd == "subs":
        r = pipeline.subtitle_video(args.media, args.words, fmt=args.fmt, preset_name=args.preset,
                                    preview_start=args.preview_start, approver=_approver(args), option=args.option)
    elif args.cmd == "promo":
        r = pipeline.promo_clip(args.media, args.words, args.start, args.dur, fmt=args.fmt,
                                preset_name=args.preset, approver=_approver(args))
    elif args.cmd == "cut":
        r = pipeline.plan_and_cut(args.media, args.words, approver=_approver(args),
                                  noise_db=args.noise_db, min_silence=args.min_silence)
    elif args.cmd == "audio":
        r = pipeline.clean_audio(args.media, target_lufs=args.lufs, true_peak=args.tp, rnnoise_model=args.rnnoise_model)
    elif args.cmd == "formats":
        r = pipeline.multi_format(args.video, args.words, args.to, preset_name=args.preset, reframe_x=args.reframe_x)
    elif args.cmd == "package":
        r = pipeline.premiere_package(args.media, args.words, approver=_approver(args), scenes_path=args.scenes,
                                      cuts_path=args.cuts, fps=args.fps, win_root=args.win_root,
                                      english_script=args.english_script)
    elif args.cmd == "visuals-template":
        r = pipeline.visuals_template(args.scenes, args.out)
        _print(r)
        return 0 if r["ok"] else 1
    elif args.cmd == "ingest":
        from core import asset_index
        r = asset_index.ingest(args.assets, args.briefs, args.out)
        if r["ok"] and args.sheet:
            r["sheet"] = asset_index.contact_sheet(r["index"], args.sheet)
        _print(r)
        return 0 if r["ok"] else 1
    elif args.cmd == "asset-search":
        from core import asset_index
        idx = json.loads(Path(args.index).read_text(encoding="utf-8"))
        _print({"query": args.query, "results": asset_index.search(idx, args.query, args.top, args.no_sharealike)})
        return 0
    elif args.cmd == "match-check":
        from core import broll_match as bm
        sg = json.loads(Path(args.suggestions).read_text(encoding="utf-8"))
        exp = [x["id"] for x in json.loads(Path(args.scenes).read_text(encoding="utf-8"))["scenes"]] if args.scenes else None
        r = bm.qa(sg, exp, sg.get("top", 3))
        if args.sheet and args.scenes and args.assets:
            r["sheet"] = bm.review_sheet(sg, args.assets, json.loads(Path(args.scenes).read_text(encoding="utf-8")),
                                         args.sheet, args.only.split(",") if args.only else None)
        _print(r)
        return 0 if r["structure"] == "PASS" else 1
    elif args.cmd == "approve-broll":
        from core import broll_match as bm
        import datetime as _dt, hashlib as _hl
        sg_bytes = Path(args.suggestions).read_bytes()
        sg = json.loads(sg_bytes.decode("utf-8"))
        idx = json.loads(Path(args.index).read_text(encoding="utf-8"))
        sc = json.loads(Path(args.scenes).read_text(encoding="utf-8"))
        try:
            picks = bm.choices_from_spec(sg, args.choices) if args.choices is not None else bm.interactive_choices(sg)
        except ValueError as e:
            _print({"ok": False, "problems": [str(e)]})
            return 1
        r = bm.approve(None, idx, args.out, sc, args.allow_missing, picks=picks)
        if r["ok"]:
            ap = Path(args.approved or Path(args.out).with_name("approved_broll.json"))
            letters = {s_["scene_id"]: {c["path"]: bm.LETTERS[k] for k, c in enumerate(s_["candidates"])} for s_ in sg["scenes"]}
            ap.write_text(json.dumps({"schema": "kang.approved_broll/1.0", "approved_by": "user",
                "approved_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
                "suggestions_sha256": _hl.sha256(sg_bytes).hexdigest(), "visuals_csv": str(args.out),
                "scenes": [{"scene": k, "options": [letters.get(k, {}).get(a, "?") for a in v], "assets": v}
                           for k, v in picks.items()],
                "skipped": [s_["scene_id"] for s_ in sg["scenes"] if s_["scene_id"] not in picks]},
                ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            r["approved_broll"] = str(ap)
        _print(r)
        return 0 if r["ok"] else 1
    elif args.cmd in ("match", "match-approve"):
        from core import broll_match as bm
        idx = json.loads(Path(args.index).read_text(encoding="utf-8"))
        sc = json.loads(Path(args.scenes).read_text(encoding="utf-8"))
        if args.cmd == "match-approve":
            r = bm.approve(args.suggestions_csv, idx, args.out, sc, args.allow_missing)
            _print(r)
            return 0 if r["ok"] else 1
        words = json.loads(Path(args.words).read_text(encoding="utf-8")) if args.words else None
        sg = bm.match(sc, idx, words, args.top, exclude_sharealike=args.no_sharealike)
        Path(args.out + ".json").write_text(json.dumps(sg, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        bm.write_csv(sg, args.out + ".csv")
        r = {"ok": True, "json": args.out + ".json", "csv": args.out + ".csv", "scenes": len(sg["scenes"]),
             "needs_manual": [s["scene_id"] for s in sg["scenes"] if s["needs_manual"]],
             "qa": bm.qa(sg, [x["id"] for x in sc["scenes"]], args.top)}
        if args.eval_csv:
            import csv as _csv
            used = {}
            with open(args.eval_csv, encoding="utf-8-sig", newline="") as f:
                for row in _csv.DictReader(f):
                    if row.get("asset"):
                        used.setdefault(row["scene"], set()).add(Path(row["asset"]).name)
            ev = bm.hit_at_k(sg, used)
            r["eval"] = {k: v for k, v in ev.items() if k != "rows"} | {"misses": [x["scene"] for x in ev["rows"] if not x["hit"]]}
        _print(r)
        return 0
    elif args.cmd == "visuals":
        r = pipeline.visual_preview(args.media, args.words, args.scenes, args.visuals_csv, args.assets,
                                    scene_ids=args.preview.split(",") if args.preview else None,
                                    approver=_approver(args), fps=args.fps, win_root=args.win_root,
                                    selected_by=args.selected_by)
        _print(r)
        if r.get("error"):
            return 1
        return 2 if r.get("visual_selection") else 0
    elif args.cmd == "review":
        r = pipeline.review_transcript(args.media, args.words, manual=args.phrase, clips=not args.no_clips)
        _print(r)
        return 0
    elif args.cmd == "apply-review":
        r = pipeline.apply_transcript_review(args.words, args.review_csv, approver=_approver(args), source=args.source)
        _print(r)
        if not r["ok"]:
            return 1
        return 0 if r["transcript_accepted"] else 2
    elif args.cmd == "second-opinion":
        r = pipeline.second_opinion(args.words, args.chunks, review_csv=args.review_csv)
    elif args.cmd == "consensus":
        r = pipeline.consensus_review(args.words, args.timed, args.text, review_csv=args.review_csv, names_path=args.names, media=args.audio)
    elif args.cmd == "hinglish":
        from core.hinglish import run_hinglish
        r = run_hinglish(args.words, args.out, yapper_dir=args.yapper_dir, table_path=args.table,
                         review_csv=args.review_csv, apply_review_fixes=args.apply_review_fixes, other_asr=args.other_asr)
    elif args.cmd == "hinglish-layer":
        from core.hinglish_review import hinglish_layer_run
        r = hinglish_layer_run(args.words, media=args.media, yapper_dir=args.yapper_dir, table_path=args.table,
                               master_review_csv=args.master_review_csv, block_s=args.block_s,
                               clips=not args.no_clips, version=args.version, other_asr=args.other_asr)
    elif args.cmd == "review-hinglish":
        from core.hinglish_review import review_pack
        r = review_pack(args.layer, media=args.media, table_path=args.table, block_s=args.block_s, other_asr=args.other_asr)
        r.pop("rows", None)
    elif args.cmd == "apply-hinglish-review":
        from core.hinglish_review import apply_hinglish_review, bulk_ok_csv
        csv_in = args.review_csv
        if args.bulk_ok_by_user:
            csv_in = str(bulk_ok_csv(args.review_csv, args.bulk_ok_by_user))
        r = apply_hinglish_review(args.layer, csv_in, allow_partial=args.partial, out=args.out)
        if not r.get("ok"):
            r["error"] = "not applied"
    elif args.cmd == "fetch-plan":
        from core.commons_fetch import plan_queries
        r = plan_queries(args.scenes, args.out, place=args.place)
    elif args.cmd == "fetch":
        from core.commons_fetch import fetch, read_queries
        qs = read_queries(args.queries_csv) if args.queries_csv else []
        qs += [{"scene": "", "query": q} for q in args.queries]
        r = fetch(qs, args.out, per_query=args.per_query, no_sharealike=args.no_sharealike,
                  min_width=args.min_width, dry_run=args.dry_run) if qs else {"error": "give --queries or --queries-csv"}
    elif args.cmd == "fetch-pool":
        from core.commons_fetch import fetch_pool
        r = fetch_pool(args.scenes, args.out, args.pool, per_scene=args.per_scene, max_pool=args.max_pool,
                       min_score=args.min_score, no_sharealike=args.no_sharealike, min_width=args.min_width,
                       dry_run=args.dry_run, pool_cache=args.pool_cache)
    elif args.cmd == "package-captions":
        from core.package_captions import repackage_captions
        r = repackage_captions(args.package, args.srt, old_tag=args.old_tag, extras=args.extra, caption_note=args.note)
    elif args.cmd == "reels":
        from core.captions_adapter import make_reel
        try:
            r = make_reel(args.audio, args.layer, style=args.style, fmt=args.format, start=args.start, dur=args.dur,
                          visuals=args.visuals, allow_draft=args.allow_draft, render=not args.no_render)
        except (PermissionError, ValueError, RuntimeError) as exc:
            r = {"error": str(exc)}
    elif args.cmd in ("beats", "beats-assign", "beats-package", "beats-preview", "beats-grid", "beats-crop-reuse"):
        from core import beats_package as bpk
        if args.cmd == "beats":
            r = bpk.beats_cmd(args.words, args.scenes, args.out, min_s=args.min, target_s=args.target, max_s=args.max,
                              anchor=args.anchor, fps=args.fps, visuals_csv=args.visuals)
        elif args.cmd == "beats-assign":
            r = bpk.assign_cmd(args.beats, args.visuals_csv, args.pool, args.out, assets=args.assets,
                               download_to=args.download_to, top_n=args.top_n, scenes_path=args.scenes,
                               no_new_downloads=args.no_new_downloads, parallax_report=args.parallax,
                               allow_crop_reuse=args.allow_crop_reuse, hinglish_words=args.hinglish_words)
        elif args.cmd == "beats-crop-reuse":
            r = bpk.crop_reuse_cmd(args.visuals_beats, args.beats, args.out, hinglish_words=args.hinglish_words, grid=args.grid)
        elif args.cmd == "beats-package":
            r = bpk.package_cmd(args.media, args.words, args.scenes, args.beats, args.visuals_beats, captions=args.captions,
                                win_root=args.win_root, fps=args.fps, extras=args.extra, zip_out=args.zip,
                                selected_by=args.selected_by)
        elif args.cmd == "beats-preview":
            a, b = (float(x) for x in args.range.split("-"))
            h = int(round(args.width * 9 / 16 / 2)) * 2
            r = bpk.preview_cmd(args.media, args.visuals_beats, args.captions, a, b, args.out, run_id=args.run,
                                w=args.width, h=h, crf=args.crf, budget_s=args.budget)
        else:
            r = bpk.grid_cmd(args.preview, args.visuals_beats, args.start, args.scenes.split(","), args.out,
                             jitter_at=args.jitter_at)
    elif args.cmd in ("parallax", "parallax-batch", "parallax-apply"):
        from core import parallax_package as ppk
        if args.cmd == "parallax":
            r = ppk.parallax_cmd(args.image, args.out, args.dur, move=args.move, strength=args.strength, width=args.width,
                                 fps=args.fps)
        elif args.cmd == "parallax-batch":
            r = ppk.batch_cmd(args.visuals_beats, run_id=args.run, beats=args.beats.split(",") if args.beats else None,
                              min_hold=args.min_hold, width=args.width, strength=args.strength, budget_s=args.budget)
        else:
            r = ppk.apply_cmd(args.visuals_beats, args.report, args.out)
    elif args.cmd in ("ai-motion-plan", "ai-motion-apply"):
        from core import ai_motion as am
        if args.cmd == "ai-motion-plan":
            r = am.plan_cmd(args.visuals_beats, beats=args.beats.split(",") if args.beats else None,
                            max_clips=args.max_clips, run_id=args.run)
        else:
            r = am.apply_cmd(args.visuals_beats, args.jobs, args.raw, args.out, run_id=args.run,
                             kernel_report=args.kernel_report)
    elif args.cmd in ("fetch-openverse", "fetch-pixabay", "asset-index-all", "beats-stock", "stock-grid"):
        from core import stock_assign as sa
        if args.cmd == "fetch-openverse":
            r = sa.fetch_openverse_cmd(args.out, min_width=args.min_width, queries_json=args.queries)
        elif args.cmd == "fetch-pixabay":
            r = sa.fetch_pixabay_cmd(args.out, verify_only=args.verify_auth, thumbs_only=args.thumbs_only,
                                     kinds=args.kind, per_query=args.per_query)
        elif args.cmd == "asset-index-all":
            r = sa.index_cmd(args.dirs, args.out)
        elif args.cmd == "beats-stock":
            r = sa.stock_cmd(args.visuals_beats, args.stock, args.out, run_id=args.run)
        else:
            r = sa.new_sources_grid(args.visuals_beats, args.out)
    elif args.cmd == "motion-fix":
        from core import motion_assign as ma
        r = ma.fix_build_cmd(args.base_run, args.out, force=args.force, run_id=args.run, budget_s=args.budget,
                             base_csv=args.base_csv, base_values=args.base_values)
    elif args.cmd in ("motion-build", "motion-grid", "motion-preview"):
        from core import motion_assign as ma
        if args.cmd == "motion-build":
            r = ma.build_cmd(args.visuals_beats, args.out, spec_path=args.spec, run_id=args.run, budget_s=args.budget)
        elif args.cmd == "motion-grid":
            r = ma.grid_cmd(args.build_run, args.out)
        else:
            r = ma.preview_cmd(args.build_run, args.media, args.captions, args.out, run_id=args.run, w=args.width)
    elif args.cmd in ("fetch-youtube-cc", "beats-youtube-cc"):
        from core import youtube_cc as yc
        if args.cmd == "fetch-youtube-cc":
            r = yc.fetch_cmd(args.out, cfg_path=args.config, search_only=args.search_only, max_probe=args.max_probe,
                             run_id=args.run)
        else:
            r = yc.assign_cmd(args.visuals_beats, args.beats, args.pool, args.out, hinglish_words=args.hinglish_words,
                               v16_rules=args.v16_rules)
    elif args.cmd == "creative-check":
        from core import creative as cr
        r = cr.check_cmd(args.visuals_beats, args.layer, profile=args.profile, run_id=args.run,
                         defer_audio=not args.with_audio, captions=args.captions)
    elif args.cmd == "plan-pictures":
        from core import picture_desk as pdk
        r = pdk.plan_cmd(args.visuals_beats, args.out, words=args.words, run_id=args.run)
    elif args.cmd == "cold-open":
        from core import cold_open as co
        r = co.cold_open_cmd(args.visuals_beats, args.out, spec=args.spec, run_id=args.run)
    elif args.cmd == "palette":
        r = pipeline.palette_from_screenshot(args.image, k=args.k)
    _print(r)
    return exit_code(args.cmd, r)


def exit_code(cmd: str, r: dict) -> int:
    """0 = done and QA passed, 1 = failed/QA failed, 2 = stopped at an approval gate (not a success)."""
    if r.get("error"):
        return 1
    for key in ("qa", "report"):  # subs/promo/formats use "qa"; audio uses "report"
        if isinstance(r.get(key), dict) and not r[key].get("pass", False):
            return 1
    if cmd == "cut":
        if r.get("truncated_words"):
            return 1
        if not r.get("output"):
            return 2
        return 0 if r.get("duration_check", {}).get("pass", False) else 1
    if cmd in ("subs", "promo") and not r.get("final"):
        return 2
    if cmd == "package" and not r.get("package"):
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
