from pydantic import BaseModel, Field

class CartItemRequest(BaseModel):
    product_id: int
    quantity: int = Field(ge=1)