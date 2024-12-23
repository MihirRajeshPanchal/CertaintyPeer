from fastapi import APIRouter, HTTPException
from certaintypeer.models.graph import MetaReviewRequest
from certaintypeer.utils.graph import add_meta_review_and_reviews

router = APIRouter()


@router.post("/create_graph")
def add_meta_review(request: MetaReviewRequest):
    try:
        result = add_meta_review_and_reviews(request)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

