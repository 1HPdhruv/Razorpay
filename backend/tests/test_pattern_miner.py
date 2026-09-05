import pytest
from app.services.discovery.miner import PatternDiscoveryEngine
from app.models.pattern import Pattern
import pandas as pd

def test_deduplication():
    # Mock candidates
    engine = PatternDiscoveryEngine()
    
    train_feat = pd.DataFrame([
        {'transaction_id': 'T1', 'f1': 'A', 'f2': 'B'},
        {'transaction_id': 'T2', 'f1': 'A', 'f2': 'B'},
        {'transaction_id': 'T3', 'f1': 'C', 'f2': 'D'},
    ])
    
    train_tgt = pd.DataFrame([
        {'transaction_id': 'T1', 'loss_flag': True, 'loss_amount': 10},
        {'transaction_id': 'T2', 'loss_flag': True, 'loss_amount': 20},
        {'transaction_id': 'T3', 'loss_flag': False, 'loss_amount': 0},
    ])
    
    # We must lower thresholds to find this
    from app.core.constants import DISCOVERY_CONFIG
    old_min = DISCOVERY_CONFIG['MIN_LOSS_COUNT']
    old_pval = DISCOVERY_CONFIG['P_VALUE_THRESHOLD']
    DISCOVERY_CONFIG['MIN_LOSS_COUNT'] = 1
    DISCOVERY_CONFIG['P_VALUE_THRESHOLD'] = 1.0
    
    patterns = engine.discover(train_feat, train_tgt)
    
    DISCOVERY_CONFIG['MIN_LOSS_COUNT'] = old_min
    DISCOVERY_CONFIG['P_VALUE_THRESHOLD'] = old_pval
    
    # We expect deduplication to remove f1=A and f2=B if they are identical sets
    # Because they perfectly overlap!
    assert len(patterns) == 1
    assert patterns[0].conditions[0].feature in ['f1', 'f2']
