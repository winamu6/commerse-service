from asyncio import Protocol
from typing import Optional, List, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from payment_service.src.models import Payment


class IWriteRepository(Protocol):

    async def create_payment(self, payment: Payment) -> Payment:
        ...

    async def update_payment(self, payment_id: int, update_data: dict) -> Payment | None:
        ...