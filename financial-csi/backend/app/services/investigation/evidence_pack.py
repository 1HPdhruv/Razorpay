from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.models.pattern import Pattern

class EvidenceItem(BaseModel):
    evidence_id: str
    transaction_id: str
    event_id: Optional[str] = None
    evidence_type: str  # PATTERN_MATCH, LOSS_OUTCOME, TIMING, EVENT_SEQUENCE, FINANCIAL, COMPARISON, BASELINE
    claim: str
    observed_value: str
    source_field: str

class EvidencePack(BaseModel):
    pattern: Pattern
    pattern_statistics: Dict[str, float]
    supporting_loss_examples: List[Dict[str, Any]]
    contrasting_non_loss_examples: List[Dict[str, Any]]
    baseline_examples: List[Dict[str, Any]]
    evidence_items: List[EvidenceItem]
