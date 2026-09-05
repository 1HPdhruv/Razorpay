# Claims Checklist

Before presenting, verify that every spoken claim maps precisely to an auditable artifact:

- [ ] **Claim**: "We evaluated X transactions."
  - **Check**: Look at `docs/generated/final_evaluation.json` -> `holdout.train_count` + `holdout.test_count`.
- [ ] **Claim**: "The system discovered Y emergent patterns."
  - **Check**: Verify `data/generated/discovered_patterns.json`.
- [ ] **Claim**: "The pattern multiplies risk by Z times on unseen data."
  - **Check**: Verify `final_evaluation.json` -> `discovery.top_pattern_risk_multiplier`.
- [ ] **Claim**: "AI investigated this specific event."
  - **Check**: Verify the frontend Investigation UI explicitly lists `EVIDENCE E-XXX` IDs next to claims.
- [ ] **Claim**: "This intervention saves $X."
  - **Check**: STOP. Change script to "This intervention *potentially prevents* $X *under simulation assumptions*."
- [ ] **Claim**: "Razorpay is sending us live events."
  - **Check**: STOP. Confirm the dashboard says "Razorpay Test Mode" and clarify no live money is moved.
