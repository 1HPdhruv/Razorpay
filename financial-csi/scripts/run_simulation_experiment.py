import sys
import os
import json
import pandas as pd
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / "backend"))

from app.models.pattern import Pattern
from app.services.simulation.intervention import get_default_scenarios
from app.services.simulation.counterfactual import CounterfactualEngine

def main():
    DATA_DIR = PROJECT_ROOT / "data" / "generated"
    
    with open(DATA_DIR / "discovered_patterns.json", "r") as f:
        patterns_raw = json.load(f)
        
    # Get the strongest pattern (usually the first one since they are sorted by score/lift)
    pattern_data = patterns_raw[0]
    pattern = Pattern(**pattern_data)
    
    print(f"Running simulation for Pattern: {pattern.pattern_id} - {pattern.description}")
    
    # Load dataset
    feat_df = pd.read_csv(DATA_DIR / "train" / "feature_matrix.csv")
    targets_df = pd.read_csv(DATA_DIR / "train" / "loss_targets.csv")
    feat_df = pd.merge(feat_df, targets_df, on="transaction_id")
    
    mask = pd.Series([True]*len(feat_df), index=feat_df.index)
    for cond in pattern.conditions:
        f_name = cond.feature
        v = cond.value
        op = cond.operator
        if op == '==':
            mask &= (feat_df[f_name] == v)
            
    matched_df = feat_df[mask]
    matched_tx = matched_df.to_dict(orient='records')
    
    print(f"Matched {len(matched_tx)} transactions.")
    
    engine = CounterfactualEngine()
    scenarios = get_default_scenarios()
    
    results = {}
    
    for scenario in scenarios:
        res = engine.simulate(pattern, scenario, matched_tx, runs=1000, seed=42)
        results[scenario.scenario_id] = {
            "name": scenario.name,
            "intervention": scenario.intervention.name,
            "effectiveness": scenario.effectiveness,
            "observed_loss_paise": res.observed_loss_paise,
            "estimated_prevented_loss_paise": res.estimated_prevented_loss_paise,
            "intervention_cost_paise": res.intervention_cost_paise,
            "false_positive_cost_paise": res.false_positive_cost_paise,
            "net_estimated_benefit_paise": res.net_estimated_benefit_paise,
            "recommendation": res.recommendation
        }
        
    output_path = DATA_DIR / "intervention_comparison.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
        
    print(f"Saved results to {output_path}")

if __name__ == "__main__":
    main()
