from sqlalchemy import Column, Integer, String

from payment_service.src.db import Base


class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String, nullable=False, index=True)
    amount = Column(String, unique=True, nullable=False, index=True)
    status = Column(String, nullable=False)
    provider = Column(String, nullable=False)