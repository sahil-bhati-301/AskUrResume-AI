"""
Resume upload and management API endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
from app.models.schemas import ResumeResponse, ResumeListResponse
from app.services.pdf_processor import extract_text_from_pdf
from app.services.embeddings import generate_embedding
from app.services.vector_store import add_resume, get_all_resumes, delete_resume

router = APIRouter()


@router.post("/upload", response_model=List[ResumeResponse])
async def upload_resumes(files: List[UploadFile] = File(...)):
    """
    Upload multiple resume PDF files
    """
    uploaded_resumes = []
    
    for file in files:
        # Validate file type
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(
                status_code=400,
                detail=f"File {file.filename} is not a PDF"
            )
        
        # Read file content
        content = await file.read()
        
        # Extract text from PDF
        try:
            text = extract_text_from_pdf(content)
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Failed to extract text from {file.filename}: {str(e)}"
            )
        
        # Generate embedding
        try:
            embedding = generate_embedding(text)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate embedding: {str(e)}"
            )
        
        # Add to vector store
        resume = add_resume(
            filename=file.filename,
            text=text,
            embedding=embedding
        )
        uploaded_resumes.append(resume)
    
    return uploaded_resumes


@router.get("/list", response_model=ResumeListResponse)
async def list_resumes():
    """
    Get all uploaded resumes
    """
    resumes = get_all_resumes()
    return ResumeListResponse(resumes=resumes, total=len(resumes))


@router.delete("/{resume_id}")
async def delete_resume_by_id(resume_id: str):
    """
    Delete a specific resume
    """
    success = delete_resume(resume_id)
    if not success:
        raise HTTPException(status_code=404, detail="Resume not found")
    return {"message": "Resume deleted successfully"}
