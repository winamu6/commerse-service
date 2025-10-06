from fastapi import Depends
from inventory_service.src.services.cached.cached_reader_service import CachedProductReader
from inventory_service.src.services.read_service import ProductReader
from inventory_service.src.services.cache_service import ProductCache
from inventory_service.src.repository.product_repository import ProductRepository
from inventory_service.src.db.database import async_session_maker
from inventory_service.src.db.cache import redis_client

async def get_product_repository() -> ProductRepository:
    async for session in async_session_maker():
        yield ProductRepository(session)

async def get_cache_service() -> ProductCache:
    yield ProductCache(redis_client)

async def get_cached_product_reader(
    repo: ProductRepository = Depends(get_product_repository),
    cache: ProductCache = Depends(get_cache_service)
) -> CachedProductReader:
    reader = ProductReader(repo)
    return CachedProductReader(reader, cache)