from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from order_service.src.api.depends import get_cached_order_reader
from order_service.src.schemas.order_schem import OrderRead
from order_service.src.services.cached.cached_reader_service import CachedOrderReader

router = APIRouter(prefix="/order_read", tags=["OrderRead"])

@router.get("/by_id/{order_id}", response_model=OrderRead)
async def get_order_by_id(
        order_id: int,
        service: CachedOrderReader = Depends(get_cached_order_reader)
):
    order = await service.get_cached_order_by_id(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.get("/list/{user_id}", response_model=List[OrderRead])
async def get_list_for_user(
        user_id: int,
        limit: int = Query(100, ge=1),
        offset: int = Query(0, ge=0),
        service: CachedOrderReader = Depends(get_cached_order_reader)
):
    orders = await service.get_cached_all_orders_for_user(user_id,
                                                          limit,
                                                          offset)

    return orders

@router.get("/list/active/{user_id}", response_model=List[OrderRead])
async def get_list_active_for_user(
        user_id: int,
        limit: int = Query(100, ge=1),
        offset: int = Query(0, ge=0),
        service: CachedOrderReader = Depends(get_cached_order_reader)
):
    orders = await service.get_cached_active_orders_for_user(user_id,
                                                             limit,
                                                             offset)

    return orders

@router.get("/list/sort/{user_id}", response_model=List[OrderRead])
async def get_sort_for_user(
        user_id: int,
        limit: int = Query(100, ge=1),
        offset: int = Query(0, ge=0),
        service: CachedOrderReader = Depends(get_cached_order_reader)
):
    orders = await service.get_cached_sorted_orders_by_status_for_user(user_id,
                                                                       limit,
                                                                       offset)

    return orders