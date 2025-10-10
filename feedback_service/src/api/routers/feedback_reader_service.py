from fastapi import APIRouter, Depends, HTTPException

from feedback_service.src.api.depends import get_cached_feedback_reader
from feedback_service.src.schemas.feedback_schem import FeedbackRead
from feedback_service.src.services.cached.cached_reader_service import CachedFeedbackReader

router = APIRouter(prefix="/feedback_read", tags=["FeedbackRead"])

@router.get("/{product_id}", response_model=FeedbackRead)
async def get_feedback_for_product(
    product_id: int,
    service: CachedFeedbackReader = Depends(get_cached_feedback_reader),
):
    product = await service.get_cached_feedback_for_product(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product