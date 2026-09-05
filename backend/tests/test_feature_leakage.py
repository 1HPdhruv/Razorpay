import pytest
import pandas as pd
from app.services.features.extractor import extract_features, to_flat_matrix

def test_feature_leakage():
    # A refund event occurring later in time should not affect the time_to_webhook calculation
    tx = pd.DataFrame([{
        'transaction_id': 'T1', 'merchant_id': 'M1', 'amount_paise': 500000, 
        'gateway': 'G1', 'payment_method': 'CARD', 'outcome': 'SUCCESS', 'loss_flag': True
    }])
    ev1 = pd.DataFrame([
        {'transaction_id': 'T1', 'merchant_id': 'M1', 'order_id': 'O1', 'event_type': 'ORDER_CREATED', 'timestamp': '2023-01-01 10:00:00'},
        {'transaction_id': 'T1', 'merchant_id': 'M1', 'order_id': 'O1', 'event_type': 'WEBHOOK_RECEIVED', 'timestamp': '2023-01-01 10:00:10'}
    ])
    ev2 = pd.DataFrame([
        {'transaction_id': 'T1', 'merchant_id': 'M1', 'order_id': 'O1', 'event_type': 'ORDER_CREATED', 'timestamp': '2023-01-01 10:00:00'},
        {'transaction_id': 'T1', 'merchant_id': 'M1', 'order_id': 'O1', 'event_type': 'WEBHOOK_RECEIVED', 'timestamp': '2023-01-01 10:00:10'},
        {'transaction_id': 'T1', 'merchant_id': 'M1', 'order_id': 'O1', 'event_type': 'REFUND_COMPLETED', 'timestamp': '2023-01-02 10:00:00'}
    ])
    
    dna1 = extract_features(tx, ev1)[0]
    dna2 = extract_features(tx, ev2)[0]
    
    assert dna1['temporal']['time_payment_to_webhook_ms'] == dna2['temporal']['time_payment_to_webhook_ms']
    
    flat2 = to_flat_matrix([dna2])
    assert 'loss_flag' not in flat2.columns
