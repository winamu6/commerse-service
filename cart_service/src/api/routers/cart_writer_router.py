from fastapi import APIRouter, Depends, HTTPException

from src.api.depends import get_cart_write_service
from src.schemas import CartResponse, CartItemRequest
from src.services.write_service import CartWriteService

router = APIRouter(prefix="/cart_write", tags=["CartWrite"])

@router.post("/cart/{user_id}/items", response_model=CartResponse)
async def add_item(
    user_id: int,
    data: CartItemRequest,
    service: CartWriteService = Depends(get_cart_write_service),
):
    cart = await service.add_item(user_id, data)
    return cart

@router.put("/cart/{user_id}/items/{product_id}", response_model=CartResponse)
async def update_quantity(
    user_id: int,
    product_id: int,
    quantity: int,
    service: CartWriteService = Depends(get_cart_write_service),
):
    cart = await service.update_quantity(user_id, product_id, quantity)
    return cart

@router.delete("/cart/{user_id}/items/{product_id}", response_model=CartResponse)
async def remove_item(
    user_id: int,
    product_id: int,
    service: CartWriteService = Depends(get_cart_write_service),
):
    cart = await service.remove_item(user_id, product_id)
    return cart

@router.delete("/cart/{user_id}")
async def clear_cart(
        user_id: int,
        service: CartWriteService = Depends(get_cart_write_service)
):
    try:
        await service.clear_cart(user_id)
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))