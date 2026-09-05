# Final Submission Checklist

## Engineering
- [x] Backend works
- [x] Frontend builds
- [x] Tests pass
- [x] Demo starts (via `./scripts/run_demo.sh`)
- [x] Evaluation reproducible
- [x] No secrets committed

## ML
- [x] No discovery/test leakage (Overlap = 0)
- [x] Hidden patterns isolated from training logic
- [x] Results measured deterministically
- [x] Stability tested
- [x] Baseline comparison included

## AI
- [x] AI role clearly defined (Evidence Translation ONLY)
- [x] Evidence grounding works via explicit JSON `EvidencePacks`
- [x] No fabricated evidence/hallucinations
- [x] Fallback clearly labeled and functional if OpenAI API drops

## Finance
- [x] Potential loss calculated from actual data (Monte Carlo outputs)
- [x] False-positive cost included in intervention simulations
- [x] Intervention cost explicitly subtracted
- [x] Counterfactual assumptions visible on UI (e.g. 60%, 75%, 90% efficacies)
- [x] No simulated savings presented as guaranteed actual savings

## Razorpay
- [x] Test Mode only
- [x] Webhook HMAC-SHA256 verification implemented
- [x] Duplicate handling works
- [x] Fixture bypass clearly labeled via `/api/webhooks/razorpay/simulate`
- [x] No live financial action

## Presentation
- [x] 30-second pitch ready
- [x] 3-minute demo ready
- [x] 5-slide deck ready
- [x] Judge Q&A ready
- [x] Limitations documented honestly
