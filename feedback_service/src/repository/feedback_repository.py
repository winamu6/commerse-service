from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from typing import List

from feedback_service.src.models.feedback import Feedback


class ProductRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_feedback(self, feedback: Feedback) -> Feedback:
        self.session.add(feedback)
        await self.session.commit()
        await self.session.refresh(feedback)
        return feedback

    async def get_feedback_for_product(self, product_id: int) -> List[Feedback]:
        stmt = select(Feedback).where(Feedback.product_id == product_id)
        result = await self.session.scalars(stmt)
        return result.first()

    async def get_avg_for_product(self, product_id: int) -> float:
        stmt = select(func.avg(Feedback.score)).where(Feedback.product_id == product_id)
        result = await self.session.execute(stmt)
        return result.scalar() or 0.0