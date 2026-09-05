import json
from fastapi import APIRouter, Request, HTTPException, Header
from app.core.config import settings
from app.services.razorpay.signature import verify_webhook_signature
from app.services.razorpay.normalizer import RazorpayNormalizer
from app.services.razorpay.webhook import WebhookManager
from app.services.razorpay.fixtures import FIXTURES
import pandas as pd
from pathlib import Path

router = APIRouter()

PROJECT_ROOT = Path(__file__).resolve().parents[4]
DATA_DIR = PROJECT_ROOT / "data" / "generated"
EVENTS_FILE = DATA_DIR / "train" / "events.csv"

def process_and_persist_event(payload_dict: dict, source: str):
    import time
    from datetime import datetime
    
    # Idempotency
    webhook_id = payload_dict.get("id") or (payload_dict.get("account_id", "") + "_" + str(payload_dict.get("created_at", "")))
    
    audit_entry = {
        "provider": "razorpay",
        "provider_event_id": webhook_id,
        "event_type": payload_dict.get("event", "unknown"),
        "received_at": datetime.now().isoformat(),
        "verification_status": "verified",
        "processing_status": "pending",
        "internal_event_id": None
    }
    
    if WebhookManager.is_processed(webhook_id):
        WebhookManager.record_status(payload_dict.get("event"), "duplicate")
        audit_entry["processing_status"] = "duplicate"
        WebhookManager.record_audit(audit_entry)
        return {"status": "ok", "message": "Duplicate webhook ignored"}
        
    normalized = RazorpayNormalizer.normalize(payload_dict, source=source)
    audit_entry["internal_event_id"] = normalized.get("event_id")
    
    if normalized["event_type"] == "UNSUPPORTED":
        WebhookManager.record_status(payload_dict.get("event"), "unsupported")
        WebhookManager.mark_processed(webhook_id)
        audit_entry["processing_status"] = "unsupported"
        WebhookManager.record_audit(audit_entry)
        return {"status": "ok", "message": "Unsupported event ignored"}
        
    if normalized["transaction_id"] == "UNMATCHED":
        WebhookManager.record_status(payload_dict.get("event"), "unmatched")
        audit_entry["processing_status"] = "unmatched"
    else:
        WebhookManager.record_status(payload_dict.get("event"), "processed")
        audit_entry["processing_status"] = "processed"
        
    # Append to events.csv
    if EVENTS_FILE.exists() and audit_entry["processing_status"] == "processed":
        df = pd.DataFrame([normalized])
        df.to_csv(EVENTS_FILE, mode='a', header=False, index=False)
        
    WebhookManager.mark_processed(webhook_id)
    WebhookManager.record_audit(audit_entry)
    return {"status": "ok"}

@router.post("/razorpay")
async def razorpay_webhook(request: Request, x_razorpay_signature: str = Header(None)):
    if not settings.RAZORPAY_ENABLED or settings.RAZORPAY_MODE != "test":
        raise HTTPException(status_code=403, detail="Integration disabled or not in test mode")
        
    if not x_razorpay_signature:
        WebhookManager.record_status("unknown", "failed")
        raise HTTPException(status_code=400, detail="Missing signature")
        
    body_bytes = await request.body()
    body_str = body_bytes.decode('utf-8')
    
    if not verify_webhook_signature(body_str, x_razorpay_signature, settings.RAZORPAY_WEBHOOK_SECRET):
        WebhookManager.record_status("unknown", "failed")
        raise HTTPException(status_code=400, detail="Invalid signature")
        
    try:
        payload_dict = json.loads(body_str)
    except json.JSONDecodeError:
        WebhookManager.record_status("unknown", "failed")
        raise HTTPException(status_code=400, detail="Malformed JSON")
        
    return process_and_persist_event(payload_dict, "razorpay_test")

@router.post("/razorpay/simulate")
async def simulate_webhook(fixture_id: str):
    if not settings.RAZORPAY_ENABLED or settings.RAZORPAY_MODE != "test":
        raise HTTPException(status_code=403, detail="Integration disabled")
        
    if fixture_id not in FIXTURES:
        raise HTTPException(status_code=404, detail="Fixture not found")
        
    payload_dict = FIXTURES[fixture_id]
    return process_and_persist_event(payload_dict, "razorpay_test_fixture")
