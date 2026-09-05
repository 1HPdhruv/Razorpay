import os
import json
import pandas as pd
from pathlib import Path
from fastapi import APIRouter, HTTPException
from app.models.pattern import Pattern, PatternCondition
from app.services.investigation.evidence import retrieve_evidence
from app.services.ai.provider import AIProvider

router = APIRouter()

# Get the project root directory assuming this file is in backend/app/api/routes
PROJECT_ROOT = Path(__file__).resolve().parents[4]
DATA_DIR = PROJECT_ROOT / "data" / "generated"

@router.get("/{pattern_id}")
async def get_investigation(pattern_id: str):
    patterns_path = DATA_DIR / "discovered_patterns.json"
    if not patterns_path.exists():
        raise HTTPException(status_code=404, detail="Patterns not found")
        
    with open(patterns_path, "r") as f:
        patterns_raw = json.load(f)
        
    pattern_data = next((p for p in patterns_raw if p['pattern_id'] == pattern_id), None)
    if not pattern_data:
        raise HTTPException(status_code=404, detail="Pattern not found")
        
    pattern = Pattern(**pattern_data)
    
    # Load dataset to extract evidence
    feat_df = pd.read_csv(DATA_DIR / "train" / "feature_matrix.csv")
    targets_df = pd.read_csv(DATA_DIR / "train" / "loss_targets.csv")
    feat_df = pd.merge(feat_df, targets_df, on="transaction_id")
    ev_df = pd.read_csv(DATA_DIR / "train" / "events.csv")
    
    evidence_pack = retrieve_evidence(pattern, feat_df, ev_df)
    
    provider = AIProvider()
    report = await provider.generate_investigation(evidence_pack)
    
    return report.model_dump()
