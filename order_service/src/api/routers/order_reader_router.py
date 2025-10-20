from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from order_service.src.api.depends import get_cached_order_reader
from order_service.src.schemas.order_schem import OrderRead
from order_service.src.services.cached.cached_reader_service import CachedOrderReader

router = APIRouter(prefix="/order_read", tags=["OrderRead"])
