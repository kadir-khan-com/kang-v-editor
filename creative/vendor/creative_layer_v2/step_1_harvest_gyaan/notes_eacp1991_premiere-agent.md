# NOTES (apne shabdon me) — eacp1991/premiere-agent

**Ye note apne shabdon me hai — source ka licence MIT/Apache nahi hai, isliye uska text copy nahi kiya gaya; seekh ke liye hai.**

- Source: eacp1991/premiere-agent — Link: https://github.com/eacp1991/premiere-agent
- Licence: **koi licence nahi** — repo page par bhi licence nahi dikha aur clone me bhi kahin koi LICENSE file nahi mili (root + saare subfolders check kiye). Ye repo ek fork hai, 0 stars, 120 commits (repo page, 2026-11-06); last commit (clone): 2026-07-07.
- Kya hai ye: Baatcheet se video edit karne wala agent — local preprocessing (speech + visual captions + audio events) se ek interleaved timeline banti hai, agent cut tay karke FCPXML + Premiere/Resolve XML + master SRT deta hai; asal cut NLE ke andar rehta hai. Iske SKILL.md (lagbhag 85 KB) ke main sections — hard rules, pacing presets, cut craft — padh kar ye note banaya hai; poori file line-by-line nahi padhi gayi.

## Techniques ka sar (apne shabdon me)

**Production-correctness ke sakht niyam (iski "Hard Rules")**
- Kabhi shabd ke beech me cut nahi: har cut edge word-level transcript ki shabd-seema (word boundary) par snap hoti hai, aur ek helper tool se har EDL range verify karna anivarya hai — haath se transcript parse karna mana hai.
- Har cut ke dono taraf kam se kam **60 ms ki asli khamoshi** (true silence) chhodni hai taaki NLE ka audio crossfade "saans" le sake.
- Pacing preset user se confirm karna har session me zaroori hai — bina preset ke strategy nahi banti.

**Pacing preset system (is repo ka sabse kaam ka idea)**
- Paach preset: **Calm / Measured / Paced (default) / Energetic / Jumpy**. Har preset chaar numbers me khulta hai: kitni lambi khamoshi hatani hai (min silence to remove), kitni chhoti baat rakhne layak hai (min talk to keep), shuruaat ka margin (lead) aur aakhir ka margin (trail).
- Sabse neeche wali seema **250 ms** par atki hai aur iski wajah perceptual hai: aaram se boli gayi connected speech me shabdon ke beech **30–200 ms** ke articulation gaps hote hi hain — ye dead air nahi, shabdon ki awaaz ka hissa hain. Isse neeche threshold rakhne se ek jumla ek-shabd wale tukdo me kat jayega. Asli editorial pauses (saans, hichkichahat, soch) lagbhag **250–300 ms** se shuru hote hain, isliye ladder 800 ms se 250 ms tak hi jaati hai.
- Lead margin ka kaam ASR ki **50–100 ms** ki aam drift ko soak karna aur sunne wale ko shabd se pehle ek saans ki jagah dena hai; margins ki legal range ek purani **30–200 ms** working-window soch se bandhi hai, Calm ka 500 ms uski upari hadd hai.
- Intra-phrase silence removal iski jaan hai: threshold se badi khamoshi agar ek hi phrase ke beech me bhi ho to phrase ko do ranges me todna padta hai — iska apna example: isi vidhi se 12 minute ka walking talking-head bina ek shabd khoye 7 minute ka ban jata hai (saikdo saans/hichkichahat wale gaps hatakar).

**Cut craft ke baaki faisle**
- Split edits (J-cut/L-cut) aur cross-dissolves is samay **deferred** hain — XML delivery sirf hard cuts support karti hai, isliye agent inhe emit hi nahi karta (technique ka jaanboojh kar chhoda hua hissa).
- Multi-take handling: har beat ke liye sabse saaf take chuno; retake detection — atak/bol-bhool wala take hatao, saaf wala rakho. Taiyaar structural archetypes se shakal chuni/adapt ki jaati hai.
- Kuch aur vyavharik baatein: visual captions par stop-words hatta kar timeline file ka token bojh lagbhag **55–60%** kam kiya jata hai taaki agent poori timeline ek baar me padh sake; delivery hamesha XML + SRT hoti hai, grade ka faisla NLE ke andar colourist par chhoda jata hai.
