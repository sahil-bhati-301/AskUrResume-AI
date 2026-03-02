"""
Pydantic schemas for request/response models
"""
from pydantic import BaseModel
from typing import List, Optional


class ResumeResponse(BaseModel):
    """Response model for a single resume"""
    id: str
    filename: str
    text_preview: str
    uploaded_at: str


class ResumeListResponse(BaseModel):
    """Response model for listing resumes"""
    resumes: List[ResumeResponse]
    total: int


class SearchRequest(BaseModel):
    """Request model for search"""
    job_description: str
    top_k: Optional[int] = 3


class EvaluationResult(BaseModel):
    """Individual resume evaluation result"""
    resume_index: int
    filename: str
    match_score: int
    strengths: List[str]
    weaknesses: List[str]
    bias: List[str]
    summary: str


class SearchResult(BaseModel):
    """Response model for search results"""
    id: str
    filename: str
    score: float
    text_preview: str
    # LLM evaluation fields
    match_score: Optional[int] = None
    strengths: Optional[List[str]] = None
    weaknesses: Optional[List[str]] = None
    bias: Optional[List[str]] = None
    summary: Optional[str] = None
