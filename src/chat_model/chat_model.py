"""
Chat Model Management
"""
from langchain_anthropic import ChatAnthropic
from typing import Optional
from src.config import Config
from src.utils.logging_config import get_logger

# Initialize logger
logger = get_logger(__name__)

def get_chat_model(
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    temperature: Optional[float] = None,
    max_tokens: Optional[int] = None
) -> ChatAnthropic:
    """
    Get chat model instance
    
    Args:
        model: Model name, defaults to the one in configuration
        api_key: API key, defaults to the one in configuration
        base_url: API base URL, defaults to the one in configuration
        temperature: Temperature parameter, defaults to the one in configuration
        max_tokens: Maximum tokens to generate, defaults to the one in configuration
        
    Returns:
        ChatAnthropic instance
    """
    # Create ChatAnthropic instance
    logger.info(f"Initializing chat model: {model or Config.ANTHROPIC_MODEL_NAME}")
    chat_model = ChatAnthropic(
        model=model or Config.ANTHROPIC_MODEL_NAME,
        anthropic_api_key=api_key or Config.ANTHROPIC_API_KEY,
        base_url=base_url or Config.ANTHROPIC_BASE_URL,
        temperature=temperature if temperature is not None else Config.TEMPERATURE,
        max_tokens=max_tokens or Config.MAX_TOKENS,
    )
    
    return chat_model

# Global singleton
_chat_model = None

def get_chat_model_singleton() -> ChatAnthropic:
    """
    Get chat model singleton
    
    Returns:
        ChatAnthropic singleton instance
    """
    global _chat_model
    if _chat_model is None:
        _chat_model = get_chat_model()
    return _chat_model
