from typing import Dict, Any, Optional
import time
import uuid
from datetime import datetime

# Map Razorpay events to internal types
EVENT_MAPPING = {
    "payment.authorized": "PAYMENT_ATTEMPT",
    "payment.captured": "CAPTURE_SUCCESS",
    "payment.failed": "PAYMENT_FAILED",
    "refund.created": "REFUND_INITIATED",
    "refund.processed": "REFUND_SUCCESS"
}

class RazorpayNormalizer:
    @staticmethod
    def normalize(webhook_payload: Dict[str, Any], source: str = "razorpay_test") -> Dict[str, Any]:
        """
        Converts Razorpay webhook structure to internal Event dict.
        """
        event_type_rzp = webhook_payload.get("event")
        internal_type = EVENT_MAPPING.get(event_type_rzp, "UNSUPPORTED")
        
        # Extract entities based on event payload structure
        payload = webhook_payload.get("payload", {})
        
        # Determine main entity (payment, refund, order)
        payment_entity = payload.get("payment", {}).get("entity", {})
        refund_entity = payload.get("refund", {}).get("entity", {})
        order_entity = payload.get("order", {}).get("entity", {})
        
        # Try to resolve identifiers
        payment_id = payment_entity.get("id") or refund_entity.get("payment_id")
        order_id = payment_entity.get("order_id") or order_entity.get("id")
        amount = payment_entity.get("amount") or refund_entity.get("amount") or 0
        
        if not order_id and not payment_id:
            # Cannot confidently associate
            order_id = "UNMATCHED"
            payment_id = "UNMATCHED"
            
        timestamp_epoch = webhook_payload.get("created_at", int(time.time()))
        dt = datetime.fromtimestamp(timestamp_epoch).isoformat()
        
        return {
            "event_id": f"EVT_{uuid.uuid4().hex[:8]}",
            "transaction_id": payment_id or order_id, # In our system, transaction_id ties the lifecycle
            "order_id": order_id,
            "event_type": internal_type,
            "timestamp": dt,
            "amount_paise": amount,
            "source": source,
            "source_event_type": event_type_rzp,
            "source_event_id": webhook_payload.get("account_id", "") + "_" + str(timestamp_epoch) # Synthetic source ID
        }
