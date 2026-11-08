"""Planner + workflow orchestration (Layers 3-7).

Every function creates/uses a Run (unique folder + manifest), never touches originals,
and stops at approval gates unless approve=True is passed explicitly.
"""
from __future__ import annotations

import json
import os
import shutil
import time
from pathlib import Path, PureWindowsPath
from typing import Any, Callable, Dict, List, Optional

from . import audio as audio_mod
from . import cutter, qa, render
from .brand import CANVAS, load_brand, resolve_fonts
from .edl import EDL, Approvals, Audio, Cut, Export, Input, Subtitles, save_edl
from .runs import Run, media_summary, write_json
from .subtitles import build_ass, build_srt, load_preset, make_layout
from .gapfill import BLOCKING_GAP_S, COVERAGE_GAP_S, fill_gaps, find_speech_gaps, repair_suspect_spans
from .words import join_split_tokens, repeated_runs, sanitize_script, apply_glossary, audit_words, load_glossary, load_words, review_sample, rows_to_words

ROOT = Path(__file__).resolve().parent.parent
Approver = Callable[[str, str], bool]


def _deny(gate: str, info: str) -> bool:
    return False


_deny.approver_name = "default-deny"


def cli_approver(gate: str, info: str) -> bool:
    print(f"\n=== APPROVAL GATE: {gate} ===\n{info}")
    try:
        return input("Approve? [y/N]: ").strip().lower() in {"y", "yes", "haan", "ha"}
    except EOFError:
        return False


cli_approver.approver_name = "cli-user"


