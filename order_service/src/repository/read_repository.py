from sqlalchemy import select, and_, not_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional

from order_service.src.models import Order, OrderItem, OrderStatus


class ReadRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_order_by_id(self, order_id: int) -> Optional[Order]:
        stmt = (
            select(Order)
            .options(selectinload(Order.items))
            .where(Order.id == order_id)
        )
        result = await self.session.scalars(stmt)
        return result.first()

    async def list_all_orders_for_user(
        self, user_id: int, limit: int = 10, offset: int = 0
    ) -> List[Order]:
        stmt = (
            select(Order)
            .where(Order.user_id == user_id)
            .options(selectinload(Order.items))
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.scalars(stmt)
        return result.all()

    async def list_active_orders_for_user(
        self, user_id: int, limit: int = 10, offset: int = 0
    ) -> List[Order]:
        stmt = (
            select(Order)
            .where(
                and_(
                    Order.user_id == user_id,
                    Order.status.notin_([OrderStatus.CANCELED, OrderStatus.COMPLETED]),
                )
            )
            .options(selectinload(Order.items))
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.scalars(stmt)
        return result.all()

    async def sort_orders_by_status(
        self, desc: bool = True, limit: int = 10, offset: int = 0
    ) -> List[Order]:
        order_by_clause = Order.status.desc() if desc else Order.status.asc()
        stmt = select(Order).order_by(order_by_clause).limit(limit).offset(offset)
        result = await self.session.scalars(stmt)
        return result.all()
