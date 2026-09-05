# Razorpay Test Mode Integration

Financial CSI supports a strict, read-only Test Mode integration with Razorpay. This allows the system to receive, normalize, and log test payment events without any risk of real-money interventions.

## Architecture

```mermaid
graph TD
    A[Razorpay Webhook (Test)] -->|POST /api/webhooks/razorpay| B(Signature Verification)
    B -->|Verified| C(Idempotency Check)
    B -->|Invalid| D[400 Bad Request]
    C -->|New| E(Razorpay Normalizer)
    C -->|Duplicate| F[Log as Duplicate]
    E --> G[Financial CSI Event]
    G --> H[Event Analytics & Audit Trail]
```

## Safety Boundaries

1. **Test Mode Only**: The application strictly refuses to operate if `RAZORPAY_MODE` is not explicitly set to `test`.
2. **Read-Only**: The backend client only fetches data (e.g. testing connections via `GET /v1/orders`). It never initiates captures, refunds, or interventions.
3. **No Automated Intervention**: Financial CSI acts purely as an observer and pattern-matcher. The results are logged for analytics.

## Configuration

Set the following environment variables (or configure `.env`):

```bash
RAZORPAY_ENABLED=true
RAZORPAY_MODE=test
RAZORPAY_KEY_ID=<your_test_key_id>
RAZORPAY_KEY_SECRET=<your_test_key_secret>
RAZORPAY_WEBHOOK_SECRET=<your_webhook_secret>
```

## Supported Events

The normalizer converts the following Razorpay events into the `Financial CSI` schema:

- `payment.authorized` -> `PAYMENT_ATTEMPT`
- `payment.captured` -> `CAPTURE_SUCCESS`
- `payment.failed` -> `PAYMENT_FAILED`
- `refund.created` -> `REFUND_INITIATED`
- `refund.processed` -> `REFUND_SUCCESS`

## Local Testing

You can use the built-in simulator to push synthetic payloads through the webhook pipeline:

```bash
POST http://localhost:8000/api/webhooks/razorpay/simulate?fixture_id=capture
```
