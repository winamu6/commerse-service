from sqlalchemy import Column, Integer, String, ForeignKey

from feedback_service.src.db import Base


class Feedback(Base):
    __tablename__ = "feedbacks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    description = Column(String, nullable=False, index=True)
    score = Column(Integer, nullable=False, index=True)

    # связь с продуктом
    product = relationship("Product", back_populates="feedbacks")