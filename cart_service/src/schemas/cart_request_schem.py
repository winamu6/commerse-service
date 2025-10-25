from pydantic import BaseModel, Field


class CartItemRequest(BaseModel):
    product_id: int = Field(...)
    name: str
    price: float
    quantity: int = Field(ge=1)

class UpdateQuantityRequest(BaseModel):
    quantity: int = Field(ge=1)