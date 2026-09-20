#!/bin/bash
set -e

exec fastapi run apps/backend/src/backend/main.py \
    --host 0.0.0.0 \
    --port "${PORT:-8000}" \
    "$@"
