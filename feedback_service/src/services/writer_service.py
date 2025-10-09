from feedback_service.src.models import Feedback
from feedback_service.src.repository import WriterRepository
from feedback_service.src.schemas import FeedbackCreate, FeedbackRead

class ProductWriter:

    def __init__(self, repository: WriterRepository):
        self.repo = repository

    async def create_feedback(self, data: FeedbackCreate) -> FeedbackRead:
        product = Feedback(**data.dict())
        product = await self.repo.create(product)
        return FeedbackRead.from_orm(product)