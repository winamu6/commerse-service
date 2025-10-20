from typing import Optional
from order_service.src.services.writer_service import OrderWriter
from order_service.src.schemas import OrderCreate, OrderRead
from order_service.src.services.cache_service import OrderCache

class CachedOrderWriter:

    def __init__(self, writer: OrderWriter, cache: OrderCache):
        self.writer = writer
        self.cache = cache

