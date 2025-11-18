from asyncio import Protocol
from typing import Optional, List, Dict, Any
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from payment_service.src.models import Payment


class IReadRepository(Protocol):

    async def get_payment_by_id(self, payment_id: int) -> Optional[Payment]:
        ...

    async def list_payments(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Payment]:
        ...

    async def filter_payments(
        self,
        filters: Optional[Dict[str, Any]] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Payment]:
        ...