# Metric Source Map

| Presentation Metric | Source Artifact/API |
| :--- | :--- |
| **Total Transactions** | `docs/generated/final_evaluation.json` |
| **Train/Test Split & Leakage** | `docs/generated/final_evaluation.json` (Holdout object) |
| **Emergent Pattern Count** | `data/generated/discovered_patterns.json` |
| **Validation Risk Multiplier (Lift)** | `final_evaluation.json` |
| **AI Evidence Grounding** | `GET /api/investigations/{pattern_id}` |
| **Simulation Effectiveness** | `backend/app/services/simulation/intervention.py` (Default Scenarios) |
| **Potentially Preventable Loss** | `GET /api/simulations` or `final_evaluation.json` |
| **False-Positive Economics** | `CounterfactualEngine` output inside `final_evaluation.json` |
| **Razorpay Events Ingested** | `data/generated/razorpay_status.json` via `GET /api/integrations/razorpay/status` |
