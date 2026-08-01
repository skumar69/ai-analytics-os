#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"
source /home/skumar/.venv/bin/activate
streamlit run frontend/app.py --server.port 8501 --server.address 0.0.0.0
