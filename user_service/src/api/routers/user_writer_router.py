from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from user_service.src.api.depends import get_cached_user_writer, get_user_writer
from user_service.src.schemas import UserCreate, UserRead, UserUpdate
from user_service.src.services.cached import CachedUserWriter
from user_service.src.services.writer_service import UserWriter

router = APIRouter(prefix="/user_write", tags=["UserWrite"])

#создать пользователя
@router.post("/", response_model=UserRead)
async def create_user(
    data: UserCreate,
    service: UserWriter = Depends(get_user_writer),
):
    user = await service.create_user(data)
    return user

#обновить данные пользователя
@router.put("/{user_id}", response_model=Optional[UserRead])
async def update_user(
    user_id: int,
    data: UserUpdate,
    service: CachedUserWriter = Depends(get_cached_user_writer),
):
    user = await service.cached_update_user(user_id, data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

#удалить пользователя
@router.delete("/{user_id}", response_model=bool)
async def delete_user(
    user_id: int,
    service: CachedUserWriter = Depends(get_cached_user_writer),
):
    success = await service.cached_delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success

#обновить пароль пользователя
@router.put("/{user_id}", response_model=Optional[UserRead])
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
@router.delete("/{user_id}", response_model=bool)
async def reset_password(
    user_id: int,
    password: str,
    service: CachedUserWriter = Depends(get_cached_user_writer),
):
    success = await service.cached_reset_password(user_id, password)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return success