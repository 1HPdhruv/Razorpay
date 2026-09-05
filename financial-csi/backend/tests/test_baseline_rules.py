import pytest
import pandas as pd
from app.services.risk.scorer import calculate_baseline_rules

def test_duplicate_capture():
    ev_df = pd.DataFrame([
        {'transaction_id': 'T1', 'event_type': 'ORDER_CREATED'},
        {'transaction_id': 'T1', 'event_type': 'CAPTURE_SUCCESS'},
        {'transaction_id': 'T1', 'event_type': 'CAPTURE_SUCCESS'}
    ])
    tx_df = pd.DataFrame([])
    rules = calculate_baseline_rules(tx_df, ev_df)

    assert len(rules) == 1
    assert rules.iloc[0]['rule_id'] == 'R1'
