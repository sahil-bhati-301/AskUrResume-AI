"""
Search API endpoints
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.models.schemas import SearchRequest, SearchResult
from app.services.embeddings import generate_embedding
from app.services.vector_store import search_resumes, get_resume_by_filename
from app.services.ai_evaluator import get_ai_evaluator

router = APIRouter()


@router.post("/search")
async def search_resumes_by_job_description(request: SearchRequest):
    """
    Search resumes by job description with LLM evaluation
    """
    # Set default top_k
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

    # Search resumes using FAISS
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

    # Get full resume texts for LLM evaluation
    resumes_for_evaluation = []
    for result in results:
        resume_data = get_resume_by_filename(result["filename"])
        if resume_data:
            resumes_for_evaluation.append({
                "id": result["id"],
                "filename": result["filename"],
                "text": resume_data["text"],
                "text_preview": result["text_preview"],
                "score": result["score"]
            })

    # Get LLM evaluation
    try:
        ai_evaluator = get_ai_evaluator()
        llm_result = ai_evaluator.evaluate_resumes(
            resumes=resumes_for_evaluation,
            job_description=request.job_description
        )

        # Map LLM evaluations to results
        evaluations = llm_result.get("evaluations", [])

        # Update results with LLM data
        for result in results:
            for eval_data in evaluations:
                if eval_data.get("filename") == result["filename"]:
                    result["match_score"] = eval_data.get("match_score")
                    result["strengths"] = eval_data.get("strengths", [])
                    result["weaknesses"] = eval_data.get("weaknesses", [])
                    result["bias"] = eval_data.get("bias", [])
                    result["summary"] = eval_data.get("summary")
                    break

    except ValueError as e:
        # API key not set, return basic results without LLM evaluation
        pass
    except Exception as e:
        # LLM evaluation failed, return basic results
        pass

    return results
