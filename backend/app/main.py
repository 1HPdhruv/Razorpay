from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, transactions, patterns, investigations, simulations, evaluation, webhooks, integrations

app = FastAPI(title="Financial CSI API", version="0.1.0")

from app.core.config import settings

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api", tags=["health"])
app.include_router(transactions.router, prefix="/api/transactions", tags=["transactions"])
app.include_router(patterns.router, prefix="/api/patterns", tags=["patterns"])
app.include_router(investigations.router, prefix="/api/investigations", tags=["investigations"])
app.include_router(simulations.router, prefix="/api/simulations", tags=["simulations"])
app.include_router(evaluation.router, prefix="/api/evaluation", tags=["evaluation"])
app.include_router(webhooks.router, prefix="/api/webhooks", tags=["webhooks"])
app.include_router(integrations.router, prefix="/api/integrations", tags=["integrations"])
