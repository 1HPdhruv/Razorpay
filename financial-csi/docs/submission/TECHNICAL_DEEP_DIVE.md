# Technical Deep-Dive

### Data Generation
A deterministic Python engine simulating realistic payment physics (Seed 42). It plants Baseline anomalies (like Duplicate Captures) and Hidden Structural anomalies (Gateway G2 Timeouts + Rapid Retries) across 10,000 transactions, generating precise timestamps and loss amounts.

### Lifecycle Reconstruction
The `LifecycleBuilder` unifies scattered, asynchronous webhook actions (e.g., `PAYMENT_ATTEMPTED` -> `AUTHORIZATION_FAILED` -> `PAYMENT_RETRIED` -> `WEBHOOK_RECEIVED`) into coherent longitudinal transaction objects.

### Financial DNA
Transmutes sequence data into machine-readable hashes. It extracts atomic (amount_band), temporal (webhook_latency_bucket), and behavioral (retry_speed_bucket) features into a flat `feature_matrix`.

### Pattern Discovery
An Apriori-based statistical miner. It evaluates the Training split, seeking interactive combinations of DNA features where the conditional loss probability far exceeds the global baseline (Lift > 1.5, p-value < 0.05). 

### Validation
An absolute 80/20 holdout. Discovered patterns are projected onto the unseen Test set to calculate a true "Test-Set Risk Multiplier", ensuring the pattern isn't merely overfit noise.

### Investigation
Evidence Retrieval gathers the raw timestamps and identifiers supporting the pattern. The `AI Investigator` is bounded by an explicit JSON `EvidencePack`, translating the statistics into a safe, non-hallucinated forensic brief.

### Simulation
The `CounterfactualEngine` runs 1000 Monte Carlo trajectories. Assuming an intervention (e.g. "Delay Capture") has an efficacy bound (60-90%), it calculates expected recovered loss and subtracts a deterministic False-Positive friction penalty to derive honest Net Benefit ranges.

### Decision Engine
A deterministic gatekeeper. If the Monte Carlo Net Benefit is negative, or if Statistical Confidence is low, it emits `DO_NOT_INTERVENE` or `REQUIRE_MANUAL_REVIEW`.

### Razorpay Integration
A webhook adapter endpoint (`/api/webhooks/razorpay`) enforces HMAC-SHA256 signature verification via `RAZORPAY_WEBHOOK_SECRET`. Valid Test Mode payloads are parsed, deduplicated, normalized, and fed directly into the `LifecycleBuilder` seamlessly alongside synthetic data.
