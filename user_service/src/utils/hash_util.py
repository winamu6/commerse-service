from passlib.context import CryptContext

#контекст для bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    #хэш пароля
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    #проверка пароля на хэш
    return pwd_context.verify(plain_password, hashed_password)
