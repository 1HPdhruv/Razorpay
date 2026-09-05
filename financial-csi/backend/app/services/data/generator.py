import os
import json
import uuid
from datetime import datetime, timedelta
import pandas as pd
import numpy as np

def generate_synthetic_data(num_transactions, seed, output_dir):
    rng = np.random.RandomState(seed)

    # 1. Generate Merchants (100)
    merchants = []
    categories = ['Food', 'Fashion', 'Electronics', 'Travel', 'Education', 'SaaS', 'Healthcare', 'Home & Lifestyle']
    for i in range(100):
        merchants.append({
            'merchant_id': f'MERCH_{rng.randint(10000, 99999)}_{i}',
            'category': rng.choice(categories),
            'baseline_failure_rate': rng.uniform(0.05, 0.2),
            'preferred_gateway': rng.choice(['G1', 'G2', 'G3', 'G4']),
            'aov_paise': int(rng.uniform(50000, 500000))
        })
    df_merchants = pd.DataFrame(merchants)

    # 2. Generate Customers (20% of txns as unique)
    customers = []
    segments = ['NEW', 'REGULAR', 'HIGH_VALUE', 'AT_RISK']
    for i in range(max(10, num_transactions // 5)):
        customers.append({
            'customer_id': f'CUST_{rng.randint(100000, 999999)}_{i}',
            'segment': rng.choice(segments, p=[0.4, 0.4, 0.1, 0.1])
        })
    df_customers = pd.DataFrame(customers)

    events = []
    transactions = []
    ground_truth = []

    start_date = datetime(2023, 1, 1)

    for i in range(num_transactions):
        tx_id = f'TX_{seed}_{i}_{rng.randint(1000, 9999)}'
        order_id = f'ORD_{tx_id}'
        merch = rng.choice(merchants)
        cust = rng.choice(customers)

        amount = int(rng.normal(merch['aov_paise'], merch['aov_paise']*0.2))
        amount = max(1000, amount) # Min 10 INR

        gateway = rng.choice(['G1', 'G2', 'G3', 'G4'], p=[0.4, 0.3, 0.2, 0.1])
        payment_method = rng.choice(['UPI', 'CARD', 'NETBANKING', 'WALLET'], p=[0.5, 0.3, 0.1, 0.1])

        created_at = start_date + timedelta(minutes=int(rng.uniform(0, 500000)))
        current_time = created_at

        tx_events = []
        def add_event(etype, status, amt=None, md=None):
            nonlocal current_time
            tx_events.append({
                'event_id': f'EV_{uuid.uuid4().hex[:8]}',
                'transaction_id': tx_id,
                'order_id': order_id,
                'merchant_id': merch['merchant_id'],
                'event_type': etype,
                'timestamp': current_time,
                'status': status,
                'amount_paise': amt,
                'gateway': gateway,
                'payment_method': payment_method,
                'metadata': md or {}
            })

        add_event('ORDER_CREATED', 'SUCCESS', amount)

        current_time += timedelta(seconds=rng.uniform(0.5, 3))
        add_event('PAYMENT_ATTEMPTED', 'PENDING', amount)

        # Decide path
        is_loss = False
        loss_type = None
        loss_amount = 0
        outcome = 'SUCCESS'

        # Hidden Pattern H1 logic (Gateway G2 + TIMEOUT + retry < 18s + webhook > 5s + amount > 2000)
        h1_active = (gateway == 'G2' and amount > 200000 and rng.random() < 0.1)

        # Hidden Pattern H2 logic (UPI + 1st attempt failed + 2nd success + high webhook latency)
        h2_active = (payment_method == 'UPI' and rng.random() < 0.05)

        first_attempt_fails = h1_active or h2_active or (rng.random() < merch['baseline_failure_rate'])

        if first_attempt_fails:
            current_time += timedelta(seconds=rng.uniform(1, 10))
            fail_code = 'TIMEOUT' if h1_active else rng.choice(['TIMEOUT', 'INSUFFICIENT_FUNDS', 'BANK_DECLINED'])
            add_event('AUTHORIZATION_FAILED', fail_code, amount)

            # Retry
            retry_delay = rng.uniform(2, 15) if h1_active else rng.uniform(20, 300)
            current_time += timedelta(seconds=retry_delay)
            add_event('PAYMENT_RETRIED', 'PENDING', amount)

            if rng.random() < 0.7 or h2_active: # Success on retry
                current_time += timedelta(seconds=rng.uniform(1, 5))
                add_event('AUTHORIZATION_SUCCESS', 'SUCCESS', amount)
                current_time += timedelta(seconds=rng.uniform(0.1, 1))
                add_event('CAPTURE_SUCCESS', 'SUCCESS', amount)

                webhook_delay = rng.uniform(6, 15) if (h1_active or h2_active) else rng.uniform(0.5, 3)
                current_time += timedelta(seconds=webhook_delay)
                add_event('WEBHOOK_RECEIVED', 'SUCCESS')

                # Baseline rule R1: Duplicate capture anomaly (1%)
                if rng.random() < 0.01:
                    current_time += timedelta(seconds=rng.uniform(0.1, 2))
                    add_event('CAPTURE_SUCCESS', 'SUCCESS', amount, {'anomaly': 'duplicate'})
                    is_loss = True
                    loss_type = 'DUPLICATE_CAPTURE'
                    loss_amount = amount
            else:
                outcome = 'FAILED'
                current_time += timedelta(seconds=rng.uniform(1, 5))
                add_event('PAYMENT_FAILED', 'FAILED', amount)
                current_time += timedelta(seconds=rng.uniform(0.5, 3))
                add_event('WEBHOOK_RECEIVED', 'SUCCESS')
        else:
            current_time += timedelta(seconds=rng.uniform(1, 5))
            add_event('AUTHORIZATION_SUCCESS', 'SUCCESS', amount)
            current_time += timedelta(seconds=rng.uniform(0.1, 1))
            add_event('CAPTURE_SUCCESS', 'SUCCESS', amount)
            current_time += timedelta(seconds=rng.uniform(0.5, 3))
            add_event('WEBHOOK_RECEIVED', 'SUCCESS')

            # Baseline rule R2: Refund before capture (impossible state)
            if rng.random() < 0.005:
                # Insert refund event before capture by manipulating last events
                tx_events.insert(-2, {
                    'event_id': f'EV_{uuid.uuid4().hex[:8]}',
                    'transaction_id': tx_id,
                    'order_id': order_id,
                    'merchant_id': merch['merchant_id'],
                    'event_type': 'REFUND_INITIATED',
                    'timestamp': tx_events[-3]['timestamp'] + timedelta(seconds=0.1),
                    'status': 'SUCCESS',
                    'amount_paise': amount,
                    'gateway': gateway,
                    'payment_method': payment_method,
                    'metadata': {}
                })
                is_loss = True
                loss_type = 'REFUND_ERROR'
                loss_amount = amount

        # Settle
        if outcome == 'SUCCESS':
            current_time += timedelta(hours=rng.uniform(24, 72))
            add_event('SETTLEMENT_CREATED', 'PENDING', amount)
            current_time += timedelta(hours=rng.uniform(1, 4))
            add_event('SETTLEMENT_COMPLETED', 'SUCCESS', amount)

            # Apply hidden pattern loss
            if h1_active and rng.random() < 0.8:
                is_loss = True
                loss_type = 'CHARGEBACK'
                loss_amount = amount
                current_time += timedelta(days=rng.uniform(5, 30))
                add_event('CHARGEBACK_CREATED', 'PENDING', amount)

            if h2_active and not is_loss and rng.random() < 0.6:
                is_loss = True
                loss_type = 'PAYMENT_STATE_DIVERGENCE'
                loss_amount = amount

        if h1_active: ground_truth.append({'tx': tx_id, 'pattern': 'H1'})
        if h2_active: ground_truth.append({'tx': tx_id, 'pattern': 'H2'})

        transactions.append({
            'transaction_id': tx_id,
            'order_id': order_id,
            'customer_id': cust['customer_id'],
            'merchant_id': merch['merchant_id'],
            'amount_paise': amount,
            'currency': 'INR',
            'payment_method': payment_method,
            'gateway': gateway,
            'created_at': created_at,
            'completed_at': current_time,
            'outcome': outcome,
            'loss_flag': is_loss,
            'loss_amount': loss_amount,
            'loss_type': loss_type
        })
        events.extend(tx_events)

    df_tx = pd.DataFrame(transactions)
    df_ev = pd.DataFrame(events)

    # Train test split at transaction level
    tx_ids = df_tx['transaction_id'].unique()
    rng.shuffle(tx_ids)
    split_idx = int(len(tx_ids) * 0.8)
    train_tx_ids = set(tx_ids[:split_idx])

    df_tx['split'] = df_tx['transaction_id'].apply(lambda x: 'train' if x in train_tx_ids else 'test')
    df_ev['split'] = df_ev['transaction_id'].apply(lambda x: 'train' if x in train_tx_ids else 'test')

    os.makedirs(f"{output_dir}/train", exist_ok=True)
    os.makedirs(f"{output_dir}/test", exist_ok=True)
    os.makedirs(f"{output_dir}/ground_truth", exist_ok=True)

    df_tx[df_tx['split'] == 'train'].drop(columns=['split']).to_csv(f"{output_dir}/train/transactions.csv", index=False)
    df_tx[df_tx['split'] == 'test'].drop(columns=['split']).to_csv(f"{output_dir}/test/transactions.csv", index=False)

    df_ev[df_ev['split'] == 'train'].drop(columns=['split']).to_csv(f"{output_dir}/train/events.csv", index=False)
    df_ev[df_ev['split'] == 'test'].drop(columns=['split']).to_csv(f"{output_dir}/test/events.csv", index=False)

    pd.DataFrame(ground_truth).to_csv(f"{output_dir}/ground_truth/hidden_patterns.csv", index=False)

    manifest = {
        "seed": seed,
        "transaction_count": num_transactions,
        "merchant_count": 100,
        "train_ratio": 0.8,
        "generator_version": "1.0",
        "total_loss": float(df_tx['loss_amount'].sum())
    }
    with open(f"{output_dir}/manifest.json", "w") as f:
        json.dump(manifest, f)

    return df_tx, df_ev
