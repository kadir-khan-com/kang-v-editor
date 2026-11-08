# Editor-tool repos for KANG (AE / Premiere / Resolve / CapCut) — tools + knowledge

Checked: 2026-11-06 IST. Scope: the 35 repos on the package's editor-round priority list (`incoming/creative_layer_2026-11-06_v2/step_1_harvest_gyaan/`), plus 11 new ones the package missed.
Machine-readable: `editor_tool_repos.json` (46 rows) and `editor_tool_rules_proposed.json` (**33 proposed rules, T-001…T-033**).

**How I checked**
- **Stars and forks:** read from each repo page (the GitHub API had hit its rate limit).
- **Last commit:** the HEAD date of a shallow clone.
- **Licence:** I read the root LICENSE in the clone, plus any nested licence files.
- **Knowledge:** I grepped every markdown/skill file for numbers about timing, easing, captions, audio, colour and export, then read the relevant sections in full.
- **De-duplication:** I checked every candidate against the package's 463 R-rules and our G/S/Q rules (`config/creative_rulebook_kang.json`). Overlaps appear as `confirms` instead of new rules.
- **Already harvested:** for the MIT repos the package already turned into R-rules, I did not re-extract their knowledge. They are marked "already harvested" with the R-ids they back.

## 1. Findings that change the plan

