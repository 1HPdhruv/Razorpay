#!/bin/bash
set -e

cd "$(dirname "$0")/.."

echo "=========================================="
echo "    FINANCIAL CSI - DEMO RESET            "
echo "=========================================="

echo "Killing stray backend/frontend processes..."
pkill -f "uvicorn app.main:app" || true
pkill -f "npm run dev" || true
pkill -f "next" || true

echo "Purging generated artifacts..."
rm -rf data/generated/*
rm -f docs/generated/final_evaluation.json
rm -f docs/generated/FINAL_EVALUATION_REPORT.md

echo "Resetting deterministic data state..."
python scripts/prepare_demo.py

echo "=========================================="
echo "Demo state reset successfully."
echo "Run ./scripts/run_demo.sh to launch."
