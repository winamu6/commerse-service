from fastapi import Depends

from feedback_service.src.repository import WriterRepository
from feedback_service.src.services.cache_service import FeedbackCache
from feedback_service.src.db.database import async_session_maker
from feedback_service.src.db.cache import redis_client
from feedback_service.src.services.cached import CachedFeedbackWriter
from feedback_service.src.services.writer_service import FeedbackWriter


async def get_feedback_write_repository() -> WriterRepository:
    async with async_session_maker() as session:
        yield WriterRepository(session)


async def get_cache_service() -> FeedbackCache:
    yield FeedbackCache(redis_client)


async def get_feedback_writer(
    repo: WriterRepository = Depends(get_feedback_write_repository),
) -> FeedbackWriter:
    return FeedbackWriter(repo)


async def get_cached_feedback_writer(
    writer: FeedbackWriter = Depends(get_feedback_writer),
    cache: FeedbackCache = Depends(get_cache_service),
) -> CachedFeedbackWriter:
    return CachedFeedbackWriter(writer, cache)