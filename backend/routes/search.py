from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.utils.rag_engine import generate_answer

router = APIRouter(prefix="/api/search", tags=["search"])

class SearchQuery(BaseModel):
    query: str

@router.post("")
async def search_documents(request: SearchQuery):
    if not request.query or not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    
    try:
        result = generate_answer(request.query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
