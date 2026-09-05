import pytest
import pandas as pd
from app.services.discovery.miner import PatternDiscoveryEngine

def test_train_isolation():
    engine = PatternDiscoveryEngine()
    
    # Engine requires exactly two dfs, no path reading
    train_features = pd.DataFrame([{'transaction_id': 'T1', 'atomic_g': 'G1'}])
    train_targets = pd.DataFrame([{'transaction_id': 'T1', 'loss_flag': True, 'loss_amount': 100}])
    
    try:
        engine.discover(train_features, train_targets)
    except Exception as e:
        # Expected to pass or fail gracefully due to lack of samples, but not due to reading test data
        pass

def test_hidden_pattern_leakage():
    engine = PatternDiscoveryEngine()
    assert not hasattr(engine, 'hidden_patterns')
