from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from cart_service.src.api.depends import get_reader_service
from cart_service.src.schemas import CartResponse
from cart_service.src.services.read_service import CartReadService

router = APIRouter(prefix="/cart_read", tags=["CartRead"])