import pytest
from app.models.simulation import Scenario, CostModel, Intervention
from app.models.pattern import Pattern, PatternCondition
from app.services.simulation.counterfactual import CounterfactualEngine
from app.services.simulation.safety import enforce_safety_policy

def test_simulation_reproducibility():
    engine = CounterfactualEngine()
    p = Pattern(
        pattern_id="P1", name="P1", description="Test", pattern_type="ASSOCIATION",
        conditions=[PatternCondition(feature="x", operator="==", value="1")],
        support=0.5, matching_transaction_count=20, loss_count=2, loss_rate=1.0,
        baseline_loss_rate=0.25, risk_multiplier=4.0, lift=4.0, p_value=0.01,
        exposure_amount=1000, average_loss_amount=1000, discovery_method="test",
        feature_importance={}, evidence_transaction_ids=[], is_predefined=False
    )
    sc = Scenario(
        scenario_id="S1", name="Test", description="Test",
        intervention=Intervention(intervention_id="I1", name="I1", description="desc", action_type="TEST", expected_delay_seconds=10, risk_level="LOW", requires_merchant_approval=False, enabled=True),
        effectiveness=0.8,
        cost_model=CostModel(intervention_cost_paise=10, false_positive_cost_paise=50),
        stopping_rules=[]
    )
    
    tx = [
        {'loss_flag': True, 'loss_amount': 100},
        {'loss_flag': True, 'loss_amount': 200},
        {'loss_flag': False, 'loss_amount': 0}
    ]
    
    # Test 1: Same seed + same inputs -> same simulation result
    res1 = engine.simulate(p, sc, tx, runs=100, seed=42)
    res2 = engine.simulate(p, sc, tx, runs=100, seed=42)
    assert res1.estimated_prevented_loss_paise == res2.estimated_prevented_loss_paise
    assert res1.confidence_interval['p10'] == res2.confidence_interval['p10']
    
    # Test 7: False positive cost is included
    assert res1.false_positive_cost_paise == 1 * 50
    assert res1.intervention_cost_paise == 3 * 10
    
    # Test 4: Negative net benefit produces DO_NOT_INTERVENE
    sc_bad = Scenario(
        scenario_id="S2", name="Bad", description="Test",
        intervention=Intervention(intervention_id="I2", name="I2", description="desc", action_type="TEST", expected_delay_seconds=10, risk_level="LOW", requires_merchant_approval=False, enabled=True),
        effectiveness=0.1,
        cost_model=CostModel(intervention_cost_paise=100000, false_positive_cost_paise=50000),
        stopping_rules=[]
    )
    res3 = engine.simulate(p, sc_bad, tx, runs=100, seed=42)
    assert res3.net_estimated_benefit_paise < 0
    assert res3.recommendation == "DO_NOT_INTERVENE"

    # Test 5: Insufficient confidence produces MANUAL_REVIEW
    p_low = Pattern(
        pattern_id="P1", name="P1", description="Test", pattern_type="ASSOCIATION",
        conditions=[PatternCondition(feature="x", operator="==", value="1")],
        support=0.5, matching_transaction_count=2, loss_count=2, loss_rate=1.0,
        baseline_loss_rate=0.25, risk_multiplier=4.0, lift=4.0, p_value=1.0, # High P Value
        exposure_amount=1000, average_loss_amount=1000, discovery_method="test",
        feature_importance={}, evidence_transaction_ids=[], is_predefined=False
    )
    res4 = engine.simulate(p_low, sc, tx, runs=100, seed=42)
    assert res4.recommendation == "REQUIRE_MANUAL_REVIEW"
    
def test_simulation_safety():
    # Test 6: No simulation can trigger real Razorpay actions
    with pytest.raises(ValueError):
        enforce_safety_policy({"execute_real_money_action": True})
