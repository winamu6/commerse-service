from pydantic import BaseModel

class RevokedToken(BaseModel):
    token: str
    revoked_at: int
    expires_at: int