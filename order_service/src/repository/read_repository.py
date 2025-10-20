from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional

from order_service.src.models import Order, OrderItem

class ReadRepository:
    def __init__(self, session: AsyncSession):
        self.session = session