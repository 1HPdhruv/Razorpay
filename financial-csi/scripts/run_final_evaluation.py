import sys
import os
import json
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(PROJECT_ROOT / "backend"))

from app.services.simulation.intervention import get_default_scenarios
from app.services.simulation.counterfactual import CounterfactualEngine

def generate_report(results: dict, output_dir: Path):
    os.makedirs(output_dir, exist_ok=True)
    
    # Machine readable output
    with open(output_dir / "final_evaluation.json", "w") as f:
        json.dump(results, f, indent=2)
        
    # Markdown Report
    md = f"""# Final Evaluation Report

Generated automatically by `run_final_evaluation.py`.

## Holdout Integrity
- Train Transactions: {results['holdout']['train_count']}
- Test Transactions: {results['holdout']['test_count']}
- Leakage (Overlap Count): {results['holdout']['overlap_count']}
- **Status**: {"PASS" if results['holdout']['overlap_count'] == 0 else "FAIL"}

## Baseline Comparison
- Number of Patterns Discovered: {results['discovery']['pattern_count']}
- Baseline Test Loss Rate: {results['baseline']['test_loss_rate']:.4f}

## Discovery Validation
- Strongest Pattern: {results['discovery']['top_pattern_id']}
- Test Set Risk Multiplier: {results['discovery']['top_pattern_risk_multiplier']:.2f}x
- Test Set Support: {results['discovery']['top_pattern_test_support']}

## Simulation Outcomes
"""
    for sim in results['simulation']:
        md += f"""### {sim['scenario']}
- Intervention: {sim['intervention']}
- Effectiveness: {sim['effectiveness']}
- Net Estimated Benefit: ₹{sim['net_benefit_paise'] / 100:.2f}
- Recommendation: {sim['recommendation']}
"""
    
    with open(output_dir / "FINAL_EVALUATION_REPORT.md", "w") as f:
        f.write(md)

def run_evaluation():
    print("Starting Final Evaluation Pipeline...")
    DATA_DIR = PROJECT_ROOT / "data" / "generated"
    DOCS_DIR = PROJECT_ROOT / "docs" / "generated"
    
    # 1. Load splits (assuming data generation already ran)
    try:
        train_df = pd.read_csv(DATA_DIR / "train" / "loss_targets.csv")
        test_df = pd.read_csv(DATA_DIR / "test" / "loss_targets.csv")
    except Exception:
        print("Data not found. Run prepare_demo.py first.")
        return
        
    train_ids = set(train_df['transaction_id'])
    test_ids = set(test_df['transaction_id'])
    overlap = len(train_ids.intersection(test_ids))
    
    print(f"Train Count: {len(train_ids)}")
    print(f"Test Count: {len(test_ids)}")
    print(f"Leakage (Overlap): {overlap}")
    
    if overlap > 0:
        print("FAIL: Leakage detected. Aborting evaluation.")
        sys.exit(1)
        
    # 2. Load Discoveries
    with open(DATA_DIR / "discovered_patterns.json", "r") as f:
        patterns = json.load(f)
        
    top_pattern = patterns[0] if patterns else None
    
    # 3. Simulate Intervention on Top Pattern
    simulations = []
    if top_pattern:
        feat_df = pd.read_csv(DATA_DIR / "train" / "feature_matrix.csv")
        targets_df = pd.read_csv(DATA_DIR / "train" / "loss_targets.csv")
        feat_df = pd.merge(feat_df, targets_df, on="transaction_id")
        
        mask = pd.Series([True]*len(feat_df), index=feat_df.index)
        for cond in top_pattern['conditions']:
            mask &= (feat_df[cond['feature']] == cond['value'])
            
        matched_tx = feat_df[mask].to_dict(orient='records')
        
        from app.models.pattern import Pattern
        engine = CounterfactualEngine()
        scenarios = get_default_scenarios()
        
        for sc in scenarios:
            res = engine.simulate(Pattern(**top_pattern), sc, matched_tx, runs=1000)
            simulations.append({
                "scenario": sc.name,
                "intervention": sc.intervention.name,
                "effectiveness": sc.effectiveness,
                "net_benefit_paise": res.net_estimated_benefit_paise,
                "recommendation": res.recommendation
            })
            
    # 4. Generate Report
    results = {
        "holdout": {
            "train_count": len(train_ids),
            "test_count": len(test_ids),
            "overlap_count": overlap
        },
        "baseline": {
            "test_loss_rate": test_df['loss_flag'].mean()
        },
        "discovery": {
            "pattern_count": len(patterns),
            "top_pattern_id": top_pattern['pattern_id'] if top_pattern else "NONE",
            "top_pattern_risk_multiplier": top_pattern.get('risk_multiplier', 0) if top_pattern else 0,
            "top_pattern_test_support": top_pattern.get('matching_transaction_count', 0) if top_pattern else 0
        },
        "simulation": simulations
    }
    
    generate_report(results, DOCS_DIR)
    print(f"Evaluation complete. Reports generated in {DOCS_DIR}")

if __name__ == "__main__":
    run_evaluation()
