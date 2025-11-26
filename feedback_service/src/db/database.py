import asyncio
import asyncpg
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from src.db import settings

DATABASE_URL = settings.DATABASE_URL_asyncpg

engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    echo=False
)

Base = declarative_base()

async_session_maker = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def wait_for_db():
    max_attempts = 60
    for i in range(max_attempts):
        try:
            conn = await asyncpg.connect(
                user=settings.DB_USER,
                password=settings.DB_PASS,
                database=settings.DB_NAME,
                host=settings.DB_HOST,
                port=settings.DB_PORT,
            )
            await conn.close()
            print("Database is ready")
            return
        except Exception as e:
            print(f"Waiting for database ({i+1}/{max_attempts})... {e}")
            await asyncio.sleep(1)
    raise RuntimeError("Database not ready after 60 seconds")