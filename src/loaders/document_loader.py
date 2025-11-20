"""
Document Loader - Using LangChain document loaders to load and process various document formats

This module provides a unified document loading interface supporting multiple file formats including PDF, Word, text, HTML, and Markdown.
It handles document loading, chunking, metadata addition, and processing state tracking to avoid reprocessing the same document.
"""
from pathlib import Path
import os
from typing import List, Optional, Dict, Any
from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    TextLoader,
)
from src.config import Config
from src.utils.text_splitter import get_recursive_splitter
from src.utils.logging_config import get_logger

# Initialize logger
logger = get_logger(__name__)

# Path to file recording processed document identifiers
PROCESSED_DOCS_RECORD = Config.PROCESSED_DOCS_RECORD

class DocumentLoaderService:
    """
    Document Loading Service
    
    Provides unified document loading, processing, and management functionality,
    supporting multiple file formats with deduplication and status tracking.
    """
    
    # Supported file types and their corresponding loaders
    SUPPORTED_LOADERS = {
        ".pdf": PyPDFLoader,
        ".docx": Docx2txtLoader,
        ".doc": Docx2txtLoader,
        ".txt": TextLoader,
        ".html": TextLoader,
        ".htm": TextLoader,
        ".md": TextLoader,
    }
    
    def __init__(self):
        """Initialize document loader service, set up text splitter"""
        self.text_splitter = get_recursive_splitter()
    
    def load_document(self, file_path: str) -> List[Document]:
        """
        Load a single document and process it into chunks
        
        Args:
            file_path: File path
        
        Returns:
            List of Document objects (chunked)
        
        Raises:
            ValueError: When file type is not supported
        """
        path = Path(file_path)
        suffix = path.suffix.lower()
        
        # Check if file type is supported
        if suffix not in self.SUPPORTED_LOADERS:
            raise ValueError(f"Unsupported file type: {suffix}, supported types: {list(self.SUPPORTED_LOADERS.keys())}")
        
        # Get appropriate loader class
        loader_class = self.SUPPORTED_LOADERS[suffix]
        
        # Create loader instance
        loader_kwargs = {"encoding": "utf-8"} if loader_class == TextLoader else {}
        loader = loader_class(str(path), **loader_kwargs)
        
        # Load document
        documents = loader.load()
        
        # Add metadata
        for doc in documents:
            doc.metadata.update({
                "source": str(path),
                "file_name": path.name,
                "file_type": suffix
            })
        
        # Process into chunks
        logger.info(f"Processing document: {path.name}")
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Document split into {len(chunks)} chunks")
        return chunks
    

    from streamlit.runtime.uploaded_file_manager import UploadedFile
    def _process_file(self, file_path : UploadedFile, skip_processed: bool) -> List[Document]:
        """
        Process a single file
        
        Args:
            file_path: File path
            skip_processed: Whether to skip already processed documents
        
        Returns:
            List of Document objects (chunked)
        """
        # Use only the filename as the document ID
        doc_id = file_path.name
        if skip_processed and self._is_document_processed(doc_id):
            logger.info(f"Skipping already processed file: {doc_id}")
            return []
        if file_path is None:
            error_msg = "No upload file provided"
            logger.error(error_msg)
            raise ValueError(error_msg)
            
        # Ensure documents directory exists
        Config.DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Create target file path
        file_path1 = Config.DOCUMENTS_DIR / file_path.name
        
        # Save file
        with open(file_path1, "wb") as f:
            f.write(file_path.getbuffer())
        
        logger.info(f"✓ Uploaded file saved to: {file_path1}")
        
        logger.info(f"Loading file: {file_path1.name}")
        try:
            # Load and process document
            chunks = self.load_document(str(file_path1))
            
            # Record processed document
            self._record_processed_document(doc_id)
            logger.info(f"  ✓ Success: {len(chunks)} chunks")
            
            return chunks
        except Exception as e:
            logger.error(f"  ✗ Failed: {e}")
            return []
    
    def _is_document_processed(self, doc_id: str) -> bool:
        """
        Check if document has already been processed (to avoid duplicates)
        
        Args:
            doc_id: Document identifier (typically file path)
        
        Returns:
            Whether it has been processed
        """
        if not PROCESSED_DOCS_RECORD.exists():
            return False
        with open(PROCESSED_DOCS_RECORD, "r", encoding="utf-8") as f:
            processed_ids = f.read().splitlines()
        return doc_id in processed_ids
    
    def _record_processed_document(self, doc_id: str) -> None:
        """
        Record processed document identifier
        
        Args:
            doc_id: Document identifier (typically file path)
        """
        with open(PROCESSED_DOCS_RECORD, "a", encoding="utf-8") as f:
            f.write(f"{doc_id}\n")
    
    def batch_process_documents(self, documents: List[Document], batch_size: int = 10) -> List[List[Document]]:
        """
        Process documents in batches for large-scale document processing
        
        Args:
            documents: List of documents
            batch_size: Number of documents per batch
            
        Returns:
            List of batches, each containing multiple documents
        """
        batches = []
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i+batch_size]
            batches.append(batch)
            logger.info(f"Created batch {len(batches)}: {len(batch)} documents")
        
        return batches
    def list_all_processed_documents(self) -> List[str]:
        """
        List all processed documents
        
        Returns:
            List of processed document identifiers
        """
        if not PROCESSED_DOCS_RECORD.exists():
            return []
        with open(PROCESSED_DOCS_RECORD, "r", encoding="utf-8") as f:
            processed_ids = f.read().splitlines()
        return processed_ids
        
    def delete_processed_document(self, doc_id: str) -> None:
        """
        Delete a processed document from list of processed documents
        """
        if Path(Config.DOCUMENTS_DIR / doc_id).exists():
            Path(Config.DOCUMENTS_DIR / doc_id).unlink()
        else:
            logger.warning(f"Document not found: {doc_id}")

        processed_ids = self.list_all_processed_documents()
        if doc_id in processed_ids:
            processed_ids.remove(doc_id)
        else:
            logger.warning(f"Document not found in list of processed documents: {doc_id}")
        with open(PROCESSED_DOCS_RECORD, "w", encoding="utf-8") as f:
            f.write("\n".join(processed_ids))

    def clear_all_processed_documents(self) -> None:
        """
        Delete all processed documents
        """
        try:
            PROCESSED_DOCS_RECORD.open("w").close()
            logger.info(f"Successfully cleared {PROCESSED_DOCS_RECORD}")
        except Exception as e:
            logger.error(f"Failed to clear file contents of {PROCESSED_DOCS_RECORD}: {e}")
        try:
            for file in Path(Config.DOCUMENTS_DIR).glob("*"):
                if file.is_file():
                    file.unlink(missing_ok=True)
            logger.info(f"Successfully cleared {Config.DOCUMENTS_DIR}")
        except Exception as e:
            logger.error(f"Failed to clear directory {Config.DOCUMENTS_DIR}: {e}")
# Global singleton instance
_LOADER_INSTANCE = None

def get_document_loader() -> DocumentLoaderService:
    """
    Get document loader singleton instance
    
    Returns:
        DocumentLoaderService instance
    """
    global _LOADER_INSTANCE
    if _LOADER_INSTANCE is None:
        _LOADER_INSTANCE = DocumentLoaderService()
    return _LOADER_INSTANCE

def is_document_processed(doc_id: str) -> bool:
    """
    Convenience function to check if document has been processed
    
    Args:
        doc_id: Document identifier
        
    Returns:
        Whether it has been processed
    """
    loader = get_document_loader()
    return loader._is_document_processed(doc_id)

def record_processed_document(doc_id: str) -> None:
    """
    Convenience function to record processed document
    
    Args:
        doc_id: Document identifier
    """
    loader = get_document_loader()
    loader._record_processed_document(doc_id)
