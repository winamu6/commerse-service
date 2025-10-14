from datetime import timedelta
from typing import Optional
from user_service.src.repository import UserReaderRepository
from user_service.src.utils.hash_util import verify_password
from user_service.src.utils.jwt_util import create_access_token, create_refresh_token, decode_token
from user_service.src.db import settings
from user_service.src.schemas import Token, TokenData


class AuthService:
    def __init__(self, reader: UserReaderRepository):
        self.reader = reader

    async def authenticate_user(self, email: str, password: str) -> Optional[Token]:
        user = await self.reader.get_user_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return None

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )
        refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return Token(access_token=access_token, refresh_token=refresh_token, token_type="bearer")

    async def refresh_tokens(self, refresh_token: str) -> Optional[Token]:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            return None

        user_id = payload.get("sub")
        user = await self.reader.get_user_by_id(user_id)
        if not user:
            return None

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        new_access_token = create_access_token(
            data={"sub": str(user.id), "email": user.email},
            expires_delta=access_token_expires
        )
        new_refresh_token = create_refresh_token(data={"sub": str(user.id)})

        return Token(access_token=new_access_token, refresh_token=new_refresh_token, token_type="bearer")
