from redis.asyncio import Redis
from feedback_service.src.db.settings import settings
from feedback_service.src.services.cache_service import FeedbackCache

redis_client = Redis.from_url(
    settings.REDIS_URL,
    encoding="UTF-8",
    decode_responses=True,
)

cache_service = FeedbackCache(redis_client)
