import pytest
import pandas as pd
from app.services.discovery.association import compute_fisher_exact, mine_associations

def test_fisher_exact_significant():
    # Large pattern bias -> very small p_value
    p_val = compute_fisher_exact(100, 9900, 20, 80)
    assert p_val < 0.05

def test_fisher_exact_insignificant():
    # No pattern bias -> large p_value
    p_val = compute_fisher_exact(100, 9900, 1, 99)
    assert p_val > 0.05

def test_mine_associations():
    df = pd.DataFrame([
        {'transaction_id': 'T1', 'atomic_gateway': 'G1', 'temporal_speed': 'FAST'},
        {'transaction_id': 'T2', 'atomic_gateway': 'G1', 'temporal_speed': 'SLOW'},
        {'transaction_id': 'T3', 'atomic_gateway': 'G2', 'temporal_speed': 'FAST'},
        {'transaction_id': 'T4', 'atomic_gateway': 'G1', 'temporal_speed': 'FAST'},
    ])
    
    target_df = pd.DataFrame([
        {'transaction_id': 'T1', 'loss_flag': True, 'loss_amount': 5000},
        {'transaction_id': 'T2', 'loss_flag': False, 'loss_amount': 0},
        {'transaction_id': 'T3', 'loss_flag': False, 'loss_amount': 0},
        {'transaction_id': 'T4', 'loss_flag': True, 'loss_amount': 10000},
    ])
    
    # We should discover G1 + FAST = 2 matches, 2 losses.
    # To test properly we need to lower the constants or just rely on logic
    from app.core.constants import DISCOVERY_CONFIG
    old_min = DISCOVERY_CONFIG['MIN_LOSS_COUNT']
    old_pval = DISCOVERY_CONFIG['P_VALUE_THRESHOLD']
    DISCOVERY_CONFIG['MIN_LOSS_COUNT'] = 1
    DISCOVERY_CONFIG['P_VALUE_THRESHOLD'] = 1.0
    
    cands, baseline, merged = mine_associations(df, target_df)
    
    DISCOVERY_CONFIG['MIN_LOSS_COUNT'] = old_min
    DISCOVERY_CONFIG['P_VALUE_THRESHOLD'] = old_pval
    
    found_g1_fast = False
    for c in cands:
        if set(c['conditions']) == {'atomic_gateway==G1', 'temporal_speed==FAST'}:
            found_g1_fast = True
            assert c['loss_rate'] == 1.0
            
    assert found_g1_fast
