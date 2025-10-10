from typing import List

from feedback_service.src.repository import ReadRepository
from feedback_service.src.schemas import FeedbackRead


class FeedbackReader:
    def __init__(self, repository: ReadRepository):
        self.repo = repository

    async def get_feedback_for_product(
        self,
        product_id: int,
        sort_by: str = "date",
        descending: bool = True,
        limit: int = 20,
        offset: int = 0
    ) -> List[FeedbackRead]:
        feedbacks = await self.repo.list_products(
            product_id=product_id,
            sort_by=sort_by,
            descending=descending,
            limit=limit,
            offset=offset
        )
        return [FeedbackRead.from_orm(fb) for fb in feedbacks]

    async def get_avg_product(self, product_id: int) -> float:
        return await self.repo.get_avg_for_product(product_id)

    async def get_count_for_product(self, product_id: int) -> int:
        return await self.repo.get_count_for_product(product_id)