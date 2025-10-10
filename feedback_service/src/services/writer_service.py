from feedback_service.src.models import Feedback
from feedback_service.src.repository import WriterRepository
from feedback_service.src.schemas import FeedbackCreate, FeedbackRead


class FeedbackWriter:
    def __init__(self, repository: WriterRepository):
        self.repo = repository

    async def create_feedback(self, data: FeedbackCreate) -> FeedbackRead:
        feedback = Feedback(**data.dict())
        feedback = await self.repo.create(feedback)
        return FeedbackRead.from_orm(feedback)
