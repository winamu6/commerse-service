from feedback_service.src.services.writer_service import FeedbackWriter
from feedback_service.src.services.cache_service import FeedbackCache
from feedback_service.src.schemas import FeedbackCreate, FeedbackRead


class CachedFeedbackWriter:

    def __init__(self, writer: FeedbackWriter, cache: FeedbackCache):
        self.writer = writer
        self.cache = cache

    async def create_feedback(self, data: FeedbackCreate) -> FeedbackRead:
        feedback = await self.writer.create_feedback(data)
        await self.cache.delete_pattern(f"feedback:list:{feedback.product_id}:*")
        await self.cache.delete(f"avg_score:{feedback.product_id}")
        await self.cache.delete(f"feedback_count:{feedback.product_id}")
        return feedback
