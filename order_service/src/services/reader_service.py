from typing import List, Optional

from src.repository import ReadRepository
from src.schemas import OrderRead


class OrderReader:
    def __init__(self, repository: ReadRepository):
        self.repo = repository

    async def get_order_by_id(self, order_id: int) -> Optional[OrderRead]:
        order = await self.repo.get_order_by_id(order_id)
        return OrderRead.from_orm(order) if order else None

    async def get_all_orders_for_user(
        self, user_id: int, limit: int = 100, offset: int = 0
    ) -> List[OrderRead]:
        orders = await self.repo.list_all_orders_for_user(user_id, limit, offset)
        return [OrderRead.from_orm(o) for o in orders]

    async def get_active_orders_for_user(
        self, user_id: int, limit: int = 100, offset: int = 0
    ) -> List[OrderRead]:
        orders = await self.repo.list_active_orders_for_user(user_id, limit, offset)
        return [OrderRead.from_orm(o) for o in orders]

    async def get_sorted_orders_by_status_for_user(
        self, user_id: int, limit: int = 100, offset: int = 0
    ) -> List[OrderRead]:
        orders = await self.repo.sort_orders_by_status_for_user(user_id, limit, offset)
        return [OrderRead.from_orm(o) for o in orders]