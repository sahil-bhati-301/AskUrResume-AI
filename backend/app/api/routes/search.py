"""
Search API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.models.schemas import SearchRequest, SearchResult
from app.services.embeddings import generate_embedding
from app.services.vector_store import search_resumes

router = APIRouter()


@router.post("/search", response_model=List[SearchResult])
async def search_resumes_by_job_description(request: SearchRequest):
    """
    Search resumes by job description
    """
    # Check if there are any resumes uploaded
    if request.top_k is None:
        request.top_k = 3
    
    # Generate embedding for job description
    try:
        job_embedding = generate_embedding(request.job_description)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate embedding: {str(e)}"
        )
    
    # Search resumes
    try:
        results = search_resumes(
            query_embedding=job_embedding,
            top_k=request.top_k
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Search failed: {str(e)}"
        )
    
    return results
