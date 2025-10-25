from fastapi import Depends
from src.db.database import async_session_maker
from src.db.cache import redis_client
from src.repository.writer_repository import WriterRepository
from src.services.writer_service import OrderWriter
from src.services.cache_service import OrderCache
from src.services.cached.cached_writer_service import CachedOrderWriter


async def get_order_write_repository() -> WriterRepository:
    async with async_session_maker() as session:
        yield WriterRepository(session)


async def get_cache_service() -> OrderCache:
    yield OrderCache(redis_client)


async def get_order_writer(
    repo: WriterRepository = Depends(get_order_write_repository),
) -> OrderWriter:
    return OrderWriter(repo)


async def get_cached_order_writer(
    writer: OrderWriter = Depends(get_order_writer),
    cache: OrderCache = Depends(get_cache_service),
) -> CachedOrderWriter:
    return CachedOrderWriter(writer, cache)