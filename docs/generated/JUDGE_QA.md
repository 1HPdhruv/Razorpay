# Judge Q&A

**1. Isn’t this just fraud detection?**
Fraud detection usually looks for stolen cards or IP anomalies (the "Who"). Financial CSI looks for sequence anomalies (the "How"). We discover that when a specific gateway times out, is retried rapidly, and the webhook is delayed by 15 seconds, it disproportionately correlates with chargeback loss. 

**2. What exactly is emergent?**
"Emergent" means the pattern wasn't hardcoded into the baseline rules. The system statistically mined the interaction between these variables (Gateway, Latency, Sequence) directly from the noise of the data itself.

**3. How do you prevent data leakage?**
We enforce a rigid absolute Train/Test transaction boundary right at dataset generation. `scripts/run_final_evaluation.py` explicitly calculates the overlap between train and test identifiers. If the overlap is > 0, the pipeline fatally aborts.

**4. How do you know the pattern isn’t random?**
We rely on Apriori logic. The pattern must exceed global support limits, satisfy a `p-value < 0.05` constraint, and critically—the `Risk Multiplier` must survive when tested against the held-out test data.

**5. Why should I trust the LLM?**
You shouldn't trust it to do math. The LLM does no discovery and no calculations. It is restricted strictly to an "Evidence-Grounded Investigation" role where it consumes deterministic statistical `EvidencePacks` and translates them into forensic briefs. Every AI claim maps to a raw transaction ID.

**6. What happens when the model is wrong?**
Our Decision Engine calculates "False-Positive Economics". Even if the model flags a pattern, if the Friction Cost of intervening (e.g. delaying capture or triggering 3DS) mathematically outweighs the Expected Prevented Loss, the system issues a `DO_NOT_INTERVENE` directive. 

**7. Can this move real money?**
No. Financial CSI is an advisory Risk Manager. The Counterfactual Simulator runs Monte Carlo estimates on *potentially* preventable loss. The Razorpay integration is strictly locked to `Test Mode` webhook consumption.

**8. Is Razorpay actually integrated?**
Yes. You can push deterministic webhooks directly to `/api/webhooks/razorpay`. It validates the `x-razorpay-signature` against a test-mode secret and organically normalizes the event payload into the platform's canonical Financial DNA matrix.
