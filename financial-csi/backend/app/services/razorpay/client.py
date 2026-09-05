import httpx
from typing import Dict, Any, Tuple
from app.core.config import settings

class RazorpayClient:
    """
    Lightweight read-only client for Razorpay Test Mode integration.
    Strictly forbids live mode actions.
    """
    
    BASE_URL = "https://api.razorpay.com/v1"

    @classmethod
    def validate_config(cls) -> Tuple[bool, str]:
        if not settings.RAZORPAY_ENABLED:
            return False, "Integration is disabled (RAZORPAY_ENABLED=false)."
        if settings.RAZORPAY_MODE != "test":
            return False, "Live mode is strictly forbidden. Set RAZORPAY_MODE=test."
        if not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
            return False, "Credentials not configured."
        return True, "Configured"

    @classmethod
    async def test_connection(cls) -> Dict[str, Any]:
        """
        Tests the connection by making a read-only request to the orders endpoint.
        Returns connection status.
        """
        is_valid, msg = cls.validate_config()
        if not is_valid:
            return {
                "success": False,
                "message": msg,
                "mode": settings.RAZORPAY_MODE
            }

        auth = (settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                # Use a safe, read-only endpoint (fetching 1 order)
                response = await client.get(
                    f"{cls.BASE_URL}/orders",
                    auth=auth,
                    params={"count": 1}
                )
                
                if response.status_code == 200:
                    return {
                        "success": True,
                        "message": "Connection successful",
                        "mode": settings.RAZORPAY_MODE
                    }
                elif response.status_code in (401, 403):
                    return {
                        "success": False,
                        "message": "Invalid API credentials",
                        "mode": settings.RAZORPAY_MODE
                    }
                else:
                    return {
                        "success": False,
                        "message": f"Unexpected response code: {response.status_code}",
                        "mode": settings.RAZORPAY_MODE
                    }
        except Exception as e:
            return {
                "success": False,
                "message": f"Connection failed: {str(e)}",
                "mode": settings.RAZORPAY_MODE
            }