def plan_hash(info: str, artifacts=(), settings: Optional[Dict[str, Any]] = None) -> str:
    """sha256 over the text shown + the CONTENT of every artifact file + the settings dict, so a changed
    preview/words/ASS/settings behind the same path gives a different hash."""
    import hashlib
    from .runs import sha256_file
    h = hashlib.sha256(info.encode("utf-8"))
    for a in artifacts:
        h.update(f"\n{Path(a).name}:{sha256_file(a)}".encode("utf-8"))
    if settings is not None:
        h.update(json.dumps(settings, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8"))
    return h.hexdigest()


AUTO_APPROVERS = {"auto(--yes)", "default-deny"}


def _gate(run: Run, gate: str, info: str, approver: Approver, artifacts=(), settings=None) -> bool:
    """Every decision is recorded in approvals.json bound to plan_hash(info, artifacts, settings) = the exact
    plan/preview shown, with the approver's identity (cli-user, auto(--yes), ...). A 'no' from a real
    approver is 'rejected'; the non-interactive default-deny leaves the gate 'pending'. auto(--yes) is
    recorded as automation, never as a human review (manifest human_approved=False)."""
    ok = approver(gate, info)
    h = plan_hash(info, artifacts, settings)
    who = getattr(approver, "approver_name", getattr(approver, "__name__", "callable"))
    value = "approved" if ok else ("pending" if who == "default-deny" else "rejected")
    run.set_approval(gate, value, plan_hash=h, approver=who)
    run.manifest.setdefault("human_approved", {})[gate] = bool(ok) and who not in AUTO_APPROVERS
    run.save()
    run.log_step(f"gate:{gate}", approved=ok, plan_hash=h[:12], approver=who)
    return ok


# --------------------------------------------------------------------------- Phase 1
def transcribe_to_words(audio_path: str, run: Optional[Run] = None, language: str = "hi",
                        model_size: str = "large-v3-turbo", initial_prompt: Optional[str] = None,
                        device: Optional[str] = None, transcriber: Optional[Callable] = None,
                        voters: Optional[Dict[str, Any]] = None, wordlist: Optional[str] = None,
                        vote_agree: bool = True, spelling_policy: Optional[str] = None) -> Dict[str, Any]:
    """Fresh run, cut=False: transcript JSON + SRT + words.json + anomaly audit + review sample.
    `transcriber(audio_samples) -> rows` can be injected for offline tests.
    `voters` {name: ct2 model dir | callable(samples)->rows} turns on the spelling voter (core/voter.py):
    second models only correct the spelling of words already there, never add/drop words or timing.
    Default off; also ENGINE_VOTERS="name=dir,..." + ENGINE_WORDLIST=<hunspell .dic>."""
    from . import engine
    run = run or Run()
    run.add_input(audio_path, "A1")
    samples = engine.load_audio(audio_path)
    if transcriber is not None:
        rows, stats = transcriber(samples), {"mocked": True}
        retry = transcriber
        fallbacks = []
    else:
        model = engine.get_model(model_size, device=device)
        rows, _ = engine.transcribe(samples, language=language, initial_prompt=initial_prompt, model=model)
        rows, stats = engine.refine_transcript(rows, samples, language=language, initial_prompt=initial_prompt, model=model)
        retry = lambda clip: engine.transcribe(clip, language=language, initial_prompt=initial_prompt, model=model,
                                               extra_opts=engine.REPAIR_ASR_OPTIONS)[0]
        # Dwarika 571 s: with the domain prompt the retry still merged a stretched token; without
        # it the same window came back word-perfect. Second chance only, never the first pass.
        fallbacks = [lambda clip: engine.transcribe(clip, language=language, initial_prompt="", model=model,
                                                    extra_opts=engine.REPAIR_ASR_OPTIONS)[0]]
    run.path("raw/.keep")  # raw ASR layer (Roadmap §6.1): written once, never edited afterwards
    raw_srt, raw_js = engine.save_outputs(rows, str(run.dir / "raw"))
    raw_words = rows_to_words(rows)
    write_json(run.path("words_raw.json"), raw_words)  # untouched ASR output
    gaps = find_speech_gaps(raw_words, samples)
    filled, gap_report = fill_gaps(raw_words, samples, gaps, retry) if gaps else (raw_words, [])
    filled, repair_report = repair_suspect_spans(filled, samples, retry, fallback_fns=fallbacks)
    leftover = find_speech_gaps(filled, samples)  # >= COVERAGE_GAP_S (2 s, Roadmap v2)
    unfilled = [g for g in leftover if g["end"] - g["start"] >= BLOCKING_GAP_S]
    needs_review = [g for g in leftover if g["end"] - g["start"] < BLOCKING_GAP_S]
    # a word still stretched past BLOCKING_WORD_S hides dropped speech: same verdict as an unfilled gap
    unfilled += [{"start": w["start"], "end": w["end"], "stretched_word": w["word"]}
                 for w in filled if w["end"] - w["start"] > BLOCKING_WORD_S]
    write_json(run.path("speech_gaps.json"), {"coverage_threshold_s": COVERAGE_GAP_S, "blocking_threshold_s": BLOCKING_GAP_S,
                                              "found": gap_report, "suspect_spans": repair_report,
                                              "still_unfilled": unfilled, "needs_review": needs_review})
    words, sanitized = sanitize_script(filled)
    words, joins = join_split_tokens(words)
    write_json(run.path("sanitized.json"), sanitized)
    write_json(run.path("joined_tokens.json"), joins)
    glossary = load_glossary(ROOT / "config" / "glossary.json")
    votes = _spelling_vote(words, samples, voters, wordlist, vote_agree, glossary, device, language, run, audio_path)
    if votes is not None:
        words, vote_changes = votes
        write_json(run.path("vote_changes.json"), vote_changes)
    words, changes = apply_glossary(words, glossary)
    write_json(run.path("glossary_changes.json"), changes)
    words = _apply_spelling_policy(words, spelling_policy, run)
    wpath = write_json(run.path("words.json"), words)
    # final transcript.srt/json come from the SAME final words (after gap-fill, repair, voter, glossary)
    srt, js = engine.save_outputs(words_to_rows(words), str(run.dir))
    audit = audit_words(words)
    audit["speech_gaps_unfilled"] = unfilled
    audit["speech_gaps_needs_review"] = needs_review
    audit["sanitized"] = sanitized
    reps = repeated_runs(words)
    audit["issues"] += reps
    audit["issue_count"] += len(reps)
    write_json(run.path("anomaly_audit.json"), audit)
    run.path("review_sample.txt").write_text(review_sample(words, 40), encoding="utf-8")
    for p, k in ((raw_srt, "srt_raw"), (raw_js, "transcript_raw"), (srt, "srt"), (js, "transcript"), (wpath, "words")):
        run.add_output(Path(p), k)
    run.log_step("transcribe", cut=False, model=model_size, words=len(words), refine=stats, audit_issues=audit["issue_count"],
                 glossary_fixes=len(changes), gaps_found=len(gap_report),
                 gap_words_added=sum(g["filled"] for g in gap_report), gaps_unfilled=len(unfilled),
                 spans_repaired=sum(r["accepted"] for r in repair_report), spans_checked=len(repair_report),
                 spelling_votes=None if votes is None else len(votes[1]))
    run.set_status("transcribed")
    return {"run_id": run.run_id, "dir": str(run.dir), "words": len(words), "audit": audit,
            "glossary_fixes": changes, "vote_changes": None if votes is None else votes[1], "speech_gaps": gap_report, "suspect_spans": repair_report, "gaps_unfilled": unfilled,
            "gaps_needs_review": needs_review}


def words_to_rows(words: List[Dict[str, Any]], gap: float = 1.0) -> List[Dict[str, Any]]:
    """Final words.json -> engine row shape ({start,end,text,words:[{w,start,end,p}]}) so the API's
    transcript.json/.srt keep their old contract. New row at a pause >= gap s or after । ? !"""
    rows: List[Dict[str, Any]] = []
    cur: List[Dict[str, Any]] = []

    def flush():
        if cur:
            rows.append({"start": cur[0]["start"], "end": cur[-1]["end"], "text": " ".join(w["w"] for w in cur),
                         "words": list(cur)})
            cur.clear()
    for w in words:
        if cur and w["start"] - cur[-1]["end"] >= gap:
            flush()
        cur.append({"w": w["word"], "start": w["start"], "end": w["end"], "p": w.get("probability", 1.0)})
        if w["word"].rstrip().endswith(("।", "?", "!")):
            flush()
    flush()
    return rows


def api_transcribe(src: str, out_dir: str, cut: bool = False, language: str = "hi",
                   transcriber: Optional[Callable] = None) -> Dict[str, Any]:
    """app.py /upload job: the SAME transcription stack as kang.py (refine, gap-fill, suspect-span
    repair, sanitize, joins, spelling voter, glossary) in its own run folder; then
    transcript.srt/json are written to out_dir so the public API contract is unchanged."""
    from . import engine
    if not os.path.isfile(src):
        raise FileNotFoundError(f"Input audio file not found: {src}")
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    audio_path = src
    if cut:  # same pre-trim the old engine.run_pipeline did for cut=True
        audio_path = str(out / "cut_input.mp3")
        engine.cut_silence(src, audio_path)
    shutil.copy2(audio_path, out / "audio_used.mp3")
    res = transcribe_to_words(audio_path, language=language, transcriber=transcriber)
    words = load_words(Path(res["dir"]) / "words.json")
    shutil.copy2(Path(res["dir"]) / "transcript.srt", out / "transcript.srt")  # same final revision as words.json
    shutil.copy2(Path(res["dir"]) / "transcript.json", out / "transcript.json")
    srt_path, json_path = str(out / "transcript.srt"), str(out / "transcript.json")
    if res["gaps_unfilled"]:
        raise RuntimeError(f"{len(res['gaps_unfilled'])} speech gap(s) still unfilled; see run {res['run_id']}")
    review = res.get("gaps_needs_review", [])
    return {"run_id": res["run_id"], "run_dir": res["dir"], "srt_path": srt_path, "json_path": json_path,
            # processing finished != transcript accepted: acceptance is a human step (Roadmap S4)
            "processing_complete": True, "review_required": bool(review), "accepted": False,
            "gaps_needs_review": review, "audit_issues": res["audit"]["issue_count"],
            "warnings": [f"{len(review)} voiced gap(s) of 2-3 s need review"] if review else [],
            "words": res["words"], "glossary_fixes": len(res["glossary_fixes"]),
            "spelling_votes": None if res["vote_changes"] is None else len(res["vote_changes"])}


_ALT_CACHE: Dict[tuple, List[Dict[str, Any]]] = {}


VOTE_BATCH = int(os.environ.get("ENGINE_VOTE_BATCH", "8"))  # 0 = sequential (old, ~4x slower on T4)


# batched passes of the Hindi fine-tunes return ~57-59% of the base word count on Dwarika (normal:
# they merge/skip fillers); only a near-empty pass means the batched mode broke for that model.
VOTE_MIN_FRAC = 0.3


def _cuda_count() -> int:
    try:
        import ctranslate2
        return max(1, ctranslate2.get_cuda_device_count())
    except Exception:
        return 1


def _alt_pass(src: str, samples, language: str, dev: str, device_index: int = 0, min_words: int = 0):
    """Full-file pass of one Hindi second model (spelling only: its words never add/drop/move ours).
    Batched inference (faster-whisper BatchedInferencePipeline, VAD chunks) is ~3-4x faster on GPU.
    Hindi fine-tunes were trained without a prompt."""
    from faster_whisper import WhisperModel
    from . import engine
    m = WhisperModel(src, device=dev, device_index=device_index,
                     compute_type="float16" if dev == "cuda" else "int8")
    try:
        if VOTE_BATCH > 0:
            from faster_whisper import BatchedInferencePipeline
            segs, _ = BatchedInferencePipeline(model=m).transcribe(
                samples, language=language, batch_size=VOTE_BATCH, word_timestamps=True, beam_size=5)
            got = [{"word": w.word.strip(), "start": round(float(w.start), 3), "end": round(float(w.end), 3),
                    "probability": round(float(w.probability), 3)}
                   for sg in segs for w in (sg.words or []) if w.word.strip() and w.end > w.start]
            # Dwarika v4: IndicWhisper medium gave no usable batched words -> 0 votes. Fall back.
            if len(got) >= min_words:
                return got
            print(f"voter {Path(src).name}: batched gave {len(got)} words (< {min_words}); sequential pass")
        return rows_to_words(engine.transcribe(samples, language=language, initial_prompt="", model=m)[0])
    finally:
        del m


def _default_voters(wordlist=None):
    import os
    cfg_p = ROOT / "config" / "voters.json"
    if not cfg_p.exists():
        return {}, wordlist
    cfg = json.loads(cfg_p.read_text(encoding="utf-8"))
    d = Path(os.environ.get("KANG_VOTER_DIR") or (ROOT / cfg.get("default_dir", "models/voters")))
    found = {n: str(d / sub) for n, sub in cfg.get("voters", {}).items() if (d / sub / "model.bin").exists()}
    wl = wordlist or os.environ.get("ENGINE_WORDLIST") or str(d / cfg.get("wordlist", "hi_IN.dic"))
    return found, wl


def _spelling_vote(words, samples, voters, wordlist, agree, glossary, device, language, run, audio_path=""):
    """None when the voter is off; else (words, changes). Missing wordlist/model = warning, never a crash."""
    import os
    from .voter import load_wordlist, spelling_vote
    if os.environ.get("ENGINE_VOTE", "1") == "0":
        return None
    if voters is None and os.environ.get("ENGINE_VOTERS"):
        voters = dict(x.split("=", 1) for x in os.environ["ENGINE_VOTERS"].split(",") if "=" in x)
    if voters is None:  # default ON: whatever config/voters.json models are set up
        voters, wordlist = _default_voters(wordlist)
        if not voters:
            run.warn("spelling voter not set up (python tools/setup_voters.py); continuing without it")
            return None
    if not voters:
        return None
    wl = wordlist or os.environ.get("ENGINE_WORDLIST")
    vocab = load_wordlist(wl, extra=glossary.values()) if wl and Path(wl).exists() else set()
    if not vocab:
        run.warn(f"spelling voter skipped: wordlist not found ({wl})")
        return None
    alts = {}
    jobs = {}
    for name, src in voters.items():
        try:
            if callable(src):
                alts[name] = rows_to_words(src(samples))
                continue
            key = (str(src), str(Path(audio_path).resolve()) if audio_path else id(samples), len(samples), language)
            if key in _ALT_CACHE:
                alts[name] = _ALT_CACHE[key]
            else:
                jobs[name] = (key, str(src))
        except Exception as e:  # one broken second model must not stop the transcript
            run.warn(f"spelling voter: {name} failed: {type(e).__name__}: {e}")
    if jobs:
        import time as _t
        dev = device or os.environ.get("ENGINE_DEVICE", "cuda")
        n_dev = _cuda_count() if dev == "cuda" else 1
        t0 = _t.time()
        from concurrent.futures import ThreadPoolExecutor
        names = list(jobs)
        import queue
        free = queue.Queue()
        for i in range(max(1, n_dev)):
            free.put(i)

        def _on_free_gpu(src):  # exactly one model per GPU at any time (v5: 2 on GPU 0 -> CUDA invalid argument)
            gi = free.get()
            try:
                return _alt_pass(src, samples, language, dev, gi, int(len(words) * VOTE_MIN_FRAC))
            finally:
                free.put(gi)
        with ThreadPoolExecutor(max_workers=max(1, min(n_dev, len(names)))) as ex:
            futs = {n: ex.submit(_on_free_gpu, jobs[n][1]) for n in names}
            for n, f in futs.items():
                try:
                    _ALT_CACHE[jobs[n][0]] = alts[n] = f.result()
                except Exception as e:
                    run.warn(f"spelling voter: {n} failed: {type(e).__name__}: {e}")
        run.log_step("voter_alt_passes", models=names, gpus=n_dev, seconds=round(_t.time() - t0, 1),
                     batch=VOTE_BATCH)
    if not alts:
        return None
    voted, ch = spelling_vote(words, alts, vocab, require_agree=agree and len(alts) >= 2)
    return voted, ch


def _apply_spelling_policy(words, policy_path: Optional[str], run: Run):
    """Opt-in per-video caption spelling (core/spelling_policy.py). Logged, never default."""
    if not policy_path:
        return words
    from .spelling_policy import apply_policy, load_policy
    pol = load_policy(policy_path)
    run.add_input(policy_path, "SPELLING_POLICY")
    words_pre = write_json(run.path("words_pre_policy.json"), words)
    words, ch = apply_policy(words, pol)
    write_json(run.path("spelling_policy_changes.json"), {"policy": str(policy_path), "video": pol.get("video"),
                                                          "decided_by": "editorial-policy", "changes": ch})
    run.log_step("spelling_policy", policy=str(policy_path), changes=len(ch), pre_policy=str(words_pre.name))
    return words


def fix_words(words_path: str, run: Optional[Run] = None, glossary_path: Optional[str] = None,
              spelling_policy: Optional[str] = None) -> Dict[str, Any]:
    """Apply config/glossary.json (+ optional per-video spelling policy) to an existing words.json
    in a NEW run (original untouched)."""
    run = run or Run()
    run.add_input(words_path, "W1")
    words, changes = apply_glossary(load_words(words_path),
                                    load_glossary(glossary_path or ROOT / "config" / "glossary.json"))
    words = _apply_spelling_policy(words, spelling_policy, run)
    wpath = write_json(run.path("words.json"), words)
    write_json(run.path("glossary_changes.json"), changes)
    run.path("review_sample.txt").write_text(review_sample(words, 40), encoding="utf-8")
    run.add_output(wpath, "words")
    run.log_step("fix_words", fixes=len(changes))
    run.set_status("words_fixed")
    return {"run_id": run.run_id, "dir": str(run.dir), "words_json": str(wpath), "fixes": changes}


# --------------------------------------------------------------------------- F01 / Phase 2
def make_subtitles(run: Run, words: List[Dict[str, Any]], fmt: str = "9:16", preset_name: str = "vox_bold_yellow",
                   brand_path: Optional[str] = None, option: Optional[str] = None) -> Dict[str, Any]:
    brand = load_brand(brand_path or ROOT / "brand.json")
    fonts, warnings = resolve_fonts(brand, ROOT / "fonts")
    for w in warnings:
        run.warn(w)
        print("WARNING:", w)
    preset = load_preset(preset_name, ROOT / "presets")
    font = fonts[preset.font_role]
    layout = make_layout(brand, preset, fmt, font)
    ass, events = build_ass(words, brand, preset, layout, font, option=option)
    ass_p = run.path(f"subs_{fmt.replace(':', 'x')}.ass")
    ass_p.write_text(ass, encoding="utf-8")
    srt_p = run.path("subs.srt")
    srt_p.write_text(build_srt(events), encoding="utf-8")
    run.add_output(ass_p, "ass")
    run.add_output(srt_p, "srt")
    checks = [qa.check_no_overlap(ass), qa.check_glyphs(font, [w["word"] for w in words])]
    if (option or ("B" if preset.highlight == "pop" else "A")) == "A":
        checks.append(qa.check_sync(ass, words))
    if events:
        t = (events[0]["start"] + events[0]["end"]) / 2
        png = run.path(f"qa/subtitle_frame_{fmt.replace(':', 'x')}.png")
        qa.render_ass_on_black(ass_p, ROOT / "fonts", CANVAS[fmt], t, png)
        checks.append(qa.check_safe_zone(png, CANVAS[fmt], layout.margin_lr, layout.margin_v))
    # Glyph/shaping test on fixed conjunct/matra sentences, same style as the real subtitles
    test_words = [{"word": w, "start": 0.2 + i * 0.4, "end": 0.55 + i * 0.4}
                  for i, w in enumerate(" ".join(qa.GLYPH_TEST_SENTENCES[:1]).split())]
    gass, _ = build_ass(test_words, brand, preset, layout, font, option="A")
    gpath = run.path(f"qa/glyph_test_{fmt.replace(':', 'x')}.ass")
    gpath.write_text(gass, encoding="utf-8")
    checks.append(qa.check_glyphs(font, qa.GLYPH_TEST_SENTENCES))
    checks.append(qa.check_shaping(gpath, ROOT / "fonts", CANVAS[fmt], 0.9, run.path("qa")))
    return {"ass": ass_p, "srt": srt_p, "events": events, "layout": layout, "brand": brand,
            "preset": preset, "font": font, "checks": checks}


def subtitle_video(video: str, words_path: str, run: Optional[Run] = None, fmt: str = "9:16",
                   preset_name: str = "vox_bold_yellow", preview_start: float = 0.0,
                   approver: Approver = _deny, option: Optional[str] = None) -> Dict[str, Any]:
    """F01: subs.ass + subs.srt + preview_10s.mp4 -> (approve) -> final.mp4 + render_settings.json."""
    run = run or Run()
    run.add_input(video, "A1")
    words = load_words(words_path)
    shutil.copy2(words_path, run.path("words.json"))
    sub = make_subtitles(run, words, fmt, preset_name, option=option)
    log = run.path("ffmpeg.log")
    src = media_summary(video)
    work_video = video
    if not src["has_video"]:
        work_video = str(render.audio_to_video(video, run.path("bg.mp4"), fmt, sub["brand"].colors.primary, log=log))
    elif (src["width"], src["height"]) != CANVAS[fmt]:
        work_video = str(render.render_format(video, fmt, run.path("reframed.mp4"), src["width"], src["height"], log=log))
    prev = render.make_preview(work_video, sub["ass"], ROOT / "fonts", run.path("preview_10s.mp4"), start=preview_start, log=log)
    run.add_output(prev, "preview")
    settings = {"fmt": fmt, "preset": sub["preset"].model_dump(), "layout": sub["layout"].model_dump(),
                "font": Path(sub["font"]).name, "filter": "ass (libass, shaping=complex)", "crf": 20}
    write_json(run.path("render_settings.json"), settings)
    report = qa.qa_report(sub["checks"])
    write_json(run.path("qa_report.json"), report)
    result: Dict[str, Any] = {"run_id": run.run_id, "dir": str(run.dir), "preview": str(prev), "qa": report, "final": None}
    if not report["pass"]:
        run.set_status("qa_failed")
        return result
    gate_art = [prev, sub["ass"], run.path("words.json")]
    gate_info = f"Preview: {prev}\nQA: PASS"
    if _gate(run, "preview", gate_info, approver, artifacts=gate_art, settings=settings):
        if not run.approval_valid("preview", plan_hash(gate_info, gate_art, settings)):  # changed since approval
            run.set_status("approval_invalidated")
            result["error"] = "preview/words/style changed after approval; re-approve"
            return result
        final = render.burn_subtitles(work_video, sub["ass"], ROOT / "fonts", run.path("final.mp4"), log=log)
        dur = media_summary(work_video)["duration"]
        chk = qa.check_export(final, dur, CANVAS[fmt])
        report = qa.qa_report(sub["checks"] + [chk])
        write_json(run.path("qa_report.json"), report)
        run.add_output(final, "final")
        result.update(final=str(final), qa=report)
        run.set_status("done" if report["pass"] else "qa_failed")
    else:
        run.set_status("awaiting_preview_approval")
    return result


DELIVERY_LUFS = -14.0  # measured on the delivered MP4, not the intermediate WAV
DELIVERY_TP = -1.5
AAC_SAFE_TP = -3.0
BLOCKING_WORD_S = 3.0  # one 'word' this long = whole sentences dropped (Dwarika 571 s: 11.56 s)
FULL_MAX_S = 3600.0  # --full mode: whole file, up to 1 hour


def promo_clip(audio_path: str, words_path: str, start: float, duration: float, run: Optional[Run] = None,
               fmt: str = "9:16", preset_name: str = "vox_bold_yellow", approver: Approver = _deny,
               max_duration: float = 60.0) -> Dict[str, Any]:
    """Phase 2 exit proof: voiceover slice -> 15-30s branded promo MP4 with word-highlight subtitles.
    max_duration is raised only by the workflow's --full mode."""
    if not 1 <= duration <= max_duration:
        raise ValueError(f"promo duration must be 1-{max_duration:g} s (roadmap: 15-30 s)")
    run = run or Run()
    run.add_input(audio_path, "A1")
    words = [dict(w) for w in load_words(words_path) if w["start"] >= start and w["end"] <= start + duration]
    for w in words:
        w["start"] = round(w["start"] - start, 3)
        w["end"] = round(w["end"] - start, 3)
    if not words:
        raise ValueError("No words inside the selected promo window")
    sliced_words = write_json(run.path("promo_words.json"), words)
    brand = load_brand(ROOT / "brand.json")
    log = run.path("ffmpeg.log")
    bg = render.audio_to_video(audio_path, run.path("promo_bg.mp4"), fmt, brand.colors.primary, start=start,
                               duration=duration, log=log)
    return subtitle_video(str(bg), str(sliced_words), run=run, fmt=fmt, preset_name=preset_name, approver=approver)


# --------------------------------------------------------------------------- M3 Workflow G (F12)
def _to_timeline(t: float, keep: List[List[float]]) -> float:
    """Source time -> time on the cut timeline (a time inside a removed range snaps to the next kept start)."""
    acc = 0.0
    for s, e in keep:
        if t < s:
            return acc
        if t <= e:
            return acc + (t - s)
        acc += e - s
    return acc


def premiere_package(media: str, words_path: str, run: Optional[Run] = None, approver: Approver = _deny,
                     scenes_path: Optional[str] = None, cuts_path: Optional[str] = None, fps: int = 25,
                     win_root: Optional[str] = None, preset_name: str = "vox_bold_yellow",
                     target_scene_s: float = 30.0, english_script: str = "asr") -> Dict[str, Any]:
    """Accepted transcript -> scenes.json -> Gate 1 (scene_plan) -> Premiere package:
    sequence.xml (FCP7 xmeml, original media, editable cuts, scene markers) + captions.srt + scenes.json
    + words.json + media/ + README_IMPORT.txt + package_manifest.json (sha256 of every file).
    Narration is kept whole unless an APPROVED cut plan (cuts.json from a run whose cut_list gate is
    approved) is passed with cuts_path."""
    from . import premiere, scenes as scenes_mod
    from .runs import sha256_file
    run = run or Run()
    inp = run.add_input(media, "A1")
    ms = media_summary(media)
    words = load_words(words_path)
    shutil.copy2(words_path, run.path("words.json"))
    result: Dict[str, Any] = {"run_id": run.run_id, "dir": str(run.dir), "package": None}
    # transcript accepted only via apply_review (writes transcript_acceptance.json next to the words)
    acc_p = Path(words_path).resolve().parent / "transcript_acceptance.json"
    transcript_accepted = False
    if acc_p.is_file():
        from .runs import sha256_file as _sha
        acc = json.loads(acc_p.read_text(encoding="utf-8"))
        transcript_accepted = bool(acc.get("accepted")) and acc.get("words_sha256") == _sha(Path(words_path))
    result["transcript_accepted"] = transcript_accepted

    keep = [[0.0, ms["duration"]]]
    if cuts_path:
        cdir = Path(cuts_path).resolve().parent
        rec = json.loads((cdir / "approvals.json").read_text(encoding="utf-8")) if (cdir / "approvals.json").is_file() else []
        last = [r for r in rec if r["gate"] == "cut_list"]
        if not last or last[-1]["value"] != "approved":
            run.set_status("blocked_unapproved_cuts")
            result["error"] = "cuts.json has no approved cut_list gate; narration kept whole is the default"
            return result
        # the approval must be for THIS cuts.json content (plan hash) and THIS source media
        cplan = json.loads(Path(cuts_path).read_text(encoding="utf-8"))
        h_now = plan_hash(cutter.cut_list_text(cplan), [cuts_path])
        if last[-1].get("plan_hash") != h_now:
            run.set_status("blocked_unapproved_cuts")
            result["error"] = "cuts.json changed after its cut_list approval (plan hash mismatch); re-run the cut gate"
            return result
        src_man = cdir / "manifest.json"
        src_inputs = json.loads(src_man.read_text(encoding="utf-8")).get("inputs", []) if src_man.is_file() else []
        if not any(i.get("sha256") == inp["sha256"] for i in src_inputs):
            run.set_status("blocked_unapproved_cuts")
            result["error"] = "cuts.json was approved for different source media (sha256 mismatch)"
            return result
        keep = cplan["keep"]
        result["cuts_approved_by"] = last[-1]["approver"]
        result["cuts_human_approved"] = last[-1]["approver"] not in AUTO_APPROVERS

    # Step 1: scene plan (generated, or the user's edited scenes.json)
    if scenes_path:
        plan = json.loads(Path(scenes_path).read_text(encoding="utf-8"))
    else:
        plan = scenes_mod.plan_scenes(words, ms["duration"], target_s=target_scene_s)
    errs = scenes_mod.validate_scenes(plan, n_words=len(words))
    sp = write_json(run.path("scenes.json"), plan)
    run.add_output(sp, "scenes")
    result["scenes"] = len(plan.get("scenes", []))
    if errs:
        run.set_status("qa_failed")
        result["error"] = "scene plan invalid"
        result["problems"] = errs
        return result

    # Gate 1: scene plan, bound to scenes.json + words.json content
    info = scenes_mod.scene_plan_text(plan)
    art = [sp, run.path("words.json")]
    if not _gate(run, "scene_plan", info, approver, artifacts=art, settings={"keep": keep, "fps": fps}):
        run.set_status("awaiting_scene_approval")
        result["scene_plan"] = info
        return result
    result["human_approved"] = run.manifest.get("human_approved", {}).get("scene_plan", False)

    # Step 2: package
    pkg = run.path("premiere_package")
    (pkg / "media").mkdir(parents=True, exist_ok=True)
    mname = Path(media).name
    shutil.copy2(media, pkg / "media" / mname)
    xml_media_path = (str(PureWindowsPath(win_root) / "media" / mname) if win_root
                      else str((pkg / "media" / mname).resolve()))
    markers = [{"at": _to_timeline(s["start"], keep), "name": f"{s['id']} {s['title']}"[:80],
                "comment": s["text"][:500]} for s in plan["scenes"]]
    w, h = (ms.get("width") or 1920, ms.get("height") or 1080)
    xml, stats = premiere.build_xmeml(
        f"KANG {run.run_id}", {"path": xml_media_path, "name": mname, "duration": ms["duration"],
                              "has_video": ms["has_video"], "channels": ms.get("channels", 2),
                              "sample_rate": ms.get("sample_rate", 48000)},
        keep, fps=fps, width=w, height=h, markers=markers)
    (pkg / "sequence.xml").write_text(xml, encoding="utf-8")
    words_tl = cutter.remap_words(words, [tuple(k) for k in keep]) if cuts_path else words
    from . import script_style
    cap_words, script_rep = script_style.apply(
        words_tl, english_script, script_style.load_table(ROOT / "config" / "english_script.json"))
    write_json(run.path("english_script_changes.json"), script_rep)
    for u in script_rep["unmapped"]:
        run.warn(f"english_script=devanagari: no mapping for '{u}' (left as transcribed)")
    sub = make_subtitles(run, cap_words, "16:9", preset_name)
    shutil.copy2(sub["srt"], pkg / "captions.srt")
    shutil.copy2(sp, pkg / "scenes.json")
    write_json(pkg / "words.json", words_tl)
    (pkg / "README_IMPORT.txt").write_text(
        "KANG Premiere package (" + run.run_id + ")\n"
        "Target: Premiere Pro 24.6.1\n"
        "Actual import verification: pending (NOT_TESTED)\n"
        "Contents: narration audio + scene markers. Video track is EMPTY (no visuals yet).\n"
        "Captions: separate captions.srt (NOT embedded in the XML).\n"
        "Transcript: " + ("ACCEPTED after human review" if transcript_accepted else
                          "NOT accepted yet - names/amounts need a listen (python kang.py review)") + "\n"
        "Paths: XML points to " + (str(PureWindowsPath(win_root) / "media" / mname) if win_root else "media/" + mname)
        + ". Put the folder exactly there or use Link Media.\n\n"
        "1. Copy this whole folder to " + (win_root or "your PC") + " (keep media/ next to sequence.xml).\n"
        "2. Premiere: File > Open Project (Ctrl+O), file type 'All Files', pick sequence.xml. It opens as its own project (File > Import of the XML failed on the test PC).\n"
        "3. Media offline? Double-click FIX_PATHS.bat first (points the XML at this folder), or Link Media > media/" + mname + ".\n"
        "4. File > Import > captions.srt, then drag it onto the sequence (caption track).\n"
        "5. Scene markers S01... sit on the sequence timeline; scenes.json has each scene's text.\n"
        f"Sequence: {stats['sequence_s']} s at {fps} fps, {stats['clips']} clip(s), {stats['markers']} markers.\n",
        encoding="utf-8")
    premiere.write_fix_paths(pkg)
    checks = [premiere.check_xmeml(xml, fps)]
    exp = round(sum(e - s for s, e in keep), 3)
    checks.append({"name": "sequence_duration", "pass": abs(stats["sequence_s"] - exp) <= 1.5 / fps * max(1, len(keep)),
                   "detail": {"expected_s": exp, "sequence_s": stats["sequence_s"]}})
    files = sorted(p for p in pkg.rglob("*") if p.is_file())
    write_json(pkg / "package_manifest.json", {"run_id": run.run_id, "source_sha256": inp["sha256"], "stats": stats,
               "status": {"transcript_accepted": transcript_accepted, "words_source": str(words_path),
                          "scene_plan_human_approved": result["human_approved"], "visuals": "NOT_STARTED",
                          "captions": "separate_srt", "caption_english_script": english_script,
                          "premiere_import": "NOT_TESTED"},
               "files": {str(p.relative_to(pkg)).replace("\\", "/"): sha256_file(p) for p in files}})
    report = qa.qa_report(checks)
    write_json(run.path("qa_report.json"), report)
    run.add_output(pkg / "sequence.xml", "premiere_xml")
    run.log_step("premiere_package", **stats)
    run.set_status("package_ready" if report["pass"] else "qa_failed")
    result.update(package=str(pkg), stats=stats, qa=report)
    # generation != acceptance: draft_package_ready / package_generated_pending_verification / qa_failed
    from .package_readiness import finalize_package_readiness
    finalize_package_readiness(run, result, pkg, words_tl, report)
    return result


# --------------------------------------------------------------------------- M3 visuals
def visuals_template(scenes_path: str, out_csv: Optional[str] = None, run: Optional[Run] = None) -> Dict[str, Any]:
    """scenes.json -> visuals.csv (one row per scene) for the user to fill: brief, asset, licence."""
    from . import scenes as scenes_mod, visuals as vis
    run = run or Run()
    run.add_input(scenes_path, "SCENES")
    plan = json.loads(Path(scenes_path).read_text(encoding="utf-8"))
    errs = scenes_mod.validate_scenes(plan)
    if errs:
        run.set_status("qa_failed")
        return {"run_id": run.run_id, "ok": False, "problems": errs}
    out = vis.write_template(plan, out_csv or run.path("visuals.csv"))
    run.add_output(out, "visuals_template")
    run.set_status("visuals_template_ready")
    return {"run_id": run.run_id, "dir": str(run.dir), "ok": True, "visuals_csv": str(out), "scenes": len(plan["scenes"])}


def visual_preview(media: str, words_path: str, scenes_path: str, visuals_csv: str, assets_dir: str,
                   scene_ids: Optional[List[str]] = None, run: Optional[Run] = None, approver: Approver = _deny,
                   fps: int = 25, preset_name: str = "vox_bold_yellow", win_root: Optional[str] = None,
                   selected_by: str = "user") -> Dict[str, Any]:
    """Approved local visuals -> (a) integration preview mp4 of the chosen contiguous scenes (visuals +
    narration + burned captions, 16:9) and (b) Premiere package whose sequence carries every approved
    visual on its own video track at scene times. Narration kept whole (no cuts in this step).
    Nothing is accepted here: transcript/timing/import status travel in package_manifest.json."""
    from . import premiere, scenes as scenes_mod, visuals as vis
    from .runs import run_ffmpeg, sha256_file
    run = run or Run()
    inp = run.add_input(media, "A1")
    run.add_input(words_path, "W1")
    run.add_input(scenes_path, "SCENES")
    run.add_input(visuals_csv, "VISUALS_CSV")
    ms = media_summary(media)
    words = load_words(words_path)
    plan = json.loads(Path(scenes_path).read_text(encoding="utf-8"))
    result: Dict[str, Any] = {"run_id": run.run_id, "dir": str(run.dir), "accepted": False}
    errs = scenes_mod.validate_scenes(plan, n_words=len(words))
    if abs(plan.get("duration", 0) - ms["duration"]) > 0.05:
        errs.append(f"scenes.json duration {plan.get('duration')} != media {ms['duration']:.3f}")
    if errs:
        run.set_status("qa_failed")
        return result | {"error": "scene plan invalid for this media/words", "problems": errs}
    sp = write_json(run.path("scenes.json"), plan)
    shutil.copy2(words_path, run.path("words.json"))
    chk = vis.validate(vis.read_csv(visuals_csv), plan, assets_dir)
    adir_abs = Path(chk["visuals"]["assets_dir"])
    try:  # portable: store assets_dir relative to the KANG root when it lives inside it
        chk["visuals"]["assets_dir"] = adir_abs.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        chk["visuals"]["assets_dir"] = adir_abs.name
    seq_end = int(ms["duration"] * fps + 1e-6) / fps  # sequence ends on a whole frame -> clamp last shot to it
    for it in chk["visuals"]["items"]:
        if it["end"] > seq_end:
            it["end"] = round(seq_end, 3)
            it["duration"] = round(it["end"] - it["start"], 3)
    chk["visuals"]["selected_by"] = selected_by
    vp = write_json(run.path("visuals.json"), chk["visuals"])
    for w_ in chk["warnings"]:
        run.warn(w_)
    result.update(visuals=len(chk["visuals"]["items"]), warnings=chk["warnings"])
    if not chk["ok"]:
        run.set_status("qa_failed")
        return result | {"error": "visuals.csv invalid", "problems": chk["problems"]}
    if not chk["visuals"]["items"]:
        run.set_status("qa_failed")
        return result | {"error": "no scene has an asset yet"}
    info = vis.selection_text(chk["visuals"])
    if not _gate(run, "visual_selection", info, approver, artifacts=[vp, sp], settings={"fps": fps, "scenes": scene_ids}):
        run.set_status("awaiting_visual_approval")
        return result | {"visual_selection": info}
    result["visuals_human_approved"] = run.manifest.get("human_approved", {}).get("visual_selection", False)
    adir = adir_abs
    log = run.path("ffmpeg.log")
    checks: List[Dict[str, Any]] = []
    acc_p = Path(words_path).resolve().parent / "transcript_acceptance.json"
    transcript_accepted = False
    if acc_p.is_file():
        acc = json.loads(acc_p.read_text(encoding="utf-8"))
        transcript_accepted = bool(acc.get("accepted")) and acc.get("words_sha256") == sha256_file(Path(words_path))

    # (b) Premiere package: narration whole + visual track + scene markers + full captions.srt
    pkg = run.path("premiere_package")
    (pkg / "media").mkdir(parents=True, exist_ok=True)
    (pkg / "visuals").mkdir(exist_ok=True)
    mname = Path(media).name
    shutil.copy2(media, pkg / "media" / mname)
    base = PureWindowsPath(win_root) if win_root else None
    vclips = []
    for it in chk["visuals"]["items"]:
        dst = pkg / "visuals" / Path(it["asset"]).name
        if not dst.exists():
            shutil.copy2(adir / it["asset"], dst)
        vinfo = media_summary(dst)
        vclips.append({"path": str(base / "visuals" / dst.name) if base else str(dst.resolve()), "name": dst.name,
                       "width": vinfo.get("width"), "height": vinfo.get("height"),
                       "kind": it["kind"], "start": it["start"], "end": it["end"], "in": it["asset_in"],
                       "src_duration": it.get("asset_duration", it["duration"]), "loop": it["fit"] == "loop"})
    markers = [{"at": s["start"], "name": f"{s['id']} {s['title']}"[:80], "comment": s["text"][:500]} for s in plan["scenes"]]
    xml, stats = premiere.build_xmeml(
        f"KANG {run.run_id} visuals", {"path": str(base / "media" / mname) if base else str((pkg / "media" / mname).resolve()),
                                       "name": mname, "duration": ms["duration"], "has_video": ms["has_video"],
                                       "channels": ms.get("channels", 2), "sample_rate": ms.get("sample_rate", 48000),
                                       "width": ms.get("width"), "height": ms.get("height")},
        [[0.0, ms["duration"]]], fps=fps, markers=markers, visual_clips=vclips)
    (pkg / "sequence.xml").write_text(xml, encoding="utf-8")
    checks.append(premiere.check_xmeml(xml, fps))
    full_sub = make_subtitles(run, words, "16:9", preset_name)
    checks.extend(c for c in full_sub.get("checks", []) if isinstance(c, dict))
    shutil.copy2(full_sub["srt"], pkg / "captions.srt")
    shutil.copy2(sp, pkg / "scenes.json")
    shutil.copy2(vp, pkg / "visuals.json")
    write_json(pkg / "words.json", words)

    # (a) integration preview of the chosen contiguous scenes
    preview = None
    if scene_ids:
        sel = vis.pick(chk["visuals"], plan, scene_ids)
        t0, t1 = sel[0]["start"], sel[-1]["end"]
        F = lambda t: int(round((t - t0) * fps))
        parts = run.path("preview_parts")
        parts.mkdir(exist_ok=True)
        lst = []
        for it in sel:
            seg = parts / f"{it.get('shot', it['scene'])}.mp4"
            nfr = F(it["end"]) - F(it["start"])
            run_ffmpeg(vis.segment_args(it, adir / it["asset"], seg, nfr / fps, 1920, 1080, fps), log)
            lst.append(f"file '{seg.resolve().as_posix()}'")
        (parts / "concat.txt").write_text("\n".join(lst) + "\n", encoding="utf-8")
        vonly = run.path("preview_visuals_only.mp4")
        run_ffmpeg(["-f", "concat", "-safe", "0", "-i", str(parts / "concat.txt"), "-c", "copy", str(vonly)], log)
        dur = F(t1) / fps
        wsl = [dict(w, start=round(w["start"] - t0, 3), end=round(w["end"] - t0, 3))
               for w in words if w["start"] >= t0 - 1e-6 and w["end"] <= t1 + 1e-6]
        sub = make_subtitles(run, wsl, "16:9", preset_name)
        checks.extend(c for c in sub.get("checks", []) if isinstance(c, dict))
        preview = run.path("preview_" + "_".join(s["scene"] for s in (sel[0], sel[-1])) + ".mp4")
        # +faststart rewrites the file at the end; on network filesystems (JuiceFS sandbox) that
        # fails with "Error writing trailer: Input/output error" -> encode on local temp, then move
        import tempfile
        tmp_out = Path(tempfile.mkdtemp(prefix="kang_prev_")) / preview.name
        run_ffmpeg(["-i", str(vonly), "-ss", f"{t0:.3f}", "-t", f"{dur:.3f}", "-i", str(media), "-map", "0:v", "-map", "1:a",
                    "-vf", render.subtitles_filter(sub["ass"], ROOT / "fonts"), "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-t", f"{dur:.3f}",
                    "-movflags", "+faststart", str(tmp_out)], log)
        shutil.move(str(tmp_out), str(preview))
        pm = media_summary(preview)
        checks.append({"name": "preview_duration", "pass": abs(pm["duration"] - dur) <= 0.1,
                       "detail": {"expected_s": round(dur, 3), "actual_s": round(pm["duration"], 3)}})
        checks.append({"name": "preview_has_audio_video", "pass": pm["has_video"] and pm["has_audio"]})
        run.add_output(preview, "visual_preview")
        result.update(preview=str(preview), preview_range_s=[round(t0, 3), round(t1, 3)],
                      preview_scenes=[i["scene"] for i in sel])

    (pkg / "README_IMPORT.txt").write_text(
        "KANG Premiere package with scene visuals (" + run.run_id + ")\n"
        "Target: Premiere Pro 24.6.1. Actual import verification: pending (NOT_TESTED)\n"
        "Video track: " + str(len(vclips)) + " scene visual(s) from visuals/; scenes without a visual stay empty.\n"
        "Visual selection: " + selected_by + ". Human visual review: "
        + ("recorded" if result["visuals_human_approved"] else "PENDING") + ".\n"
        "Narration: whole (no cuts). Captions: separate captions.srt.\n"
        "Durations: scenes.json = source audio time (" + f"{plan.get('duration', 0):.3f}" + " s); sequence and visuals end on the last whole frame at "
        + str(fps) + " fps (" + f"{seq_end:.3f}" + " s). Difference < 1 frame, by design.\n"
        "Hindi source transcript: " + ("ACCEPTED" if transcript_accepted else "DRAFT - not accepted (listening review pending)") + "\n"
        "Word-level caption timing: " + ("see transcript acceptance" if transcript_accepted else "NOT verified") + "\n"
        "Paths: XML points to " + (str(base) if base else "this folder") + " (media/ and visuals/ next to sequence.xml).\n\n"
        "1. Extract anywhere (or to " + (str(base) if base else "your PC") + "), then double-click FIX_PATHS.bat\n"
        "   (rewrites sequence.xml to this folder, says PASS/WARN). No Link Media needed.\n"
        "2. Premiere: File > Open Project (Ctrl+O), file type 'All Files', pick sequence.xml (not File > Import).\n"
        "3. Home key (playhead 00:00:00:00), select captions.srt in the Project panel after File > Import, press '.' (Overwrite).\n"
        "4. If anything still shows offline: right-click > Link Media > media/ or visuals/.\n", encoding="utf-8")
    credits = [n for n in ("CREDITS.txt", "CREDITS.json") if (adir / n).is_file()]
    for n in credits:  # rights evidence travels with the visuals and is hashed in the manifest
        shutil.copy2(adir / n, pkg / n)
    if vclips and not credits:
        run.warn("assets dir has no CREDITS.txt/CREDITS.json; licence evidence not packaged")
    premiere.write_fix_paths(pkg)
    files = sorted(p for p in pkg.rglob("*") if p.is_file())
    report = qa.qa_report(checks)
    write_json(pkg / "package_manifest.json", {
        "run_id": run.run_id, "source_sha256": inp["sha256"], "stats": stats,
        "status": {"transcript_accepted": transcript_accepted, "words_source": str(words_path),
                   "scene_plan_human_approved": False, "visuals": "selected_by:" + selected_by,
                   "visuals_human_approved": result["visuals_human_approved"],
                   "captions": "separate_srt", "premiere_import": "NOT_TESTED",
                   "preview": "integration_preview" if preview else "none"},
        "files": {str(p.relative_to(pkg)).replace("\\", "/"): sha256_file(p) for p in files}})
    write_json(run.path("qa_report.json"), report)
    run.add_output(pkg / "sequence.xml", "premiere_xml")
    run.log_step("visual_preview", visual_items=len(vclips), preview=bool(preview), **stats)
    result.update(package=str(pkg), stats=stats, qa=report)
    from .package_readiness import finalize_package_readiness
    finalize_package_readiness(run, result, pkg, words, report)
    return result


# --------------------------------------------------------------------------- F03
def review_transcript(media: str, words_path: str, run: Optional[Run] = None, manual: Optional[List[str]] = None,
                      clips: bool = True, pad_s: float = 1.5) -> Dict[str, Any]:
    """Make review.csv (+ one mp3 clip per span) for the human listen. Changes NO words."""
    from . import review as rv, scenes as scenes_mod
    run = run or Run()
    run.add_input(media, "A1")
    words = load_words(words_path)
    shutil.copy2(words_path, run.path("words.json"))
    spans = rv.review_spans(words)
    man, missing = [], []
    for ph in manual or []:
        m = rv.find_phrase(words, ph)
        (man.append(m) if m else missing.append(ph))
    spans = rv.merge_manual(spans, man, words)
    rdir = run.path("review")
    rdir.mkdir(parents=True, exist_ok=True)
    if clips:
        cdir = rdir / "clips"
        cdir.mkdir(exist_ok=True)
        for s in spans:
            out = cdir / f"{s['id']}_{int(s['start'] // 60):02d}m{int(s['start'] % 60):02d}s.mp3"
            ss = max(0.0, s["start"] - pad_s)
            from .runs import run_ffmpeg
            run_ffmpeg(["-ss", f"{ss:.2f}", "-t", f"{s['end'] + pad_s - ss:.2f}", "-i", media,
                               "-vn", "-ac", "1", "-b:a", "96k", str(out)])
            s["clip"] = "clips/" + out.name
    plan = scenes_mod.plan_scenes(words, media_summary(media)["duration"])
    csv_p = rv.write_review_csv(rdir / "review.csv", spans, plan)
    run.add_output(csv_p, "review_csv")
    pri = {k: sum(1 for s in spans if s["priority"] == k) for k in (1, 2, 3)}
    run.log_step("review_transcript", spans=len(spans), **{f"p{k}": v for k, v in pri.items()})
    run.set_status("review_required")
    return {"run_id": run.run_id, "dir": str(run.dir), "review_csv": str(csv_p), "spans": len(spans),
            "by_priority": pri, "manual_not_found": missing, "transcript_accepted": False}


TEXT_SOURCES = {"human": "human_reviewed", "auto-extraction": "auto_extraction_recommended"}


def apply_transcript_review(words_path: str, review_csv: str, run: Optional[Run] = None,
                            approver: Approver = _deny, source: str = "human") -> Dict[str, Any]:
    """Apply the human's review.csv -> new words.json. Acceptance (transcript_acceptance.json) is
    written only when every priority-1 row has an action AND a human approves the transcript gate."""
    from . import review as rv
    from .runs import sha256_file
    run = run or Run()
    words = load_words(words_path)
    rows = rv.read_review_csv(review_csv)
    status = TEXT_SOURCES[source]
    res = rv.apply_review(words, rows, text_status=status)
    result: Dict[str, Any] = {"run_id": run.run_id, "dir": str(run.dir), "ok": res["ok"], "problems": res["problems"],
                              "applied": res["applied"], "transcript_accepted": False, "text_status": status}
    if not res["ok"]:
        run.set_status("qa_failed")
        return result
    shutil.copy2(review_csv, run.path("review.csv"))
    wp = write_json(run.path("words.json"), res["words"])
    run.add_output(wp, "words_reviewed")
    write_json(run.path("review_changes.json"), res["applied"])
    open_p1 = [r["id"] for r in rows if str(r.get("priority")) == "1" and not (r.get("action") or "").strip()]
    result["words"] = str(wp)
    result["open_priority1"] = open_p1
    result["timing_unverified"] = res.get("timing_unverified", [])
    not_listened = [a["id"] for a in res["applied"] if a["text_status"] != "human_reviewed" or a["content_review_pending"]]
    result["not_listened"] = not_listened
    if source != "human" or not_listened:  # auto-extraction / editorial-policy / pending rows: a DRAFT, never accepted
        run.path("transcript.txt").write_text(" ".join(w["word"] for w in res["words"]), encoding="utf-8")
        run.log_step("apply_review_draft", source=source, fixes=len(res["applied"]))
        run.set_status("draft_corrected_not_accepted")
        result["status"] = "draft_corrected_not_accepted"
        return result
    if open_p1:
        run.set_status("review_required")
        return result
    info = f"Transcript review: {len(res['applied'])} fix(es) applied, {len(rows)} rows reviewed. Accept transcript?"
    if _gate(run, "transcript", info, approver, artifacts=[wp, run.path("review.csv")]):
        human = run.manifest.get("human_approved", {}).get("transcript", False)
        who = getattr(approver, "approver_name", getattr(approver, "__name__", "callable"))
        write_json(run.path("transcript_acceptance.json"), {"accepted": human, "words_sha256": sha256_file(wp),
                                                            "approver": who, "text_accepted": human,
                                                            "changed_word_timing_review_required": bool(res.get("timing_unverified", [])),
                                                            "timing_unverified": res.get("timing_unverified", []),
                                                            "full_audio_sync": "NOT_TESTED"})
        result["transcript_accepted"] = human
        run.set_status("transcript_accepted" if human else "review_required")
    else:
        run.set_status("awaiting_transcript_approval")
    return result


def plan_and_cut(media: str, words_path: str, run: Optional[Run] = None, approver: Approver = _deny,
                 noise_db: float = -34.0, min_silence: float = 0.45) -> Dict[str, Any]:
    run = run or Run()
    inp = run.add_input(media, "A1")
    words = load_words(words_path)
    total = media_summary(media)["duration"]
    sil = cutter.detect_silence(media, noise_db, min_silence, total)
    fill = cutter.load_fillers(ROOT / "config" / "fillers.json")
    plan = cutter.plan_cuts(words, sil, total, fill)
    plan["silences"] = sil
    words = plan.pop("words_tightened")  # silence-aware word bounds (used for QA + remap)
    run.path("cut_list.txt").write_text(cutter.cut_list_text(plan), encoding="utf-8")
    write_json(run.path("words_tightened.json"), words)
    bad = cutter.check_no_word_truncated(words, plan["keep"], fill["auto"])
    write_json(run.path("cuts.json"), plan)
    has_video = media_summary(media)["has_video"]
    edl = EDL(run_id=run.run_id, inputs=[Input(id="A1", path=inp["path"], sha256=inp["sha256"])],
              cuts=[Cut(src="A1", **{"in": s}, out=e, type="jumpcut") for s, e in plan["keep"]],
              approvals=Approvals(cut_list="pending", preview="pending"))
    save_edl(edl, run.path("edl.json"))
    result: Dict[str, Any] = {"run_id": run.run_id, "dir": str(run.dir), "plan": plan["stats"], "truncated_words": bad, "output": None}
    run.log_step("cut_plan", **plan["stats"], truncated=len(bad))
    if bad:
        run.set_status("qa_failed")
        return result
    if _gate(run, "cut_list", cutter.cut_list_text(plan), approver, artifacts=[run.path("cuts.json")]):
        ext = ".mp4" if has_video else ".wav"
        out = cutter.render_cuts(media, plan["keep"], run.path(f"cut{ext}"), video=has_video, log=run.path("ffmpeg.log"))
        new_words = cutter.remap_words(words, plan["keep"])
        write_json(run.path("words_cut.json"), new_words)
        dur = media_summary(out)["duration"]
        result["output"] = str(out)
        result["duration_check"] = {"expected": plan["stats"]["kept_dur"], "actual": dur,
                                    "pass": abs(dur - plan["stats"]["kept_dur"]) <= 1 / 30 + 0.05}
        edl.approvals.cut_list = "approved"
        save_edl(edl, run.path("edl.json"))
        run.add_output(out, "cut")
        run.set_status("cut_done")
    else:
        run.set_status("awaiting_cut_approval")
    return result


# --------------------------------------------------------------------------- F04
def clean_audio(media: str, run: Optional[Run] = None, target_lufs: float = -14.0, true_peak: float = -1.5,
                rnnoise_model: Optional[str] = None) -> Dict[str, Any]:
    run = run or Run()
    run.add_input(media, "A1")
    has_video = media_summary(media)["has_video"]
    out = run.path("clean.mp4" if has_video else "clean.wav")
    rep = audio_mod.clean_audio(media, out, target_lufs, true_peak, rnnoise_model=rnnoise_model,
                                video_copy=has_video, log=run.path("ffmpeg.log"))
    write_json(run.path("loudness_report.json"), rep)
    run.add_output(out, "clean_audio")
    run.log_step("audio_cleanup", passed=rep["pass"], after=rep["after"])
    run.set_status("audio_done" if rep["pass"] else "qa_failed")
    return {"run_id": run.run_id, "dir": str(run.dir), "output": str(out), "report": rep}


# --------------------------------------------------------------------------- F05
def multi_format(video: str, words_path: Optional[str], formats: List[str], run: Optional[Run] = None,
                 preset_name: str = "vox_bold_yellow", reframe_x: float = 0.5) -> Dict[str, Any]:
    run = run or Run()
    run.add_input(video, "A1")
    src = media_summary(video)
    words = load_words(words_path) if words_path else None
    outs, checks = {}, []
    for fmt in formats:
        ass = make_subtitles(run, words, fmt, preset_name)["ass"] if words else None
        out = render.render_format(video, fmt, run.path(f"out_{fmt.replace(':', 'x')}.mp4"), src["width"], src["height"],
                                   ass_path=ass, fonts_dir=ROOT / "fonts", reframe_x=reframe_x, log=run.path("ffmpeg.log"))
        c = qa.check_export(out, src["duration"], CANVAS[fmt])
        c["name"] = f"export_{fmt}"
        checks.append(c)
        outs[fmt] = str(out)
        run.add_output(out, f"export_{fmt}")
    report = qa.qa_report(checks)
    write_json(run.path("qa_report.json"), report)
    run.set_status("done" if report["pass"] else "qa_failed")
    return {"run_id": run.run_id, "dir": str(run.dir), "outputs": outs, "qa": report}


# --------------------------------------------------------------------------- F19-lite
def palette_from_screenshot(image: str, run: Optional[Run] = None, k: int = 5) -> Dict[str, Any]:
    from .style import extract_palette, palette_to_brand_draft
    run = run or Run()
    run.add_input(image, "IMG1")
    draft = palette_to_brand_draft(extract_palette(image, k))
    p = write_json(run.path("brand_draft.json"), draft)
    run.add_output(p, "brand_draft")
    run.set_status("draft_ready")
    return {"run_id": run.run_id, "dir": str(run.dir), "draft": draft}


# --------------------------------------------------------------------------- Phase 3 workflow
def workflow_clip(source: str, start: float = 0.0, duration: float = 60.0,
                  formats: Optional[List[str]] = None, preset_name: str = "vox_bold_yellow",
                  approver: Approver = _deny, language: str = "hi", device: Optional[str] = None,
                  model_size: str = "large-v3-turbo", initial_prompt: Optional[str] = None,
                  transcriber: Optional[Callable] = None, full: bool = False,
                  spelling_policy: Optional[str] = None) -> Dict[str, Any]:
    """Phase 3 exit proof, one call, no code edits:
    full=True: process the whole file from `start` (duration ignored, max 1 h); default formats 16:9.
    slice -> transcribe (+glossary) -> F03 cut [gate] -> F04 clean -> F01/F02 subtitles per format [gate].
    Each stage is its own child run; the parent run records child IDs and the combined verdict."""
    from .runs import run_ffmpeg
    if full:
        duration = round(media_summary(source)["duration"] - start, 3)
        formats = formats or ["16:9"]
        if not 5 <= duration <= FULL_MAX_S:
            raise ValueError(f"full mode: source after --start must be 5-{FULL_MAX_S:g} s, got {duration}")
    elif not 5 <= duration <= 60:
        raise ValueError("workflow clip duration must be 5-60 s (use full=True / --full for the whole file)")
    formats = formats or ["9:16", "16:9", "1:1"]
    max_render = FULL_MAX_S if full else 60.0
    t0 = time.time()
    wf = Run()
    wf.add_input(source, "SRC")
    sl = wf.path("source_slice.wav")
    run_ffmpeg(["-ss", f"{start:.3f}", "-t", f"{duration:.3f}", "-i", str(source), "-vn", "-ac", "1",
                "-ar", "48000", str(sl)], log_path=wf.path("ffmpeg.log"))
    stages: Dict[str, Any] = {}
    verdict: List[Dict[str, Any]] = []

    def done(status: str) -> Dict[str, Any]:
        summary = {"run_id": wf.run_id, "dir": str(wf.dir), "source": str(source), "start": start,
                   "duration": duration, "full": full, "seconds_taken": round(time.time() - t0, 1), "stages": stages, "checks": verdict,
                   "pass": bool(verdict) and all(c["pass"] for c in verdict) and status == "done"}
        write_json(wf.path("workflow_report.json"), summary)
        wf.set_status(status)
        return summary

    t = transcribe_to_words(str(sl), language=language, model_size=model_size, initial_prompt=initial_prompt,
                            spelling_policy=spelling_policy,
                            device=device, transcriber=transcriber)
    stages["transcribe"] = t["run_id"]
    words_path = Path(t["dir"]) / "words.json"
    verdict.append({"name": "subtitle_coverage", "pass": not t["gaps_unfilled"],
                    "detail": {"gaps_found": len(t["speech_gaps"]),
                               "words_added": sum(g["filled"] for g in t["speech_gaps"]),
                               "suspect_spans": len(t.get("suspect_spans", [])),
                               "spans_repaired": sum(r["accepted"] for r in t.get("suspect_spans", [])),
                               "unfilled": t["gaps_unfilled"],
                               "needs_review_2_3s": t.get("gaps_needs_review", []),
                               "coverage_threshold_s": COVERAGE_GAP_S, "blocking_threshold_s": BLOCKING_GAP_S}})
    verdict.append({"name": "transcript_audit", "pass": True, "blocking": False,  # review flags, not a failure
                    "review_flags": t["audit"]["issue_count"], "detail": {"issues": t["audit"]["issue_count"], "glossary_fixes": len(t["glossary_fixes"])}})

    c = plan_and_cut(str(sl), str(words_path), approver=approver)
    stages["cut"] = c["run_id"]
    if not c["output"]:
        verdict.append({"name": "cut", "pass": False, "detail": {"truncated": c["truncated_words"]}})
        return done("awaiting_cut_approval" if not c["truncated_words"] else "qa_failed")
    verdict.append({"name": "cut", "pass": c["duration_check"]["pass"] and not c["truncated_words"],
                    "detail": {**c["plan"], "duration_check": c["duration_check"]}})

    # Internal true-peak target sits 1 dB under the -1.5 dBTP delivery target: the one AAC
    # encode in render adds ~0.8 dB. The delivered file itself is measured below (final_audio).
    a = clean_audio(c["output"], true_peak=AAC_SAFE_TP)
    stages["audio"] = a["run_id"]
    rep = a["report"]
    verdict.append({"name": "loudness", "pass": rep["pass"],
                    "detail": {"before": rep["before"]["integrated_lufs"], "after": rep["after"]["integrated_lufs"],
                               "true_peak": rep["after"]["true_peak_dbtp"]}})

    words_cut = Path(c["dir"]) / "words_cut.json"
    clean_dur = media_summary(a["output"])["duration"]
    finals = {}
    for fmt in formats:
        p = promo_clip(a["output"], str(words_cut), 0.0, min(clean_dur, max_render), fmt=fmt,
                       preset_name=preset_name, approver=approver, max_duration=max_render)
        stages[f"render_{fmt}"] = p["run_id"]
        verdict.append({"name": f"render_{fmt}", "pass": bool(p["final"]) and p["qa"]["pass"],
                        "detail": {"failed": p["qa"]["failed"], "final": bool(p["final"])}})
        if p["final"]:
            dst = wf.path(f"final_{fmt.replace(':', 'x')}.mp4")
            shutil.copy2(p["final"], dst)
            wf.add_output(dst, f"final_{fmt}")
            finals[fmt] = str(dst)
            tp = audio_mod.ensure_final_true_peak(dst, DELIVERY_TP, log=wf.path("ffmpeg.log"))
            fl = tp["measured"]
            verdict.append({"name": f"final_audio_{fmt}",
                            "pass": fl["true_peak_dbtp"] <= DELIVERY_TP and abs(fl["integrated_lufs"] - DELIVERY_LUFS) <= 1.0,
                            "detail": {"integrated_lufs": fl["integrated_lufs"], "true_peak": fl["true_peak_dbtp"],
                                       "tp_fix_passes": tp["passes"],
                                       "limits": {"true_peak_max": DELIVERY_TP, "lufs": DELIVERY_LUFS}}})
    stages["finals"] = finals
    return done("done" if len(finals) == len(formats) else "awaiting_preview_approval")


def second_opinion(words_path: str, chunks_path: str, review_csv: Optional[str] = None,
                   run: Optional[Run] = None, label: str = "nemotron") -> Dict[str, Any]:
    """Second-model hints for review (changes no words): review.csv + nemotron_hint/nemotron_agrees,
    and disagreements.json (every place the two models differ, classed)."""
    from . import second_opinion as so, review as rv
    run = run or Run()
    run.add_input(words_path, "W1")
    run.add_input(chunks_path, "SECOND_ASR")
    words = load_words(words_path)
    chunks = json.loads(Path(chunks_path).read_text(encoding="utf-8"))
    chunks = chunks["chunks"] if isinstance(chunks, dict) else chunks
    al = so.align(words, chunks)
    dis = so.disagreements(al)
    kinds = {k: sum(1 for d in dis if d["kind"] == k) for k in ("content", "spelling", "spacing", "number", "script")}
    write_json(run.path("disagreements.json"), {"label": label, "counts": kinds, "items": dis})
    run.add_output(run.path("disagreements.json"), "second_opinion")
    res: Dict[str, Any] = {"run_id": run.run_id, "dir": str(run.dir), "counts": kinds, "review_csv": None}
    if review_csv:
        rows = so.annotate_rows(rv.read_review_csv(review_csv), al, words)
        outp = so.write_csv(run.path("review_with_hints.csv"), rows)
        run.add_output(outp, "review_csv")
        res["review_csv"] = str(outp)
        res["rows"] = len(rows)
        res["rows_disagree"] = sum(1 for r in rows if r["nemotron_agrees"] == "no")
    run.log_step("second_opinion", **kinds)
    run.set_status("hints_ready")
    return res


def consensus_review(words_path: str, timed_path: Optional[str] = None, text_path: Optional[str] = None,
                     review_csv: Optional[str] = None, names_path: Optional[str] = None,
                     run: Optional[Run] = None, media: Optional[str] = None, pad_s: float = 1.5) -> Dict[str, Any]:
    """3-model consensus hints (ours + timed 2nd ASR + untimed text). Changes no words: writes consensus.csv,
    consensus.json and, with review_csv, review_consensus.csv (consensus_status / consensus_suggestion)."""
    from . import consensus as cs, second_opinion as so, review as rv
    run = run or Run()
    run.add_input(words_path, "W1")
    words = load_words(words_path)
    timed = text = None
    if timed_path:
        run.add_input(timed_path, "TIMED_ASR")
        timed = cs.timed_words(json.loads(Path(timed_path).read_text(encoding="utf-8")))
    if text_path:
        run.add_input(text_path, "TEXT_ASR")
        text = Path(text_path).read_text(encoding="utf-8")
    names_path = names_path or str(Path(__file__).resolve().parent.parent / "config" / "name_suggestions.json")
    c = cs.consensus(words, timed, text, cs.load_names(names_path))
    write_json(run.path("consensus.json"), c)
    run.add_output(run.path("consensus.json"), "consensus")
    if media:  # one mp3 clip per priority-1/2 row that no pattern already covers
        from .runs import run_ffmpeg
        cdir = run.path("clips")
        cdir.mkdir(exist_ok=True)
        for r in c["rows"]:
            r["clip"] = ""
            if r["priority"] <= 2 and not r["pattern"]:  # 0 amount, 1 disagreement, 2 name/number
                out = cdir / f"{r['id']}_{int(r['start'] // 60):02d}m{int(r['start'] % 60):02d}s.mp3"
                ss = max(0.0, r["start"] - pad_s)
                run_ffmpeg(["-ss", f"{ss:.2f}", "-t", f"{r['end'] + pad_s - ss:.2f}", "-i", media,
                            "-vn", "-ac", "1", "-b:a", "96k", str(out)])
                r["clip"] = "clips/" + out.name
    cols = ["id", "priority", "status", "kind", "pattern", "start", "end", "first", "last", "ours", "nemotron",
            "mai", "suggestion", "mai_alignment"] + (["clip"] if media else [])
    so.write_csv(run.path("consensus.csv"), [{k: r[k] for k in cols} | {"action": "", "correct_text": ""}
                                              for r in c["rows"]])
    run.add_output(run.path("consensus.csv"), "consensus_csv")
    if c["patterns"]:
        so.write_csv(run.path("consensus_patterns.csv"), [p | {"action": ""} for p in c["patterns"]])
        run.add_output(run.path("consensus_patterns.csv"), "consensus_patterns")
    res: Dict[str, Any] = {"run_id": run.run_id, "dir": str(run.dir), "counts": c["counts"],
                           "words": c["words"], "all_agree_pct": c["all_agree_pct"], "review_csv": None,
                           "note": "hints only; agreement is not truth; nothing applied"}
    if review_csv:
        rows = cs.annotate_review(rv.read_review_csv(review_csv), c, words)
        outp = so.write_csv(run.path("review_consensus.csv"), rows)
        run.add_output(outp, "review_csv")
        res["review_csv"] = str(outp)
        res["review_rows_by_status"] = {s: sum(1 for r in rows if r["consensus_status"] == s)
                                        for s in ("others_agree", "all_differ", "name_hint", "ours_majority", "format_only", "all_agree")}
    res["patterns"] = len(c["patterns"])
    res["rows_priority_1"] = sum(1 for r in c["rows"] if r["priority"] == 1)
    res["rows_amount_p0"] = sum(1 for r in c["rows"] if r["priority"] == 0)
    res["listen_rows"] = sum(1 for r in c["rows"] if r["priority"] <= 2 and not r["pattern"])
    res["pattern_rows_covered"] = sum(p["count"] for p in c["patterns"])
    run.log_step("consensus", **c["counts"])
    run.set_status("hints_ready")
    return res
