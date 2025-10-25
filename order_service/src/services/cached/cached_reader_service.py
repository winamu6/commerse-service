from typing import List, Optional
from src.services.reader_service import OrderReader
from src.schemas import OrderRead
from src.services.cache_service import OrderCache


class CachedOrderReader:

    def __init__(self, reader: OrderReader, cache: OrderCache):
        self.reader = reader
        self.cache = cache

    async def get_cached_order_by_id(self, order_id: int) -> Optional[OrderRead]:
        cache_key = f"order:{order_id}"
        cached = await self.cache.get(cache_key)
        if cached:
            return OrderRead(**cached)

        order = await self.reader.get_order_by_id(order_id)
        if order:
            await self.cache.set(cache_key, order.dict(), expire=120)
        return order

    async def get_cached_all_orders_for_user(
            self, user_id: int, limit: int = 100, offset: int = 0
    ) -> List[OrderRead]:
        cache_key = f"orders:user:{user_id}:all:{limit}:{offset}"
        cached = await self.cache.get(cache_key)
        if cached:
            return [OrderRead(**o) for o in cached]

        orders = await self.reader.get_all_orders_for_user(user_id, limit, offset)
        await self.cache.set(cache_key, [o.dict() for o in orders], expire=60)
        return orders

    async def get_cached_active_orders_for_user(
            self, user_id: int, limit: int = 100, offset: int = 0
    ) -> List[OrderRead]:
        cache_key = f"orders:user:{user_id}:active:{limit}:{offset}"
        cached = await self.cache.get(cache_key)
        if cached:
            return [OrderRead(**o) for o in cached]

        orders = await self.reader.get_active_orders_for_user(user_id, limit, offset)
        await self.cache.set(cache_key, [o.dict() for o in orders], expire=60)
        return orders

    async def get_cached_sorted_orders_by_status_for_user(
            self, user_id: int, limit: int = 100, offset: int = 0
    ) -> List[OrderRead]:
        cache_key = f"orders:user:{user_id}:sorted:{limit}:{offset}"
        cached = await self.cache.get(cache_key)
        if cached:
            return [OrderRead(**o) for o in cached]

        orders = await self.reader.get_sorted_orders_by_status_for_user(
            user_id, limit, offset
        )
        await self.cache.set(cache_key, [o.dict() for o in orders], expire=60)
        return orders