from pydantic import BaseModel

class FeedbackCreate(BaseModel):
    description: str
    cost: int

class FeedbackRead(BaseModel):
    description: str
    cost: int

    class Config:
        orm_mode = True
