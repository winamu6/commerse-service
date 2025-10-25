from pydantic import BaseModel
from typing import List

class CartItemResponse(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int
    item_total: float

class CartResponse(BaseModel):
    user_id: int
    items: List[CartItemResponse]
    total_price: float

    class Config:
        from_attributes = True