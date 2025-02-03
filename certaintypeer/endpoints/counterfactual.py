from fastapi import APIRouter, HTTPException
from certaintypeer.constants.certaintypeer import rag
from certaintypeer.models.counterfactual import Review

router = APIRouter()

@router.post("/find_similar")
async def nlp(request: Review):
    try:
        request = "Analyze the similar reviews and their confidence and rating score and give counterfactual reasoning for given review " + request.review + "with confidence score " + request.confidence + "and rating score " + request.rating
        retriever_result = rag.search(query_text=request, return_context=True, retriever_config={"top_k": 5})
        return {"result": retriever_result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))