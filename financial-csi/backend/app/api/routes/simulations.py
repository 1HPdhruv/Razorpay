import os
import json
import pandas as pd
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.models.pattern import Pattern
from app.services.simulation.intervention import get_default_scenarios, INTERVENTIONS
from app.services.simulation.counterfactual import CounterfactualEngine

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[4]
DATA_DIR = PROJECT_ROOT / "data" / "generated"

class SimulationRequest(BaseModel):
    pattern_id: str
    scenario_id: str
    seed: int = 42
    runs: int = 1000

@router.get("/pattern/{pattern_id}")
def get_scenarios(pattern_id: str):
    # Simply returns available scenarios
    scenarios = get_default_scenarios()
    return {"scenarios": [s.model_dump() for s in scenarios]}

@router.post("/intervention")
def simulate_intervention(req: SimulationRequest):
    patterns_path = DATA_DIR / "discovered_patterns.json"
    if not patterns_path.exists():
        raise HTTPException(status_code=404, detail="Patterns not found")
        
    with open(patterns_path, "r") as f:
        patterns_raw = json.load(f)
        
    pattern_data = next((p for p in patterns_raw if p['pattern_id'] == req.pattern_id), None)
    if not pattern_data:
        raise HTTPException(status_code=404, detail="Pattern not found")
        
    pattern = Pattern(**pattern_data)
    scenarios = get_default_scenarios()
    scenario = next((s for s in scenarios if s.scenario_id == req.scenario_id), None)
    if not scenario:
        raise HTTPException(status_code=404, detail="Scenario not found")
        
    feat_df = pd.read_csv(DATA_DIR / "train" / "feature_matrix.csv")
    targets_df = pd.read_csv(DATA_DIR / "train" / "loss_targets.csv")
    feat_df = pd.merge(feat_df, targets_df, on="transaction_id")
    
    # filter df based on pattern condition
    mask = pd.Series([True]*len(feat_df), index=feat_df.index)
    for cond in pattern.conditions:
        f_name = cond.feature
        v = cond.value
        op = cond.operator
        if op == '==':
            mask &= (feat_df[f_name] == v)
            
    matched_df = feat_df[mask]
    matched_tx = matched_df.to_dict(orient='records')
    
    engine = CounterfactualEngine()
    result = engine.simulate(pattern, scenario, matched_tx, req.runs, req.seed)
    
    return result.model_dump()
