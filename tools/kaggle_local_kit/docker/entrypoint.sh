#!/usr/bin/env bash
# /kaggle/input/<name> (read-only dataset) -> /kaggle/working (fresh writable copy) -> preflight -> command
set -u
SRC="$(find /kaggle/input -mindepth 1 -maxdepth 1 -type d | head -n1)"
[ -z "$SRC" ] && { echo "FAIL: /kaggle/input me project mount nahi hua"; exit 2; }
DEST=/kaggle/working/ai-video-engine          # Kang ka asli Kaggle path
rm -rf /kaggle/working/* /kaggle/working/.[!.]* 2>/dev/null
mkdir -p "$DEST" && cp -a "$SRC"/. "$DEST"/
rm -rf "$DEST"/_kaggle_sandbox "$DEST"/.git "$DEST"/__pycache__
cd "$DEST"
export ENGINE_BASE_DIR="$DEST"
echo "[docker] input=$SRC (ro)  working=$DEST (fresh)"
python /kit/kaggle_preflight.py --project "$DEST" --require "${KANG_REQUIRE:-}" || { echo "PREFLIGHT FAIL"; exit 1; }
echo "[docker] running: $*"
"$@"; rc=$?
echo "================ RESULT: $([ $rc -eq 0 ] && echo PASS || echo FAIL) (rc=$rc) ================"
exit $rc
