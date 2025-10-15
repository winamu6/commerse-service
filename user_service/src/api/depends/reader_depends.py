from fastapi import Depends
from user_service.src.db.database import async_session_maker
from user_service.src.db.cache import redis_client
from user_service.src.repository.reader_repository import UserReaderRepository
from user_service.src.services.reader_service import UserReader
from user_service.src.services.cache_service import UserCache
from user_service.src.services.cache.cached_reader_service import CachedUserReader


async def get_user_read_repository() -> UserReaderRepository:
    async with async_session_maker() as session:
        yield UserReaderRepository(session)


async def get_cache_service() -> UserCache:
    yield UserCache(redis_client)


async def get_user_reader(
    repo: UserReaderRepository = Depends(get_user_read_repository),
) -> UserReader:
    return UserReader(repo)


async def get_cached_user_reader(
    reader: UserReader = Depends(get_user_reader),
    cache: UserCache = Depends(get_cache_service),
) -> CachedUserReader:
    return CachedUserReader(reader, cache)