# Razorpay Webhook Fixtures
# Mimics actual Test Mode payloads

PAYMENT_CAPTURED_FIXTURE = {
  "entity": "event",
  "account_id": "acc_TestModeAccount",
  "event": "payment.captured",
  "contains": [
    "payment"
  ],
  "payload": {
    "payment": {
      "entity": {
        "id": "pay_TestPayment123",
        "entity": "payment",
        "amount": 50000,
        "currency": "INR",
        "status": "captured",
        "order_id": "order_TestOrder123",
        "method": "card",
        "captured": True,
        "description": "Test Transaction",
        "created_at": 1725528000
      }
    }
  },
  "created_at": 1725528005
}

PAYMENT_FAILED_FIXTURE = {
  "entity": "event",
  "account_id": "acc_TestModeAccount",
  "event": "payment.failed",
  "contains": [
    "payment"
  ],
  "payload": {
    "payment": {
      "entity": {
        "id": "pay_TestPaymentFail",
        "entity": "payment",
        "amount": 120000,
        "currency": "INR",
        "status": "failed",
        "order_id": "order_TestOrderFail",
        "method": "upi",
        "error_code": "BAD_REQUEST_ERROR",
        "error_description": "Payment failed due to timeout",
        "created_at": 1725529000
      }
    }
  },
  "created_at": 1725529002
}

FIXTURES = {
    "capture": PAYMENT_CAPTURED_FIXTURE,
    "fail": PAYMENT_FAILED_FIXTURE
}
