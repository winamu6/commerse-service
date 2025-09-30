from typing import Optional

from inventory_service.src.models import Product
from inventory_service.src.repository import ProductRepository
from inventory_service.src.schemas import ProductCreate, ProductRead, ProductUpdate


class ProductWriter:

    def __init__(self, repository: ProductRepository):
        self.repo = repository

    async def create_product(self, data: ProductCreate) -> ProductRead:
        product = Product(**data.dict())
        product = await self.repo.create(product)
        return ProductRead.from_orm(product)

    async def update_product(self, product_id: int, data: ProductUpdate) -> Optional[ProductRead]:
        update_data = data.dict(exclude_unset=True)
        product = await self.repo.update_product(product_id, update_data)
        return ProductRead.from_orm(product) if product else None

    async def delete_product(self, product_id: int) -> bool:
        return await self.repo.delete_product(product_id)