from src.services.cache_service import CartCache
from src.models.cart import Cart

class CartWriteRepository:

    _CART_TTL_SECONDS = 60 * 60 * 24 * 7

    def __init__(self, cache_service: CartCache) -> None:
        self._cache = cache_service

    async def save_cart(self, cart: Cart) -> None:
        cache_key = self._build_key(cart.user_id)
        await self._cache.set(cache_key, cart.model_dump(), expire=self._CART_TTL_SECONDS)

    async def delete_cart(self, user_id: int) -> None:
        cache_key = self._build_key(user_id)
        await self._cache.delete(cache_key)

    @staticmethod
    def _build_key(user_id: int) -> str:
        return f"cart:{user_id}"