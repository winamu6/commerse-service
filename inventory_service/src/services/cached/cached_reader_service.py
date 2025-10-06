from functools import cache
from typing import List, Optional
from inventory_service.src.services.read_service import ProductReader
from inventory_service.src.schemas import ProductRead
from inventory_service.src.services import ProductCache


class CachedProductReader:
    """Reader-сервис с поддержкой кэширования через Redis."""

    def __init__(self, reader: ProductReader, cache: ProductCache):
        self.reader = reader
        self.cache = cache

    async def get_product_by_id(self, product_id: int) -> Optional[ProductRead]:
        cache_key = f"product:{product_id}"
        cached = await self.cache.get(cache_key)
        if cached:
            return ProductRead(**cached)

        product = await self.reader.get_product_by_id(product_id)
        if product:
            await self.cache.set(cache_key, product.dict(), expire=120)
        return product

    async def get_list_products(self, limit: int = 100, offset: int = 0) -> List[ProductRead]:
        cache_key = f"products:list:{limit}:{offset}"
        cached = await self.cache.get(cache_key)
        if cached:
            return [ProductRead(**p) for p in cached]

        products = await self.reader.get_list_products(limit, offset)
        await self.cache.set(cache_key, [p.dict() for p in products], expire=60)
        return products

    async def get_products_by_name(self, name: str, limit: int = 100, offset: int = 0) -> List[ProductRead]:
        cache_key = f"products:name:{name}:{limit}:{offset}"
        cached = await self.cache.get(cache_key)
        if cached:
            return [ProductRead(**p) for p in cached]

        products = await self.reader.get_products_by_name(name, limit, offset)
        await self.cache.set(cache_key, [p.dict() for p in products], expire=60)
        return products

    async def filter_products_by_category(self, category: str, limit: int = 100, offset: int = 0) -> List[ProductRead]:
        cache_key = f"products:category:{category}:{limit}:{offset}"
        cached = await self.cache.get(cache_key)
        if cached:
            return [ProductRead(**p) for p in cached]

        products = await self.reader.filter_products_by_category(category, limit, offset)
        await self.cache.set(cache_key, [p.dict() for p in products], expire=60)
        return products

    async def sort_products_by_rating(self, order: str = "desc") -> List[ProductRead]:
        cache_key = f"products:sorted:{order}"
        cached = await self.cache.get(cache_key)
        if cached:
            return [ProductRead(**p) for p in cached]

        products = await self.reader.sort_products_by_rating()
        await self.cache.set(cache_key, [p.dict() for p in products], expire=60)
        return products

    async def get_products_by_seller(self, seller_id: int, limit: int = 100, offset: int = 0) -> List[ProductRead]:
        cache_key = f"products:seller:{seller_id}:{limit}:{offset}"
        cached = await self.cache.get(cache_key)
        if cached:
            return [ProductRead(**p) for p in cached]

        products = await self.reader.get_products_by_seller(seller_id, limit, offset)
        await self.cache.set(cache_key, [p.dict() for p in products], expire=60)
        return products