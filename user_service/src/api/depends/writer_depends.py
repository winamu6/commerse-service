from fastapi import Depends
from user_service.src.db.database import async_session_maker
from user_service.src.db.cache import redis_client
from user_service.src.repository.writer_repository import UserWriterRepository
from user_service.src.repository.reader_repository import UserReaderRepository
from user_service.src.services.writer_service import UserWriter
from user_service.src.services.cache_service import UserCache
from user_service.src.services.cache.cached_writer_service import CachedUserWriter


async def get_user_read_repository() -> UserReaderRepository:
    async with async_session_maker() as session:
        yield UserReaderRepository(session)


async def get_user_write_repository() -> UserWriterRepository:
    async with async_session_maker() as session:
        yield UserWriterRepository(session)


async def get_cache_service() -> UserCache:
    yield UserCache(redis_client)


async def get_user_writer(
    reader_repo: UserReaderRepository = Depends(get_user_read_repository),
    writer_repo: UserWriterRepository = Depends(get_user_write_repository),
) -> UserWriter:
    return UserWriter(reader_repo, writer_repo)


async def get_cached_user_writer(
    writer: UserWriter = Depends(get_user_writer),
    cache: UserCache = Depends(get_cache_service),
) -> CachedUserWriter:
    return CachedUserWriter(writer, cache)