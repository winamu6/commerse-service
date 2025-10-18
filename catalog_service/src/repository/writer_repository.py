from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from src.models import Product

class WriterRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def update_product(self, product_id: int, update_data: dict) -> Optional[Product]:
        product = await self.session.get(Product, product_id)
        if not product:
            return None

        for key, value in update_data.items():
            setattr(product, key, value)

        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def delete_product(self, product_id: int) -> bool:
        product = await self.session.get(Product, product_id)
        if not product:
            return False
        await self.session.delete(product)
        await self.session.commit()
        return True