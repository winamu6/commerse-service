from sqlalchemy import Column, Integer, String, DateTime, func

from src.db import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    product_id = Column(Integer, nullable=False, index=True)
    description = Column(String, nullable=False, index=True)
    score = Column(Integer, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False, index=True)

    # product = relationship("Product", back_populates="feedbacks")