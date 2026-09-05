from app.models.simulation import Intervention, Scenario, CostModel

INTERVENTIONS = {
    "REQUIRE_VERIFICATION": Intervention(
        intervention_id="REQUIRE_VERIFICATION",
        name="Require Verification",
        description="Temporarily hold transaction until secondary verification completes.",
        action_type="REQUIRE_VERIFICATION",
        expected_delay_seconds=300,
        risk_level="MEDIUM",
        requires_merchant_approval=True,
        enabled=True
    ),
    "HOLD_SECOND_CAPTURE": Intervention(
        intervention_id="HOLD_SECOND_CAPTURE",
        name="Hold Second Capture",
        description="Prevent duplicate captures on fast retries by holding the state.",
        action_type="HOLD_SECOND_CAPTURE",
        expected_delay_seconds=60,
        risk_level="LOW",
        requires_merchant_approval=False,
        enabled=True
    ),
    "DELAY_RETRY": Intervention(
        intervention_id="DELAY_RETRY",
        name="Delay Retry",
        description="Force artificial latency on retries to ensure webhooks sync.",
        action_type="DELAY_RETRY",
        expected_delay_seconds=30,
        risk_level="LOW",
        requires_merchant_approval=False,
        enabled=True
    ),
    "MERCHANT_ESCALATION": Intervention(
        intervention_id="MERCHANT_ESCALATION",
        name="Merchant Escalation",
        description="Escalate high-risk event entirely to merchant dashboard for manual review.",
        action_type="ESCALATE_TO_MERCHANT",
        expected_delay_seconds=86400,
        risk_level="HIGH",
        requires_merchant_approval=True,
        enabled=True
    )
}

def get_default_scenarios():
    return [
        Scenario(
            scenario_id="SCENARIO_CONSERVATIVE",
            name="Conservative",
            description="Low intervention effectiveness assumption, high false-positive penalty.",
            intervention=INTERVENTIONS["REQUIRE_VERIFICATION"],
            effectiveness=0.60,
            cost_model=CostModel(intervention_cost_paise=500, false_positive_cost_paise=2000), # 5 INR per int, 20 INR per FP
            stopping_rules=["IF_NET_BENEFIT_NEGATIVE"]
        ),
        Scenario(
            scenario_id="SCENARIO_BALANCED",
            name="Balanced",
            description="Moderate effectiveness, balanced cost penalties.",
            intervention=INTERVENTIONS["HOLD_SECOND_CAPTURE"],
            effectiveness=0.75,
            cost_model=CostModel(intervention_cost_paise=100, false_positive_cost_paise=500), # 1 INR per int, 5 INR per FP
            stopping_rules=["IF_NET_BENEFIT_NEGATIVE"]
        ),
        Scenario(
            scenario_id="SCENARIO_AGGRESSIVE",
            name="Aggressive",
            description="High effectiveness, lower false-positive penalty sensitivity.",
            intervention=INTERVENTIONS["DELAY_RETRY"],
            effectiveness=0.90,
            cost_model=CostModel(intervention_cost_paise=50, false_positive_cost_paise=100), # 0.5 INR per int, 1 INR per FP
            stopping_rules=[]
        )
    ]
