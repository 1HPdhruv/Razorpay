import argparse
import sys
import os
import json

# Add backend to path so we can import services
sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))

from app.services.data.generator import generate_synthetic_data
from app.services.data.validator import validate_generated_data
from app.services.lifecycle.builder import build_lifecycles
from app.services.features.extractor import extract_features

def main():
    parser = argparse.ArgumentParser(description="Financial CSI Synthetic Data Generator")
    parser.add_argument('--transactions', type=int, default=10000, help='Number of transactions to generate')
    parser.add_argument('--seed', type=int, default=42, help='Deterministic random seed')
    parser.add_argument('--output', type=str, default='data/generated', help='Output directory')

    args = parser.parse_args()

    print(f"Generating {args.transactions} transactions with seed {args.seed}...")
    tx_df, ev_df = generate_synthetic_data(args.transactions, args.seed, args.output)

    # Generate Lifecycles
    print("Building lifecycles...")
    lc_df = build_lifecycles(ev_df)
    train_txs = tx_df[tx_df['split'] == 'train']['transaction_id']
    test_txs = tx_df[tx_df['split'] == 'test']['transaction_id']

    lc_df[lc_df['transaction_id'].isin(train_txs)].to_csv(f"{args.output}/train/lifecycles.csv", index=False)
    lc_df[lc_df['transaction_id'].isin(test_txs)].to_csv(f"{args.output}/test/lifecycles.csv", index=False)

    
    # We do NOT extract advanced features here in Phase 3. 
    # Use build_features.py instead.
    # Validate
    print("Validating data...")
    report, status = validate_generated_data(args.output)
    print(report)

    if status == 'FAIL':
        sys.exit(1)

if __name__ == '__main__':
    main()
