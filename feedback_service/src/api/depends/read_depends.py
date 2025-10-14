from fastapi import Depends
from feedback_service.src.services.cached.cached_reader_service import CachedFeedbackReader
from feedback_service.src.services.reader_service import FeedbackReader
from feedback_service.src.services.cache_service import FeedbackCache
from feedback_service.src.repository.read_repository import ReadRepository
from feedback_service.src.db.database import async_session_maker
from feedback_service.src.db.cache import redis_client

async def get_feedback_read_repository() -> ReadRepository:
    async with async_session_maker() as session:
        yield ReadRepository(session)


async def get_cache_service() -> FeedbackCache:
    yield FeedbackCache(redis_client)


async def get_feedback_reader(
    repo: ReadRepository = Depends(get_feedback_read_repository),
) -> FeedbackReader:
    return FeedbackReader(repo)


async def get_cached_feedback_reader(
    reader: FeedbackReader = Depends(get_feedback_reader),
    cache: FeedbackCache = Depends(get_cache_service),
) -> CachedFeedbackReader:
    return CachedFeedbackReader(reader, cache)