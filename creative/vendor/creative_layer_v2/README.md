# Creative Layer — Rules Engine (User ka plan, 2026-11-05)

Video editing automation ki missing "creative layer": techniques ko RULES bana ke ek Python
rules engine (Claude nahi) har beat par lagayega, aur ek critic har rule ko score dega.

## Folders (ek step = ek folder)

- `step_1_harvest_gyaan/` — Gyaan jama: har source (GitHub repo/skill ya science) ki EK file,
  file ka naam = source ka naam, andar us source se nikala hua PURA usable data
  (techniques, numbers, thresholds, checklists). Sirf MIT/Apache sources ka content
  istemal ke liye nikala jata hai; licence-bina/AGPL/GPL wale sirf index file me note hain.
- `step_2_rules/` — Har technique ka RULE roop: kab lagana hai, kya karna hai, kyun,
  kitni baar, aur saboot ka tag: 🟢 research se sabit / 🟡 measured study / 🟠 sirf editor ki raay.
- `step_3_order/` — Takraav ka order (asli brain): Kahani > Samajh aana > Rhythm > Style/Effect.
  Khula design point: Murch Emotion ko Kahani se upar rakhta hai (51%); user ke plan me
  emotion engine se bahar hai (insaan ki aankh). Is step me ye faisla saaf hoga.
- `step_4_worker_critic/` — Python rules engine (worker: har beat par rule lagaye;
  critic: har rule ka score de) + uske tests.

## Seema (user ke shabdon me)
Rules ye nahi bata sakte ki photo sundar hai ya emotion sahi hai.
Wo insaan ki aankh ka kaam hai.

## Status
- Step 1: extraction PURA (2026-11-05 raat). step_1_harvest_gyaan/ me 20 files, ~1.1 MB:
  15 GitHub source files (sab MIT, ExpoCut ⚠️ attribution note ke saath; pifferologo repo
  GitHub par 404 hai — mirror se extraction, gap file me likha hai), 4 science files,
  1 licence-index file. Pehle ke saransh: ~/workspace/research_notes/creative-harvest-*.md
  (note: creative-harvest-github.md disk par adhoora/truncated save hai — asal record ab
  step_1 ki per-source files hain).
- Step 2: PURA (2026-11-06). step_2_rules/ me rules.json + MASTER_RULES.md — **261 rules**
  (Kahani 86 · Samajh 47 · Rhythm 66 · Style 62; evidence 🟢 10 · 🟡 52 · 🟠 199;
  83 machine-checkable) + CONFLICTS.md (24 takraav-vishay).
- Step 3: PURA. step_3_order/ORDER.md — meta-niyam, emotion ka kendriya faisla
  (engine ke bahar, insaan ka veto, engine sirf flag), 24 takraavon ke faisle, 5 profiles.
- Step 4: PURA. step_4_worker_critic/ me engine.py (stdlib Python worker+critic),
  profiles.json, test_engine.py (**16/16 tests PASS**), demo/ (long 79.3%, shorts 87.1%).
- Editor round (2026-11-06 subah): After Effects / Premiere Pro / DaVinci Resolve / CapCut ke
  tool-specific sources — step_1 ab **49 files** hai (21 naye extraction + 8 apne-shabdon wale
  notes + INDEX addendum); editor-wise sar neeche wale paragraph me hai.
- Round 2 MERGE + ENGINE UPDATE + ASLI TEST (2026-11-06): editor-round ke sources se D1+D2
  clusters ne 202 naye rules banaye; unified kul ab **463 rules** (Kahani 113 · Samajh 79 ·
  Rhythm 121 · Style 150; 🟢 10 · 🟡 55 · 🟠 398; **153 machine-checkable**). ORDER_ADDENDUM.md
  me 14 naye takraavon ke faisle; engine update — 7 profiles, tests **31/31 PASS**, demo dobara
  (long 76.5% · shorts 87.2%; purane verdicts unchanged). **Pehli ASLI pariksha:** beats_converter.py
  se Dwarika (Member 2 wala asal dharmik content, 692.35 s, 7 scenes) ki beats file bani aur engine
  chala — 11 rules evaluate hue, score 36.4% (7 fail: 5 hook-pariwaar — scene-plan me hook label hi
  nahi hota; first-30s changes sirf 1 — scene-level data ki granularity; WPM 200.1 vs English band
  160–195 — ye ekmatra pakki, data-paki khoj). 143 rules data na hone se skip; **human flags 0** —
  engine ki flag keywords English hain, Hindi text par andhe (khoj gayi asli kami). Report:
  step_4_worker_critic/demo/dwarika_beats.report.md + DWARIKA_DATA_NOTES.md.
  notes licence-bahar wale sources ke liye — user ki nayi policy: seekh sabse, text-copy sirf
  MIT/Apache ki; notes_* files me disclaimer ke saath apni bhasha me sar). Khaas finding:
  Premiere ki dedicated craft-skill lagbhag exist nahi karti (zyada tar MCP/tool servers);
  AE motion-design sabse ameer; CapCut craft patli, tooling bhaari.
