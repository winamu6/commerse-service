from typing import List
from feedback_service.src.services.reader_service import FeedbackReader
from feedback_service.src.schemas import FeedbackRead
from feedback_service.src.services.cache_service import FeedbackCache


class CachedFeedbackReader:

    def __init__(self, reader: FeedbackReader, cache: FeedbackCache):
        self.reader = reader
        self.cache = cache

    async def get_cached_feedback_for_product(
        self, product_id: int, limit: int = 100, offset: int = 0
    ) -> List[FeedbackRead]:
        cache_key = f"feedback:list:{product_id}:{limit}:{offset}"
        cached = await self.cache.get(cache_key)
        if cached:
            return [FeedbackRead(**f) for f in cached]

        feedbacks = await self.reader.get_feedbacks_for_product(product_id, limit, offset)
        await self.cache.set(cache_key, [f.model_dump() for f in feedbacks], expire=60)
        return feedbacks

    async def get_cached_avg_product(self, product_id: int) -> float:
        cache_key = f"avg_score:{product_id}"
        cached = await self.cache.get(cache_key)
        if cached is not None:
            return float(cached)

        avg = await self.reader.get_avg_rating_for_product(product_id)
        if avg is not None:
            await self.cache.set(cache_key, avg, expire=120)
        return avg

    async def get_cached_count_for_product(self, product_id: int) -> int:
        cache_key = f"feedback_count:{product_id}"
        cached = await self.cache.get(cache_key)
        if cached is not None:
            return int(cached)

        count = await self.reader.get_feedback_count_for_product(product_id)
        if count is not None:
            await self.cache.set(cache_key, count, expire=120)
        return count
