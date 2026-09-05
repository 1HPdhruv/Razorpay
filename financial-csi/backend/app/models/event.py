from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EventBase(BaseModel):
    event_id: str
    transaction_id: str
    order_id: str
    merchant_id: str
    event_type: str
    timestamp: datetime
    status: str
    amount_paise: Optional[int] = None
    gateway: Optional[str] = None
    payment_method: Optional[str] = None
    metadata: dict = {}
