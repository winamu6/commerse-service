from fastapi import APIRouter, Depends, HTTPException
from typing import List

from feedback_service.src.api.depends import get_cached_feedback_reader
from feedback_service.src.schemas.feedback_schem import FeedbackRead
from feedback_service.src.services.cached.cached_reader_service import CachedFeedbackReader

router = APIRouter(prefix="/feedback_read", tags=["FeedbackRead"])

# отзывы для конкретного продукта
@router.get("/{product_id}/list", response_model=List[FeedbackRead])
async def get_feedback_for_product(
    product_id: int,
    limit: int = 100,
    offset: int = 0,
    service: CachedFeedbackReader = Depends(get_cached_feedback_reader),
):
    feedbacks = await service.get_cached_feedback_for_product(product_id, limit, offset)
    if not feedbacks:
        raise HTTPException(status_code=404, detail="Feedbacks not found")
    return feedbacks


# средняя оценка отзывов
@router.get("/{product_id}/avg", response_model=float)
async def get_avg_for_product(
    product_id: int,
    service: CachedFeedbackReader = Depends(get_cached_feedback_reader),
):
    avg = await service.get_cached_avg_product(product_id)
    if avg is None:
        raise HTTPException(status_code=404, detail="No feedback found for product")
    return avg


# количество отзывов
@router.get("/{product_id}/count", response_model=int)
async def get_count_for_product(
    product_id: int,
    service: CachedFeedbackReader = Depends(get_cached_feedback_reader),
):
    count = await service.get_cached_count_for_product(product_id)
    if count is None:
        raise HTTPException(status_code=404, detail="No feedback found for product")
    return count
