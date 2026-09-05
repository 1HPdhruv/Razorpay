import argparse
import sys
import os
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))
from app.services.features.extractor import extract_features, to_flat_matrix
from app.services.features.quality import check_feature_quality
from app.services.data.targets import extract_targets

def main():
    parser = argparse.ArgumentParser(description="Financial CSI Feature Builder")
    parser.add_argument('--input', type=str, required=True, help='Input directory with generated data')
    parser.add_argument('--output', type=str, required=True, help='Output directory for features')
    args = parser.parse_args()
    
    for split in ['train', 'test']:
        print(f"Processing {split} split...")
        tx_path = f"{args.input}/{split}/transactions.csv"
        ev_path = f"{args.input}/{split}/events.csv"
        
        if not os.path.exists(tx_path) or not os.path.exists(ev_path):
            print(f"Skipping {split}, data not found.")
            continue
            
        tx_df = pd.read_csv(tx_path)
        ev_df = pd.read_csv(ev_path)
        
        # 1. Targets
        extract_targets(tx_df, f"{args.output}/{split}/loss_targets.csv")
        
        # 2. Features
        dna_list = extract_features(tx_df, ev_df)
        matrix = to_flat_matrix(dna_list)
        
        # Drop loss flag from tx_df if doing full extraction to avoid target leakage, 
        # but my extractor strictly uses row_tx['amount_paise'], 'gateway', 'payment_method', 'outcome', etc. 
        # Outcome is an atomic feature (as per Phase 3 prompt), but we shouldn't use loss_flag in discovery matrix.
        # My extractor doesn't add loss_flag.
        
        matrix.to_csv(f"{args.output}/{split}/feature_matrix.csv", index=False)
        
        if split == 'train':
            print("Checking feature quality on train split...")
            report = check_feature_quality(matrix, args.output)
            print(report)

if __name__ == '__main__':
    main()
