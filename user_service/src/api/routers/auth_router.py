from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Header
from user_service.src.api.depends import get_cached_auth_service
from user_service.src.schemas import Token, UserRead
from user_service.src.utils.jwt_util import decode_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
async def login(
    email: str,
    password: str,
    service=Depends(get_cached_auth_service),
):
    token = await service.authenticate_user(email, password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    return token


@router.post("/refresh", response_model=Token)
async def refresh_tokens(
    refresh_token: str,
    service=Depends(get_cached_auth_service),
):
    token = await service.refresh_tokens(refresh_token)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid or revoked refresh token")
    return token


@router.post("/logout")
async def logout(
    refresh_token: str,
    service=Depends(get_cached_auth_service),
):
    await service.revoke_refresh_token(refresh_token)
    return {"detail": "Logged out successfully"}


@router.get("/users/me", response_model=UserRead)
async def get_current_user(
    authorization: Optional[str] = Header(None),
    service=Depends(get_cached_auth_service),
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Authorization header missing")

    token_str = authorization.split(" ")[1]
    payload = decode_token(token_str)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload["sub"])
    user = await service.reader.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
