from fastapi import APIRouter, HTTPException
from app.core.config import settings
from app.services.razorpay.webhook import WebhookManager
from app.services.razorpay.client import RazorpayClient

router = APIRouter()

@router.get("/razorpay/status")
def get_razorpay_status():
    status = WebhookManager.get_status()
    
    return {
        "enabled": settings.RAZORPAY_ENABLED,
        "mode": settings.RAZORPAY_MODE,
        "credentials_configured": bool(settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET),
        "webhook_secret_configured": bool(settings.RAZORPAY_WEBHOOK_SECRET),
        **status
    }

@router.post("/razorpay/test-connection")
async def test_razorpay_connection():
    result = await RazorpayClient.test_connection()
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

@router.get("/razorpay/events")
def get_razorpay_events():
    return WebhookManager.get_audit_log()
