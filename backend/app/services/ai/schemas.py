from pydantic import BaseModel
from typing import List, Dict, Optional

class EvidenceCitation(BaseModel):
    claim: str
    evidence_ids: List[str]

class InvestigationReport(BaseModel):
    pattern_id: str
    headline: str
    summary: str
    why_it_matters: str
    observations: List[str]
    supporting_evidence: List[EvidenceCitation]
    contradicting_or_limiting_evidence: List[EvidenceCitation]
    possible_mechanism: str
    financial_exposure: Dict[str, float]
    recommended_control: str
    confidence: str
    limitations: List[str]
