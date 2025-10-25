from typing import Optional
from cart_service.src.services.cache_service import CartCache
from cart_service.src.models.cart import Cart

class CartReadRepository:

    def __init__(self, cache_service: CartCache) -> None:
        self._cache = cache_service

    async def get_cart(self, user_id: int) -> Cart:
        cache_key = self._build_key(user_id)
        cached_data: Optional[dict] = await self._cache.get(cache_key)
        if not cached_data:
            return Cart(user_id=user_id, items=[], total_price=0.0)
        return Cart(**cached_data)

    @staticmethod
    def _build_key(user_id: int) -> str:
        return f"cart:{user_id}"