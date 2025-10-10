from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class FeedbackBase(BaseModel):
    description: str
    cost: int


class FeedbackCreate(FeedbackBase):
    product_id: int
    user_id: Optional[int]

class FeedbackRead(FeedbackBase):
    id: int
    product_id: int
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
