from pydantic import BaseModel, Field
from decimal import Decimal
from typing import Optional, List
from enum import Enum
from datetime import datetime


class PaymentStatus(str, Enum):
    pending = "pending"
    processing = "processing"
    success = "success"
    failed = "failed"
    refunded = "refunded"


class PaymentBase(BaseModel):
    order_id: str = Field(..., example="ORD-2025-001")
    amount: Decimal = Field(..., example="1999.99")
    currency: str = Field(default="RUB", example="RUB")
    provider: str = Field(..., example="yookassa")


class PaymentCreate(PaymentBase):
    user_id: Optional[int] = Field(None, example=42)


class PaymentUpdateStatus(BaseModel):
    payment_uid: str
    status: PaymentStatus
    provider_response: Optional[dict] = None


class PaymentOut(BaseModel):
    id: int
    payment_uid: str
    order_id: str
    user_id: Optional[int]
    amount: Decimal
    currency: str
    provider: str
    status: PaymentStatus
    provider_payment_id: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes: True


class PaymentList(BaseModel):
    payments: List[PaymentOut]
