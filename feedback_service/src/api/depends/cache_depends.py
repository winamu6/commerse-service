from src.services.cache_service import FeedbackCache
from src.db.cache import redis_client


def get_cache_service() -> FeedbackCache:
    return FeedbackCache(redis_client)