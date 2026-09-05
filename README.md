# Financial CSI

**An AI risk manager that finds payment loss patterns nobody wrote a rule for — then proves, mathematically, whether fixing them is even worth it.**

🔗 **Live demo:** [razorpay-swart.vercel.app](https://razorpay-swart.vercel.app)
📚 **Docs:** see [`/docs`](./docs) for architecture, API spec, and the full write-up

---

## The problem

Most fraud and risk systems are built on rules someone had to think of first: *"block this IP after 5 failures,"* *"decline anything over $500."* That works for the fraud patterns you already know about.

It doesn't work for the losses that come from **interaction effects** — a gateway timeout, followed by an aggressive retry, followed by a delayed webhook, all inside a 30-second window, quietly resulting in a duplicate capture or an order that ships without ever getting paid for. No single event in that chain looks dangerous. The *combination* is what costs money, and nobody writes an IF-THEN rule for a combination they've never seen.

## What Financial CSI does

Instead of starting from predefined rules, Financial CSI starts from the data and lets the patterns emerge:

1. **Reconstructs payment lifecycles** into a structured, categorical event sequence — we call this a transaction's **Financial DNA**.
2. **Mines that DNA statistically** (Apriori-based pattern discovery) to surface event combinations that show up disproportionately often in losses — combinations no analyst specified in advance.
3. **Grounds every AI explanation in real evidence.** The LLM never freelances a diagnosis — it's handed a deterministic `EvidencePack` (raw timestamps, IDs, statistical support) and asked only to explain *that*, which keeps it from hallucinating a story that isn't in the data.
4. **Simulates the fix before you ship it.** Every discovered pattern goes through a Monte Carlo counterfactual simulation that weighs the loss it would prevent against the false-positive cost of blocking legitimate customers — so you only act on interventions that are actually worth the friction.

## Why this is different

The novel part isn't "AI reads your transactions" — plenty of tools do that. It's that the **pattern discovery step is unsupervised and combinatorial**: rather than a team of analysts hypothesizing fraud vectors by hand, the system mines the interaction topology of the event data itself and surfaces combinations humans never specified. AI only enters *after* that — as an evidence-grounded explainer, not a black-box detector.

## What's live right now

The deployed app has six working areas:

| Section | What it does |
|---|---|
| **Dashboard** | Overview of discovered risk and system status |
| **Patterns** | Browse mined event-combinations tied to loss |
| **Investigations** | Drill into a pattern's evidence and AI-generated forensic brief |
| **Simulations** | Run Monte Carlo counterfactuals on a proposed intervention |
| **Evaluation** | Train/test holdout results — how well patterns validate on unseen data |
| **Integrations** | Razorpay Test Mode webhook status |

> **Note:** the Razorpay integration ships in Test Mode only, and the demo instance runs without live Razorpay keys configured — so the Integrations page will correctly show "Not configured" unless you supply your own test credentials.

## Tech stack

- **Backend:** FastAPI (Python 3.11), SQLite, Apriori-based pattern mining
- **Frontend:** Next.js 14, TypeScript, Tailwind CSS, Recharts
- **Integration:** Razorpay Test Mode webhooks, verified via HMAC-SHA256
- **Deployment:** Frontend on Vercel, backend on Render

## Safety by design

This is a simulator, not a live risk engine, and it's built to stay that way:

- **Strict train/test holdout** — no overlapping identifiers between the two, and every discovered pattern is validated against data the mining step never saw.
- **No live financial action, ever.** Razorpay is integrated read-only, in Test Mode only — the backend refuses to run in any other mode. It never captures, refunds, or intervenes on a real payment.
- **Savings are always framed as estimates.** Every dollar figure is labeled "potentially preventable loss under simulation assumptions," tied to an explicit, adjustable intervention efficacy (e.g. 60% / 75% / 90%), never presented as a guarantee.

## Getting started

### Prerequisites
- Python 3.11+
- Node.js 18+
- A Razorpay **Test Mode** account (optional — only needed if you want to exercise the webhook integration; everything else runs on synthetic data)

### 1. Clone the repo

```bash
git clone https://github.com/1HPdhruv/Razorpay.git
cd Razorpay
```

### 2. Set up the backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example ../.env   # then fill in the values below
uvicorn app.main:app --reload
```

The API will be live at `http://localhost:8000`, with interactive docs at `http://localhost:8000/docs`.

### 3. Set up the frontend

In a second terminal:

```bash
cd frontend
npm install
npm run dev
```

The dashboard will be live at `http://localhost:3000`.

### 4. Configure your environment

Copy `.env.example` to `.env` and fill in what you need:

```bash
# Local dev CORS
CORS_ORIGINS='["http://localhost:3000", "http://127.0.0.1:3000"]'

# Frontend → backend URL
NEXT_PUBLIC_API_URL="http://localhost:8000"

# Optional: only needed to exercise the live Razorpay webhook flow
RAZORPAY_ENABLED=true
RAZORPAY_MODE=test          # must stay "test" — the app refuses to boot otherwise
RAZORPAY_KEY_ID=
RAZORPAY_KEY_SECRET=
RAZORPAY_WEBHOOK_SECRET=
```

Get your Razorpay test credentials from **Dashboard → Account & Settings → API Keys (Test Mode)**, and your webhook secret from **Dashboard → Webhook Settings**.

## API overview

A quick map of what's available (full spec in [`docs/API_SPEC.md`](./docs/API_SPEC.md)):

- `GET /api/health` — service health check
- `GET /api/transactions` / `GET /api/transactions/{id}` — reconstructed payment lifecycles
- `GET /api/patterns` / `GET /api/patterns/{id}` — discovered risk patterns
- `GET /api/investigations/{pattern_id}` — evidence-grounded forensic brief for a pattern
- `POST /api/simulations/intervention` — run a Monte Carlo counterfactual
- `GET /api/evaluation` — holdout validation results

## Project structure

```
.
├── backend/          FastAPI service (app/, tests/, requirements.txt)
├── frontend/          Next.js dashboard (src/, public/)
├── data/               synthetic dataset + generated artifacts
├── docs/               architecture, API spec, data model, evaluation, and more
├── docker-compose.yml  local multi-service orchestration
└── render.yaml         backend deployment config for Render
```

Deeper documentation lives in [`/docs`](./docs) — architecture diagrams, the data model, the ML approach under consideration, the Razorpay integration contract, and the reasoning behind each design choice are all written up there.

## Limitations (in the interest of being upfront)

- **The benchmark data is synthetic.** It's designed to simulate realistic failure modes, but real-world deployment would need proper hyperparameter tuning against live data.
- **This finds correlation, not causation.** The discovery engine flags statistical risk-multipliers; it doesn't prove a given event combination *caused* the loss.
- **Simulated savings assume clean execution.** The Net Estimated Benefit numbers assume a merchant can actually implement the intervention at the stated efficacy, with no unexpected side effects.

## Contributing

This is currently a solo hackathon project — issues and PRs are welcome if you want to poke at it, but there's no formal contribution process yet.

## License

No license has been added yet — treat this as "all rights reserved" until one is.
