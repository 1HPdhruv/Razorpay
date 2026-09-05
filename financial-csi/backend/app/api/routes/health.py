from fastapi import APIRouter
import json
from pathlib import Path

from app.core.config import settings
import os

router = APIRouter()

@router.get("/health")
def check_health():
    eval_file = settings.DOCS_DIR / "final_evaluation.json"
    eval_data = None
    if eval_file.exists():
        with open(eval_file, "r") as f:
            eval_data = json.load(f)
            
    # Count patterns
    pattern_file = settings.DATA_DIR / "discovered_patterns.json"
    pattern_count = 0
    if pattern_file.exists():
        with open(pattern_file, "r") as f:
            pattern_count = len(json.load(f))
            
    manifest_path = settings.DATA_DIR / "manifest.json"
    dataset_loaded = (settings.DATA_DIR / "train" / "loss_targets.csv").exists()
    transaction_count = 0
    
    if manifest_path.exists():
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
            transaction_count = manifest.get('transaction_count', 0)

    return {
        "status": "ok", 
        "version": "0.2.0",
        "dataset_loaded": dataset_loaded,
        "transaction_count": transaction_count,
        "pattern_count": pattern_count,
        "evaluation": eval_data
    }
