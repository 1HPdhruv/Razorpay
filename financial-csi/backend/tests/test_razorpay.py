import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.razorpay.signature import verify_webhook_signature
from app.services.razorpay.normalizer import RazorpayNormalizer
from app.services.razorpay.fixtures import PAYMENT_CAPTURED_FIXTURE
from app.services.razorpay.webhook import WebhookManager
from app.core.config import settings

client = TestClient(app)

def test_signature_verification():
    secret = "mysecret"
    payload = '{"test": 123}'
    
    # Generate valid signature
    import hmac
    import hashlib
    valid_sig = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    
    assert verify_webhook_signature(payload, valid_sig, secret) == True
    assert verify_webhook_signature(payload, "invalid_sig", secret) == False
    assert verify_webhook_signature(payload, valid_sig, "") == False

def test_event_normalization():
    norm = RazorpayNormalizer.normalize(PAYMENT_CAPTURED_FIXTURE)
    assert norm["event_type"] == "CAPTURE_SUCCESS"
    assert norm["transaction_id"] == "pay_TestPayment123"
    assert norm["amount_paise"] == 50000
    assert norm["source"] == "razorpay_test"

def test_webhook_api_disabled():
    # settings.RAZORPAY_ENABLED is False by default
    res = client.post("/api/webhooks/razorpay/simulate?fixture_id=capture")
    assert res.status_code == 403

def test_webhook_simulate(monkeypatch):
    monkeypatch.setattr(settings, "RAZORPAY_ENABLED", True)
    monkeypatch.setattr(settings, "RAZORPAY_MODE", "test")
    
    res = client.post("/api/webhooks/razorpay/simulate?fixture_id=capture")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
    
    # Second time should be duplicate
    res2 = client.post("/api/webhooks/razorpay/simulate?fixture_id=capture")
    assert res2.status_code == 200
    assert "Duplicate" in res2.json()["message"]

def test_razorpay_connection_endpoint(monkeypatch):
    monkeypatch.setattr(settings, "RAZORPAY_ENABLED", True)
    monkeypatch.setattr(settings, "RAZORPAY_MODE", "test")
    monkeypatch.setattr(settings, "RAZORPAY_KEY_ID", "rzp_test_fake")
    monkeypatch.setattr(settings, "RAZORPAY_KEY_SECRET", "fake_secret")
    
    # We expect a failure because these are fake keys and they'll hit the live API
    # But we mock the httpx client to return 200
    import httpx
    class MockResponse:
        status_code = 200
        
    class MockAsyncClient:
        def __init__(self, *args, **kwargs):
            pass
        async def __aenter__(self):
            return self
        async def __aexit__(self, exc_type, exc_val, exc_tb):
            pass
        async def get(self, *args, **kwargs):
            return MockResponse()
            
    monkeypatch.setattr(httpx, "AsyncClient", MockAsyncClient)
    
    res = client.post("/api/integrations/razorpay/test-connection")
    assert res.status_code == 200
    assert res.json()["success"] == True
    
def test_razorpay_connection_live_mode_blocked(monkeypatch):
    monkeypatch.setattr(settings, "RAZORPAY_ENABLED", True)
    monkeypatch.setattr(settings, "RAZORPAY_MODE", "live")
    
    res = client.post("/api/integrations/razorpay/test-connection")
    # Will fail at validation before even hitting the endpoint
    assert res.status_code == 400
    assert "Live mode is strictly forbidden" in res.json()["detail"]
