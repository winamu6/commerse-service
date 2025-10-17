from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Response

from user_service.src.api.depends import get_cached_user_writer, get_user_writer
from user_service.src.schemas import UserCreate, UserRead, UserUpdate
from user_service.src.services.cached import CachedUserWriter
from user_service.src.services.writer_service import UserWriter

router = APIRouter(prefix="/user_write", tags=["UserWrite"])

#создать пользователя
@router.post("/users", response_model=UserRead)
async def create_user(
    data: UserCreate,
    response: Response,
    service: UserWriter = Depends(get_user_writer),
):
    user = await service.create_user(data)

    token = await service.authenticate_user(user.email, user.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        secure=False,
        samesite="lax",
    )

    return user

#обновить данные пользователя
@router.put("/users/{user_id}/update", response_model=Optional[UserRead])
async def update_user(
    user_id: int,
    data: UserUpdate,
    service: CachedUserWriter = Depends(get_cached_user_writer),
):
    user = await service.cached_update_user(user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#обновить роль пользователя
@router.put("/users/{user_id}/role", response_model=Optional[UserRead])
async def update_user_role(
    user_id: int,
    role: str,
    service: CachedUserWriter = Depends(get_cached_user_writer),
):
    user = await service.cached_update_user_role(user_id, role)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#удалить пользователя
@router.delete("/users/{user_id}/delete", response_model=bool)
async def delete_user(
    user_id: int,
    service: CachedUserWriter = Depends(get_cached_user_writer),
):
    success = await service.cached_delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success

#обновить пароль пользователя
@router.put("/users/{user_id}/update_password", response_model=Optional[UserRead])
async def update_password(
    user_id: int,
    old_password: str,
    new_password: str,
    service: CachedUserWriter = Depends(get_cached_user_writer),
):
    user = await service.cached_update_password(user_id, old_password, new_password)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#сброс пароля
@router.put("/users/{user_id}/reset_password", response_model=bool)
async def reset_password(
    user_id: int,
    password: str,
    service: CachedUserWriter = Depends(get_cached_user_writer),
):
    success = await service.cached_reset_password(user_id, password)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success