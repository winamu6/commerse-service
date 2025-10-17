from typing import Optional

from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    description: str
    cost: int
    quantity: int
    category: str

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    cost: Optional[int] = None
    quantity: Optional[int] = None
    category: Optional[str] = None

class ProductRead(BaseModel):
    id: int
    name: str
    description: str
    cost: int
    quantity: int
    category: str
    seller_id: int

    class Config:
        orm_mode = True
