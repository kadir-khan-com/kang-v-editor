# NOTES (apne shabdon me) — AdamGarceau/resolve-toolkit ki techniques

> **Ye note apne shabdon me hai — source ka licence MIT/Apache nahi hai, isliye uska text copy nahi kiya gaya; seekh ke liye hai.**
> Source: https://github.com/AdamGarceau/resolve-toolkit · Licence: KOI NAHI (repo me LICENSE file nahi) · 1 star · repo bana 2026-08-31 (repo page, 2026-11-06). Ek editor ke personal, asal-use-wale Claude Code skills + Fusion title pack ka sangrah hai.

## Techniques / ideas (sar, apni bhasha me)

- **Frame-perfect rough cut (perfect-cuts):** Talking-head ki raw recording ko WhisperX se transcribe karo, transcript se retakes aur false starts pehchano, unhe hata ke rough cut banao. Output ek saath kai roop me rakho — Resolve XML, EDL, SRT, aur ek cut log (har cut ka hisaab, taaki faisla ulta bhi ja sake aur jaanch bhi ho).
- **Tighten karne ka niyam (dr-tighten):** Bani hui cut se dead air aur filler words (um, uh, "you know") hatao, lekin cut SIRF silence me ya word boundary par lage — jumla beech se kabhi na kate. Shorts aur longform ke liye alag profiles (dono ki saans alag hoti hai).
- **Ek camera se nakli multicam (podcast-punch-in):** Do logon ke ek static wide shot ko "multicam" jaisa banao — jo bol raha hai us par digital punch-in switch karo. Bolne wale ki pehchan awaaz ki pitch se hoti hai; na cloud chahiye, na GPU.
- **Snap captions (dr-snap-captions):** Har caption beat par ek Fusion title template lagao aur uska text scripting API se set karo — TikTok-style snap captions Resolve ke andar hi ban jate hain.
- **Voiceover finish (resolve-vo-finish):** Aakhiri awaaz wala pass — level theek karo, saansein (breaths) ghatao, aur master ko **−6 dBFS peak** par rakho.
- **Script se B-roll (script-to-broll):** Apni clip library ka ek JSONL index banao; script ki har line ko us index se match karke shot ke sujhaav do.
- **Fusion scripting ka kadwa niyam:** Fusion (motion-graphics page) ko script karte waqt node *connect* calls hamesha EK-EK karke bhejo, parallel batch kabhi nahi — Fusion ki scripting queue single-threaded hai, parallel batch Resolve ko itna deadlock kar deta hai ki force-quit karna padta hai.
- **Title templates ka pattern:** Fusion Text+ macros ke roop me editable title pack — chapter card, lower third, stat callout, terminal heading, repo URL — jo Effects panel se timeline par lagte hain aur wahi edit hote hain.
