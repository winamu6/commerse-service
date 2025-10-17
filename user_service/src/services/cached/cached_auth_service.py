from typing import Optional

from user_service.src.db import settings
from user_service.src.repository import UserReaderRepository
from user_service.src.schemas import Token
from user_service.src.services.auth_service import AuthService
from user_service.src.services.cache_service import UserCache


class CachedAuthService(AuthService):

    def __init__(self, reader: UserReaderRepository, cache: UserCache):
        super().__init__(reader=reader, revoked_token_repo=cache)
        self.cache = cache

    async def logout(self, refresh_token: str) -> bool:
        await super().revoke_refresh_token(refresh_token)
        return True

    async def refresh_tokens(self, refresh_token: str) -> Optional[Token]:
        return await super().refresh_tokens(refresh_token)

    async def authenticate_user(self, email: str, password: str) -> Optional[Token]:
        cache_key = f"user_token:{email}"

        cached_data = await self.cache.get(cache_key)
        if cached_data:
            try:
                return Token.parse_raw(cached_data)
            except Exception:
                pass

        token = await super().authenticate_user(email, password)
        if token:
            await self.cache.setex(
                cache_key,
                settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
                token.json(),
            )

        return token