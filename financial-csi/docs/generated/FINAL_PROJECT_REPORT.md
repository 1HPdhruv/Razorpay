# Financial CSI: Final Project Report

## 1. Executive Summary
Financial CSI is an AI-powered Risk Manager designed to automatically discover, explain, and mitigate previously unspecified combinations of payment events associated with merchant loss. Moving beyond predefined rule engines, it leverages statistical data mining to uncover "Emergent Patterns", utilizes deterministic LLM extraction for grounded explanations, and safely evaluates mitigation strategies via counterfactual Monte Carlo simulations.

## 2. Architecture & Pipeline
The system operates on a unified canonical event pipeline:
1. **Ingestion & Generation:** Either synthetic baseline datasets or real `Razorpay Test Mode` webhooks.
2. **Lifecycle Reconstruction:** Unifies scattered webhook actions (payment attempts, captures, fails, timeouts) into coherent longitudinal objects.
3. **Financial DNA:** Transmutes raw sequence data into categorical hashes and temporal bounds.
4. **Pattern Discovery:** Apriori-based statistical association rules engine analyzing `TRAIN_SYNTHETIC` to find combinations yielding asymmetric loss risk.
5. **AI Investigation:** A constrained LLM extraction engine converting raw `EvidencePacks` into readable forensic briefs without hallucination.
6. **Simulation Engine:** Evaluates counterfactual intervention strategies iteratively to compute strict `Net Estimated Benefit` ranges.

## 3. Discovery Method
The engine uses conditional association mining. It computes base support rates for isolated DNA components (e.g. `webhook_latency_bucket==ELEVATED`), cross-references joint occurrences, and isolates conditional subsets whose posterior loss probability significantly eclipses the global baseline (`lift` > 1.5, `p-value` < 0.05).

## 4. Evidence Grounding
LLM integration is rigorously bounded. AI does not "discover" fraud. Instead, the backend mathematically identifies a pattern and extracts matching loss/non-loss rows into a structured `EvidencePack`. The LLM's system prompt restricts it to synthesizing *only* the specific fields passed, mandating the linkage of explicit `EV-XXX` reference tags against every generated claim.

## 5. Counterfactual Simulation
Potential interventions (e.g., `REQUIRE_VERIFICATION`) are mapped through a probabilistic filter. Rather than assuming 100% effectiveness, the simulation randomizes success across 1000 runs per pattern based on configurable efficacy matrices, subtracting mathematically defined false-positive penalty costs to produce honest bounds (P10 to P90) of expected Net Benefit.

## 6. Razorpay Integration
The prototype seamlessly consumes Razorpay webhook callbacks via `POST /api/webhooks/razorpay` utilizing HMAC-SHA256 signature verification. Valid events are deterministically deduplicated, converted to internal representations, and tracked as `razorpay_test` payloads natively integrated into the exact same DNA pipeline.

## 7. Evaluation & Holdout Validation
The system preserves a strict `80/20` partition line.
- **Leakage Control:** Explicit transaction overlap count evaluates to precisely `0`. 
- **Validation Execution:** The pipeline independently discovers mechanisms on the training split, and the reported `test-set risk multiplier` confirms survival of the insight onto untouched data.

## 8. False Positive Economics & Stability
No pattern is actioned based purely on lift. The final `Decision Engine` intercepts statistical findings with a cost-benefit boundary: if intervention friction outweighs the prevented loss, the backend emits `DO_NOT_INTERVENE`.

## 9. Explicit Limitations
1. **Synthetic Data Bound:** Benchmark models assume the topology of the provided synthetic generator; real-world behavior will introduce additional entropy.
2. **Probability, not Causation:** Statistical pattern co-occurrence does not implicitly prove that an intervention will directly prevent the loss; they are correlated insights.
3. **Read-Only API:** No intervention actions are fired back to external production gateways; this tool operates as an informational simulator.

## 10. Reproducibility
The exact demo environment can be generated deterministically:
```bash
./scripts/run_demo.sh
```
This script initializes the core 10,000 transaction dataset using Seed 42, processes all DNA boundaries, executes evaluation simulations, and stands up the FastAPI backend and Next.js UI organically.
