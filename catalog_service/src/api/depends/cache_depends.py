from src.services.cache_service import ProductCache
from src.db.cache import redis_client


def get_cache_service() -> ProductCache:
    return ProductCache(redis_client)