from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from order_service.src.api.depends import get_cached_order_writer
from order_service.src.schemas import OrderCreate, OrderRead, OrderStatus
from order_service.src.services.cached.cached_writer_service import CachedOrderWriter

router = APIRouter(prefix="/orders_writer", tags=["OrdersWriter"])

#создание заказа
@router.post("/", response_model=OrderRead)
async def create_order(
    data: OrderCreate,
    service: CachedOrderWriter = Depends(get_cached_order_writer),
):
    order = await service.cached_create_order(data)
    return order

#обновить статус заказа
@router.put("/update/{order_id}", response_model=Optional[OrderRead])
async def update_order(
    order_id: int,
    data: OrderStatus,
    service: CachedOrderWriter = Depends(get_cached_order_writer),
):
    order = await service.cached_update_order(order_id, data)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

#удалить заказ из базы данных
@router.delete("/delete/{order_id}", response_model=bool)
async def delete_order(
    order_id: int,
    service: CachedOrderWriter = Depends(get_cached_order_writer),
):
    success = await service.cached_delete_order(order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Order not found")
    return success