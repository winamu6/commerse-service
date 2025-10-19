from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import EmailStr

from src.api.depends import get_cached_auth_service
from src.schemas import Token

router = APIRouter(prefix="/auth", tags=["Auth"])

# вход в аккаунт + получить токен
@router.post("/login", response_model=Token)
async def login(
    email: EmailStr,
    password: str,
    response: Response,
    service=Depends(get_cached_auth_service),
):
    token = await service.authenticate_user(email, password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    response.set_cookie(
        key="refresh_token",
        value=token.refresh_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )

    return token

# обновить токен пользователя
@router.post("/refresh", response_model=Token)
async def refresh_tokens(
    refresh_token: str,
    response: Response,
    service=Depends(get_cached_auth_service),
):
    token = await service.refresh_tokens(refresh_token)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid or revoked refresh token")

    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        secure=True,
        samesite="lax",
    )
    response.set_cookie(
        key="refresh_token",
        value=token.refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
    )

    return token

# выйти из аккаунта
@router.post("/logout")
async def logout(
    refresh_token: str,
    response: Response,
    service=Depends(get_cached_auth_service),
):
    await service.revoke_refresh_token(refresh_token)

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    return {"detail": "Logged out successfully"}