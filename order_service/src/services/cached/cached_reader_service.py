from typing import List, Optional
from order_service.src.services.reader_service import OrderReader
from order_service.src.schemas import OrderRead
from order_service.src.services.cache_service import OrderCache


class CachedOrderReader:

    def __init__(self, reader: OrderReader, cache: OrderCache):
        self.reader = reader
        self.cache = cache

