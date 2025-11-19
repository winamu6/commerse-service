from sqlalchemy.ext.asyncio import AsyncSession
from payment_service.src.models import Payment


class WriterRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_payment(self, payment: Payment) -> Payment:
        self.session.add(payment)
        try:
            await self.session.commit()
            await self.session.refresh(payment)
        except Exception as e:
            await self.session.rollback()
            raise e
        return payment

    async def update_payment(self, payment_id: int, update_data: dict) -> Payment | None:
        payment = await self.session.get(Payment, payment_id)
        if not payment:
            return None

        for key, value in update_data.items():
            if hasattr(payment, key):
                setattr(payment, key, value)

        try:
            await self.session.commit()
            await self.session.refresh(payment)
        except Exception as e:
            await self.session.rollback()
            raise e

        return payment