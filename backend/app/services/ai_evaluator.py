"""
AI Evaluator Service using Gemini
Provides LLM-based evaluation for resume-job matching
"""
import os
import json
import re
from typing import Optional, List, Dict, Any
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
        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def evaluate_resumes(
        self,
        resumes: List[Dict[str, Any]],
        job_description: str
    ) -> Dict[str, Any]:
        """
        Evaluate multiple resumes against a job description

        Args:
            resumes: List of resume objects with id, filename, text
            job_description: The job description

        Returns:
            Dictionary with evaluation results in JSON format
        """
        # Build resume summaries for the prompt
        resume_summaries = []
        for i, resume in enumerate(resumes):
            # Truncate long texts for the prompt
            text = resume.get("text", "")[:2000]
            resume_summaries.append(f"Resume {i+1}: {resume.get('filename', 'Unknown')}\n{text}")

        resumes_text = "\n\n---\n\n".join(resume_summaries)

        prompt = f"""You are an expert HR recruiter. Evaluate how well each of the following resumes matches the job description.

Job Description:
{job_description}

Resumes:
{resumes_text}

Provide a JSON response with the following structure for EACH resume:

{{
  "resume_index": 1,
  "filename": "resume.pdf",
  "match_score": 85,
  "strengths": ["Python developer with 5 years experience", "Strong ML background"],
  "weaknesses": ["No experience with cloud platforms", "Limited leadership experience"],
  "bias": ["Overqualified for entry-level position"],
  "summary": "A strong candidate with relevant technical skills"
}}

Return a JSON array with entries for ALL resumes. Only return valid JSON, no other text."""

        response = self.model.generate_content(prompt)

        # Parse the JSON response
        try:
            # Try to extract JSON from response
            text = response.text.strip()
            # Find JSON array in the response
            json_match = re.search(r'\[.*\]', text, re.DOTALL)
            if json_match:
                evaluations = json.loads(json_match.group())
            else:
                evaluations = json.loads(text)
        except json.JSONDecodeError:
            # Fallback: create basic response
            evaluations = [
                {
                    "resume_index": i + 1,
                    "filename": r.get("filename", "Unknown"),
                    "match_score": 50,
                    "strengths": ["Unable to analyze"],
                    "weaknesses": ["Unable to analyze"],
                    "bias": ["Unable to analyze"],
                    "summary": "Error parsing LLM response"
                }
                for i, r in enumerate(resumes)
            ]

        return {
            "evaluations": evaluations,
            "job_description": job_description,
            "model": "gemini-2.5-flash"
        }


# Global instance (lazy loading)
_ai_evaluator: Optional[AIEvaluator] = None


def get_ai_evaluator() -> AIEvaluator:
    """Get or create AI evaluator instance"""
    global _ai_evaluator
    if _ai_evaluator is None:
        _ai_evaluator = AIEvaluator()
    return _ai_evaluator
