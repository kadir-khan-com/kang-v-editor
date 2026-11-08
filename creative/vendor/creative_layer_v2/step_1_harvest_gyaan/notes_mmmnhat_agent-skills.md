# NOTES (apne shabdon me) — mmmnhat/agent-skills ("VisionCut")

**Ye note apne shabdon me hai — source ka licence MIT/Apache nahi hai, isliye uska text copy nahi kiya gaya; seekh ke liye hai.**

- Source: mmmnhat/agent-skills — Link: https://github.com/mmmnhat/agent-skills
- Licence: **koi licence nahi** — repo page par licence line nahi aayi aur clone me bhi kahin LICENSE file nahi mili (root + subfolders check kiye). 0 stars, 46 commits (repo page, 2026-11-06); last commit (clone): 2026-10-17.
- Kya hai ye: "VisionCut" — ek autonomous video editorial suite: Premiere Pro MCP par chalne wali kai skills (clean-cut, pacing-editor, comedy-timing, clip-inspector, correct-color, auto-match-loudness, remove-pauses, synchronize-clips aadi), zyada tar Vietnamese + English mix me likhi hui. README aur technique-wali skills ke key sections/numbers padh kar ye note banaya hai; suite ki har skill line-by-line nahi padhi gayi.

## Techniques ka sar (apne shabdon me)

**Pacing editor (Premiere timeline architecture)**
- 5-track audio layout iska fixed template hai: A1 = clip ki asli awaaz, A2 = khaali, sirf voiceover ke liye reserved, A3 = cuts par sync transition SFX (whoosh), A4 = action peaks par climax SFX (punch/impact), A5 = background music jo climax moments par **−12 dB** tak auto-duck hoti hai.
- Retention ke liye "W-Curve" reordering: 30 second jaise chhote target par clips ko chronological kram ki jagah retention curve ke hisaab se dobara sajaya jata hai (ya tez chronological fast-cut rakha jata hai).
- Ek vyavharik ginti: Premiere bridge par clip-by-clip sequential commands **90–120 second** lete hain, isliye saari clips ek atomic batch call me bhejni chahiye (~0.9 s) — ye tool-usage ka niyam hai, craft kam.

**Comedy timing (is suite ka sabse pakka technique hissa)**
- Har comedy incident ko 4-act ki ek lagatar ghatna mana jata hai, kul **8–14 second** (zyada se zyada 15 s):
  - Premise/Setup: **2.0–3.5 s** (max 4.0) — IN point wahan se jahan jaanboojh ki harkat shuru ho; camera shake/unsettled shuruwat hatao.
  - Escalation: **1.5–3.0 s** (max 3.5) — tension/vadna badhti hai, darshak ke dimaag me prediction banti hai.
  - Punchline/Climax: **1.5–2.5 s** (max 3.0) — asal vaardaat ka pal.
  - Aftermath/Reaction: **2.0–4.0 s** (max 4.5) — OUT sirf tab jab reaction settle ho jaye; vaardaat ke baad kam se kam **1.5 s** reaction pakki; reaction ko beech me kaatna sakht mana hai.
- Ek incident = ek hi lagatar cut (**4–11 s**), poora scene ke andar band. Agar isolated scene 9 s se lambi ho to window climax ke aas-paas rakho: peak se **4 s pehle** se peak ke **3.5 s baad** tak. Bohot tang window (sirf peak −1.5 s) lene se premise mar jati hai — mana hai.
- Compilation rips ke kinare par pichle/agale clip ke **2–5 second** chipke hote hain; scene isolation me **±0.08 s** ki safety margin ke saath wo hissa poora hatao. Kisi bhi cut edge par padosi scene ka **1–2 frame bhi bleed nahi** hona chahiye (zero frame bleed), aur file ke pehle 3 second ko aankh band karke lena (blind jump-cut) mana hai kyunki wo aksar kisi aur hi scene ka hissa hota hai.

**Clean-cut / baaki skills ke numbers**
- Scene split frame-accurate rakhne ki tarkeeb: seek ko frame time se **0.25 frame pehle** rakho (quarter-frame centering) aur tail ko **0.5 frame** pehle kaato — dono taraf bleed khatm karne ke liye.
- Pause removal skill 10 ms tak ke chhote pauses bhi kaat sakti hai; **1 second ya usse lambi khamoshi hamesha kat-ti hai**. Iske ek observed example me ripple delete ke baad video coverage 100% se 42.5% reh gayi.
- Clip inspection: har clip ki 4-frame filmstrip (0%, 33%, 66%, 100%) 1280×180 contact strip me — poori footage list ek nazar me scan karne ke liye; teaser/intro shots aam taur par **1.5 s/shot se chhote** hote hain, aur intro scenes ki ginti fix mat mano (0 bhi ho sakti hai, 12 bhi).
