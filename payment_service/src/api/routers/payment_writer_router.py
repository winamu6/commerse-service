from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query

from payment_service.src.api.depends import get_cached_payment_writer
from payment_service.src.schemas import PaymentResponse, PaymentCreate, PaymentUpdate
from payment_service.src.services.cached.cached_writer_service import CachedPaymentWriter

router = APIRouter(prefix="/payment_writer", tags=["PaymentWrite"])


#Создание платежа
@router.post("/", response_model=PaymentResponse)
async def create_order(
    data: PaymentCreate,
    service: CachedPaymentWriter = Depends(get_cached_payment_writer),
):
    order = await service.cached_create_payment(data)
    return order

#Обновление платежа
@router.put("/update/{payment_id}", response_model=PaymentResponse)
async def update_order(
    payment_id: int,
    update_data: PaymentUpdate,
    service: CachedPaymentWriter = Depends(get_cached_payment_writer),
):
    order = await service.cached_update_payment(payment_id, update_data)
    if not order:
        raise HTTPException(status_code=404, detail="Payment not found")
    return order
