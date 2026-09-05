from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    transaction_id: str
    order_id: str
    customer_id: str
    merchant_id: str
    amount_paise: int
    currency: str = "INR"
    payment_method: str
    gateway: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    outcome: str
    loss_flag: bool
    loss_amount: float
    loss_type: Optional[str] = None
