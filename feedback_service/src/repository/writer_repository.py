from sqlalchemy.ext.asyncio import AsyncSession

from src.models.feedback import Feedback


class WriterRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_feedback(self, feedback: Feedback) -> Feedback:
        self.session.add(feedback)
        await self.session.commit()
        await self.session.refresh(feedback)
        return feedback
