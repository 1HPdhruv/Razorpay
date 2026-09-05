# Demo Failure Plan

**If Razorpay is unavailable or tunneling fails:**
Use the `Razorpay Test Fixture` via the `POST /api/webhooks/razorpay/simulate?fixture_id=capture` endpoint. The frontend Dashboard handles this gracefully. Explicitly inform judges: "We are using deterministic payloads hitting the exact same normalization pipeline because live Ngrok tunneling is down."

**If OpenAI API is unavailable (Rate limits/Timeout):**
The `backend/app/services/discovery/ai_investigator.py` has a native deterministic fallback. It will construct a structured, non-generative brief outlining the `EvidencePack` strictly. Explain to judges: "Due to conference wifi/API rate limits, the system has gracefully fallen back to deterministic structural explanation rather than generative text."

**If backend fails (500 Error):**
Press `Ctrl+C` in the terminal to kill the processes, then run `./scripts/reset_demo.sh` to safely purge caches, followed by `./scripts/run_demo.sh` to restart. This takes < 60 seconds.

**If discovery is slow (Compute bottlenecks):**
The dataset size can be manually tuned down in `scripts/prepare_demo.py` from 10,000 to 2,000 transactions to decrease Apriori runtime from 15 seconds to 2 seconds. 

**If simulation fails:**
Navigate directly to `/evaluation`. The previous simulation calculations are deterministically cached in `docs/generated/final_evaluation.json`. Display those evaluation artifacts and clearly explain that they represent the standard Pipeline run output. Never fabricate emergency metrics.
