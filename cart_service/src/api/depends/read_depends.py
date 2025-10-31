from fastapi import Depends
from src.db.cache import redis_client
from src.services.cache_service import CartCache
from src.repository import CartReadRepository
from src.services.read_service import CartReadService


async def get_cache_service() -> CartCache:
    yield CartCache(redis_client)


async def get_cart_read_repository(
    cache_service: CartCache = Depends(get_cache_service),
) -> CartReadRepository:
    yield CartReadRepository(cache_service)


async def get_cart_read_service(
    repository: CartReadRepository = Depends(get_cart_read_repository),
) -> CartReadService:
    yield CartReadService(repository)
