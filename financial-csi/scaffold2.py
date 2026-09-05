import os

def write_file(path, content=""):
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

# DOCS
write_file("docs/PRODUCT.md", """
# Product Concept: Financial CSI

## Target User
Risk Operations Managers and Data Scientists at Razorpay.

## Problem
Simple rules-based fraud detection catches obvious patterns but misses complex, multi-step behaviors that lead to merchant loss (e.g., chargebacks, high gateway fees without settlement, specific webhook delays following fast retries). 

## Solution
Financial CSI analyzes the entire payment-event lifecycle, extracts temporal and behavioral features, and discovers hidden patterns associated with unusually high merchant loss.

## Intended Demo
The final demo will show a dashboard identifying a previously unknown risk pattern, explaining the evidence, validating it on held-out data, and simulating the monetary impact of an intervention.
""")

write_file("docs/ARCHITECTURE.md", """
# Architecture

```text
Payment Events
      ↓
Data Validation
      ↓
Transaction Lifecycle
      ↓
Feature Extraction
      ↓
Pattern Discovery
      ↓
Risk Evaluation
      ↓
AI Investigation
      ↓
Intervention Simulation
      ↓
FastAPI
      ↓
Next.js Dashboard
```
""")

write_file("docs/DATA_MODEL.md", """
# Data Model

Describes entities and relationships.

- **Transaction**: The core payment attempt.
- **Event**: A state change or action within a transaction lifecycle.
- **Pattern**: A sequence or combination of events associated with risk.
- **Investigation**: AI explanation of a pattern's evidence.
- **Simulation**: Counterfactual evaluation of an intervention.
""")

write_file("docs/ML_APPROACH.md", """
# ML Approach

Candidate approaches (to be evaluated):
- Clustering (e.g., DBSCAN on behavioral features)
- Association-rule mining (e.g., FP-Growth for event sequences)
- Anomaly detection (e.g., Isolation Forests)
- Supervised validation (e.g., XGBoost on extracted features)
- Temporal sequence features
""")

write_file("docs/EVALUATION.md", """
# Evaluation Metrics

- Train/discovery vs held-out evaluation
- Precision, Recall, F1
- False-positive rate & cost
- Monetary exposure (₹)
- Potential preventable loss
""")

write_file("docs/API_SPEC.md", """
# API Specification

- `GET /api/health`
- `GET /api/transactions`
- `GET /api/transactions/{transaction_id}`
- `GET /api/patterns`
- `GET /api/patterns/{pattern_id}`
- `GET /api/investigations/{pattern_id}`
- `POST /api/simulations/intervention`
- `GET /api/evaluation`
""")

write_file("docs/DEMO_SCRIPT.md", """
# Demo Script (Placeholder)

1. Open dashboard
2. Show merchant exposure
3. Run discovery
4. Show previously unknown pattern
5. Investigate evidence
6. Show held-out validation
7. Simulate intervention
8. Show potential loss prevented
""")

write_file("docs/DEVELOPMENT_PLAN.md", """
# Development Plan

Phase 1: Project scaffold
Phase 2: Synthetic transaction generator
Phase 3: Transaction lifecycle engine
Phase 4: Feature engineering
Phase 5: Pattern discovery
Phase 6: Held-out evaluation
Phase 7: AI investigation/explanation
Phase 8: Intervention simulation
Phase 9: Razorpay Test Mode integration
Phase 10: Dashboard implementation
Phase 11: Demo hardening
""")

# BACKEND - MAIN
write_file("backend/app/main.py", """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, transactions, patterns, investigations, simulations, evaluation

app = FastAPI(title="Financial CSI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["transactions"])
app.include_router(patterns.router, prefix="/api/patterns", tags=["patterns"])
app.include_router(investigations.router, prefix="/api/investigations", tags=["investigations"])
app.include_router(simulations.router, prefix="/api/simulations", tags=["simulations"])
app.include_router(evaluation.router, prefix="/api/evaluation", tags=["evaluation"])
""")

write_file("backend/app/api/routes/health.py", """
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
def check_health():
    return {"status": "ok", "version": "0.1.0"}
""")

write_file("backend/app/api/routes/transactions.py", """
from fastapi import APIRouter

router = APIRouter()

@router.get("")
def list_transactions():
    # TODO: Implement in later phase
    return []

@router.get("/{transaction_id}")
def get_transaction(transaction_id: str):
    # TODO: Implement in later phase
    return {"transaction_id": transaction_id}
""")

write_file("backend/app/api/routes/patterns.py", """
from fastapi import APIRouter

router = APIRouter()

@router.get("")
def list_patterns():
    # TODO: Implement in later phase
    return []

@router.get("/{pattern_id}")
def get_pattern(pattern_id: str):
    # TODO: Implement in later phase
    return {"pattern_id": pattern_id}
""")

write_file("backend/app/api/routes/investigations.py", """
from fastapi import APIRouter

router = APIRouter()

@router.get("/{pattern_id}")
def get_investigation(pattern_id: str):
    # TODO: Implement in later phase
    return {"pattern_id": pattern_id, "explanation": "Pending..."}
""")

write_file("backend/app/api/routes/simulations.py", """
from fastapi import APIRouter

router = APIRouter()

@router.post("/intervention")
def simulate_intervention():
    # TODO: Implement in later phase
    return {"status": "simulated"}
""")

write_file("backend/app/api/routes/evaluation.py", """
from fastapi import APIRouter

router = APIRouter()

@router.get("")
def get_evaluation():
    # TODO: Implement in later phase
    return {}
""")

