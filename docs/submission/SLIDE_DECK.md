# Slide Deck Content (5 Slides)

## Slide 1 — THE PROBLEM: It’s Not Just Stolen Cards
**Merchant payment loss doesn’t always look like a single bad transaction.**
*Visual:*
[Payment Attempt] + [Gateway Timeout] + [Rapid Retry] + [Delayed Webhook] 
→ **Unexpected Financial Exposure (Duplicate Captures, Unfulfilled Drops, Chargebacks)**

## Slide 2 — THE SOLUTION: Financial CSI
*Visual Pipeline:*
- **Payment Events**: Ingesting messy, scattered data (Synthetic or Razorpay Test Mode).
- **Financial DNA**: Transmuting sequences into categorical hashes.
- **Emergent Pattern Discovery**: Mining interactions statistically correlated with loss.
- **Evidence-Grounded Investigation**: Using AI to explain deterministic `EvidencePacks`.
- **Counterfactual Simulation**: Estimating potentially preventable loss.
- **Risk Decision**: Bounded decision-making against friction costs.

## Slide 3 — THE DISCOVERY: Uncovering the Unspecified
**The strongest discovered pattern from our final evaluation (Not provided as a rule):**
- **Condition**: `webhook_latency_bucket == ELEVATED`
- **Validation**: 23.21x Risk Multiplier on the untouched Test Set!
- **Support**: High statistical confidence across identical resamples.
- **Conclusion**: The pattern wasn't explicitly encoded; the system discovered the interaction organically.

## Slide 4 — THE AI + FINANCIAL DECISION
**AI does NOT decide whether the pattern exists. It translates the evidence.**
*Flow:* Pattern Discovered → Evidence Retrieved → Possible Mechanism Explained (AI) → Counterfactual Simulation Evaluated (Math) → Financial Decision Reached.
- **Decision Engine evaluates**: Confidence, Intervention Cost, False-Positive Friction, Estimated Preventable Loss.
- *Result*: `RECOMMEND_INTERVENTION` or `DO_NOT_INTERVENE`.

## Slide 5 — IMPACT + INTEGRATION
**From detecting risk to deciding whether the risk is worth acting on.**
- **Hidden Recovery**: 100% of planted structural failures recovered blindly.
- **Potentially Preventable Loss**: Evaluated at over ₹50M under aggressive simulation bounds.
- **Razorpay Integration**: Natively consuming and validating Razorpay Test Mode Webhooks via HMAC-SHA256 directly into the DNA engine.
