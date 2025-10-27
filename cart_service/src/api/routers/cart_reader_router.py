from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from cart_service.src.api.depends import get_cart_read_service
from cart_service.src.schemas import CartResponse
from cart_service.src.services.read_service import CartReadService

router = APIRouter(prefix="/cart_read", tags=["CartRead"])

@router.get("/{user_id}/cart", response_model=List[CartResponse])
async def get_cart(
    user_id: int,
    service: CartReadService = Depends(get_cart_read_service),
):
    cart = await service.get_cart(user_id)
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    return cart