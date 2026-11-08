# Creative critic: v17b → v18 (profile travel_vlog_hi, Hinglish captions SRT, audio rules deferred)

Runs: v17b original = runs/2026-11-06_KANG_001 (critic code of 2026-11-06); v17b re-check = runs/2026-11-07_KANG_012 (same v17b CSV, today's critic: card-item dedupe, R-236 off for travel_vlog_hi, KANG checks per SHOT, Q-006 added); v18 = runs/2026-11-07_KANG_011 (runs/2026-11-07_KANG_008/visuals_beats_v18.csv, package runs/2026-11-07_KANG_009).
The fair before/after is **v17b re-check → v18** (same critic code). Cells = status (number of findings). Agent-made, not human-reviewed.

| Rule | Name | v17b original | v17b re-check | v18 | v18 first finding / note |
|---|---|---|---|---|---|
| R-001 | Vaada sabse pehle | FAIL (1) | FAIL (1) | PASS (0) |  |
| R-005 | On-screen hook chhota aur alag | FAIL (1) | FAIL (1) | PASS (0) |  |
| R-011 | Proof 8 second ke andar | PASS (0) | PASS (0) | PASS (0) |  |
| R-028 | Title/thumbnail ka vaada video me sach me pura k | FAIL (1) | FAIL (1) | PASS (0) |  |
| R-031 | First-5-seconds checklist pass karo | FAIL (1) | FAIL (1) | PASS (0) |  |
| R-064 | Cold-open payoff tease — result pehle, setup baa | — | — | PASS (0) |  |
| R-091 | On-screen text ka reading-time formula | FAIL (6) | FAIL (1) | FAIL (1) | on-screen text 13 shabd, 4.32s dikhta hai — kam se kam 4.8s chahiye (formula) |
| R-112 | Text overlay jaldi + har number/naam screen par | FAIL (1) | FAIL (1) | PASS (0) |  |
| R-157 | Visual floor = perceived motion, cut count nahi | PASS (0) | PASS (0) | PASS (0) |  |
| R-158 | Hook/fast sections me visual change har 3–5s | — | — | PASS (0) |  |
| R-160 | Section ke hisaab se pace badlo | FAIL (1) | FAIL (1) | FAIL (1) | 522.28-529.36s tak 7.08s koi visual change nahi — hadd 5s (ORDER #2) |
| R-166 | Long-form B-roll/screen-share cadence (CraigHewi | PASS (0) | PASS (0) | PASS (0) |  |
| R-180 | Hook ki lambai 9-24 shabd | — | — | FAIL (1) | hook 7 shabd — band 9-24 (ORDER #17) |
| R-221 | Jump cut: dead air hatao, pace tez karo | — | — | PASS (0) |  |
| R-236 | Shorts overlay — dusra hook, 5-7 shabd | FAIL (1) | — | — |  |
| R-338 | Lambai ka ratio — sabse lamba shot sabse chhote  | FAIL (1) | FAIL (1) | FAIL (1) | sabse lamba / sabse chhota shot (beats proxy) ratio 9.3 — band 2-4 |
| R-359 | Opening: 40s me vaada, 60s me saboot | PASS (0) | PASS (0) | PASS (0) |  |
| R-400 | Hook me dead air = retention ki maut | FAIL (1) | FAIL (1) | PASS (0) |  |
| G-004 | Narrated still hold 3-10 s | FAIL (12) | FAIL (11) | PASS (0) | per shot; teaser exempt |
| G-006 | Max 2 same camera moves in a row | PASS (0) | PASS (0) | PASS (0) | per shot |
| G-008 | Parallax not back to back | FAIL (3) | PASS (0) | PASS (0) | per shot |
| G-013 | Caption speed <= 22 cps (Hindi/Hinglish) | FAIL (16) | FAIL (16) | FAIL (16) | 1.89s: 23.1 cps 'kaise hain aap sabhi,' |
| Q-001 | Narrated shot <= ~7 s (WARN level) | PASS (0) | WARN (2) | WARN (2) | S17_b03: shot 10.04s > 7 |
| Q-002 | Same shot length not 3x in a row | PASS (0) | PASS (0) | PASS (0) | per shot; teaser exempt |
| Q-006 | Accent budget (parallax/AI <= ~1 per 3 cuts) | — | FAIL (1) | PASS (0) | 15 accent shots; KANG proxy: accents >= 3 shots apart |
| S-004 | Caption on screen 0.83-7 s | FAIL (95) | FAIL (95) | FAIL (95) | 1.89s: 0.78s |
| S-021 | Narration WPM hard limits 115-230 | PASS (0) | PASS (0) | PASS (0) | measured 196.7 WPM |

| Summary | v17b original | v17b re-check | v18 |
|---|---|---|---|
| engine evaluated | 14 | 13 | 17 |
| engine passed | 4 | 4 | 13 |
| engine failed | 10 | 9 | 4 |
| engine skipped | 107 | 107 | 103 |
| engine findings_count | 15 | 9 | 4 |
| engine overall_score_pct | 28.6 | 30.8 | 76.5 |
| KANG stat beats | 137 | 137 | 137 |
| KANG stat avg_shot_s | 5.05 | 5.05 | 5.05 |
| KANG stat min_shot_s | 2.52 | 2.52 | 2.08 |
| KANG stat max_shot_s | 19.44 | 19.44 | 19.44 |
| KANG stat visual_changes_first_30s | 8 | 8 | 7 |
| KANG checks passed | 4/8 | 4/9 | 6/9 |

## What changed and why (v18 = picture desk run 2026-11-07_KANG_007 + cold open 2026-11-07_KANG_008)
- **Cold open (hook)**: 0–6.32 s = 4 teaser shots (Setu drone day, Setu night lasers, Dwarkadhish spire, S16_b06 AI flag) + Hinglish title overlay "DWARKA · GUJARAT / Shri Krishna ki nagri" from 0.3 s, over the unchanged greeting narration. Fixes R-001, R-028, R-031, R-400 (hook at 0 s, no dead air), R-112 (first text 0.3 s, was 57.5 s), R-005 (7-word on-screen hook), R-064 (tease 6.32 s inside 3–8 s). S01_b01 (exact S01_1 still) and S01_b02 (representative photo) left the timeline; S01_b03 (S01_2 temple parallax) starts at 6.32 s, on "bhagwan Shri Krishna ki nagri".
- **Picture desk**: G-004 11 short stills fixed by moving 11 cuts to other word onsets − 0.2 s (lead rule), 0 merges, 0 unresolved; G-008 the 3 continued_with_motion holds are one shot each (parallax clip covers it); Q-006 S03_b06 parallax → Ken Burns; Q-002 respected (4 cut choices skipped the smallest shift because it made 3 equal-length shots).
- **Critic changes (2026-11-07)**: card items deduped per (clip, shown_text) (S03_b05 14 → 10 tokens); R-236 off for travel_vlog_hi (Shorts only); KANG checks G-004/G-006/G-008/Q-001/Q-002 measured per SHOT (same-asset beats merged, as the package does) — that alone clears G-008 on v17b (the 3 findings were same-photo holds) and makes Q-001 show 2 WARNs that per-beat hid; Q-006 added (accents ≥ 3 shots apart); teaser rows → one hook beat (tease, overlay); card_values.csv found via the card clips' source_dir when the CSV lives in a later run.

## Still failing (not in this task's scope / honest)
- R-180 hook 7 words vs band 9–24: the engine counts the hook's on-screen title; the spoken opening is a greeting. Not gamed.
- R-091 S08_b04 card: 13 words on screen for 4.32 s (formula wants 4.8 s) — card timing is narration-bound; unchanged.
- R-160 S17 Setu clip 10.04 s without a visual change (also Q-001 WARN) and Q-001 S18_b05 parallax hold 8.12 s — needs a second clip/cut; not done.
- R-338 longest/shortest ratio 9.3 (beats proxy; CARD_C11 19.44 s hold vs the 2.08 s S01_b02 beat that is now part of the S01_b03 shot).
- G-013 (16) / S-004 (95): caption timing — captions unchanged by instruction.
- KANG stat "visual changes first 30 s" 8 → 7 is a counting artefact (the 4 teaser shots are one hook beat); real cuts in the first 30 s went up by 2.
