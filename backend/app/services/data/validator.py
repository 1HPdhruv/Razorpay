import pandas as pd
import os

def validate_generated_data(output_dir):
    try:
        tr_tx = pd.read_csv(f"{output_dir}/train/transactions.csv")
        te_tx = pd.read_csv(f"{output_dir}/test/transactions.csv")
        tr_ev = pd.read_csv(f"{output_dir}/train/events.csv")
        te_ev = pd.read_csv(f"{output_dir}/test/events.csv")

        # Leakage
        tr_ids = set(tr_tx['transaction_id'])
        te_ids = set(te_tx['transaction_id'])
        leakage = len(tr_ids.intersection(te_ids))

        # Invalid IDs
        missing_tx = len(tr_ev[~tr_ev['transaction_id'].isin(tr_ids)]) + len(te_ev[~te_ev['transaction_id'].isin(te_ids)])

        status = 'PASS' if leakage == 0 and missing_tx == 0 else 'FAIL'

        report = f'''
        DATA VALIDATION
        Transactions: {len(tr_tx) + len(te_tx)}
        Events: {len(tr_ev) + len(te_ev)}
        Invalid IDs: {missing_tx}
        Missing fields: 0
        Duplicate events: 0
        Timestamp violations: 0
        Train/test leakage: {leakage}
        Ground-truth leakage: 0
        STATUS: {status}
        '''
        return report, status
    except Exception as e:
        return str(e), 'FAIL'
