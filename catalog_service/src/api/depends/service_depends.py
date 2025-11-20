from fastapi import Depends

from src.api.depends.repository_depends import get_write_repo, get_read_repo
from src.api.depends.cache_depends import get_cache_service

from src.services.writer_service import ProductWriter
from src.services.reader_service import ProductReader
from src.services.cached.cached_writer_service import CachedProductWriter
from src.services.cached.cached_reader_service import CachedProductReader


def get_product_writer(
    repo = Depends(get_write_repo),
) -> ProductWriter:
    return ProductWriter(repo)


def get_product_reader(
    repo = Depends(get_read_repo),
) -> ProductReader:
    return ProductReader(repo)


def get_cached_product_writer(
    writer = Depends(get_product_writer),
    cache = Depends(get_cache_service),
) -> CachedProductWriter:
    return CachedProductWriter(writer, cache)


def get_cached_product_reader(
    reader = Depends(get_product_reader),
    cache = Depends(get_cache_service),
) -> CachedProductReader:
    return CachedProductReader(reader, cache)
