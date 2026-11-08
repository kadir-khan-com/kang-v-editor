---
title: "KANG Extended Roadmap v5.2"
subtitle: "v5.1 + review changes (2026-10-31). Ye v5.0 ko replace nahi karta."
---

## 1. v5.1 se kya badla

1. Phase 2 (Semantic Search) aur Phase 6 (Smart Matching) **merge**: dono CLIP/embedding wale kaam hain. Order ab Ingest → rule-based Matcher → CLIP.
2. **Hindi queries:** original CLIP sirf English samajhta hai. Multilingual model (M-CLIP / multilingual SigLIP) ya query-translate step zaroori. Tab tak alias table (मंदिर→temple, नागेश्वर→nageshwar…).
3. **Vector DB baad mein:** 10k assets tak numpy cosine. FAISS/Chroma/Qdrant sirf jab library 10k+ ho jaye.
4. **Ek renderer:** FFmpeg canonical renderer hai (abhi PASS). MoviePy *ya* Editly mein se sirf ek evaluate hoga (Editly = Node.js runtime extra).
5. **Premiere ke liye FCP7 XML writer hi rahega** (H-layout, 24.6.1 par PASS). OTIO sirf internal/neutral model, DaVinci jaise editors ke liye baad mein.
6. **Commands vendor-neutral:** har /kang-* = `kang.py <subcommand>`. Claude skills/plugins sirf thin wrapper; Antigravity ya koi aur agent same CLI chala sake.
7. **Baseline = v5_1 (KANG_008)**: CREDITS.txt/json package ke andar aur manifest hash mein, `visual_track` flag, relative assets_dir. Premiere evidence aate hi manifest update.
8. **Scope gate:** Shorts, talking-head, multi-format (Phase 5, 7) M3 exit ke baad: Dwarika text, sync aur rights close hone par (roadmap v2 rule).

## 2. Architecture (same as v5.1)

| Layer | Kaam | Policy |
|---|---|---|
| Core Engine | FFmpeg, ASR, asset index, timeline, renderer, QA, manifest | Stable, versioned |
| KANG Skills | kang.py subcommands: ingest, match, approve, build, premiere | Add/remove |
| Plugins | Claude skills, MCP servers, editor bridges | Optional wrappers |
| Profiles | Travel doc, talking-head, Shorts/Reels, faceless | Rules per format |
| Projects | `runs/<date>_KANG_NNN`, immutable inputs, manifest | Never overwrite |

## 3. Implementation plan (revised)

| Phase | Deliverable | Success criteria | Status |
|---|---|---|---|
| 0 Baseline lock | v5_1 package + evidence | Premiere screenshot/evidence in manifest | Premiere test chal raha hai |
| 1 Asset Ingest | `kang.py ingest` → index.json, contact sheet | 54 Dwarika assets indexed, licence per asset | **Done (2026-10-31)**, 4 tests PASS |
| 2 Rule Matcher | `kang.py match` → broll_suggestions.json | Har scene ke 3 candidates + reason; user approve | Next |
| 3 Semantic (CLIP) | multilingual embeddings, numpy cosine | Untagged library par test queries ka top-3 relevant | Evaluation |
| 4 Skills wrap | /kang-new, /kang-ingest, /kang-broll, /kang-build | Ek command se setup → preview | Proposed |
| 5 Multi-format | Shorts/Reels adapter, OTIO internal | Ek project se long-form + Shorts | M3 exit ke baad |
| 6 Talking-head | silence/filler cuts (auto-editor evaluate), retakes | Raw take se clean rough cut | M3 exit ke baad |
| 7 Plugin ecosystem | MCP servers, community plugins | Nayi capability bina core rewrite | Future |

## 4. Tools: decision rule same (isolated test → licence/security → adopt/adapt/reject)

| Tool | Phase | Note |
|---|---|---|
| Multilingual CLIP / SigLIP | 3 | GTX 1650 (4 GB) par ViT-B/32 size theek |
| MoviePy *ya* Editly | 4 | Sirf ek; FFmpeg canonical |
| ffmpeg-skill | reference | Hamara FFmpeg layer already hai; ideas lo |
| OTIO | 5 | Internal only; Premiere = FCP7 XML |
| auto-editor, openshorts, auto-subs, FunClip | 5–6 | P2 evaluation |
| OpenCut-AI | 3 | Matching reference only; cloud/paid exclude |
| Concat, pyJianYingDraft | — | Jab tak CapCut output na chahiye |
| LivePortrait, VideoReTalking, Hypit | — | Reject for now |

## 5. Data contracts

- **assets/index.json (kang.assets/1.0, implemented):** asset_id (sha256[:12]), path, type, width/height/duration, sha256, tags, description, title, author, source_url, licence, licence_url, licence_info (family, sharealike, attribution_required, commercial_ok), embedding_ref (null until Phase 3), rights_status (recorded_not_cleared / unknown).
- **broll_suggestions.json (Phase 2):** scene_id, candidates [asset_id, score, reason], approval_status.
- visuals.json, qa_report.json, manifest.json: v5.1 jaisa. schema_version/config_hash/tool_versions abhi planned.

## 6. Honest note on Phase 1 test

Dwarika ke tags file names aur briefs se bane hain, jo selection ke waqt hi likhe gaye the. Isliye "नागेश्वर मंदिर → S13" jaisi search ka sahi aana **expected hai, proof nahi**. Asli matching test Phase 3 mein bina-tag wali library par hoga.

## 7. Rights (same rule)

54 assets: 48 CC BY-SA, 3 CC BY, 2 PD, 1 CC0. Clearance alag gate hai. Options: SA assets ko contain-fit, ya CC BY/CC0/PD/apni photos se swap. `asset-search --no-sharealike` swap candidates dikhata hai. Ye legal advice nahi hai.
