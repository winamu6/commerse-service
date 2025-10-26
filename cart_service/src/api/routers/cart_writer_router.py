from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query

from cart_service.src.api.depends import get_writer_service
from cart_service.src.schemas import CartResponse
from cart_service.src.services.write_service import CartWriteService

router = APIRouter(prefix="/cart_write", tags=["CartWrite"])