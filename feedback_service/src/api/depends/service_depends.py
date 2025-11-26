from fastapi import Depends

from src.api.depends.repository_depends import get_write_repo, get_read_repo
from src.api.depends.cache_depends import get_cache_service

from src.services.writer_service import FeedbackWriter
from src.services.reader_service import FeedbackReader
from src.services.cached.cached_writer_service import CachedFeedbackWriter
from src.services.cached.cached_reader_service import CachedFeedbackReader


def get_feedback_writer(
    repo = Depends(get_write_repo),
) -> FeedbackWriter:
    return FeedbackWriter(repo)


def get_feedback_reader(
    repo = Depends(get_read_repo),
) -> FeedbackReader:
    return FeedbackReader(repo)


def get_cached_feedback_writer(
    writer = Depends(get_feedback_writer),
    cache = Depends(get_cache_service),
) -> CachedFeedbackWriter:
    return CachedFeedbackWriter(writer, cache)


def get_cached_feedback_reader(
    reader = Depends(get_feedback_reader),
    cache = Depends(get_cache_service),
) -> CachedFeedbackReader:
    return CachedFeedbackReader(reader, cache)
