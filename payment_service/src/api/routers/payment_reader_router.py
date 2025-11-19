from typing import List, Optional, Dict, Any

from fastapi import APIRouter, Depends, HTTPException, Query

from payment_service.src.api.depends import get_cached_payment_reader
from payment_service.src.schemas.payment_schem import PaymentResponse, PaymentFilter
from payment_service.src.services.cached.cached_reader_service import CachedPaymentReader

router = APIRouter(prefix="/payment_read", tags=["PaymentRead"])

#получить платеж по id
@router.get("/by_id/{payment_id}", response_model=PaymentResponse)
async def get_payment_by_id(
        payment_id: int,
        service: CachedPaymentReader = Depends(get_cached_payment_reader)
):
    payment= await service.get_cached_payment_by_id(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment

#получить список платежей
@router.get("/list/", response_model=List[PaymentResponse])
async def get_list_payment(
        limit: int = Query(100, ge=1),
        offset: int = Query(0, ge=0),
        service: CachedPaymentReader = Depends(get_cached_payment_reader)
):
    payment = await service.get_cached_list_payments(limit, offset)

    return payment

#получить отфильтрованный список платежей
@router.get("/filter", response_model=List[PaymentResponse])
async def filter_payments(
        filters: PaymentFilter = Depends(),
        limit: int = Query(100, ge=1),
        offset: int = Query(0, ge=0),
        service: CachedPaymentReader = Depends(get_cached_payment_reader)
):
    return await service.get_cached_filter_payment(filters, limit, offset)