from typing import List, Optional, Dict, Any
from payment_service.src.repository import ReadRepository
from payment_service.src.schemas import PaymentResponse


class PaymentReader:
    def __init__(self, repository: ReadRepository):
        self.repo = repository

    async def get_payment_by_id(self, payment_id: int) -> Optional[PaymentResponse]:
        payment = await self.repo.get_payment_by_id(payment_id)
        return PaymentResponse.from_orm(payment) if payment else None

    async def get_list_payments(self, limit: int = 100, offset: int = 0) -> List[PaymentResponse]:
        payments = await self.repo.list_payments(limit=limit, offset=offset)
        return [PaymentResponse.from_orm(p) for p in payments]

    async def get_filter_payment(
        self,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[PaymentResponse]:
        payments = await self.repo.filter_payments(filters=filters, limit=limit, offset=offset)
        return [PaymentResponse.from_orm(p) for p in payments]