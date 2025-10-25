from typing import Optional, Tuple, List

from order_service.src.services.writer_service import OrderWriter
from order_service.src.schemas import OrderCreate, OrderRead, OrderStatus
from order_service.src.services.cache_service import OrderCache

class CachedOrderWriter:

    def __init__(self, writer: OrderWriter, cache: OrderCache):
        self.writer = writer
        self.cache = cache

    async def cached_create_order(self, order_data: OrderCreate):
        order_read, _ = await self.writer.create_order(order_data, order_data.items)

        cache_key = f"order:{order_read.id}"
        await self.cache.set(cache_key, order_read.model_dump_json(), expire=120)
        await self.cache.delete_pattern(f"orders:user:{order_read.user_id}:*")

        return order_read

    async def cached_update_order(
            self, order_id: int, new_status: OrderStatus
    ) -> Optional[OrderRead]:
        order = await self.writer.update_order(order_id, new_status)
        if not order:
            return None

        cache_key = f"order:{order.id}"

        await self.cache.set(cache_key, order.model_dump_json(), expire=120)
        await self.cache.delete_pattern(f"orders:user:{order.user_id}:*")

        return order

    async def cached_delete_order(self, order_id: int) -> bool:
        deleted = await self.writer.delete_order(order_id)

        if deleted:
            await self.cache.delete(f"order:{order_id}")
            await self.cache.delete_pattern("orders:user:*")

        return deleted