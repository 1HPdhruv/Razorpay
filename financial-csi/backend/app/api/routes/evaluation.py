import json
from pathlib import Path
from fastapi import APIRouter, HTTPException

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[4]
DATA_DIR = PROJECT_ROOT / "docs" / "generated"

@router.get("")
def get_evaluation():
    eval_file = DATA_DIR / "final_evaluation.json"
    if not eval_file.exists():
        raise HTTPException(status_code=404, detail="Evaluation not found. Run final evaluation script.")
        
    with open(eval_file, "r") as f:
        return json.load(f)
