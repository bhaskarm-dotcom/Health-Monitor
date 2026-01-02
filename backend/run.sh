#!/bin/bash
# Run script for backend server

cd "$(dirname "$0")"
cd src
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python3 -m uvicorn server:app --reload --host 0.0.0.0 --port 8001

