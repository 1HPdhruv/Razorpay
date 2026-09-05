def calculate_baseline_rules(tx_df, ev_df):
    rules = []
    for tx_id, tx_group in ev_df.groupby('transaction_id'):
        types = tx_group['event_type'].tolist()

        if types.count('CAPTURE_SUCCESS') > 1:
            rules.append({'transaction_id': tx_id, 'rule_id': 'R1', 'reason': 'Duplicate capture'})

        if 'REFUND_INITIATED' in types and 'CAPTURE_SUCCESS' in types:
            r_idx = types.index('REFUND_INITIATED')
            c_idx = types.index('CAPTURE_SUCCESS')
            if r_idx < c_idx:
                rules.append({'transaction_id': tx_id, 'rule_id': 'R2', 'reason': 'Refund before capture'})

        if types.count('PAYMENT_RETRIED') > 3:
            rules.append({'transaction_id': tx_id, 'rule_id': 'R3', 'reason': 'Excessive retries'})

    import pandas as pd
    return pd.DataFrame(rules)
