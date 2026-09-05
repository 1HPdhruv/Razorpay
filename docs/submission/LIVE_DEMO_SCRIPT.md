# Live Demo Script (3 Minutes)

**[0:00–0:25 — PROBLEM]**
*(Screen: Main Dashboard)*
"Traditional risk systems rely on static rules to catch obvious bad actors. But modern merchants bleed revenue from complex interactions—a gateway times out, the user retries rapidly, a webhook is delayed. None of these trigger alarms alone, but together they cause massive chargebacks and unfulfilled drops. Financial CSI doesn't wait for humans to guess these rules; it discovers them organically."

**[0:25–0:55 — DISCOVERY]**
*(Screen: Navigate to Patterns Page. Click the top pattern.)*
"Here’s what the system discovered on a 10,000 transaction dataset. Without being explicitly told to look for it, the Apriori engine found a combination of events resulting in a 23x Risk Multiplier. Crucially, this isn't overfit training data—this multiplier was validated strictly on the held-out test set."

**[0:55–1:35 — INVESTIGATION]**
*(Screen: Navigate to Investigation Detail)*
"A black box 'Risk Score' is useless to a merchant. We use AI here, but strictly as an Evidence-Grounded Investigator. The AI isn’t guessing; it is summarizing a deterministic `EvidencePack` retrieved from the payment lifecycle. You can trace every claim—the timestamps, the gateway, the contrastive examples—directly back to the raw database."

**[1:35–2:15 — SIMULATION]**
*(Screen: Scroll down to Simulation)*
"Finding a pattern is easy. Knowing if it's worth fixing is hard. This is a counterfactual simulation. We estimate potentially preventable loss by assuming a 90% effective intervention. But look at the False-Positive cost—intervening adds friction. We explicitly subtract the cost of stopping legitimate customers from the savings to produce a realistic Net Estimated Benefit."

**[2:15–2:40 — DECISION]**
*(Screen: Show Recommendation Badge)*
"Because the Net Benefit is overwhelmingly positive and the statistical confidence is high, the Decision Engine issues a `RECOMMEND_INTERVENTION`. If the friction cost was too high, it would actively refuse to intervene."

**[2:40–3:00 — RAZORPAY]**
*(Screen: Point to Razorpay Integration Card on Dashboard)*
"Finally, we don't just run on synthetic data. The system actively ingests, validates via HMAC-signature, and normalizes Razorpay Test Fixtures directly into our Financial DNA pipeline. The system doesn’t just ask whether a transaction looks risky. It asks whether a discovered risk is supported by evidence and economically worth acting on."
