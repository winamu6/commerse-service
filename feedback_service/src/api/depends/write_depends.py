from fastapi import Depends

from src.repository import WriterRepository
from src.services.cache_service import FeedbackCache
from src.db.database import async_session_maker
from src.db.cache import redis_client
from src.services.cached import CachedFeedbackWriter
from src.services.writer_service import FeedbackWriter


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