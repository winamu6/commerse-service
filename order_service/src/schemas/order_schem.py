from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class OrderStatus(str, Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    SHIPPED = "SHIPPED"
    COMPLETED = "COMPLETED"
    CANCELED = "CANCELED"

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    price: float = Field(..., gt=0)

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemRead(OrderItemBase):
    id: int

    class Config:
        orm_mode = True

class OrderCreate(BaseModel):
    user_id: int
    items: List[OrderItemCreate]

class OrderRead(BaseModel):
    id: int
    user_id: int
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
    items: List[OrderItemRead]

    class Config:
        from_attributes: True