# NOTES (apne shabdon me) — appariciojunior/video-editor-skills ki techniques

> **Ye note apne shabdon me hai — source ka licence MIT/Apache nahi hai, isliye uska text copy nahi kiya gaya; seekh ke liye hai.**
> Source: https://github.com/appariciojunior/video-editor-skills · Licence: CC BY-NC 4.0 (commercial use mana) · 415 stars · 57 forks · repo bana 2026-10-23 (repo page, 2026-11-06). DaVinci Resolve Studio ke liye Claude Code skills ka set hai; andar koi code nahi — sirf method, niyam aur traps hain, jo asal edits se seekhe gaye.

## Techniques / ideas (sar, apni bhasha me)

- **First-pass editor ki taqseem:** Insaaan film kare aur taste ke faisle le; agent mehnat wala hissa kare — import, retakes/dead air ki safai, B-roll sambhalna, captions likhna, brand motion graphics, export me madad. Suraksha ka usool: raw footage kabhi modify nahi hoti; Resolve ke andar agent sirf NAYI cheezein jodta hai (nayi timelines/clips), editor ke template ya purane projects ko haath nahi lagata.
- **Rough-cut me kya bache, kya jaye:** Retakes, false starts aur dead air pehle hatao. Do cheezein pehchan ke bachao — ek, wo hisse jo bolne wale ne "editor ke liye note" ke taur par bole hon; do, punchlines.
- **Vlog pacing ka tareeka:** Silence detection se pauses kaato, lekin har cut par chhote pads (kinaro par thodi hawa) rakho taaki bolna ghuta hua na lage. Scene ke edges par room rakho. Jump cuts ko naram karne ke liye halka zoom punch-in istemal hota hai.
- **B-roll ka usool:** B-roll pehle dhoondo aur khud DEKHO, phir use action aur kahani ke hisaab se kaato — sirf khaali jagah bharne ke liye nahi.
- **Awaaz ki safai:** Loudness normalize karo; awaaz muffled (band) lage to pehle diagnosis, phir EQ recipe se use saaf karo.
- **Music aur SFX:** Video ke har section ke hisaab se music cues chuno; bolte waqt music ko voice ke neeche ducking envelope se dabao; SFX zarf se — tasteful, har jagah nahi.
- **Captions ka niyam:** Captions import karne se PEHLE padh ke saaf karo — sahi shabdo wali, ek-line captions.
- **Motion overlays:** Brand graphics ko bole gaye shabdon ke timing par lagao, aur chehre + captions ke ilake ko hamesha khaali rakho (face- and caption-safe).
- **Resolve scripting ki seekh alag rakho:** API me kya kaam karta hai, kya bina error ke chup-chaap fail ho jata hai, aur kya Resolve ko crash karta hai — ye traps ek alag skill me likhe hain taaki har edit par dobara na seekhne padein.
- **Export ki soch:** Quality waisi ki waisi, lekin file size par nazar — 25 GB jaisi deliver files se bachne wali settings.
- **Har video se seekh jama karo:** Editor jo feedback de ("zyada choppy hai", "B-roll par music tez karo") use apni memory file me jodte jao, taaki agla video pehle se smarter bane. Starting values (thresholds waghera) ek config template me rakhe jate hain, skills ke andar bikhre nahi.
