from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from inventory_service.src.db import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(String, nullable=False, index=True)
    cost = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    category = Column(String, nullable=False, index=True)
    rating = Column(Float, nullable=False, default=0)
    seller_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)

    feedbacks = relationship("Feedback", back_populates="product")
