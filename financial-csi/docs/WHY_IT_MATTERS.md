# Why It Matters

### Why not traditional rules?
Static rules (like "Block IP" or "Decline if amount > $500") degrade quickly. Bad actors adapt, but more importantly, platform-level systemic losses often stem from complex integration glitches or edge-case gateway timeouts that a single "IF-THEN" rule will never catch.

### Why event interactions (Financial DNA)?
Loss often emerges in the *spaces between* events. A timeout isn't inherently fatal. A retry isn't inherently fatal. A delayed webhook isn't inherently fatal. But when they combine within a 30-second window, they often result in duplicate captures or unfulfilled inventory drops. Transmuting these into "Financial DNA" allows ML systems to mine sequential interactions.

### Why evidence-grounded AI?
Generative LLMs hallucinate badly in financial domains. By restricting the AI exclusively to interpreting deterministic `EvidencePacks`, we bridge the gap between "Black Box Data Science" and "Merchant Operations." The merchant gets a readable explanation, and the system maintains mathematical integrity.

### Why counterfactual simulation & false-positive economics?
Blocking 100% of suspicious traffic stops fraud, but it also bankrupts the merchant by blocking legitimate customers. Monte Carlo simulations force the system to prove that the proposed intervention won't cost more in friction/lost-sales (False Positives) than it saves in avoided loss.

### Why is this useful to a merchant?
It automates the most difficult part of financial reconciliation: figuring out *why* systemic losses are happening without waiting for a data science team to manually construct a SQL dashboard 30 days after the incident.
