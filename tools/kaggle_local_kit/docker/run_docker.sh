#!/usr/bin/env bash
# Linux/Mac/WSL:  ./run_docker.sh "/path/to/AI Auto Edit" "python test_offline.py" [--offline] [--gpu]
set -e
PROJECT="$1"; CMD="${2:-python test_offline.py}"; shift 2 || true
KIT="$(cd "$(dirname "$0")/.." && pwd)"; IMG=kang-kaggle-lite
[ -z "$(docker images -q $IMG)" ] && docker build -f "$KIT/docker/Dockerfile.lite" -t $IMG "$KIT"
EXTRA=()
for a in "$@"; do [ "$a" = "--offline" ] && EXTRA+=(--network none); [ "$a" = "--gpu" ] && EXTRA+=(--gpus all); done
docker run --rm -v "$PROJECT:/kaggle/input/kang-project:ro" "${EXTRA[@]}" $IMG $CMD
