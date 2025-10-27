from fastapi import Depends
from cart_service.src.db.cache import redis_client
from cart_service.src.services.cache_service import CartCache
from cart_service.src.repository import CartReadRepository
from cart_service.src.services.read_service import CartReadService


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
