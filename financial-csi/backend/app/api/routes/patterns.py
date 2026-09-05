from fastapi import APIRouter, HTTPException
import json
import os

router = APIRouter()

from app.core.config import settings

@router.get("/")
def get_patterns():
    path = settings.DATA_DIR / "discovered_patterns.json"
    if not path.exists():
        return []
    with open(path, "r") as f:
        return json.load(f)

@router.get("/{pattern_id}")
def get_pattern(pattern_id: str):
    path = settings.DATA_DIR / "discovered_patterns.json"
    if not path.exists():
        raise HTTPException(status_code=404, detail="Patterns not found")
        
    with open(path, "r") as f:
        patterns = json.load(f)
        
    for p in patterns:
        if p['pattern_id'] == pattern_id:
            return p
            
    raise HTTPException(status_code=404, detail="Pattern not found")
