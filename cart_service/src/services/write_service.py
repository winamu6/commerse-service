from src.repository.read_repository import CartReadRepository
from src.repository import CartWriteRepository
from src.schemas import (
    CartItemRequest,
    CartItemResponse,
    CartResponse,
)
from src.models.cart import Cart, CartItem


class CartWriteService:

    def __init__(
        self,
        read_repo: CartReadRepository,
        write_repo: CartWriteRepository,
    ):
        self.read_repo = read_repo
        self.write_repo = write_repo

    async def add_item(self, user_id: int, item_data: CartItemRequest) -> CartResponse:
        cart = await self.read_repo.get_cart(user_id)
        new_item = CartItem(**item_data.model_dump())

        for existing in cart.items:
            if existing.product_id == new_item.product_id:
                existing.quantity += new_item.quantity
                break
        else:
            cart.items.append(new_item)

        cart.total_price = sum(i.price * i.quantity for i in cart.items)
        await self.write_repo.save_cart(cart)
        return await self._to_response(cart)

    async def update_quantity(
        self, user_id: int, product_id: int, quantity: int
    ) -> CartResponse:
        cart = await self.read_repo.get_cart(user_id)

        for item in cart.items:
            if item.product_id == product_id:
                item.quantity = quantity
                break
        else:
            return await self._to_response(cart)  # товар не найден — вернуть без изменений

        cart.total_price = sum(i.price * i.quantity for i in cart.items)
        await self.write_repo.save_cart(cart)
        return await self._to_response(cart)

    async def remove_item(self, user_id: int, product_id: int) -> CartResponse:
        cart = await self.read_repo.get_cart(user_id)
        cart.items = [i for i in cart.items if i.product_id != product_id]
        cart.total_price = sum(i.price * i.quantity for i in cart.items)

        await self.write_repo.save_cart(cart)
        return await self._to_response(cart)

    async def clear_cart(self, user_id: int):
        await self.write_repo.delete_cart(user_id)

    async def _to_response(self, cart: Cart) -> CartResponse:
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
        return CartResponse(
            user_id=cart.user_id,
            items=items,
            total_price=sum(i.price * i.quantity for i in cart.items),
        )