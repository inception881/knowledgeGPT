"""
Text Splitting Utilities
"""
from langchain_text_splitters import (
    RecursiveCharacterTextSplitter,
    CharacterTextSplitter,
    TokenTextSplitter
)
from src.config import Config
from src.utils.logging_config import get_logger

# Initialize logger
logger = get_logger(__name__)

def get_recursive_splitter():
    """
    Get recursive character splitter
    Suitable for most texts, attempts to split at natural boundaries like paragraphs and sentences
    """
    return RecursiveCharacterTextSplitter(
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP,
        separators=["\n\n", "\n", "。", "！", "？", ".", "!", "?", " ", ""],
        length_function=len,
    )

def get_character_splitter():
    """
    Get simple character splitter
    Suitable for simple texts, splits by character count
    """
    return CharacterTextSplitter(
        separator="\n",
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP,
        length_function=len,
    )

def get_token_splitter(encoding_name="cl100k_base"):
    """
    Get token-based splitter
    Suitable for scenarios requiring precise token count control
    
    Args:
        encoding_name: Encoding name, defaults to OpenAI's cl100k_base
    """
    return TokenTextSplitter(
        encoding_name=encoding_name,
        chunk_size=Config.CHUNK_SIZE,
        chunk_overlap=Config.CHUNK_OVERLAP,
    )

def split_text(text, splitter_type="recursive"):
    """
    Split text
    
    Args:
        text: Text to split
        splitter_type: Splitter type, options: "recursive", "character", "token"
    
    Returns:
        List of text chunks after splitting
    """
    logger.info(f"Splitting text using {splitter_type} splitter")
    if splitter_type == "recursive":
        splitter = get_recursive_splitter()
    elif splitter_type == "character":
        splitter = get_character_splitter()
    elif splitter_type == "token":
        splitter = get_token_splitter()
    else:
        error_msg = f"Unsupported splitter type: {splitter_type}"
        logger.error(error_msg)
        raise ValueError(error_msg)
    
    return splitter.split_text(text)
