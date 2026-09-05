from pydantic import BaseModel
from typing import Dict, Any, List

class FinancialDNA(BaseModel):
    transaction_id: str
    atomic: Dict[str, Any]
    financial: Dict[str, Any]
    temporal: Dict[str, Any]
    behavioral: Dict[str, Any]
    lifecycle: Dict[str, Any]
    sequence: Dict[str, Any]
    relational: Dict[str, Any]
    deviation: Dict[str, Any]
    interactions: Dict[str, Any]
