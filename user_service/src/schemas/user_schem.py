from datetime import date
from typing import Optional

from pydantic import BaseModel, Field

class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str
    password_confirm: str

class UserUpdate(BaseModel):
    description: Optional[str] = None
    cost: Optional[int] = None
    date: Optional[date] = None

class UserRead(BaseModel):
    id: int
    date: date
    description: str
    cost: int
