from payment_service.src.services.cache_service import PaymentCache
from payment_service.src.db.cache import redis_client


def get_cache_service() -> PaymentCache:
    return PaymentCache(redis_client)