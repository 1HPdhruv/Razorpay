# Financial CSI: One-Page Summary

**The Problem**
Merchants lose millions to complex technical interaction failures (e.g., gateway timeouts meeting rapid retries and delayed webhooks, causing duplicate captures or abandoned carts). Traditional static rules engines cannot predict or encode these interactive edges effectively. 

**The Solution**
Financial CSI is an AI Risk Manager that shifts from "Deterministic Rules" to "Emergent Discovery." It mines the operational interaction of payment lifecycles to automatically discover hidden structural loss.

**Key Innovation**
We transmute raw, scattered webhook sequences into "Financial DNA." Our Apriori engine mathematically discovers interactions correlated with financial loss that human operators failed to specify. 

**How AI Is Used (Evidence Grounding)**
LLMs hallucinate in finance. We restrict the AI explicitly to interpreting deterministic `EvidencePacks` provided by the backend. It acts as an investigator translating raw data into a forensic brief, never as a black-box fraud detector.

**Evaluation & Safety**
- **Strict Data Holdout**: The Train/Test isolation is absolute (Overlap = 0). Patterns must mathematically survive on unseen data to be validated.
- **Counterfactual Simulation**: Before recommending action, Monte Carlo engines simulate interventions, aggressively subtracting False-Positive friction costs. If friction outweighs the prevented loss, the Decision Engine recommends `DO_NOT_INTERVENE`.
- **Integration**: Razorpay webhooks are fully supported but locked explicitly to HMAC-SHA256 verified Test Mode payloads. No live financial actions are taken.

**Demo Flow (1-Command deployment)**
```bash
./scripts/run_demo.sh
```
This script initializes synthetic data, runs the discovery engine, executes the evaluations, spins up the backend API, and launches the Next.js React Dashboard natively.
