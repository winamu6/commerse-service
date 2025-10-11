from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from inventory_service.src.api.depends import get_cached_product_reader
from inventory_service.src.schemas.product_schem import ProductRead
from inventory_service.src.services.cached.cached_reader_service import CachedProductReader

router = APIRouter(prefix="/products_read", tags=["ProductsRead"])

@router.get("/by_id/{product_id}", response_model=ProductRead)
async def get_product_by_id(
    product_id: int,
    service: CachedProductReader = Depends(get_cached_product_reader),
):
    product = await service.get_cached_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/list", response_model=List[ProductRead])
async def get_list_products(
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    service: CachedProductReader = Depends(get_cached_product_reader),
):
    products = await service.get_cached_list_products(limit, offset)
    return products


@router.get("/by_name", response_model=List[ProductRead])
async def get_products_by_name(
    name: str,
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    service: CachedProductReader = Depends(get_cached_product_reader),
):
    products = await service.get_cached_products_by_name(name, limit, offset)
    return products


@router.get("/by_category", response_model=List[ProductRead])
async def get_products_by_category(
    category: str,
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    service: CachedProductReader = Depends(get_cached_product_reader),
):
    products = await service.filter_cached_products_by_category(category, limit, offset)
    return products


@router.get("/sorted_by_rating", response_model=List[ProductRead])
async def sort_products_by_rating(
    order: str = Query("desc", regex="^(asc|desc)$"),
    service: CachedProductReader = Depends(get_cached_product_reader),
):
    products = await service.sort_cached_products_by_rating(order)
    return products


@router.get("/by_seller/{seller_id}", response_model=List[ProductRead])
async def get_products_by_seller(
    seller_id: int,
    limit: int = Query(100, ge=1),
    offset: int = Query(0, ge=0),
    service: CachedProductReader = Depends(get_cached_product_reader),
):
    products = await service.get_cached_products_by_seller(seller_id, limit, offset)
    return products
