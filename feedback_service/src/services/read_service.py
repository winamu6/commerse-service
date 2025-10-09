from feedback_service.src.repository import ReadRepository
from feedback_service.src.schemas import FeedbackRead

class ProductReader:
    def __init__(self, repository: ReadRepository):
        self.repo = repository

    async def get_feedback_for_product(self, product_id: int, sort_by: str, descending: bool, limit: int, offset: int) -> ProductRead | None:
        feedback = await self.repo.get_product_by_id(product_id, sort_by, descending, limit, offset)
        return FeedbackRead.from_orm(feedback) if feedback else None

    async def get_avg_product(self, product_id: int) -> float:
        avg = await self.repo.get_avg_for_product(product_id)
        return avg