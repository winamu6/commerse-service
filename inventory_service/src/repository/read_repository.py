from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional

from inventory_service.src.models import Product

class ReadRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_product_by_id(self, product_id: int) -> Optional[Product]:
        stmt = select(Product).where(Product.id == product_id).options(selectinload(Product.feedbacks))
        result = await self.session.scalars(stmt)
        return result.first()

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

    async def get_products_by_seller(self, seller_id: int, limit: int, offset: int) -> List[Product]:
        stmt = select(Product).where(Product.seller_id == seller_id).limit(limit).offset(offset)
        result = await self.session.scalars(stmt)
        return result.all()
