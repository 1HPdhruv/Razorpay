import os

dirs = [
    "docs",
    "data/raw",
    "data/processed",
    "data/generated",
    "backend/app/api/routes",
    "backend/app/core",
    "backend/app/models",
    "backend/app/schemas",
    "backend/app/services/data",
    "backend/app/services/lifecycle",
    "backend/app/services/features",
    "backend/app/services/discovery",
    "backend/app/services/risk",
    "backend/app/services/investigation",
    "backend/app/services/simulation",
    "backend/app/services/evaluation",
    "backend/app/repositories",
    "backend/app/utils",
    "backend/tests/fixtures",
    "frontend/public",
    "frontend/src/app/patterns",
    "frontend/src/app/investigations",
    "frontend/src/app/simulations",
    "frontend/src/app/evaluation",
    "frontend/src/components/layout",
    "frontend/src/components/dashboard",
    "frontend/src/components/patterns",
    "frontend/src/components/investigations",
    "frontend/src/components/simulations",
    "frontend/src/components/evaluation",
    "frontend/src/lib",
    "frontend/src/hooks",
    "frontend/src/types",
    "scripts"
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

def write_file(path, content=""):
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

# Gitkeeps
for path in ["data/raw/.gitkeep", "data/processed/.gitkeep", "data/generated/.gitkeep", "backend/tests/fixtures/.gitkeep", "frontend/public/.gitkeep"]:
    write_file(path, "")

# Init files
init_dirs = [
    "backend/app", "backend/app/api", "backend/app/api/routes", "backend/app/core",
    "backend/app/models", "backend/app/schemas", "backend/app/services",
    "backend/app/services/data", "backend/app/services/lifecycle", "backend/app/services/features",
    "backend/app/services/discovery", "backend/app/services/risk", "backend/app/services/investigation",
    "backend/app/services/simulation", "backend/app/services/evaluation", "backend/app/repositories",
    "backend/app/utils", "backend/tests"
]
for d in init_dirs:
    write_file(os.path.join(d, "__init__.py"), "")

# Basic Files
write_file(".gitignore", """
.env
.env.*
!.env.example
node_modules/
.next/
__pycache__/
*.pyc
.pytest_cache/
.venv/
venv/
*.db
*.sqlite
*.sqlite3
data/raw/*
data/processed/*
data/generated/*
.DS_Store
""")

write_file(".env.example", """
OPENAI_API_KEY=
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
DATABASE_URL=sqlite:///./financial_csi.db
NEXT_PUBLIC_API_URL=http://localhost:8000
""")

write_file("docker-compose.yml", """
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
    environment:
      - DATABASE_URL=sqlite:///./financial_csi.db

  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
""")

write_file("README.md", """
# Financial CSI

**AI Risk Manager for discovering previously unidentified payment-event patterns associated with merchant loss.**

*A Razorpay AI Buildathon prototype for Track 02 — AI Risk Manager.*

## Problem
Existing simple fraud detection is often insufficient. Financial CSI discovers hidden, multi-step payment-event patterns (e.g., specific timeouts leading to fast retries and eventual chargebacks) that cause financial loss.

## Architecture
- **Backend:** Python, FastAPI, SQLite, scikit-learn, pandas
- **Frontend:** Next.js, React, Tailwind CSS, Recharts
- **AI Abstraction:** Extensible service for LLM integration

## Project Structure
Phase 1 - Scaffold complete.

## How to Run

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Current Status
**Phase 1 — Scaffold.** Do not expect functional AI models or real Razorpay integrations yet.
""")

write_file("data/README.md", "# Data Directory\nContains raw, processed, and generated dataset files for Financial CSI.")

# Backend Setup
write_file("backend/requirements.txt", """
fastapi==0.110.0
uvicorn==0.29.0
pydantic==2.6.4
pydantic-settings==2.2.1
pandas==2.2.1
numpy==1.26.4
scikit-learn==1.4.1.post1
python-dotenv==1.0.1
httpx==0.27.0
pytest==8.1.1
""")

write_file("backend/pytest.ini", """
[pytest]
pythonpath = .
testpaths = tests
""")

write_file("backend/README.md", "# Backend\nFastAPI service for Financial CSI.")

