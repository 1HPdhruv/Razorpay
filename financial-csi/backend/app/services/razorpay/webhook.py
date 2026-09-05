import json
import os
from pathlib import Path
from typing import Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parents[4]
DATA_DIR = PROJECT_ROOT / "data" / "generated"
PROCESSED_WEBHOOKS_FILE = DATA_DIR / "processed_webhooks.json"
RAZORPAY_STATUS_FILE = DATA_DIR / "razorpay_status.json"

class WebhookManager:
    @staticmethod
    def is_processed(webhook_id: str) -> bool:
        if not PROCESSED_WEBHOOKS_FILE.exists():
            return False
        with open(PROCESSED_WEBHOOKS_FILE, "r") as f:
            processed = json.load(f)
        return webhook_id in processed
        
    @staticmethod
    def mark_processed(webhook_id: str):
        processed = []
        if PROCESSED_WEBHOOKS_FILE.exists():
            with open(PROCESSED_WEBHOOKS_FILE, "r") as f:
                processed = json.load(f)
        processed.append(webhook_id)
        with open(PROCESSED_WEBHOOKS_FILE, "w") as f:
            json.dump(processed, f)
            
    @staticmethod
    def record_status(event_type: str, status: str):
        """status: processed, duplicate, failed, unsupported, unmatched"""
        data = {
            "events_received": 0,
            "events_processed": 0,
            "events_failed": 0,
            "events_duplicate": 0,
            "unmatched_events": 0,
            "last_webhook_received_at": None
        }
        if RAZORPAY_STATUS_FILE.exists():
            try:
                with open(RAZORPAY_STATUS_FILE, "r") as f:
                    data = json.load(f)
            except:
                pass
                
        data["events_received"] += 1
        import time
        from datetime import datetime
        data["last_webhook_received_at"] = datetime.now().isoformat()
        
        if status == "processed":
            data["events_processed"] += 1
        elif status == "duplicate":
            data["events_duplicate"] += 1
        elif status == "failed":
            data["events_failed"] += 1
        elif status == "unmatched":
            data["unmatched_events"] += 1
            
        with open(RAZORPAY_STATUS_FILE, "w") as f:
            json.dump(data, f)
            
    @staticmethod
    def get_status() -> dict:
        if RAZORPAY_STATUS_FILE.exists():
            with open(RAZORPAY_STATUS_FILE, "r") as f:
                return json.load(f)
        return {
            "events_received": 0,
            "events_processed": 0,
            "events_failed": 0,
            "events_duplicate": 0,
            "unmatched_events": 0,
            "last_webhook_received_at": None
        }

    @staticmethod
    def record_audit(audit_entry: Dict[str, Any]):
        audit_file = DATA_DIR / "razorpay_audit_log.json"
        log = []
        if audit_file.exists():
            try:
                with open(audit_file, "r") as f:
                    log = json.load(f)
            except Exception:
                pass
        
        # Prepend new entry
        log.insert(0, audit_entry)
        
        # Keep last 100 for lightweight demo log
        if len(log) > 100:
            log = log[:100]
            
        with open(audit_file, "w") as f:
            json.dump(log, f)

    @staticmethod
    def get_audit_log() -> list:
        audit_file = DATA_DIR / "razorpay_audit_log.json"
        if audit_file.exists():
            try:
                with open(audit_file, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return []
