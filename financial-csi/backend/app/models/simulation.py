from pydantic import BaseModel
from typing import List, Dict, Optional, Literal

class Intervention(BaseModel):
    intervention_id: str
    name: str
    description: str
    action_type: str # e.g. REQUIRE_VERIFICATION, HOLD_SECOND_CAPTURE
    expected_delay_seconds: int
    risk_level: str # LOW, MEDIUM, HIGH
    requires_merchant_approval: bool
    enabled: bool

class CostModel(BaseModel):
    intervention_cost_paise: int
    false_positive_cost_paise: int

class Scenario(BaseModel):
    scenario_id: str
    name: str
    description: str
    intervention: Intervention
    effectiveness: float # 0.0 to 1.0
    cost_model: CostModel
    stopping_rules: List[str]

class SimulationResult(BaseModel):
    simulation_id: str
    pattern_id: str
    scenario_id: str
    transactions_evaluated: int
    observed_loss_paise: int
    estimated_prevented_loss_paise: int
    estimated_residual_loss_paise: int
    intervention_cost_paise: int
    false_positive_cost_paise: int
    net_estimated_benefit_paise: int
    prevention_rate: float
    assumption_effectiveness: float
    simulation_runs: int
    confidence_interval: Dict[str, int] # p10, median, p90 (paise)
    limitations: List[str]
    recommendation: Literal["RECOMMEND_INTERVENTION", "DO_NOT_INTERVENE", "REQUIRE_MANUAL_REVIEW"]
