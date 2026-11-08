# Framing / empty-area checks (real visual pass)
Status per item: OPEN / DECIDED. Not import failures.
- OPEN (2026-10-31): S02 showed checkerboard on both sides in Premiere with the TEST still (contain-fit, narrower than 16:9). Decide in real visual pass: fill frame (cover) vs keep a background. KANG_006 real assets are all 1920 wide (>=16:9) with fit=cover -> preview has no empty area; Premiere view at 100% still to be confirmed by user.
- OPEN: S02 real still (Dwarka gate, 4:3) crops top of arch/"Welcome to Dwarka" sign under cover; consider top-anchored crop or contain+blurred background.
- Rule for all 22 scenes: every frame of the sequence must be covered (no transparent/black gaps) unless a background is chosen on purpose.
