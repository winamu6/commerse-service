import datetime
from user_service.src.services.auth_service import AuthService
from user_service.src.services.cache_service import UserCache
from user_service.src.utils.jwt_util import decode_token


class CachedAuthService:

    def __init__(self, auth_service: AuthService, cache: UserCache):
        self.auth = auth_service
        self.cache = cache

    async def logout(self, refresh_token: str):
        payload = decode_token(refresh_token)
        if payload:
            exp = payload.get("exp")
            if not exp:
                return
            ttl = int(exp - datetime.datetime.utcnow().timestamp())
            await self.cache.setex(f"blacklist:{refresh_token}", ttl, "1")

    async def refresh_tokens(self, refresh_token: str):
        if await self.cache.get(f"blacklist:{refresh_token}"):
            return None
        return await self.auth.refresh_tokens(refresh_token)
