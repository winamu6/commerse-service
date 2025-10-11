from fastapi import APIRouter, Depends, HTTPException

from inventory_service.src.api.depends import get_cached_product_reader
from inventory_service.src.schemas.product_schem import ProductRead
from inventory_service.src.services.cached.cached_reader_service import CachedProductReader

router = APIRouter(prefix="/products_read", tags=["ProductsRead"])

@router.get("/{product_id}", response_model=ProductRead)
async def get_product_by_id(
    product_id: int,
    service: CachedProductReader = Depends(get_cached_product_reader),
):
    product = await service.get_cached_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product