import pytest
import pandas as pd
from app.services.investigation.evidence import retrieve_evidence
from app.models.pattern import Pattern, PatternCondition

def test_evidence_extraction():
    p = Pattern(
        pattern_id="P1", name="P1", description="Test", pattern_type="ASSOCIATION",
        conditions=[PatternCondition(feature="atomic_gateway", operator="==", value="G1")],
        support=0.5, matching_transaction_count=2, loss_count=1, loss_rate=0.5,
        baseline_loss_rate=0.25, risk_multiplier=2.0, lift=2.0, p_value=0.01,
        exposure_amount=1000, average_loss_amount=1000, discovery_method="test",
        feature_importance={}, evidence_transaction_ids=[], is_predefined=False
    )
    
    feat_df = pd.DataFrame([
        {'transaction_id': 'T1', 'atomic_gateway': 'G1', 'loss_flag': True, 'loss_amount': 1000},
        {'transaction_id': 'T2', 'atomic_gateway': 'G1', 'loss_flag': False, 'loss_amount': 0},
        {'transaction_id': 'T3', 'atomic_gateway': 'G2', 'loss_flag': False, 'loss_amount': 0},
    ])
    
    ev_df = pd.DataFrame() # Not strictly needed for basic matching test
    
    pack = retrieve_evidence(p, feat_df, ev_df)
    
    # We should have 1 supporting loss example and 1 contrasting non-loss
    assert len(pack.supporting_loss_examples) == 1
    assert pack.supporting_loss_examples[0]['transaction_id'] == 'T1'
    
    assert len(pack.contrasting_non_loss_examples) == 1
    assert pack.contrasting_non_loss_examples[0]['transaction_id'] == 'T2'
    
    # Baseline examples are those NOT matching the pattern
    assert len(pack.baseline_examples) == 1
    assert pack.baseline_examples[0]['transaction_id'] == 'T3'
    
    assert len(pack.evidence_items) == 2
