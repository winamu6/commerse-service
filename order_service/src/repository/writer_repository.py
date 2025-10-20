from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from order_service.src.models import Order, OrderItem

class WriterRepository:
    def __init__(self, session: AsyncSession):
        self.session = session