1. **CapCut is not a path for this user.** CapCut has been blocked in India since 2020 and was still blocked when checked on 29 Oct 2026 (not on the Indian Play Store or App Store, and capcut.com does not load; https://comparecrest.com/capcut-alternatives-india/).
   - Every CapCut/JianYing draft tool gets **c (skip) as code**: pyJianYingDraft, pyCapCut, capcut-cli, capcut-mate, VectCutAPI and cutcli.
   - Their recipes are still used as **ideas**.
   - pyJianYingDraft targets JianYing (the China edition), and newer JianYing drafts are encrypted.
2. **Premiere 24.6.1 has no UXP.** UXP plugins start at Premiere 25.6 (https://developer.adobe.com/premiere-pro/uxp/introduction/).
   - Only CEP/ExtendScript works on the user's version. Adobe plans to disable CEP panels by default in Dec 2028 (https://developer.adobe.com/uxp/migration-center/).
   - The CEP MCPs (hetpatel-11 and leancoderkavy, both MIT, "Premiere 2020+") can drive 24.6. They can add **MOGRT titles with text fields, markers and captions** after KANG's xmeml is imported.
   - This is the one thing FCP7 XML cannot carry well (titles/graphics). **It adds to FCP7 XML; it does not replace it.** The xmeml stays the core because it needs no install and opens in Premiere and Resolve. A CEP step would need the user to install a panel and keep Premiere open.
3. **After Effects (user has 24.6): nexrender (MIT, 1.9k★) is the most practical AE automation.**
   - It renders JSON jobs against **.aep templates through aerender**, with no AE window open.
   - KANG could fill AE-designed chapter/title/map cards automatically.
   - **Cost:** someone has to design the templates once, and aerender is heavy on 8 GB RAM. Better suited to short cards than whole videos.
   - The AE MCP servers (Dakkshin, ishu86 and forks) need AE open with a panel, so they suit interactive work, not KANG's batch run.
4. **DaVinci Resolve: no free headless path.**
   - External scripting is Studio-only.
   - The free edition can only be driven through a script started inside Resolve (Workspace ▸ Scripts). samuelgursky's docs say this was measured on 21.0.x only.
   - Resolve is not on the user's PC. FCP7 XML already imports into Resolve, so nothing changes.
5. **OTIO FCP7 adapter (Apache-2.0):** use it as a validator.
   - It can re-parse KANG's xmeml and emit EDL/OTIO.
   - It is not a replacement writer: its feature matrix shows **no transitions**.
6. **Engine-report design (T-015).** samuelgursky's Rule-of-Six audit refuses to give one composite score, because the measurable criteria are only ~26% of Murch's weights.
   - Our step_4 engine prints a single % (Dwarika 36.4%). Proposal: show per-layer pass/fail plus a coverage line instead.
7. **Package errors:**
   - **NandhaKishorM/laya** is not a video tool (it is a multilingual decision engine).
   - **tamedpanda/CapCutAPI** and **cooperka/capcut-export** return 404.
   - **pyCapCut** has no LICENSE file.
   - **fancyboi999/capcut-mcp**, **luhailiang98/CapCutAPI-YYZC** and **yanghoxom/capcut-project-exporter** have no licence.
   - **LobzyJay** has been renamed to `motion-design-with-claude-and-codex`.

## 2. Top 3 picks

| # | Pick | Why |
|---|---|---|
| 1 | **scriptituk/xfade-easing** (MIT) | Plugs straight into KANG's FFmpeg renderer, CPU only, with no app or install beyond FFmpeg. It gives eased transitions on stock FFmpeg (custom expressions, T-032). Lowest risk and immediate visible gain. |
| 2 | **hetpatel-11/Adobe_Premiere_Pro_MCP** (MIT, 824★) — or leancoderkavy/premiere-pro-mcp (MIT) | The only realistic way to put real **MOGRT titles/captions/markers** into the user's Premiere 24.6 sequence after the xmeml import. Optional opt-in step, needs the CEP panel installed. leancoderkavy also documents interchange loss for FCP7 xmeml. |
| 3 | **inlife/nexrender** (MIT, 1.9k★) | Batch-renders AE templates the user already has the app for, with no GUI. It turns "AE-quality" title, map and chapter cards into data. Needs one-time template design. |

**Knowledge winners (ideas, not code):**
- **ronak-create/FableCut** (MIT): 12 T-rules.
- **samuelgursky/davinci-resolve-mcp** (MIT): 8 T-rules covering audit design, handles, sound density and split edits.
- **juliang8507/cli-anything-capcut** (MIT): anti-"AI slop" list and colour recipes.
- **renezander030/capcut-cli** (MIT): Ken Burns, the unfinished-pan ending and animation-length defaults.

**Also usable as a tool:** **bradautomates/claude-video** (MIT) can let an agent "watch" KANG renders as frames plus transcript for QA.

## 3. Licence summary (46 repos)
- **OK (MIT / Apache-2.0; chvndler's README says ISC but its LICENSE file is MIT): 35.** Includes laya, which is off-topic.
- **IDEA_ONLY: 9.**
  - No licence: dvschultz, AdamGarceau, pyCapCut, fancyboi999, luhailiang98, yanghoxom, Qwen-Video-Edit (only vendored licences).
  - No licence, fork of a non-commercial project: eacp1991 (PolyForm NC family).
  - GPL-3.0: pymiere.
- **Gone (404): 2.**
- **IDEA_ONLY rules (written fully in own words, nothing copied):** T-018, T-019, T-020 (all from AdamGarceau).

## 4. Proposed T-rules — overview (details in JSON)
- **33 rules.** Evidence is 🟠 for all, since every source is a tool or skill document, not an official spec or study.
- **Two plan-level rules:**
  - T-015: critic design, no single score.
  - T-016: a cutaway never straddles a beat. This can be checked directly on the visuals_beats CSV.
- **Directly machine-checkable with what KANG already has:** T-002 and T-003 (luma/cast via FFmpeg signalstats), T-004, T-010, T-011, T-016, T-017, T-030.
- **Conflicts flagged inside the rules:**
  - T-009 vs R-304: motion blur on every layer.
  - T-022 vs R-422: dissolve share 5% vs 30%.
  - T-023 vs R-266: LUT intensity.
  - T-025 vs G-002/G-005: pull-out amplitude, and linear Ken Burns.
  - T-007: FableCut contradicts itself on fonts.
  - VectCut's 9:16 caption y 75–80% vs **G-010** (the official Shorts UI zone). G-010 should win.
- **Confirmations only (no new rule written):**
  - FableCut pop 0→1.12→1 ≈ R-326.
  - editly Ken Burns zoom 0.1 / clip 4 s ≈ G-002/G-004.
  - VectCut ducking 7.5–10 dB ≈ R-103.
  - AdamGarceau 2-frame 0 dB crossfade ≈ R-269.
  - cli-anything-capcut SFX ≤1 per 5 cuts ≈ R-222.
  - mrbuslov gaps >1 s cut ≈ R-162.
  - FableCut speed ramp into drop ≈ R-418.
  - cutcli highlighted keyword per line ≈ R-378.

## 5. Tool verdict table

Columns: repo · editor · ★ · last commit · licence → verdict · what it is · Windows/CPU fit · KANG use (a = code via thin adapter, b = ideas/numbers, c = skip) · T-rules · risks

| Repo | Editor | ★ | Last commit | Licence → verdict | What | Win/CPU fit | KANG use | T-rules | Risks |
|---|---|---|---|---|---|---|---|---|---|
| [ishu86/after-effects-mcp](https://github.com/ishu86/after-effects-mcp) | AE | 46 | 2026-10-08 | MIT → **OK** | MCP server (70+ tools) driving AE via a bridge panel: comps, text, keyframes, expressions, lower-third/title presets; ships a Claude skill. | Windows OK; AE must be open with panel | b (already harvested → R-rules); a only if we later automate AE live | — | Needs AE running + panel; user must run it; small (46★). |
| [justajazz/ae-mcp-bridge](https://github.com/justajazz/ae-mcp-bridge) | AE | 1 | 2026-10-09 | MIT (ports Dakkshin, MIT) → **OK** | Small AE MCP bridge fork. | Windows OK | c | — | 1★, tiny; prefer upstream Dakkshin. |
| [aedev-tools/adobe-agent-skills](https://github.com/aedev-tools/adobe-agent-skills) | AE/Pr | 116 | 2026-03-02 | Apache-2.0 → **OK** | Agent skills for AE/Premiere scripting (ExtendScript API knowledge). | n/a (docs) | b (already harvested) | — | Last commit 2026-03; API notes, not craft. |
| [chvndler/aeft.jsx](https://github.com/chvndler/aeft.jsx) | AE | 4 | 2026-07-27 | MIT (README says ISC; LICENSE file MIT) → **OK** | ExtendScript helper library for AE. | Windows OK | c | — | 4★. |
| [yumehiko/ae-agent-skills](https://github.com/yumehiko/ae-agent-skills) | AE | 38 | 2026-08-13 | MIT → **OK** | Declarative JSON→AE scene CLI + skills (Japanese). Safe margins action 10% / title 20%; ease = [speed, influence 0.1–100]. | Windows OK, needs AE | c for now; a later if KANG emits AE scenes | — | Schema is author-specific. |
| [iart-ai/motion-design-skills](https://github.com/iart-ai/motion-design-skills) | AE/web | 201 | 2026-06-22 | MIT → **OK** | Motion-design principles skills (easing curves, stagger, overshoot expressions). | docs | b (already harvested; numbers in R-3xx) | — | - |
| [LobzyJay/motion-design-with-claude (renamed …-and-codex)](https://github.com/LobzyJay/motion-design-with-claude) | AE | 37 | 2026-09-23 | MIT → **OK** | AE motion skills incl. expression references (inertial bounce etc.). | docs | b (already harvested) | — | Repo renamed (redirect works). |
| [SebastianBoehler/autoresearch_after_effects_finetune](https://github.com/SebastianBoehler/autoresearch_after_effects_finetune) | AE | 0 | 2026-06-11 | MIT → **OK** | Experiment to fine-tune a model on AE motion; includes motion-piece rules. | docs | b (already harvested) | — | 0★. |
| [dvschultz/adobe-hut](https://github.com/dvschultz/adobe-hut) | AE/Pr | 24 | 2026-07-12 | NONE → **IDEA_ONLY** | ~50 skill files of UXP/ExtendScript API reference + agents. | docs | b ideas only (API facts); notes_ file exists | — | No licence: no copying. |
| [koptsev63/premiere-claude-bridge](https://github.com/koptsev63/premiere-claude-bridge) | Pr | 2 | 2026-11-05 | MIT → **OK** | Premiere bridge + skills (end cards, room tone under black, watch skill). | Windows OK, CEP | b (already harvested) | — | 2★; one sub-skill self-labelled paid pack (MIT in repo). |
| [ZeusSheen/ppro-agent-bridge](https://github.com/ZeusSheen/ppro-agent-bridge) | Pr | 2 | 2026-11-03 | MIT → **OK** | Experimental Premiere agent bridge. | Windows OK | b (already harvested) | — | Experimental, 2★. |
| [leancoderkavy/premiere-pro-mcp](https://github.com/leancoderkavy/premiere-pro-mcp) | Pr | 489 | 2026-11-05 | MIT → **OK** | Large Premiere MCP (CEP + UXP), interchange loss reports (OTIO/FCP7 xmeml/EDL/AAF), caption timing previews, music-remix plans. | Windows OK; CEP works on Pr 24.6 (UXP needs 25.6+) | a (optional post-import automation) + b | T-010 | CEP panel install (unsigned/debug); CEP support planned to end ~Dec 2028; host validation 'not_run' per its own docs. |
| [hetpatel-11/Adobe_Premiere_Pro_MCP](https://github.com/hetpatel-11/Adobe_Premiere_Pro_MCP) | Pr | 824 | 2026-10-24 | MIT → **OK** | Most-starred Premiere MCP (283 tools via search_tools/invoke_tool); CEP bridge; MOGRT import + text fields, captions, markers, export. | Windows OK; Premiere 2020+ (CEP) → fits 24.6.1 | a (optional): post-import step to drop MOGRT titles/markers into KANG's sequence | — | Needs CEP panel install + Node; agent-driven (user must run Premiere); design still depends on real MOGRT files. |
| [vamshicreates/premiere-editing-dna](https://github.com/vamshicreates/premiere-editing-dna) | Pr | 0 | 2026-09-29 | MIT → **OK** | Measure an editor's 'DNA' (ASL, cuts/min) from past edits. | Python | b (already harvested) | — | 0★. |
| [eacp1991/premiere-agent](https://github.com/eacp1991/premiere-agent) | Pr | 0 | 2026-07-07 | NONE (fork of Kemerd/premiere-agent = PolyForm NC) → **IDEA_ONLY** | Large Premiere agent SKILL (pacing presets, word-boundary cuts). | Windows OK | b ideas only; notes_ file exists | — | NC licence family. |
| [ChaiWithJai/davinci-resolve-claude-skills](https://github.com/ChaiWithJai/davinci-resolve-claude-skills) | Resolve | 32 | 2026-05-17 | MIT → **OK** | Resolve craft skills built from BMD training PDFs (audio chain, skin saturation, crossfades). | docs | b (already harvested) | — | 2 commits. |
| [samuelgursky/davinci-resolve-mcp](https://github.com/samuelgursky/davinci-resolve-mcp) | Resolve | 3953 | 2026-11-04 | MIT → **OK** | Most-starred Resolve MCP (3.9k★): full scripting API + audits (rule of six, split edits, sound density, handles, pre-balance, beat cuts, B-roll placement). Free edition reachable only via in-app Workspace▸Scripts bridge (external scripting is Studio-only). | Windows OK; Resolve not installed on user PC | b (strong ideas); a only if user installs Resolve | T-003, T-011, T-012, T-013, T-014, T-015, T-016, T-017 | Free-edition bridge stated as measured on 21.0.x only. |
| [AdamGarceau/resolve-toolkit](https://github.com/AdamGarceau/resolve-toolkit) | Resolve | 1 | 2026-08-31 | NONE → **IDEA_ONLY** | Resolve+Claude skills: perfect-cuts, tighten profiles, punch-in, VO finish, snap captions, Fusion title pack. | macOS paths | b ideas only (own words) | T-018, T-019, T-020 | No licence; macOS-centric. |
| [tashisleepy/capcut-ai-director](https://github.com/tashisleepy/capcut-ai-director) | CapCut | 3 | 2026-04-04 | MIT → **OK** | CapCut 'director' knowledge (beat drops, speed ramps, endings). | docs | b (already harvested) | — | CapCut blocked in India. |
| [GuanYixuan/pyJianYingDraft](https://github.com/GuanYixuan/pyJianYingDraft) | CapCut/JianYing | 4815 | 2026-10-14 | Apache-2.0 → **OK (code)** | Python draft generator for JianYing (China CapCut) — 4.8k★. | Windows OK; CPU | c for KANG | — | JianYing ≠ CapCut; newer JianYing drafts encrypted; CapCut blocked in India. |
| [GuanYixuan/pyCapCut](https://github.com/GuanYixuan/pyCapCut) | CapCut | 735 | 2026-10-16 | NO LICENSE FILE → **IDEA_ONLY** | CapCut-flavoured sibling of pyJianYingDraft (735★); export must be manual in CapCut. | Windows OK | c | — | No licence + CapCut blocked in India. |
| [notinmood/JianyingDraft.PY](https://github.com/notinmood/JianyingDraft.PY) | JianYing | 213 | 2024-05-11 | MIT → **OK** | Older JianYing draft writer (last commit 2024-05). | Windows | c | — | Stale; format drift. |
| [tamedpanda/CapCutAPI](https://github.com/tamedpanda/CapCutAPI) | CapCut | — | CLONE_FAIL | — → **GONE (HTTP 404)** | — | — | c | — | Repo not found 2026-11-06. |
| [luhailiang98/CapCutAPI-YYZC](https://github.com/luhailiang98/CapCutAPI-YYZC) | CapCut | 32 | 2025-09-11 | NONE → **IDEA_ONLY** | FastAPI+Redis CapCut/JianYing service with Windows UI automation. | Windows | c | — | No licence. |
| [fancyboi999/capcut-mcp](https://github.com/fancyboi999/capcut-mcp) | CapCut | 96 | 2025-08-21 | NONE (README only) → **IDEA_ONLY** | CapCutAPI fork (HTTP API to build drafts); last commit 2025-08. | Python | c | — | No licence; stale. |
| [renezander030/capcut-cli](https://github.com/renezander030/capcut-cli) | CapCut/JianYing | 1115 | 2026-11-04 | MIT → **OK** | Zero-dep Node CLI editing local CapCut/JianYing drafts (1.1k★); recipes for Ken Burns, unfinished pan, intro/outro animation catalogue, retake detection. | Windows OK | b (recipes); code c | T-025, T-026, T-027 | CapCut blocked in India. |
| [cooperka/capcut-export](https://github.com/cooperka/capcut-export) | CapCut | — | CLONE_FAIL | — → **GONE (HTTP 404)** | — | — | c | — | Not found; similar: emosheeep/capcut-export (not checked). |
| [yanghoxom/capcut-project-exporter](https://github.com/yanghoxom/capcut-project-exporter) | CapCut | 9 | 2026-05-28 | NONE → **IDEA_ONLY** | Go GUI batch-exporting CapCut draft segments to MP4 via FFmpeg (NVENC). | Windows | c | — | No licence. |
| [juliang8507/cli-anything-capcut](https://github.com/juliang8507/cli-anything-capcut) | CapCut | 7 | 2026-09-21 | MIT → **OK** | Windows-only CLI over pyCapCut (50+ commands, --json); Korean skill with anti-'AI slop' checklist and colour mood recipes. | Windows only | b (checklist numbers) | T-007, T-021, T-022, T-023, T-024 | Built on unlicensed pyCapCut; CapCut blocked in India. |
| [mrbuslov/capcut-ai-editor](https://github.com/mrbuslov/capcut-ai-editor) | CapCut | 123 | 2026-10-27 | MIT → **OK** | MCP that cuts silences (>1 s gaps between CapCut auto-captions) and duplicate takes (keeps last). | Python | c | — | CapCut blocked in India. |
| [xuliang2024/cutcli-cookbook](https://github.com/xuliang2024/cutcli-cookbook) | CapCut/JianYing | 201 | 2026-05-26 | MIT → **OK** | Cookbook/templates/prompts for the cutcli draft CLI (cutcli itself is a separate closed tool + cloud render). | bash examples | b (template ideas) | T-007, T-010, T-025, T-028, T-029 | cutcli binary not open source; cloud render. |
| [junwen853/travel-video-studio-skill](https://github.com/junwen853/travel-video-studio-skill) | generic | 2 | 2026-08-09 | MIT → **OK** | Actively released travel-video skill (route honesty, transition budgets, scenic audio). | docs | b (already harvested; most KANG-relevant) | — | 2★ but 200+ releases. |
| [NandhaKishorM/laya](https://github.com/NandhaKishorM/laya) | — | 35069 | 2026-11-06 | Apache-2.0 → **OK but OFF-TOPIC** | Multilingual 'System 1' decision/classification engine (35k★) — not a video tool. | Python | c | — | Mislisted in package. |
| [ronak-create/FableCut](https://github.com/ronak-create/FableCut) | generic NLE | 780 | 2026-10-30 | MIT → **OK** | Browser NLE whose timeline is one JSON file; MCP/REST; captions, auto-duck, silence cut, scopes, beat retime, export presets, motion-graphics skill (780★). | Node, zero deps; Windows OK; CPU | b (richest new knowledge); a optional preview/edit UI for KANG output | T-001, T-002, T-003, T-004, T-005, T-006, T-007, T-008, T-009, T-017, T-031, T-033 | Sponsored README; young project. |
| [bradautomates/claude-video](https://github.com/bradautomates/claude-video) | generic | 19950 | 2026-09-25 | MIT → **OK** | '/watch' skill: URL/local video → timestamped frames (≤2 fps cap, near-duplicate dedupe) + transcript for an agent (19.9k★). | Python+ffmpeg; Windows OK | a (QA: let an agent look at KANG renders) | — | Cloud ASR optional; for Hindi prefer local. |
| [yunpeng1998/Qwen-Video-Edit](https://github.com/yunpeng1998/Qwen-Video-Edit) | model | 131 | 2026-09-01 | NO OWN LICENSE (vendored deps only) → **IDEA_ONLY** | Instruction-based video editing model (diffusion). | needs big GPU | c | — | Heavy model; out of scope. |
| [inlife/nexrender](https://github.com/inlife/nexrender) | AE | 1862 | 2026-06-03 | MIT → **OK** | Data-driven AE template rendering via aerender from JSON jobs (1.9k★); replaces text/images/audio in .aep templates; no AE GUI. | Windows OK; needs AE installed (user has 24.6) | a (best AE path): render title/map/chapter cards from AE templates headlessly | — | Templates must be designed by a human; aerender is heavy on 8 GB RAM; AE 2023+ needs explicit output module. |
| [OpenTimelineIO/otio-fcp-adapter](https://github.com/OpenTimelineIO/otio-fcp-adapter) | interchange | 11 | 2026-04-08 | Apache-2.0 → **OK** | Official OTIO adapter reading/writing FCP7 XML (Premiere's interchange). No transitions support. | Python, CPU | a (validator: re-read KANG xmeml, emit EDL/OTIO) | — | Writer drops transitions/effects → keep KANG's own xmeml writer. |
| [scriptituk/xfade-easing](https://github.com/scriptituk/xfade-easing) | FFmpeg | 126 | 2026-09-09 | MIT → **OK** | Easing curves + ported GL transitions for FFmpeg xfade, usable as plain expressions on stock FFmpeg. | CPU, Windows OK | a (drop into KANG renderer) | T-032 | Expression mode slower than custom build; avoid back/elastic. |
| [mifi/editly](https://github.com/mifi/editly) | FFmpeg | 5583 | 2025-02-20 | MIT → **OK** | Declarative Node/FFmpeg editor (5.6k★); Ken Burns default zoom 0.1, transition 0.5 s, clip 4 s. | Node + headless-gl (painful on Windows) | b (defaults confirm G-002/G-004) | T-010 | Last commit 2025-02. |
| [sun-guannan/VectCutAPI](https://github.com/sun-guannan/VectCutAPI) | CapCut/JianYing | 2361 | 2026-10-24 | Apache-2.0 (vectcut-skill/ MIT) → **OK** | CapCut/JianYing draft API + MCP (2.4k★) with 'capcut-director' skill (9:16 type scale, safe zones, ducking). | Python; Windows OK | b | T-005, T-029, T-030, T-031, T-033 | CapCut blocked in India; its 9:16 caption y 75–80% conflicts with G-010. |
| [Hommy-master/capcut-mate](https://github.com/Hommy-master/capcut-mate) | CapCut/JianYing | 2106 | 2026-11-01 | Apache-2.0 → **OK** | FastAPI service generating JianYing/CapCut drafts (2.1k★); cloud render only for JianYing. | Python 3.11; Windows OK | c | — | CapCut blocked in India. |
| [mikechambers/adb-mcp](https://github.com/mikechambers/adb-mcp) | Pr/PS/ID | 739 | 2026-07-08 | MIT → **OK** | Adobe dev's MCP for Photoshop/Premiere/InDesign via UXP (739★). | Windows OK | c (user's Pr 24.6 has no UXP) | T-010 | Not usable until Premiere ≥25.6. |
| [Dakkshin/after-effects-mcp](https://github.com/Dakkshin/after-effects-mcp) | AE | 854 | 2026-04-01 | MIT → **OK** | Original popular AE MCP (854★) that many forks build on. | Windows OK; AE open | c (nexrender better for batch) | — | Last commit 2026-04. |
| [qmasingarbe/pymiere](https://github.com/qmasingarbe/pymiere) | Pr | 474 | 2025-03-05 | GPL-3.0 → **IDEA_ONLY** | Python↔Premiere via ExtendScript link panel; unmaintained. | Windows OK | c | — | GPL + unmaintained; its own README says use XML/OTIO to just create a timeline. |
| [mateo-khalil/davinci-resolve-mcp](https://github.com/mateo-khalil/davinci-resolve-mcp) | Resolve | 0 | 2026-06-19 | MIT → **OK** | Free-edition Resolve MCP via Lua file bridge inside Resolve. | Windows OK | c (Resolve not installed) | — | 0★. |

## 6. Not done / limits
- **No live API metadata.** The GitHub API was rate-limited, so archived flags and API `pushed_at` are missing. Star counts are from the repo pages, last-commit dates from the clones.
- **Harvested repos not re-mined.** I did not re-read the MIT repos the package already harvested line by line. Their knowledge is in R-rules already. I only read the 20+ repos that were never harvested, plus FableCut's full CLAUDE.md sections (Captions, Audio mix, Color, Recipes, Export).
- **FFmpeg mapping still needed.** The colour recipe numbers (T-024) are on CapCut's −1..+1 slider scale and must be calibrated to FFmpeg eq/colortemperature on test frames.
- **Nothing installed.** No models or apps were installed. The clones were shallow, in work/, and deleted afterwards.
