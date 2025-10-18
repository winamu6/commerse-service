from fastapi import APIRouter, Depends

from src.api.depends import get_cached_feedback_writer
from src.schemas import FeedbackCreate
from src.schemas.feedback_schem import FeedbackRead
from src.services.cached import CachedFeedbackWriter

router = APIRouter(prefix="/feedback_write", tags=["FeedbackWrite"])

#создание отзыва
@router.post("/", response_model=FeedbackRead)
async def create_product(
    data: FeedbackCreate,
    service: CachedFeedbackWriter = Depends(get_cached_feedback_writer),
):
    feedback = await service.cached_create_feedbacks(data)
    return feedback