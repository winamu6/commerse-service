from fastapi import APIRouter, Depends

from feedback_service.src.api.depends import get_cached_feedback_writer
from feedback_service.src.schemas import FeedbackCreate
from feedback_service.src.schemas.feedback_schem import FeedbackRead
from feedback_service.src.services.cached import CachedFeedbackWriter

router = APIRouter(prefix="/feedback_write", tags=["FeedbackWrite"])

#создание отзыва
@router.post("/", response_model=FeedbackRead)
async def create_product(
    data: FeedbackCreate,
    service: CachedFeedbackWriter = Depends(get_cached_feedback_writer),
):
    feedback = await service.cached_create_feedbacks(data)
    return feedback