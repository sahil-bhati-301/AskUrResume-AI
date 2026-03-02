"""
Test script to verify Gemini API is working
Run: python test_llm.py
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Test the AI evaluator
try:
    from app.services.ai_evaluator import AIEvaluator
    
    print("Initializing AI Evaluator...")
    evaluator = AIEvaluator()
    print("✓ AI Evaluator initialized successfully!")
    
    # Test prompt
    test_resume = """
    John Doe
    Python Developer with 5 years experience
    Skills: Python, Django, FastAPI, PostgreSQL, Docker, AWS
    Experience:
    - Senior Python Developer at Tech Corp (2020-Present)
    - Python Developer at Startup Inc (2018-2020)
    Education: BS Computer Science
    """
    
    test_job = """
    We are looking for a Python developer with experience in:
    - Python, Django, FastAPI
    - Cloud platforms (AWS)
    - Database design
    - Microservices architecture
    """
    
    print("\nTesting resume evaluation...")
    result = evaluator.evaluate_resumes(
        resumes=[{"filename": "test_resume.pdf", "text": test_resume}],
        job_description=test_job
    )
    
    print("\n✓ Evaluation result:")
    print(result)
    
except ValueError as e:
    print(f"✗ Error: {e}")
    print("\nPlease run: python setup_env.py")
except Exception as e:
    print(f"✗ Unexpected error: {e}")
