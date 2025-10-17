from fastapi import Depends
from user_service.src.db.database import async_session_maker
from user_service.src.db.cache import redis_client
from user_service.src.repository.reader_repository import UserReaderRepository
from user_service.src.services.auth_service import AuthService
from user_service.src.services.cache_service import UserCache
from user_service.src.services.cached.cached_auth_service import CachedAuthService


async def get_user_read_repository() -> UserReaderRepository:
    async with async_session_maker() as session:
        yield UserReaderRepository(session)


async def get_cache_service() -> UserCache:
    yield UserCache(redis_client)


async def get_auth_service(
    reader_repo: UserReaderRepository = Depends(get_user_read_repository),
) -> AuthService:
    return AuthService(reader=reader_repo)


async def get_cached_auth_service(
    reader_repo: UserReaderRepository = Depends(get_user_read_repository),
    cache: UserCache = Depends(get_cache_service),
) -> CachedAuthService:
    return CachedAuthService(reader=reader_repo, cache=cache)
