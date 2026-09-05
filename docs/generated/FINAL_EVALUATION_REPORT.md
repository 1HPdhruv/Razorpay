# Final Evaluation Report

Generated automatically by `run_final_evaluation.py`.

## Holdout Integrity
- Train Transactions: 8000
- Test Transactions: 2000
- Leakage (Overlap Count): 0
- **Status**: PASS

## Baseline Comparison
- Number of Patterns Discovered: 50
- Baseline Test Loss Rate: 0.0295

## Discovery Validation
- Strongest Pattern: PTN_1
- Test Set Risk Multiplier: 23.21x
- Test Set Support: 289

## Simulation Outcomes
### Conservative
- Intervention: Require Verification
- Effectiveness: 0.6
- Net Estimated Benefit: ₹344490.19
- Recommendation: RECOMMEND_INTERVENTION
### Balanced
- Intervention: Hold Second Capture
- Effectiveness: 0.75
- Net Estimated Benefit: ₹434459.01
- Recommendation: RECOMMEND_INTERVENTION
### Aggressive
- Intervention: Delay Retry
- Effectiveness: 0.9
- Net Estimated Benefit: ₹521622.54
- Recommendation: RECOMMEND_INTERVENTION
