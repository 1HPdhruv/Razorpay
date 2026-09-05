# Final Judge Q&A

**Q1: What’s actually novel here?**
We shifted from deterministic, human-authored baseline rules to "Emergent Discovery." Instead of predicting fraud vectors, we mathematically mine the interaction topology of the payment event lifecycle (Financial DNA) to discover combinations associated with loss.

**Q2: How do you know your patterns aren’t random?**
They must survive a strict Apriori engine (`p-value < 0.05`) and maintain a high Risk Multiplier when evaluated exclusively against a pristine held-out Test dataset.

**Q3: How did you prevent data leakage?**
Data is split 80/20 at the transaction generation layer. Our evaluation script explicitly computes the identifier intersection between Train and Test to guarantee a 0-overlap integrity barrier before allowing the pipeline to proceed.

**Q4: Why use an LLM?**
We use an LLM exclusively for "Evidence-Grounded Investigation." It translates complex deterministic statistical outputs (EvidencePacks) into readable forensic briefs for non-technical merchant operators.

**Q5: What happens when the LLM is wrong?**
We constrain hallucination heavily via the prompt schema, forcing it to cite specific timestamps. Furthermore, the LLM makes *no financial decisions*. If it fails, the deterministic Decision Engine still correctly evaluates Net Benefit via Monte Carlo logic.

**Q6: Is this actually causal?**
No. Statistical association is not proof of causality. We explicitly frame findings as "associated with elevated loss" rather than "causes loss."

**Q7: How are false positives handled?**
The Counterfactual Simulator aggressively penalizes the "Potentially Preventable Loss" metric by subtracting the estimated friction cost of blocking legitimate customers (False Positives).

**Q8: Can this automatically block a payment?**
No. It is currently built as an advisory Simulator. It evaluates the economics of blocking, but does not execute live API refunds or blocks.

**Q9: Is Razorpay really integrated?**
Yes. A fully functional webhook ingestion API verifies incoming payloads via HMAC-SHA256, deduplicates them, and normalizes them into the Financial DNA matrix natively.

**Q10: Why isn’t this just anomaly detection?**
Anomaly detection flags "unusual" behavior, creating noise. Financial CSI mines behavior explicitly and disproportionately correlated with *actual financial loss*.

**Q11: Why synthetic data?**
Production PI/PCI-compliant transaction data with rich loss-labels is unavailable in a 24-hour hackathon. The synthetic generator provides deterministic physics to mathematically validate the engine's capability.

**Q12: What would you do with production data?**
Retune the Apriori support and lift hyperparameters to account for the massive increase in real-world entropy and noise.

**Q13: What is the biggest limitation?**
The system relies on the physics of the data generator. While it blindly recovers planted hidden patterns, live production data is infinitely messier.

**Q14: How would you measure success in production?**
A/B test the system's `RECOMMEND_INTERVENTION` directives. Measure the delta in Net Prevented Loss minus the increase in False-Positive friction escalations over 30 days.

**Q15: Why would a merchant pay for this?**
Because finding out *why* systemic technical loss is happening currently takes a team of data scientists weeks of SQL querying. Financial CSI automates the discovery, explanation, and financial justification in seconds.
