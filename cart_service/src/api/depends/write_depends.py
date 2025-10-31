from fastapi import Depends
from cart_service.src.db.cache import redis_client
from cart_service.src.services.cache_service import CartCache
from cart_service.src.repository import CartWriteRepository, CartReadRepository
from cart_service.src.services.write_service import CartWriteService
from cart_service.src.api.depends.read_depends import get_cart_read_repository


async def get_cache_service() -> CartCache:
    yield CartCache(redis_client)


async def get_cart_write_repository(
    cache_service: CartCache = Depends(get_cache_service),
) -> CartWriteRepository:
    yield CartWriteRepository(cache_service)


async def get_cart_write_service(
    read_repo: CartReadRepository = Depends(get_cart_read_repository),
    write_repo: CartWriteRepository = Depends(get_cart_write_repository),
) -> CartWriteService:
    yield CartWriteService(read_repo, write_repo)
