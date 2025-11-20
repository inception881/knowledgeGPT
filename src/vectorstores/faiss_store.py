"""
FAISS Vector Store Management

This module provides a unified management interface for FAISS vector storage, including creation, loading, updating, and querying.
FAISS is an efficient vector similarity search library used to store document vector representations and perform fast retrieval.
"""
import uuid
from pathlib import Path
from typing import List, Optional, Dict, Any, Union
import hashlib

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore

from src.config import Config
from src.embedding import get_embeddings, get_embeddings_singleton
from src.loaders.document_loader import get_document_loader
from src.utils.logging_config import get_logger

# Initialize logger
logger = get_logger(__name__)

# Vector store path
FAISS_INDEX_PATH = Config.FAISS_INDEX_PATH

# Ensure directory exists
FAISS_INDEX_PATH.mkdir(parents=True, exist_ok=True)

class FAISSVectorStore:
    """FAISS Vector Store Management Class"""
    
    def __init__(self, embeddings: Optional[Embeddings] = None):
        """
        Initialize FAISS vector store manager
        
        Args:
            embeddings: Embedding model, defaults to global singleton
        """
        self.embeddings = embeddings or get_embeddings_singleton()
        self.vector_store = self._load_or_create_vector_store()
    
    def _load_or_create_vector_store(self) -> FAISS:
        """
        Load or create FAISS vector store
        
        If a saved vector store exists, load it; otherwise create an empty one.
        
        Returns:
            FAISS vector store instance
        """
        # Check if saved vector store exists
        if FAISS_INDEX_PATH.exists() and any(FAISS_INDEX_PATH.iterdir()):
            try:
                logger.info(f"✅ Loading existing vector store (path: {FAISS_INDEX_PATH})")
                vector_store = FAISS.load_local(
                    folder_path=str(FAISS_INDEX_PATH),
                    embeddings=self.embeddings,
                    allow_dangerous_deserialization=True
                )
                return vector_store
            except Exception as e:
                logger.warning(f"⚠️ Failed to load vector store: {e}, will create a new one")
        
        # If no documents, create an empty vector store
        logger.warning("⚠️ No existing vector store found or loading failed, creating empty vector store")
        vector_store = FAISS.from_texts(
            ["初始化文档"], self.embeddings
        )
        vector_store.save_local(str(FAISS_INDEX_PATH))
        return vector_store
    
    def get_retriever(self, k: int = None):
        """
        Get retriever
        
        Args:
            k: Number of documents to retrieve, defaults to value in configuration
            
        Returns:
            Retriever instance
        """
        search_kwargs = {"k": k or Config.TOP_K}
        return self.vector_store.as_retriever(search_type="mmr",search_kwargs=search_kwargs)
    
    def add_documents(self, documents: List[Document], batch_size: int = 10, ids: Optional[List[str]] = None) -> bool:
        """
        Add documents to vector store
        
        Args:
            documents: List of document chunks to add
            batch_size: Batch processing size
            ids: Optional list of document IDs, if provided, length must match documents
            
        Returns:
            Whether documents were successfully added
        """
        if not documents:
            logger.warning("⚠️ No documents to add")
            return False
        
        # Generate document IDs
        if ids is None:
            # Generate an ID for each document, format: source_file_path_UUID
            generated_ids = []
            for doc in documents:
                source = doc.metadata.get("file_name", "")
                doc_uuid = str(uuid.uuid4())
                generated_ids.append(f"{source}_{doc_uuid}")
            ids = generated_ids
        
        # Ensure document and ID counts match
        if len(documents) != len(ids):
            error_msg = f"Document count ({len(documents)}) does not match ID count ({len(ids)})"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Use document loader service's batch processing capability
        loader = get_document_loader()
        batches = loader.batch_process_documents(documents, batch_size)
        id_batches = [ids[i:i+batch_size] for i in range(0, len(ids), batch_size)]
        logger.info(f"✅ Document batching complete: {len(batches)} batches")
        
        # Vectorize and merge into vector store (using pre-divided batches)
        for i, (batch, batch_ids) in enumerate(zip(batches, id_batches)):
            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(batch, self.embeddings, ids=batch_ids)
            else:
                # Use add_documents instead of from_documents and merge_from to pass IDs
                self.vector_store.add_documents(documents=batch, ids=batch_ids)
            logger.info(f"✅ Processed batch {i+1}/{len(batches)}")
        
        # Save updated vector store locally
        if self.vector_store:
            self.vector_store.save_local(str(FAISS_INDEX_PATH))
            logger.info(f"✅ Vector store update complete, saved to: {FAISS_INDEX_PATH}")
            return True
        
        return False
    

    
    def search(self, query: str, k: int = None) -> List[Document]:
        """
        Search for relevant documents
        
        Args:
            query: Query text
            k: Number of documents to return, defaults to value in configuration
            
        Returns:
            List of relevant documents
        """
        return self.vector_store.similarity_search(query, k=k or Config.TOP_K)
    
    def search_with_score(self, query: str, k: int = None) -> List[tuple]:
        """
        Search for relevant documents and return similarity scores
        
        Args:
            query: Query text
            k: Number of documents to return, defaults to value in configuration
            
        Returns:
            List of (document, score) tuples
        """
        return self.vector_store.similarity_search_with_score(query, k=k or Config.TOP_K)
    
    def save(self, path: Optional[str] = None) -> None:
        """
        Save vector store locally
        
        Args:
            path: Save path, defaults to path in configuration
        """
        save_path = path or str(FAISS_INDEX_PATH)
        self.vector_store.save_local(save_path)
        logger.info(f"✅ Vector store saved to: {save_path}")
    
    # def load_documents_and_update(self, document_paths: List[str]) -> bool:
    #     """
    #     加载文档并更新向量库
        
    #     Args:
    #         document_paths: 文档路径列表
            
    #     Returns:
    #         是否成功更新
    #     """
    #     print(f"\n📚 开始更新知识库（新文档数：{len(document_paths)}）")
        
    #     # 使用文档加载器服务加载文档
    #     loader = get_document_loader()
    #     all_docs = loader.process_documents(document_paths, skip_processed=True)
        
    #     if not all_docs:
    #         print("⚠️ 无新增文档，知识库未更新")
    #         return False
        
    #     print(f"✅ 成功加载 {len(all_docs)} 个新文档")
        
    #     # 添加文档到向量库
    #     return self.add_documents(all_docs)
    
    from langchain_community.vectorstores import FAISS


    # 假设 vector_store 是你已加载的 LangChain FAISS 对象
    # e.g., vector_store = FAISS(...)
    def clear(self) -> None:
        # 1) Clear underlying faiss index (memory)
        import faiss
        from langchain_community.docstore.in_memory import InMemoryDocstore
        index: faiss.Index = self.vector_store.index
        index.reset()  # Clear all vectors (ntotal will become 0)

        # 2) Clear LangChain mappings and docstore (implementation dependent)
        self.vector_store.index_to_docstore_id = {}   # Clear index->doc id mapping
        # If there's a docstore, reset to a new empty docstore (example using InMemoryDocstore)
        try:
            self.vector_store.docstore = InMemoryDocstore()
        except Exception:
            # If reset not possible, can manually delete saved docstore file (method A)
            pass

        # 3) Save and overwrite locally (overwrite original index file/directory)
        self.vector_store.save_local(str(FAISS_INDEX_PATH))  # Overwrite previously saved location
        logger.info("Index has been reset and saved to faiss_index")
    def delete(self, ids: List[str]) -> bool:
        """
        Delete documents with specified IDs from vector store
        
        Args:
            ids: List of document IDs to delete
            
        Returns:
            Whether deletion was successful
        """
        if not ids:
            logger.warning("⚠️ No document IDs provided for deletion")
            return False
        
        try:
            self.vector_store.delete(ids=ids)
            # Save updated vector store locally
            self.save()
            logger.info(f"✅ Successfully deleted {len(ids)} documents")
            return True
        except Exception as e:
            logger.error(f"⚠️ Failed to delete documents: {e}")
            return False
    
    def delete_by_source(self, doc_id:str) -> bool:
        """
        Delete documents from a specific source file from vector store

        Args:
            doc_id: Source filename

        Returns:
            Whether deletion was successful
        """
        if not doc_id:
            logger.warning("⚠️ No source file path provided for deletion")
            return False
        
        try:
            # Get all document IDs
            all_ids = list(self.vector_store.index_to_docstore_id.values())
            logger.debug(f"all_ids: {all_ids}")
            
            # Find matching IDs
            ids_to_delete = []

            for id in all_ids:
                # Ignore UUID part
                if id.startswith(f"{doc_id}_"):
                    ids_to_delete.append(id)
            
            if not ids_to_delete:
                logger.warning("⚠️ No matching documents found")
                return False
            
            # Delete matching documents
            self.vector_store.delete(ids=ids_to_delete)
            
            # Save updated vector store locally
            self.save()
            logger.info(f"✅ Successfully deleted {len(ids_to_delete)} documents")
            return True
        except Exception as e:
            logger.error(f"⚠️ Failed to delete documents: {e}")
            return False
    
    # def clear(self) -> None:
    #     """清空向量库"""
    #     # 创建一个新的空向量库
    #     self.vector_store = FAISS.from_texts(
    #         ["初始化文档"], self.embeddings
    #     )
    #     self.save()
    #     print("✅ 向量库已清空")


# Global singleton
_vector_store_instance = None

def get_faiss_vector_store() -> FAISSVectorStore:
    """
    Get FAISS vector store singleton
    
    Returns:
        FAISSVectorStore singleton instance
    """
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = FAISSVectorStore()
    return _vector_store_instance
