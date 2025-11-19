import json
from typing import List, Optional, Dict, Any
from payment_service.src.services.reader_service import PaymentReader
from payment_service.src.schemas import PaymentResponse
from payment_service.src.services.cache_service import PaymentCache


class CachedPaymentReader:

    def __init__(self, reader: PaymentReader, cache: PaymentCache):
        self.reader = reader
        self.cache = cache

    async def get_cached_payment_by_id(self, payment_id: int) -> Optional[PaymentResponse]:
        cache_key = f"payment:{payment_id}"
        cached = await self.cache.get(cache_key)

        if cached:
            return PaymentResponse(**cached)

        payment = await self.reader.get_payment_by_id(payment_id)
        if payment:
            await self.cache.set(cache_key, payment.dict(), expire=120)

        return payment

    async def get_cached_list_payments(self, limit: int = 100, offset: int = 0) -> List[PaymentResponse]:
        cache_key = f"payments:list:{limit}:{offset}"
        cached = await self.cache.get(cache_key)

        if cached:
            return [PaymentResponse(**item) for item in cached]

        payments = await self.reader.get_list_payments(limit, offset)
        await self.cache.set(cache_key, [p.dict() for p in payments], expire=60)

        return payments

    async def get_cached_filter_payment(
        self,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[PaymentResponse]:

        filters_key = json.dumps(filters or {}, sort_keys=True)
        cache_key = f"payments:filter:{filters_key}:{limit}:{offset}"

        cached = await self.cache.get(cache_key)
        if cached:
            return [PaymentResponse(**item) for item in cached]

        payments = await self.reader.get_filter_payment(filters, limit, offset)

        await self.cache.set(cache_key, [p.dict() for p in payments], expire=60)

        return payments
