import pandas as pd

def build_lifecycles(events_df):
    events_df['timestamp'] = pd.to_datetime(events_df['timestamp'])
    sorted_ev = events_df.sort_values(by=['transaction_id', 'timestamp'])

    lifecycles = []
    for tx_id, group in sorted_ev.groupby('transaction_id'):
        lc_str = []
        for _, row in group.iterrows():
            lc_str.append(f"{row['event_type']} ({row['timestamp'].strftime('%H:%M:%S.%f')[:-3]})")

        lifecycles.append({
            'transaction_id': tx_id,
            'lifecycle': " -> ".join(lc_str)
        })
    return pd.DataFrame(lifecycles)
