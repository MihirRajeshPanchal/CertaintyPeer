import shutil
import os
from certaintypeer.utils.hybrid_search import create_embeddings
from fastapi import APIRouter, File, Form, UploadFile
from typing import Dict


router = APIRouter()

@router.post("/hybrid_search")
async def generate_schema(file: UploadFile = File(...), query: str = Form(...)) -> Dict:
    try:
        temp_file_path = f"certaintypeer/temp_{file.filename}"
        with open(temp_file_path, "wb") as temp_file:
            shutil.copyfileobj(file.file, temp_file)
        
        docs_with_score = create_embeddings(temp_file_path, query)
        if docs_with_score:
            os.remove(temp_file_path)
            return {"response": docs_with_score}
        else:
            return {"error": "Error in generating schema"}
    except Exception as e:
        return {"error": str(e)}