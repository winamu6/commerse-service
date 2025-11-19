from typing import Optional, List, Dict, Any
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from payment_service.src.models import Payment


class ReadRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_payment_by_id(self, payment_id: int) -> Optional[Payment]:
        stmt = select(Payment).where(Payment.id == payment_id)
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_payments(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None
    ) -> List[Payment]:
        stmt = select(Payment)
        if offset:
            stmt = stmt.offset(offset)
        if limit:
            stmt = stmt.limit(limit)

        result = await self._session.execute(stmt)
        return result.scalars().all()

    async def filter_payments(
        self,
        filters: Dict[str, Any],
        created_from: Optional[Any] = None,
        created_to: Optional[Any] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Payment]:

        stmt = select(Payment)

        conditions = []

        for field, value in filters.items():
            if hasattr(Payment, field):
                conditions.append(getattr(Payment, field) == value)

        if created_from:
            conditions.append(Payment.created_at >= created_from)
        if created_to:
            conditions.append(Payment.created_at <= created_to)

        if conditions:
            stmt = stmt.where(and_(*conditions))

        stmt = stmt.offset(offset).limit(limit)

        result = await self._session.execute(stmt)
        return result.scalars().all()
