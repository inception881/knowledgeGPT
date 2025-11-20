"""
Embedding Model Management
"""
from langchain_openai import OpenAIEmbeddings
from typing import Optional
from src.config import Config
from src.utils.logging_config import get_logger

# Initialize logger
logger = get_logger(__name__)

def get_embeddings(
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None
) -> OpenAIEmbeddings:
    """
    Get embedding model instance
    
    Args:
        model: Model name, defaults to the one in configuration
        api_key: API key, defaults to the one in configuration
        base_url: API base URL, defaults to the one in configuration
        
    Returns:
        OpenAIEmbeddings instance
    """
    logger.info(f"Initializing embedding model: {model or Config.OPENAI_EMBEDDING_MODEL}")
    return OpenAIEmbeddings(
        model=model or Config.OPENAI_EMBEDDING_MODEL,
        openai_api_key=api_key or Config.OPENAI_API_KEY,
        base_url=base_url or Config.OPENAI_BASE_URL
    )

# Global singleton
_embeddings = None

def get_embeddings_singleton() -> OpenAIEmbeddings:
    """
    Get embedding model singleton
    
    Returns:
        OpenAIEmbeddings singleton instance
    """
    global _embeddings
    if _embeddings is None:
        _embeddings = get_embeddings()
    return _embeddings
