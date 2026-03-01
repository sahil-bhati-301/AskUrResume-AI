"""
Embedding generation service
Uses Sentence Transformers to generate text embeddings
"""
from sentence_transformers import SentenceTransformer
import numpy as np

# Use a lightweight model for faster processing
MODEL_NAME = "all-MiniLM-L6-v2"

# Global model instance (lazy loading)
_model = None


def get_model():
    """
    Get or create the sentence transformer model
    Uses lazy loading to avoid loading model on every request
    """
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def generate_embedding(text: str) -> np.ndarray:
    """
    Generate embedding vector for given text
    
    Args:
        text: Input text string
        
    Returns:
        Embedding vector as numpy array
    """
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")
    
    model = get_model()
    
    # Generate embedding
    embedding = model.encode(text, convert_to_numpy=True)
    
    return embedding
