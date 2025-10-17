from typing import Optional

from fastapi import Depends, HTTPException, Cookie, Header
from user_service.src.db.database import async_session_maker
from user_service.src.db.cache import redis_client
from user_service.src.repository.reader_repository import UserReaderRepository
from user_service.src.schemas import UserRead
from user_service.src.services.auth_service import AuthService
from user_service.src.services.cache_service import UserCache
from user_service.src.services.cached.cached_auth_service import CachedAuthService
from user_service.src.utils import decode_token


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

async def get_current_user_from_cookie(
    access_token: Optional[str] = Cookie(None),
    authorization: Optional[str] = Header(None),
    service: CachedAuthService = Depends(get_cached_auth_service),
) -> UserRead:
    token_str = None
    if access_token:
        token_str = access_token
    elif authorization and authorization.startswith("Bearer "):
        token_str = authorization.split(" ")[1]

    if not token_str:
        raise HTTPException(status_code=401, detail="Authorization token missing")

    payload = decode_token(token_str)
    if not payload or "sub" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_id = int(payload["sub"])
    user = await service.reader.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user