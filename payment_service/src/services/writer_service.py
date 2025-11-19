from typing import Optional
from payment_service.src.models import Payment
from payment_service.src.repository import IWriteRepository
from payment_service.src.schemas import PaymentCreate, PaymentResponse, PaymentUpdate


class PaymentWriter:
    def __init__(self, repository: IWriteRepository):
        self.repo = repository

    async def create_payment(self, payment: PaymentCreate) -> PaymentResponse:
        payment_model = Payment(**payment.dict(exclude_unset=True))
        payment_db = await self.repo.create_payment(payment_model)
        return PaymentResponse.from_orm(payment_db)

    async def update_payment(self, payment_id: int, update_data: PaymentUpdate) -> Optional[PaymentResponse]:
        data = update_data.dict(exclude_unset=True)
        payment_db = await self.repo.update_payment(payment_id, data)
        if payment_db is None:
            return None
        return PaymentResponse.from_orm(payment_db)

