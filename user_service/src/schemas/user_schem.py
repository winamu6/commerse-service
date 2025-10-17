from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, constr, Field


class UserCreate(BaseModel):
    full_name: constr(min_length=1, max_length=255)
    email: EmailStr
    password: constr(min_length=8, max_length=64)
    password_confirm: str

    def validate_passwords(self):
        if self.password != self.password_confirm:
            raise ValueError("Passwords do not match")


class UserUpdate(BaseModel):
    full_name: Optional[constr(min_length=1, max_length=255)] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=8, max_length=64)] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None


class UserRead(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool
    is_verified: bool
    role: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
