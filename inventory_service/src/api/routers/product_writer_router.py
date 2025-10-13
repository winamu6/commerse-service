from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from inventory_service.src.api.depends import get_cached_product_writer
from inventory_service.src.schemas import ProductCreate, ProductRead, ProductUpdate
from inventory_service.src.services.cached.cached_writer_service import CachedProductWriter

router = APIRouter(prefix="/products_write", tags=["ProductsWrite"])


@router.post("/", response_model=ProductRead)
async def create_product(
    data: ProductCreate,
    service: CachedProductWriter = Depends(get_cached_product_writer),
):
    product = await service.cached_create_product(data)
    return product


@router.put("/{product_id}", response_model=Optional[ProductRead])
async def update_product(
    product_id: int,
    data: ProductUpdate,
    service: CachedProductWriter = Depends(get_cached_product_writer),
):
    product = await service.cached_update_product(product_id, data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.delete("/{product_id}", response_model=bool)
async def delete_product(
    product_id: int,
    service: CachedProductWriter = Depends(get_cached_product_writer),
):
    success = await service.cached_delete_product(product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return success
