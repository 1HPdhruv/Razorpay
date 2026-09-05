import pytest
import pandas as pd
from app.services.features.extractor import extract_features, to_flat_matrix
from app.core.constants import TEMPORAL_BUCKETS, AMOUNT_BANDS

def test_feature_engineering_sequence():
    tx = pd.DataFrame([{
        'transaction_id': 'T1', 'merchant_id': 'M1', 'amount_paise': 500000, 
        'gateway': 'G1', 'payment_method': 'CARD', 'outcome': 'SUCCESS'
    }])
    ev = pd.DataFrame([
        {'transaction_id': 'T1', 'merchant_id': 'M1', 'order_id': 'O1', 'event_type': 'AUTHORIZATION_FAILED', 'timestamp': '2023-01-01 10:00:00'},
        {'transaction_id': 'T1', 'merchant_id': 'M1', 'order_id': 'O1', 'event_type': 'PAYMENT_RETRIED', 'timestamp': '2023-01-01 10:00:10'},
        {'transaction_id': 'T1', 'merchant_id': 'M1', 'order_id': 'O1', 'event_type': 'AUTHORIZATION_SUCCESS', 'timestamp': '2023-01-01 10:00:12'},
    ])
    
    dna = extract_features(tx, ev)[0]
    
    assert dna['temporal']['retry_speed_bucket'] == 'FAST'
    assert dna['sequence'].get('AUTHORIZATION_FAILED -> PAYMENT_RETRIED') == 1
    assert 'AUTHORIZATION_FAILED -> PAYMENT_RETRIED [FAST]' in dna['sequence']
    
def test_feature_deterministic():
    tx = pd.DataFrame([{'transaction_id': 'T1', 'merchant_id': 'M1', 'amount_paise': 50000, 'gateway': 'G1', 'payment_method': 'CARD', 'outcome': 'SUCCESS'}])
    ev = pd.DataFrame([{'transaction_id': 'T1', 'merchant_id': 'M1', 'order_id': 'O1', 'event_type': 'ORDER_CREATED', 'timestamp': '2023-01-01 10:00:00'}])
    dna1 = extract_features(tx, ev)
    dna2 = extract_features(tx, ev)
    assert dna1 == dna2
