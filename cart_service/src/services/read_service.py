from cart_service.src.repository.read_repository import CartReadRepository
from cart_service.src.schemas import CartResponse, CartItemResponse


class CartReadService:

    def __init__(self, repository: CartReadRepository):
        self.repository = repository

    async def get_cart(self, user_id: int) -> CartResponse:
        cart = await self.repository.get_cart(user_id)

        items = [
            CartItemResponse(
                product_id=i.product_id,
                name=i.name,
                price=i.price,
                quantity=i.quantity,
                item_total=i.price * i.quantity,
            )
            for i in cart.items
        ]
        total_price = sum(item.item_total for item in items)

        return CartResponse(
            user_id=cart.user_id,
            items=items,
            total_price=total_price,
        )