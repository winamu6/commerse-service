from sqlalchemy import select, func, desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from feedback_service.src.models.feedback import Feedback


class FeedbackRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_feedback(self, feedback: Feedback) -> Feedback:
        self.session.add(feedback)
        await self.session.commit()
        await self.session.refresh(feedback)
        return feedback

    async def get_feedback_for_product(
        self,
        product_id: int,
        sort_by: str = "date",
        descending: bool = True,
        limit: int = 20,
        offset: int = 0
    ) -> List[Feedback]:

        stmt = select(Feedback).where(Feedback.product_id == product_id)

        if sort_by == "date":
            stmt = stmt.order_by(desc(Feedback.created_at) if descending else asc(Feedback.created_at))
        elif sort_by == "score":
            stmt = stmt.order_by(desc(Feedback.score) if descending else asc(Feedback.score))
        else:
            raise ValueError("sort_by должен быть 'date' или 'score'")

        stmt = stmt.offset(offset).limit(limit)
        result = await self.session.scalars(stmt)
        return result.all()

    async def get_avg_for_product(self, product_id: int) -> float:
        stmt = select(func.avg(Feedback.score)).where(Feedback.product_id == product_id)
        result = await self.session.execute(stmt)
        return result.scalar() or 0.0
