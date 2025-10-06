from typing import Optional
from inventory_service.src.services import ProductWriter
from inventory_service.src.schemas import ProductCreate, ProductRead, ProductUpdate
from inventory_service.src.services import ProductCache

class CachedProductWriter:
    """Writer-сервис, который очищает кэш Redis при изменении данных."""

    def __init__(self, writer: ProductWriter, cache: ProductCache):
        self.writer = writer
        self.cache = cache

    async def create_product(self, data: ProductCreate) -> ProductRead:
        product = await self.writer.create_product(data)
        await self.cache.delete_pattern("products:list:*")
        await self.cache.delete_pattern("products:category:*")
        await self.cache.delete_pattern("products:name:*")
        return product

    async def update_product(self, product_id: int, data: ProductUpdate) -> Optional[ProductRead]:
        product = await self.writer.update_product(product_id, data)
        if product:
            await self.cache.delete(f"product:{product_id}")
            await self.cache.delete_pattern("products:list:*")
            await self.cache.delete_pattern("products:category:*")
            await self.cache.delete_pattern("products:name:*")
        return product

    async def delete_product(self, product_id: int) -> bool:
        success = await self.writer.delete_product(product_id)
        if success:
            await self.cache.delete(f"product:{product_id}")
            await self.cache.delete_pattern("products:list:*")
            await self.cache.delete_pattern("products:category:*")
            await self.cache.delete_pattern("products:name:*")
        return success
