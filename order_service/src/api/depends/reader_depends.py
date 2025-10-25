from fastapi import Depends
from src.db.database import async_session_maker
from src.db.cache import redis_client
from src.repository.read_repository import ReadRepository
from src.services.reader_service import OrderReader
from src.services.cache_service import OrderCache
from src.services.cached.cached_reader_service import CachedOrderReader


async def get_order_read_repository() -> ReadRepository:
    async with async_session_maker() as session:
        yield ReadRepository(session)


async def get_cache_service() -> OrderCache:
    yield OrderCache(redis_client)


async def get_order_reader(
    repo: ReadRepository = Depends(get_order_read_repository),
) -> OrderReader:
    return OrderReader(repo)


async def get_cached_order_reader(
    reader: OrderReader = Depends(get_order_reader),
    cache: OrderCache = Depends(get_cache_service),
) -> CachedOrderReader:
    return CachedOrderReader(reader, cache)