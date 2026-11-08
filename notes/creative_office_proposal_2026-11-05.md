# Creative Office (Editing Brain) — proposal 2026-11-05 22:44 (Hark), NOT_STARTED, awaiting user go

User idea: structure-based program that knows editing science; "creativity office" with a worker doing the job. Skill > model. No sound/music now. No heavy model setup.
No earlier user roadmap for this brain exists (checked journal + docs/KANG_Extended_Roadmap_v5.2.md). Closest: Story & Retention plan (notes/research_story_layer_2026-11-05.md).

Design:
- Brain = rulebook as data (config/editing_science/*.json). Each rule: trigger, treatment, why (attention reset / open loop / pattern interrupt / prediction), source, limits (max per minute), test.
- Desks: 1 Intent desk (tag each beat: number/fact, place intro, story moment, emotion/devotion, tip/instruction, list, transition, hook) rule-based on Hindi/Hinglish words + position.
  2 Picture desk (intent -> visual treatment library with rotation: number->card, place->map/detail-first reveal, list->fast 3-5 shot sequence, emotion->slow push-in hold, tip->text pop).
  3 Rhythm desk (fast-slow-fast curve, no same shot length 3x, change every <=8 s, one transition style).
  4 Story desk (cold open, open loop, bookend, chapters) — needs user answers.
  5 Critic desk (scorecard per rule, violations list) -> review.
- Worker = existing KANG (beats, cards, maps, parallax, package). LLM optional later only to choose among rules.
- Phase 1 on Dwarika: intent tagging + treatment library + critic report on v17b, then v18 A/B.
- Style Pack desk idea (fixed visual language, from Ali Abdaal tutorial) proposed 23:40, awaiting go.
- Contact sheet before render step + HyperFrames (Apache-2.0, Node, not evaluated) noted 23:45 from Ali Abdaal AI-editing video.
- 23:58 Final structure sent: rulebook (priority Story > Clarity > Rhythm > Style) + desks in order: intent, picture, rhythm, style pack, story, critic. Flow: narration -> intent -> plan -> contact sheet before render -> KANG render -> critic -> combined review v17b vs v18. Milestone 1: rulebook v0 + intent + picture desks + critic report on v17b + contact sheet.
- Awaiting user: cold open may repeat later moment? pop words Roman or Devanagari? Dwarika style mood (old paper / temple colours / clean modern)?
- USER DECISIONS 2026-11-06 00:10: cold open MAY repeat a later moment; on-screen pop words ALWAYS Hinglish (Roman); Dwarika style mood = saaf modern (clean modern). Audio/music/sound saved for later: only after visuals are perfect.
- 00:15 Design rule: desks use fixed JSON schemas so an optional LLM can fill the same slots later; LLM proposes, rulebook validates, user approves; KANG must run fully without LLM.
- 00:18 AE-style options sent: (1) user designs AE template -> Lottie/Bodymovin -> KANG fills text (my pick; renderer licence NOT checked), (2) HyperFrames, (3) own renderer. Asked if user can make a small AE template.
- 00:20 Corrected: tracking/rotoscope/3D track not impossible, need moving footage. Offered 'text behind object' on stills via small segmentation model (licence research pending, awaiting user).
- 07:15 User uploaded creative-layer-full-package (own/other-agent build): 49 harvest files, 463 rules (🟢10 🟡55 🟠398; 153 machine-checkable; ~74 audio-ish), ORDER + addendum, engine.py stdlib worker+critic, 31/31 tests PASS (my run). Copied to kang/incoming/creative_layer_2026-11-06. Gaps: critic only (no planner/treatment/hands), Dwarika demo used other data (Vosk, 7 scenes), not KANG v17b 132 beats. Plan: adopt as rulebook+critic; connect to v17b CSV; audio rules off; add intent/picture planner + hands.
- 07:20 Package v2: + flag_keywords_hi.json (Hindi/Hinglish human-flag words), hindi_hinglish profile, engine update; 36/36 tests PASS (my run); Dwarika demo now 15 human flags, score still 36.4% on same 7-scene data. Use v2 as base (kang/incoming/creative_layer_2026-11-06_v2).
