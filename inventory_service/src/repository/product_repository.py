from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional

from inventory_service.src.models import Product


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, product: Product) -> Product:
        self.session.add(product)
        await self.session.commit()
        await self.session.refresh(product)
        return product

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        stmt = select(Product).where(Product.id == product_id).options(selectinload(Product.feedbacks))
        result = await self.session.scalars(stmt)
        return result.first()

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

    async def list_products(self, limit: int, offset: int) -> List[Product]:
        stmt = select(Product).limit(limit).offset(offset)
        result = await self.session.scalars(stmt)
        return result.all()

    async def search_products_by_name(self, product_name: str, limit: int, offset: int) -> List[Product]:
        stmt = select(Product).where(Product.name.ilike(f"%{product_name}%")).limit(limit).offset(offset)
        result = await self.session.scalars(stmt)
        return result.all()

    async def filter_products_by_category(self, category: str, limit: int, offset: int) -> List[Product]:
        stmt = select(Product).where(Product.category == category).limit(limit).offset(offset)
        result = await self.session.scalars(stmt)
        return result.all()

    async def sort_products_by_rating(self, desc: bool = True, limit: int = 10, offset: int = 0) -> List[Product]:
        order = Product.rating.desc() if desc else Product.rating.asc()
        stmt = select(Product).order_by(order).limit(limit).offset(offset)
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_products_by_seller(self, seller_id: int, limit: int = 10, offset: int = 0) -> List[Product]:
        stmt = select(Product).where(Product.seller_id == seller_id).limit(limit).offset(offset)
        result = await self.session.scalars(stmt)
        return result.all()
