# Financial CSI: Deployment Readiness Report

This repository has been audited and prepared for production deployment. The architecture utilizes **Vercel** for the Next.js frontend and **Render** for the FastAPI backend.

## 1. Frontend Configuration (Vercel)

The frontend is a standard Next.js application.

*   **Root Directory**: `frontend`
*   **Framework**: Next.js
*   **Build Command**: `npm run build`
*   **API Base URL Mechanism**: All API calls have been refactored to use `NEXT_PUBLIC_API_URL` via a centralized `API_BASE_URL` wrapper (`src/lib/api.ts`).
*   **Environment Variable**:
    *   `NEXT_PUBLIC_API_URL=https://<your-render-backend-url>.onrender.com`

**Vercel Readiness**: READY. The project can be deployed to Vercel by selecting the `frontend/` directory as the project root.

## 2. Backend Configuration (Render)

The backend is a standard FastAPI application. A `render.yaml` file has been provided to automate the infrastructure configuration.

*   **Root Directory**: `backend`
*   **Build Command**: `pip install -r requirements.txt`
*   **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
*   **Health Endpoint**: `GET /api/health`
*   **CORS Configuration**: The `allow_origins=["*"]` wildcard has been removed. Configure `CORS_ORIGINS` to safely explicitly allow the deployed Vercel domain.
*   **Environment Variables**:
    *   `CORS_ORIGINS='["https://<your-vercel-app>.vercel.app"]'`
    *   `PYTHON_VERSION=3.11.9`

**Render Readiness**: READY. Connect Render to the repository and it will automatically detect the `render.yaml` configuration.

## 3. Data & Filesystem Architecture

The Financial CSI prototype relies on a static, pre-generated ML dataset (10,000 transactions, 50 patterns) to guarantee deterministic evaluation results during the hackathon.

*   **Git Tracking**: The `.gitignore` has been surgically modified to track only the necessary read-only ML artifacts (e.g., `data/generated/train/*.csv`, `discovered_patterns.json`) while continuing to ignore disposable runtime files.
*   **Render Filesystem Requirements**: The Render Web Service tier utilizes an **ephemeral filesystem**, meaning any files written during runtime will be destroyed on the next deploy or server restart.
    *   **Decision**: We explicitly *embrace* this behavior for the prototype. The Razorpay Test Mode integration writes its audit logs to `razorpay_audit_log.json` and `financial_csi.db` at runtime. Since this data is purely demonstrative and isolated from the core ML data (which ships statically in the Git repository), losing the webhook logs on restart is an acceptable and cost-effective trade-off compared to provisioning a Persistent Disk.

## 4. Razorpay Test Mode Setup

The Razorpay integration operates purely in an observational Test Mode capacity.

*   **Webhook Configuration**: Configure Razorpay Test Mode to send webhooks to `https://<your-render-backend-url>.onrender.com/api/webhooks/razorpay`.
*   **Environment Variables (Server-Side ONLY)**:
    *   `RAZORPAY_MODE=test`
    *   `RAZORPAY_ENABLED=true`
    *   `RAZORPAY_KEY_ID=<your-test-key-id>`
    *   `RAZORPAY_KEY_SECRET=<your-test-key-secret>`
    *   `RAZORPAY_WEBHOOK_SECRET=<your-webhook-secret>`
*   **Security Alert**: These variables must NEVER be prefixed with `NEXT_PUBLIC_` or shared with the frontend.

## 5. Known Risks & Considerations

1.  **Ephemeral Data Wipe**: Any Razorpay events received in production will be cleared when the Render service restarts. As noted above, this is an intentional architectural decision for the hackathon prototype.
2.  **CORS Mismatch**: If `CORS_ORIGINS` is formatted improperly (e.g. invalid JSON) or does not perfectly match the Vercel URL (including `https://`), the dashboard will fail to load data. Double check the formatting in Render's dashboard.
3.  **Missing Optional LLM**: If `OPENAI_API_KEY` is not provided, the Investigation phase will gracefully fall back to a deterministic local template. This will not crash the application.
