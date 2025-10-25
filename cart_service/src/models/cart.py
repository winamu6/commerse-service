from pydantic import BaseModel, Field
from typing import List

class CartItem(BaseModel):
    product_id: int
    name: str
    price: float
    quantity: int = Field(ge=1)

class Cart(BaseModel):
    user_id: int
    items: List[CartItem] = []
    total_price: float = 0.0
