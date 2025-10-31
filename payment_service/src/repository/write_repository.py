from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional, Tuple, List

from payment_service.src.models import Payment, PaymentStatus


class WriterRepository:
    def __init__(self, session: AsyncSession):
        self.session = session