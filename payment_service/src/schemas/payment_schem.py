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


class PaymentUpdate(BaseModel):
    order_id: Optional[str] = None
    amount: Optional[Decimal] = None
    currency: Optional[str] = None
    provider: Optional[str] = None
    user_id: Optional[int] = None
    status: Optional[PaymentStatus] = None
    provider_payment_id: Optional[str] = None
    provider_response: Optional[dict] = None


class PaymentFilter(BaseModel):
    user_id: Optional[int] = Field(None, example=42)
    order_id: Optional[str] = Field(None, example="ORD-2025-001")
    status: Optional[PaymentStatus] = Field(None)
    provider: Optional[str] = Field(None, example="yookassa")

    created_from: Optional[datetime] = None
    created_to: Optional[datetime] = None

    def to_sql_filters(self):
        return {
            k: v
            for k, v in self.dict().items()
            if v is not None and not k.startswith("created_")
        }


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


class PaymentResponse(BaseModel):
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
    payments: List[PaymentResponse]

class PaymentCreate(BaseModel):
    payment_uid: str = Field(..., example="PAY-2025-0001")
    order_id: str = Field(..., example="ORD-2025-001")
    user_id: Optional[int] = Field(None, example=42)

    amount: Decimal = Field(..., example="1999.99")
    currency: str = Field(default="RUB", example="RUB")

    status: PaymentStatus = Field(default=PaymentStatus.pending)
    provider: str = Field(..., example="yookassa")

    provider_payment_id: Optional[str] = Field(None, example="YK-123456")
    provider_response: Optional[dict] = Field(None, example={"raw": "response data"})

    class Config:
        json_schema_extra = {
            "example": {
                "payment_uid": "PAY-2025-0001",
                "order_id": "ORD-2025-001",
                "user_id": 42,
                "amount": "1999.99",
                "currency": "RUB",
                "status": "pending",
                "provider": "yookassa",
                "provider_payment_id": "YK-123456",
                "provider_response": {"ok": True}
            }
        }