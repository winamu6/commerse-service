from fastapi import Depends
from inventory_service.src.db.database import async_session_maker
from inventory_service.src.db.cache import redis_client
from inventory_service.src.repository.read_repository import ReadRepository
from inventory_service.src.services.reader_service import ProductReader
from inventory_service.src.services.cache_service import ProductCache
from inventory_service.src.services.cached.cached_reader_service import CachedProductReader


async def get_product_read_repository() -> ReadRepository:
    async with async_session_maker() as session:
        yield ReadRepository(session)


async def get_cache_service() -> ProductCache:
    yield ProductCache(redis_client)


async def get_product_reader(
    repo: ReadRepository = Depends(get_product_read_repository),
) -> ProductReader:
    return ProductReader(repo)


async def get_cached_product_reader(
    reader: ProductReader = Depends(get_product_reader),
    cache: ProductCache = Depends(get_cache_service),
) -> CachedProductReader:
    return CachedProductReader(reader, cache)
