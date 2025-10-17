from datetime import datetime, timedelta
from typing import Optional

from user_service.src.repository import UserReaderRepository
from user_service.src.repository.revoked_token_repository import RevokedTokenRepository
from user_service.src.utils.hash_util import verify_password
from user_service.src.utils.jwt_util import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from user_service.src.db import settings
from user_service.src.schemas import Token


class AuthService:
    def __init__(self,
                 reader: UserReaderRepository,
                 revoked_token_repo: Optional[RevokedTokenRepository] = None):

        self.reader = reader
        self.revoked_token_repo = revoked_token_repo

    async def _generate_tokens(self, user) -> Token:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires,
        )
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
        )

    async def _is_token_revoked(self, token: str) -> bool:
        if not self.revoked_token_repo:
            return False
        return await self.revoked_token_repo.is_revoked(token)

    async def _revoke_token(self, token: str):
        payload = decode_token(token)
        if not payload or payload.get("type") != "refresh":
            return

        exp = payload.get("exp")
        if not exp:
            return

        ttl = int(exp - datetime.utcnow().timestamp())
        if ttl <= 0:
            return

        if self.revoked_token_repo:
            await self.revoked_token_repo.add(token, ttl=ttl)

    async def authenticate_user(self, email: str, password: str) -> Optional[Token]:
        user = await self.reader.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return await self._generate_tokens(user)

    async def refresh_tokens(self, refresh_token: str) -> Optional[Token]:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return None

        if await self._is_token_revoked(refresh_token):
            return None

        user_id = payload.get("sub")
        user = await self.reader.get_user_by_id(user_id)
        if not user:
            return None

        await self._revoke_token(refresh_token)

        return await self._generate_tokens(user)

    async def revoke_refresh_token(self, refresh_token: str) -> bool:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return False

        if await self._is_token_revoked(refresh_token):
            return True

        await self._revoke_token(refresh_token)
        return True
