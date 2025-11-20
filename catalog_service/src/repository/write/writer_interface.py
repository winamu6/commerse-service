from asyncio import Protocol
from typing import Optional, List

from src.models import Product


class IWriterRepository(Protocol):

    async def create(self, product: Product) -> Product:
        ...

    async def update_product(self, product_id: int, update_data: dict) -> Optional[Product]:
        ...

    async def delete_product(self, product_id: int) -> bool:
        ...