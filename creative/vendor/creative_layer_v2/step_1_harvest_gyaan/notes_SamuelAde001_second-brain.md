# NOTES (apne shabdon me) — SamuelAde001/second-brain ke `video-edit-pass` skill ki techniques

> **Ye note apne shabdon me hai — source ka licence MIT/Apache nahi hai, isliye uska text copy nahi kiya gaya; seekh ke liye hai.**
> Source: https://github.com/SamuelAde001/second-brain (skill: `.claude/skills/video-edit-pass/`) · Licence: KOI NAHI (personal vault repo) · 1 star (repo page, 2026-11-06). Skill DaVinci Resolve me long-form talking-head/tutorial video ke liye bani hai.

## Techniques / ideas (sar, apni bhasha me)

- **Do-phase wala kram:** Pehle CUT pass, phir TRANSCRIPT pass — aur dono ke beech me editor khud dobara cut kare. Dusra phase tabhi shuru ho jab editor nayi (re-cut) subtitle file bhej de; purani subtitles par transcript banana bekaar hai kyunki pehle phase ka saara kaam hi cut badalna hai.
- **Inputs ki shartein:** Current cut ki subtitle file (SRT/VTT) laazmi hai. Timeline XML (Resolve se FCP7/xmeml export) ho to behtar — usi se frame rate, flash frames aur timeline start timecode verify hota hai; bina uske EDL ke timecodes galat jagah pad sakte hain.
- **Phase 1 me dhundna kya hai:** Duplicate takes, misspeaks (galat bole gaye hisse), garbled audio, flash frames, redundancy (ek hi baat dobara), aur script ke wo sections jo video me missing hain.
- **Markers EDL me do, rang-birange XML me nahi:** Resolve FCP7 XML import karte waqt clip colours (label2) ko ignore kar deta hai — rang XML me ghusane se gayab ho jayenge. Isliye marker EDL hi sahi rasta hai. Rangon ki tier vyavastha: Tier A = laal (Red), flash frames = Fuchsia, Tier B = peela (Yellow), Tier C = neela (Blue), notes aur re-record ki maangein = hari (Green).
- **Pehle naapo, phir raay do:** Kaam ki shuruaat taiyaar scripts se hoti hai — subtitle parse, XML audit, repeats dhundna — aur unki output padhne ke BAAD hi editorial raay banti hai.
- **Phase 2 ka hasil:** Re-cut subtitles se ek chaptered, ALL-CAPS editing transcript banta hai jisse editor padh ke cut kar sake, saath me ek contiguous chapter marker EDL.
