from pydantic import BaseModel
from typing import List

class InvestigationBase(BaseModel):
    investigation_id: str
    pattern_id: str
    explanation: str
    evidence_events: List[dict]
