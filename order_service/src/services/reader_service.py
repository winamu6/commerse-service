from typing import List

from order_service.src.repository import ReadRepository
from order_service.src.schemas import OrderRead

class ProductReader:
    def __init__(self, repository: ReadRepository):
        self.repo = repository

    async def get_order_by_id(self, product_id: int) -> OrderRead | None:
        product = await self.repo.get_order_by_id(product_id)
        return OrderRead.from_orm(product) if product else None

    async def get_list_all_orders_for_users(self, user_id: int,limit: int = 100, offset: int = 0) -> List[OrderRead]:
        orders = await self.repo.list_all_orders_for_user(user_id ,limit, offset)
        return [OrderRead.from_orm(o) for o in orders]

    async def get_list_active_orders_for_users(self, user_id: int,limit: int = 100, offset: int = 0) -> List[OrderRead]:
        orders = await self.repo.list_active_orders_for_user(user_id ,limit, offset)
        return [OrderRead.from_orm(o) for o in orders]

    async def get_sort_order_by_status_for_user(self, user_id: int,limit: int = 100, offset: int = 0) -> List[OrderRead]:
        orders = await self.repo.sort_orders_by_status_for_user(user_id ,limit, offset)
        return [OrderRead.from_orm(o) for o in orders]