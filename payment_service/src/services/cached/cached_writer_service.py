from typing import Optional, Dict, Any
from payment_service.src.schemas import PaymentCreate, PaymentResponse
from payment_service.src.services.cache_service import PaymentCache
from payment_service.src.services.writer_service import PaymentWriter


class CachedPaymentWriter:

    def __init__(self, writer: PaymentWriter, cache: PaymentCache):
        self.writer = writer
        self.cache = cache

    async def _invalidate_payment_cache(self, payment_id: int):
        await self.cache.delete(f"payment:{payment_id}")

    async def _invalidate_lists_cache(self):
        await self.cache.delete_pattern("payments:list:*")
        await self.cache.delete_pattern("payments:filter:*")

    async def create_payment(self, payment: PaymentCreate) -> PaymentResponse:
        payment_response = await self.writer.create_payment(payment)

        await self._invalidate_lists_cache()

        await self._invalidate_payment_cache(payment_response.id)

        return payment_response

    async def update_payment(self, payment_id: int, update_data: Dict[str, Any]) -> Optional[PaymentResponse]:
        updated_payment = await self.writer.update_payment(payment_id, update_data)

        if updated_payment is None:
            return None

        await self._invalidate_payment_cache(payment_id)

        await self._invalidate_lists_cache()

        return updated_payment
