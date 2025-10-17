from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi import Response

from user_service.src.api.depends import get_cached_auth_service
from user_service.src.api.depends.auth_depends import get_current_user_from_cookie
from user_service.src.schemas import Token, UserRead

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login", response_model=Token)
async def login(
    email: str,
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
        secure=False,
        samesite="lax",
    )

    return token


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
        key="refresh_token",
        value=token.refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
    )

    return token


@router.post("/logout")
async def logout(
    refresh_token: str,
    service=Depends(get_cached_auth_service),
):
    await service.revoke_refresh_token(refresh_token)
    return {"detail": "Logged out successfully"}


@router.get("/users/me", response_model=UserRead)
async def me(current_user=Depends(get_current_user_from_cookie)):
    return current_user