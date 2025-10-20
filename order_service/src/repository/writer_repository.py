from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, Tuple, List

from order_service.src.models import Order, OrderItem, OrderStatus


class WriterRepository:
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create_order(self, order: Order, order_items: List[OrderItem]) -> Tuple[Order, List[OrderItem]]:
        self.session.add(order)
        for item in order_items:
            item.order = order
            self.session.add(item)

        await self.session.commit()
        await self.session.refresh(order)
        for item in order_items:
            await self.session.refresh(item)

        return order, order_items


    async def update_order_status(self, order_id: int, new_status: OrderStatus) -> Optional[Order]:
        result = await self.session.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        if not order:
            return None

        order.status = new_status
        await self.session.commit()
        await self.session.refresh(order)
        return order


    async def delete_order(self, order_id: int) -> bool:
        order = await self.session.get(Order, order_id)
        if not order:
            return False

        await self.session.delete(order)
        await self.session.commit()
        return True