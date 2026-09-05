#!/bin/bash
set -e

# Change to project root
cd "$(dirname "$0")/.."

echo "=========================================="
echo "    FINANCIAL CSI - HACKATHON DEMO        "
echo "=========================================="

echo "[1/4] Preparing data and warming ML cache..."
python scripts/prepare_demo.py

echo "[2/4] Starting Backend (Port 8000)..."
cd backend
# Use a detached screen or background process for the backend
nohup uvicorn app.main:app --reload --port 8000 > backend.log 2>&1 &
BACKEND_PID=$!
cd ..

echo "[3/4] Starting Frontend (Port 3000)..."
cd frontend
nohup npm run dev > frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "=========================================="
echo "  DEMO IS RUNNING!"
echo "  Frontend: http://localhost:3000"
echo "  Backend:  http://localhost:8000/docs"
echo "=========================================="
echo "Press Ctrl+C to stop both servers."

# Trap ctrl-c and kill background processes
trap "echo 'Stopping servers...'; kill $BACKEND_PID; kill $FRONTEND_PID; exit" INT
wait
