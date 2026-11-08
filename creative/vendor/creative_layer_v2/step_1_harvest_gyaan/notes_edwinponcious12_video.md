# NOTES (apne shabdon me) — edwinponcious12/video ke `davinci-resolve` skill ki techniques

> **Ye note apne shabdon me hai — source ka licence MIT/Apache nahi hai, isliye uska text copy nahi kiya gaya; seekh ke liye hai.**
> Source: https://github.com/edwinponcious12/video (skill: `.claude/skills/davinci-resolve/`) · Licence: KOI NAHI (LICENSE file nahi) · 0 stars · repo bana 2026-09-27 (repo page, 2026-11-06). Ek personal video pipeline hai jisme Premiere aur Resolve do "lanes" hain; ye note Resolve lane ki hai.

## Techniques / ideas (sar, apni bhasha me)

- **Lane ka usool — HOW alag, WHAT alag:** Skill khud ko sirf mechanics (HOW) tak rakhti hai; look, numbers aur "done" ki paribhasha format ke preset me rehti hai. Pehle preset padho (target kya hai), phir lane ke steps chalao (kaise hoga). Ye alagav hi is design ki jaan hai.
- **EDL ko asal timeline par replay karna:** Rough cut ki EDL (cuts.json) ko raw footage ke against replay karke Resolve timeline par alag-alag, trimmable clips ki surat me dobara banao — ek hi scripted call me poori timeline khadi ho jati hai, aur aage ka kaam asal Resolve clips par hota hai.
- **Audio ki seema aur uska hal:** Resolve ke scripting API ke paas audio effects ka koi surface nahi hai — isliye audio polish timeline ke bahar, ffmpeg se har source file par hoti hai, aur phir taiyaar file ko ReplaceClip se timeline me badal diya jata hai.
- **Premiere ki teen aadatein jo Resolve me nuksaan karti hain:**
  1. 1080p asset ko 4K timeline par haath se scale mat karo — Resolve use khud conform kar deta hai; upar se Motion Scale 200 lagane se wo 400% ho ke crop ho jayega.
  2. Alpha wale video ko premultiply mat karo — Resolve STRAIGHT alpha chahta hai aur use khud pehchan leta hai.
  3. Adjustment layer mat dhundo — Resolve me uska badal color group hai, jise track ghusane ki bhi zaroorat nahi padti.
- **Bridge panel nahi chahiye:** Premiere ke bar-aks yahan koi bridge panel nahi; MCP seedha Resolve ke official scripting API se app ke andar (in-process) baat karta hai — Edit, Fusion, Color, Fairlight chaaron ek hi API se. Shart bas ye hai ki Resolve chalu ho.
- **API se aage ka kaam:** Silence-ripple auto cuts, AI subtitles ke saath transcript-based cut proposals, Fusion node graphs, aur custom DCTL color shaders — sab scripting API se chalaye jate hain.
