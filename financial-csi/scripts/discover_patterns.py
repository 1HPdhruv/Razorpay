import argparse
import sys
import os
import pandas as pd
import json

sys.path.append(os.path.join(os.path.dirname(__file__), '../backend'))
from app.services.discovery.miner import PatternDiscoveryEngine

def main():
    parser = argparse.ArgumentParser(description="Financial CSI Pattern Discovery")
    parser.add_argument('--input', type=str, required=True, help='Input directory with features')
    parser.add_argument('--output', type=str, required=True, help='Output directory for patterns')
    args = parser.parse_args()
    
    # 1. strictly load train data
    feat_path = f"{args.input}/train/feature_matrix.csv"
    targets_path = f"{args.input}/train/loss_targets.csv"
    
    print("Loading training data ONLY...")
    feat_df = pd.read_csv(feat_path)
    targets_df = pd.read_csv(targets_path)
    
    print(f"Features: {feat_df.shape}")
    print(f"Targets: {targets_df.shape}")
    
    engine = PatternDiscoveryEngine()
    patterns = engine.discover(feat_df, targets_df)
    
    print(f"Discovered {len(patterns)} significant patterns.")
    
    # Serialize
    pattern_dicts = [p.model_dump() for p in patterns]
    
    with open(f"{args.output}/discovered_patterns.json", "w") as f:
        json.dump(pattern_dicts, f, indent=2)
        
    flat_patterns = []
    for p in pattern_dicts:
        flat = p.copy()
        flat['conditions'] = " AND ".join([f"{c['feature']}=={c['value']}" for c in flat['conditions']])
        del flat['feature_importance']
        del flat['evidence_transaction_ids']
        flat_patterns.append(flat)
        
    pd.DataFrame(flat_patterns).to_csv(f"{args.output}/discovered_patterns.csv", index=False)
    
    report = {
        "transactions_analyzed": len(feat_df),
        "patterns_discovered": len(patterns),
        "emergent_patterns": len([p for p in patterns if p.status == 'EMERGENT']),
        "top_pattern": pattern_dicts[0]['description'] if patterns else None
    }
    
    with open(f"{args.output}/discovery_experiment.json", "w") as f:
        json.dump(report, f, indent=2)

if __name__ == '__main__':
    main()
