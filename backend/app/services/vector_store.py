"""
Vector store service using FAISS
Manages in-memory storage of resume embeddings and metadata
"""
import faiss
import numpy as np
from datetime import datetime
from typing import List, Dict, Any
import uuid

# In-memory storage
_resumes: Dict[str, Dict[str, Any]] = {}
_faiss_index = None
_embedding_dimension = 384  # all-MiniLM-L6-v2 produces 384-dim embeddings


def _get_faiss_index():
    """Get or create the FAISS index"""
    global _faiss_index
    if _faiss_index is None:
        # Create a new index with inner product (cosine similarity)
        _faiss_index = faiss.IndexFlatIP(_embedding_dimension)
    return _faiss_index


def add_resume(filename: str, text: str, embedding: np.ndarray) -> Dict[str, Any]:
    """
    Add a resume to the vector store
    
    Args:
        filename: Name of the PDF file
        text: Extracted text content
        embedding: Vector embedding of the text
        
    Returns:
        Resume metadata dictionary
    """
    # Normalize embedding for cosine similarity
    embedding = embedding / np.linalg.norm(embedding)
    
    # Create resume metadata
    resume_id = str(uuid.uuid4())
    resume_data = {
        "id": resume_id,
        "filename": filename,
        "text": text,
        "embedding": embedding,
        "uploaded_at": datetime.utcnow().isoformat()
    }
    
    # Store metadata
    _resumes[resume_id] = resume_data
    
    # Add to FAISS index
    index = _get_faiss_index()
    index.add(embedding.reshape(1, -1))
    
    return {
        "id": resume_id,
        "filename": filename,
        "text_preview": text[:200] + "..." if len(text) > 200 else text,
        "uploaded_at": resume_data["uploaded_at"]
    }


def get_all_resumes() -> List[Dict[str, Any]]:
    """
    Get all uploaded resumes
    
    Returns:
        List of resume metadata
    """
    result = []
    for resume in _resumes.values():
        result.append({
            "id": resume["id"],
            "filename": resume["filename"],
            "text_preview": resume["text"][:200] + "..." if len(resume["text"]) > 200 else resume["text"],
            "uploaded_at": resume["uploaded_at"]
        })
    return result


def delete_resume(resume_id: str) -> bool:
    """
    Delete a resume from the store
    
    Note: FAISS doesn't support deletion efficiently, so we mark it
    For a production system, you'd want to rebuild the index
    
    Args:
        resume_id: ID of the resume to delete
        
    Returns:
        True if deleted, False if not found
    """
    if resume_id in _resumes:
        del _resumes[resume_id]
        # For simplicity, we don't rebuild the index
        # In production, you'd rebuild or use a different approach
        return True
    return False


def search_resumes(query_embedding: np.ndarray, top_k: int = 10) -> List[Dict[str, Any]]:
    """
    Search for resumes matching a job description
    
    Args:
        query_embedding: Embedding of the job description
        top_k: Number of results to return
        
    Returns:
        List of matching resumes with scores
    """
    if not _resumes:
        return []
    
    # Normalize query embedding
    query_embedding = query_embedding / np.linalg.norm(query_embedding)
    
    # Search in FAISS
    index = _get_faiss_index()
    search_k = min(top_k, index.ntotal)
    
    if search_k == 0:
        return []
    
    scores, indices = index.search(
        query_embedding.reshape(1, -1),
        search_k
    )
    
    # Get matching resumes
    results = []
    resume_list = list(_resumes.values())
    
    for score, idx in zip(scores[0], indices[0]):
        if idx >= 0 and idx < len(resume_list):
            resume = resume_list[idx]
            results.append({
                "id": resume["id"],
                "filename": resume["filename"],
                "score": float(score),
                "text_preview": resume["text"][:200] + "..." if len(resume["text"]) > 200 else resume["text"]
            })
    
    return results
