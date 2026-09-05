import hmac
import hashlib

def verify_webhook_signature(payload_body: str, signature: str, secret: str) -> bool:
    """
    Verifies the Razorpay webhook signature.
    Official doc: HMAC SHA256 of the payload body using the webhook secret.
    """
    if not signature or not secret:
        return False
        
    expected_mac = hmac.new(
        key=secret.encode('utf-8'),
        msg=payload_body.encode('utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()
    
    return hmac.compare_digest(expected_mac, signature)
