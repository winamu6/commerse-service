from asyncio import Protocol
from typing import List

from src.models.feedback import Feedback


class IReadRepository(Protocol):


    async def get_feedback_for_product(
        self,
        product_id: int,
        sort_by: str = "date",
        descending: bool = True,
        limit: int = 20,
        offset: int = 0
    ) -> List[Feedback]:
        ...


    async def get_avg_for_product(self, product_id: int) -> float:
        ...


    async def get_count_for_product(self, product_id: int) -> int:
        ...