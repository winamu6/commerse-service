from typing import List, Optional, Dict, Any

from payment_service.src.models import Payment
from payment_service.src.repository import IWriteRepository
from payment_service.src.schemas import PaymentCreate, PaymentResponse


class PaymentWriter:
    def __init__(self, repository: IWriteRepository):
        self.repo = repository

    async def create_payment(self, payment: PaymentCreate) -> PaymentResponse:
        payment_model = Payment(
            order_id=payment.order_id,
            amount=payment.amount,
            currency=payment.currency,
            provider=payment.provider,
            user_id=payment.user_id
        )
        payment_db = await self.repo.create_payment(payment_model)
        return PaymentResponse.from_orm(payment_db)

    async def update_payment(self, payment_id: int, update_data: dict) -> PaymentResponse | None:
        payment_db = await self.repo.update_payment(payment_id, update_data)
        if payment_db is None:
            return None
        return PaymentResponse.from_orm(payment_db)
