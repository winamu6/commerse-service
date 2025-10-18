from fastapi import Depends
from src.db.database import async_session_maker
from src.db.cache import redis_client
from src.repository.writer_repository import WriterRepository
from src.services.writer_service import ProductWriter
from src.services.cache_service import ProductCache
from src.services.cached.cached_writer_service import CachedProductWriter


async def get_product_write_repository() -> WriterRepository:
    async with async_session_maker() as session:
        yield WriterRepository(session)


async def get_cache_service() -> ProductCache:
    yield ProductCache(redis_client)


async def get_product_writer(
    repo: WriterRepository = Depends(get_product_write_repository),
) -> ProductWriter:
    return ProductWriter(repo)


async def get_cached_product_writer(
    writer: ProductWriter = Depends(get_product_writer),
    cache: ProductCache = Depends(get_cache_service),
) -> CachedProductWriter:
    return CachedProductWriter(writer, cache)
