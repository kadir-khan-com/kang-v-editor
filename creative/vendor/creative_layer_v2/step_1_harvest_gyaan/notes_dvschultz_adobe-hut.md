# NOTES (apne shabdon me) — dvschultz/adobe-hut

**Ye note apne shabdon me hai — source ka licence MIT/Apache nahi hai, isliye uska text copy nahi kiya gaya; seekh ke liye hai.**

- Source: dvschultz/adobe-hut — Link: https://github.com/dvschultz/adobe-hut
- Licence: **koi licence nahi mila** — repo page ki details me licence line nahi aayi aur clone me bhi kahin LICENSE file nahi mili (root + subfolders check kiye). 24 stars, 129 commits (repo page, 2026-11-06); repo 2013 se hai, last commit (clone): 2026-07-12.
- Kya hai ye: Adobe applications ke liye ek bada personal knowledge base — `.claude/` folder me skill files aur expert agents. Lekin iska vishay **plugin/extension development** hai (UXP aur ExtendScript APIs), editing craft nahi.

## Andar kya hai (apne shabdon me, sirf pehchan ke liye)

- **After Effects hissa (sabse bada):** lagbhag 33 skill files — expressions par ek poori shrinkhala (expression library, expression reference, 3D expressions, text expressions, expressions ko link karna, debug karna), AEQuery library ke upar bane skills (selectors, wrappers, project/file settings, UI), scripting operations (layer ops, shape ops, markers, MOGRT, trim/resequence, randomize, batch export, EDL), aur C++ SDK/AEGP par bhi skills (effects, SmartFX). Saath me `after-effects-expressions`, `after-effects-scripter`, `after-effects-sdk` aur `premiere-uxp-expert` jaise expert agents.
- **Premiere Pro hissa:** UXP API ke skills — tracks, sequence, project, markers, actions, manifest. Ye Premiere ke **plugin API** ka gyaan hai (panel kaise banaye, API se sequence/tracks kaise chhue), timeline par cut kaise lagaye — iska nahi.
- Baaki hissa Photoshop aur InDesign ke UXP skills/agents ka hai — is round ke scope se bahar.

**Verdict (note ka kaaran):** Ye ek kaam ka API reference bhandar hai unke liye jo Adobe extensions banate hain, lekin isme editing technique (pacing, cut craft, motion design ke niyam) nahi ke barabar hai — aur licence bhi nahi hai. Isliye na full extraction, na technique note ke aage kuch; sirf ye pehchan-note rakha hai taaki aage koi ise craft source samajh kar dobara na khode.
