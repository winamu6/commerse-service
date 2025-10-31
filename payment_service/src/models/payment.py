from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Enum, func
from payment_service.src.db import Base
import enum


class PaymentStatus(str, enum.Enum):
    pending = "pending"
    processing = "processing"
    success = "success"
    failed = "failed"
    refunded = "refunded"


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    payment_uid = Column(String, unique=True, index=True)
    order_id = Column(String, nullable=False, index=True)
    user_id = Column(Integer, nullable=True)
    amount = Column(Numeric(10, 2), nullable=False)
    currency = Column(String(3), default="RUB")

    status = Column(Enum(PaymentStatus), default=PaymentStatus.pending, nullable=False)
    provider = Column(String, nullable=False)

    provider_payment_id = Column(String, nullable=True, index=True)
    provider_response = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())