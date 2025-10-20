from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from order_service.src.api.depends import get_cached_order_writer
from order_service.src.schemas import OrderCreate, OrderRead, OrderStatus
from order_service.src.services.cached.cached_writer_service import CachedOrderWriter

router = APIRouter(prefix="/products_write", tags=["ProductsWrite"])