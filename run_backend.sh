#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"
source /home/skumar/.venv/bin/activate
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
