from src.models import Feedback
from src.repository import IWriterRepository
from src.schemas import FeedbackCreate, FeedbackRead


class FeedbackWriter:
    def __init__(self, repository: IWriterRepository):
        self.repo = repository

    async def create_feedback(self, data: FeedbackCreate) -> FeedbackRead:
        feedback = Feedback(**data.dict())
        feedback = await self.repo.create(feedback)
        return FeedbackRead.from_orm(feedback)
