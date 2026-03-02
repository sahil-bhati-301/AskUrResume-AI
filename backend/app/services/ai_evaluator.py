"""
AI Evaluator Service using Gemini
Provides LLM-based evaluation for resume-job matching
"""
import os
from typing import Optional
import google.generativeai as genai


class AIEvaluator:
    """AI evaluator using Gemini for resume-job matching analysis"""
    
    def __init__(self):
        """Initialize Gemini with API key from environment"""
        api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key or api_key == "your_api_key_here":
            raise ValueError(
                "GEMINI_API_KEY not set. "
                "Run 'python setup_env.py' to configure your API key."
            )
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")
    
    def evaluate_resume(
        self,
        resume_text: str,
        job_description: str
    ) -> dict:
        """
        Evaluate how well a resume matches a job description
        
        Args:
            resume_text: The resume content
            job_description: The job description
            
        Returns:
            Dictionary with evaluation results
        """
        prompt = f"""
You are an expert HR recruiter. Evaluate how well the following resume 
matches the job description.

Resume:
{resume_text}

Job Description:
{job_description}

Provide a detailed evaluation with:
1. Match Score (0-100%)
2. Key strengths (what the candidate offers)
3. Missing skills (what's required but not found)
4. Summary (2-3 sentences overall fit)
"""
        
        response = self.model.generate_content(prompt)
        
        return {
            "evaluation": response.text,
            "model": "gemini-2.0-flash"
        }
    
    def generate_interview_questions(
        self,
        resume_text: str,
        job_description: str
    ) -> dict:
        """
        Generate interview questions based on resume and job description
        
        Args:
            resume_text: The resume content
            job_description: The job description
            
        Returns:
            Dictionary with generated questions
        """
        prompt = f"""
Based on the following resume and job description, generate 
5 relevant interview questions to ask the candidate.

Resume:
{resume_text}

Job Description:
{job_description}

Generate questions that:
- Assess technical skills mentioned in the job
- Explore experience relevant to the role
- Are specific to the candidate's background
"""
        
        response = self.model.generate_content(prompt)
        
        return {
            "questions": response.text,
            "model": "gemini-2.0-flash"
        }


# Global instance (lazy loading)
_ai_evaluator: Optional[AIEvaluator] = None


def get_ai_evaluator() -> AIEvaluator:
    """Get or create AI evaluator instance"""
    global _ai_evaluator
    if _ai_evaluator is None:
        _ai_evaluator = AIEvaluator()
    return _ai_evaluator
