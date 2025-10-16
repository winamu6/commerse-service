from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from user_service.src.api.depends import get_cached_user_reader
from user_service.src.schemas.user_schem import UserRead
from user_service.src.services.cached.cached_reader_service import CachedUserReader

router = APIRouter(prefix="/user_read", tags=["UserRead"])

#пользователь по id
@router.get("/by_id/{user_id}", response_model=UserRead)
async def get_product_by_id(
    user_id: int,
    service: CachedUserReader = Depends(get_cached_user_reader),
):
    product = await service.get_cached_user_by_id(user_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

#пользователь по email
@router.get("/email/{email}", response_model=UserRead)
async def get_user_by_mail(
    email: str,
    service: CachedUserReader = Depends(get_cached_user_reader),
):
    product = await service.get_cached_user_by_mail(email)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

#список пользователей
@router.get("/list", response_model=List[UserRead])
async def get_list_products(
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    service: CachedUserReader = Depends(get_cached_user_reader),
):
    products = await service.get_cached_all_users(limit, offset)
    return products