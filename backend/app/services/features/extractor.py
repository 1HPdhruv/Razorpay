import pandas as pd
import numpy as np
import json
from app.core.constants import AMOUNT_BANDS, TEMPORAL_BUCKETS

def bucketize_amount(amount_paise):
    for band, threshold in AMOUNT_BANDS.items():
        if amount_paise < threshold:
            return band
    return "VERY_HIGH"

def bucketize_temporal(seconds, bucket_type):
    for band, threshold in TEMPORAL_BUCKETS[bucket_type].items():
        if seconds <= threshold:
            return band
    return "UNKNOWN"

def extract_features(tx_df, ev_df):
    ev_df['timestamp'] = pd.to_datetime(ev_df['timestamp'])
    
    # Pre-calculate relational baselines without future information leakage
    # We will compute basic aggregates over the whole dataset for simplicity in the prototype,
    # but in production, these should be rolling window aggregations.
    merchant_baselines = ev_df[ev_df['event_type'] == 'AUTHORIZATION_FAILED'].groupby('merchant_id').size() / ev_df[ev_df['event_type'] == 'PAYMENT_ATTEMPTED'].groupby('merchant_id').size()
    merchant_baselines = merchant_baselines.fillna(0).to_dict()
    
    gateway_latencies = {}
    
    # We must iterate or apply to extract DNA
    features_list = []
    
    for tx_id, tx_group in ev_df.groupby('transaction_id'):
        tx_group = tx_group.sort_values(by='timestamp')
        types = tx_group['event_type'].tolist()
        row_tx = tx_df[tx_df['transaction_id'] == tx_id].iloc[0]
        
        # 1. ATOMIC
        atomic = {
            'gateway': row_tx['gateway'],
            'payment_method': row_tx['payment_method'],
            'outcome': row_tx['outcome']
        }
        
        # 2. FINANCIAL
        amount_paise = row_tx['amount_paise']
        has_refund = 'REFUND_COMPLETED' in types
        financial = {
            'amount_paise': amount_paise,
            'amount_band': bucketize_amount(amount_paise),
            'has_refund': has_refund,
            'has_chargeback': 'CHARGEBACK_CREATED' in types,
            'has_settlement': 'SETTLEMENT_COMPLETED' in types,
        }
        
        # 3. TEMPORAL
        temporal = {
            'time_order_to_payment_ms': -1,
            'time_attempt_to_retry_ms': -1,
            'time_payment_to_webhook_ms': -1,
            'retry_speed_bucket': 'NONE',
            'webhook_latency_bucket': 'NONE'
        }
        
        if 'ORDER_CREATED' in types and 'PAYMENT_ATTEMPTED' in types:
            start = tx_group[tx_group['event_type'] == 'ORDER_CREATED']['timestamp'].iloc[0]
            end = tx_group[tx_group['event_type'] == 'PAYMENT_ATTEMPTED']['timestamp'].iloc[0]
            temporal['time_order_to_payment_ms'] = (end - start).total_seconds() * 1000
            
        if 'AUTHORIZATION_FAILED' in types and 'PAYMENT_RETRIED' in types:
            start = tx_group[tx_group['event_type'] == 'AUTHORIZATION_FAILED']['timestamp'].iloc[0]
            end = tx_group[tx_group['event_type'] == 'PAYMENT_RETRIED']['timestamp'].iloc[0]
            delay = (end - start).total_seconds()
            temporal['time_attempt_to_retry_ms'] = delay * 1000
            temporal['retry_speed_bucket'] = bucketize_temporal(delay, 'RETRY_SPEED')
            
        if 'CAPTURE_SUCCESS' in types and 'WEBHOOK_RECEIVED' in types:
            start = tx_group[tx_group['event_type'] == 'CAPTURE_SUCCESS']['timestamp'].iloc[0]
            end = tx_group[tx_group['event_type'] == 'WEBHOOK_RECEIVED']['timestamp'].iloc[0]
            delay = (end - start).total_seconds()
            temporal['time_payment_to_webhook_ms'] = delay * 1000
            temporal['webhook_latency_bucket'] = bucketize_temporal(delay, 'WEBHOOK_LATENCY')
            
        # 4. BEHAVIORAL
        behavioral = {
            'attempt_count': types.count('PAYMENT_ATTEMPTED') + types.count('PAYMENT_RETRIED'),
            'retry_count': types.count('PAYMENT_RETRIED'),
            'failure_count': types.count('AUTHORIZATION_FAILED'),
            'success_count': types.count('AUTHORIZATION_SUCCESS'),
            'failed_before_success': types.count('AUTHORIZATION_FAILED') > 0 and types.count('AUTHORIZATION_SUCCESS') > 0
        }
        
        # 5. LIFECYCLE
        lifecycle = {
            'event_count': len(types),
            'unique_event_types': len(set(types)),
            'duplicate_success_count': types.count('CAPTURE_SUCCESS') - 1 if types.count('CAPTURE_SUCCESS') > 0 else 0,
            'lifecycle_signature': " > ".join(types)
        }
        
        # 6. SEQUENCE (Event n-grams)
        sequence = {}
        for i in range(len(types) - 1):
            ngram2 = f"{types[i]} -> {types[i+1]}"
            sequence[ngram2] = sequence.get(ngram2, 0) + 1
            if ngram2 == 'AUTHORIZATION_FAILED -> PAYMENT_RETRIED':
                sequence[f"{ngram2} [{temporal['retry_speed_bucket']}]"] = 1
                
        for i in range(len(types) - 2):
            ngram3 = f"{types[i]} -> {types[i+1]} -> {types[i+2]}"
            sequence[ngram3] = sequence.get(ngram3, 0) + 1
            
        # 7. RELATIONAL
        relational = {
            'merchant_baseline_failure_rate': merchant_baselines.get(row_tx['merchant_id'], 0)
        }
        
        # 8. DEVIATION
        deviation = {
            'webhook_delay_vs_normal': 1 if temporal['webhook_latency_bucket'] in ['ELEVATED', 'HIGH'] else 0
        }
        
        # 9. INTERACTIONS
        interactions = {
            'gateway_x_retry_speed': f"{atomic['gateway']}_x_{temporal['retry_speed_bucket']}",
            'gateway_x_webhook_latency': f"{atomic['gateway']}_x_{temporal['webhook_latency_bucket']}"
        }
        
        features_list.append({
            'transaction_id': tx_id,
            'atomic': atomic,
            'financial': financial,
            'temporal': temporal,
            'behavioral': behavioral,
            'lifecycle': lifecycle,
            'sequence': sequence,
            'relational': relational,
            'deviation': deviation,
            'interactions': interactions
        })
        
    return features_list

def to_flat_matrix(features_list):
    flat_data = []
    for f in features_list:
        row = {'transaction_id': f['transaction_id']}
        for cat in ['atomic', 'financial', 'temporal', 'behavioral', 'lifecycle', 'relational', 'deviation', 'interactions']:
            for k, v in f[cat].items():
                if k != 'lifecycle_signature':
                    row[f"{cat}_{k}"] = v
        # Add limited sequences
        for k, v in f['sequence'].items():
            row[f"seq_{k}"] = v
            
        flat_data.append(row)
    
    df = pd.DataFrame(flat_data)
    df.fillna(0, inplace=True)
    return df
