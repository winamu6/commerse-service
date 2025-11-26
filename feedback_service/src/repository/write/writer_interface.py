from asyncio import Protocol

from src.models.feedback import Feedback


class IWriterRepository(Protocol):

    async def add_feedback(self, feedback: Feedback) -> Feedback:
        ...