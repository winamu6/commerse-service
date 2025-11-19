from fastapi import Depends

from payment_service.src.api.depends.repository_depends import get_write_repo, get_read_repo
from payment_service.src.api.depends.cache_depends import get_cache_service

from payment_service.src.services.writer_service import PaymentWriter
from payment_service.src.services.reader_service import PaymentReader
from payment_service.src.services.cached.cached_writer_service import CachedPaymentWriter
from payment_service.src.services.cached.cached_reader_service import CachedPaymentReader


def get_payment_writer(
    repo = Depends(get_write_repo),
) -> PaymentWriter:
    return PaymentWriter(repo)


def get_payment_reader(
    repo = Depends(get_read_repo),
) -> PaymentReader:
    return PaymentReader(repo)


def get_cached_payment_writer(
    writer = Depends(get_payment_writer),
    cache = Depends(get_cache_service),
) -> CachedPaymentWriter:
    return CachedPaymentWriter(writer, cache)


def get_cached_payment_reader(
    reader = Depends(get_payment_reader),
    cache = Depends(get_cache_service),
) -> CachedPaymentReader:
    return CachedPaymentReader(reader, cache)
