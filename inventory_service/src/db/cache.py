from redis.asyncio import Redis

from inventory_service.src.db.settings import Settings
from inventory_service.src.services import ProductCache

redis_client = Redis.from_url(Settings.REDIS_URL, decode_responses=True)
cache_service = ProductCache(redis_client)
