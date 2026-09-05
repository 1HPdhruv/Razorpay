from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class PatternCondition(BaseModel):
    feature: str
    operator: str
    value: Any

class Pattern(BaseModel):
    pattern_id: str
    name: str
    description: str
    pattern_type: str  # e.g. ASSOCIATION, ANOMALY, CLUSTER, BASELINE
    conditions: List[PatternCondition]
    support: float
    matching_transaction_count: int
    loss_count: int
    loss_rate: float
    baseline_loss_rate: float
    risk_multiplier: float
    lift: float
    p_value: float
    confidence_interval: Optional[List[float]] = None
    exposure_amount: float
    average_loss_amount: float
    discovery_method: str
    feature_importance: Dict[str, float]
    evidence_transaction_ids: List[str]
    is_predefined: bool = False
    stability_score: float = 0.0
    status: str = "EMERGENT" # KNOWN or EMERGENT
