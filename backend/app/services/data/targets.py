import pandas as pd

def extract_targets(tx_df, output_path):
    targets = tx_df[['transaction_id', 'loss_flag', 'loss_amount', 'loss_type']]
    targets.to_csv(output_path, index=False)
