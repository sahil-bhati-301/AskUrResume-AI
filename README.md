# AskUrResume-AI (AURA)

## Abstract

AskUrResume-AI (AURA) is a resume screening and matching system that uses semantic search to rank resumes against a given job description. The system allows users to upload multiple resumes in PDF format and then input a job description to find the most relevant candidates.

## Scope

The project involves building a web service with the following capabilities:

1. **Resume Upload** - Users can upload multiple resumes in PDF format
2. **Job Description Input** - Users can provide a text-based job description
3. **Semantic Matching** - The system matches resumes against the job description using vector embeddings
4. **Ranked Results** - Returns a sorted list of resumes based on relevance to the job description

## Tech Stack

- **Backend**: FastAPI (Python)
- **Vector Search**: FAISS (Facebook AI Similarity Search)
- **Frontend**: React

## How It Works

1. Resumes uploaded by users are processed to extract text from PDF files
2. Each resume is converted into a vector embedding using sentence transformers
3. When a job description is submitted, it is also converted to a vector embedding
4. FAISS performs similarity search to find the most relevant resumes
5. Results are ranked and displayed to the user with match scores
