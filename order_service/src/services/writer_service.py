from typing import Optional, List, Tuple

from src.models import Order, OrderItem
from src.repository import WriterRepository
from src.schemas import OrderCreate, OrderRead
from src.schemas.order_schem import OrderItemBase, OrderStatus


class OrderWriter:
    def __init__(self, repository: WriterRepository):
        self.repo = repository

    async def create_order(
            self,
            order_data: OrderCreate,
            order_items_data: List[OrderItemBase],
    ) -> Tuple[OrderRead, List[OrderItem]]:
        order = Order(user_id=order_data.user_id)
        order_items = [
            OrderItem(
                product_id=item.product_id,
                quantity=item.quantity,
                price=item.price,
            )
            for item in order_items_data
        ]

        order, order_items = await self.repo.create_order(order, order_items)

        order_read = OrderRead.model_validate(order, from_attributes=True)  # ✅

        return order_read, order_items

    async def update_order(
        self, order_id: int, new_status: OrderStatus
    ) -> Optional[OrderRead]:
        order = await self.repo.update_order_status(order_id, new_status)
        return OrderRead.model_validate(order, from_attributes=True) if order else None

    async def delete_order(self, order_id: int) -> bool:
        return await self.repo.delete_order(order_id)
