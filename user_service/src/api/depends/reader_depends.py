from fastapi import Depends
from src.db.database import async_session_maker
from src.db.cache import redis_client
from src.repository.reader_repository import UserReaderRepository
from src.services.reader_service import UserReader
from src.services.cache_service import UserCache
from src.services.cached.cached_reader_service import CachedUserReader


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