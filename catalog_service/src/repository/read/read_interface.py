from asyncio import Protocol
from typing import Optional, List

from src.models import Product


class IReadRepository(Protocol):

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        ...

    async def list_products(self, limit: int, offset: int) -> List[Product]:
        ...

    async def search_products_by_name(self, product_name: str, limit: int, offset: int) -> List[Product]:
        ...

    async def filter_products_by_category(self, category: str, limit: int, offset: int) -> List[Product]:
        ...

    async def sort_products_by_rating(self, desc: bool = True, limit: int = 10, offset: int = 0) -> List[Product]:
        ...

    async def get_products_by_seller(self, seller_id: int, limit: int, offset: int) -> List[Product]:
        ...