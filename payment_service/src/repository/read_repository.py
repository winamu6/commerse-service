from sqlalchemy import select, and_, not_, case
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional

from payment_service.src.models import Payment, PaymentStatus


class ReadRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

