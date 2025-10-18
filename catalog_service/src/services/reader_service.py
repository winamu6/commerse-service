from typing import List

from src.repository import ReadRepository
from src.schemas import ProductRead

class ProductReader:
    def __init__(self, repository: ReadRepository):
        self.repo = repository

    async def get_product_by_id(self, product_id: int) -> ProductRead | None:
        product = await self.repo.get_product_by_id(product_id)
        return ProductRead.from_orm(product) if product else None

    async def get_list_products(self, limit: int = 100, offset: int = 0) -> List[ProductRead]:
        products = await self.repo.list_products(limit, offset)
        return [ProductRead.from_orm(p) for p in products]

    async def get_products_by_name(self, product_name: str, limit: int = 100, offset: int = 0) -> List[ProductRead]:
        products = await self.repo.search_products_by_name(product_name, limit, offset)
        return [ProductRead.from_orm(p) for p in products]

    async def filter_products_by_category(self, category: str, limit: int = 100, offset: int = 0) -> List[ProductRead]:
        products = await self.repo.filter_products_by_category(category, limit, offset)
        return [ProductRead.from_orm(p) for p in products]

    async def sort_products_by_rating(self) -> List[ProductRead]:
        products = await self.repo.sort_products_by_rating()
        return [ProductRead.from_orm(p) for p in products]

    async def get_products_by_seller(self, seller_id: int, limit: int = 100, offset: int = 0) -> List[ProductRead]:
        products = await self.repo.get_products_by_seller(seller_id, limit, offset)
        return [ProductRead.from_orm(p) for p in products]