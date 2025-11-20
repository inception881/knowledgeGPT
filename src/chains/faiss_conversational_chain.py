"""
FAISS-based Conversational RAG Chain - Multi-turn dialogue with memory
Implemented using LangChain Agent
"""
from langchain_core.documents import Document
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain.agents import create_agent
from langchain.tools import BaseTool
from langchain.agents.middleware import SummarizationMiddleware
# from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.sqlite import SqliteSaver

from typing import List, Dict, Any
from pathlib import Path

from src.config import Config
from src.prompts.templates import PromptTemplate
from src.chat_model import get_chat_model
from src.loaders.document_loader import get_document_loader
from src.vectorstores.faiss_store import get_faiss_vector_store
from src.utils.logging_config import get_logger

# Initialize logger
logger = get_logger(__name__)

# Vector store path
FAISS_INDEX_PATH = Config.FAISS_INDEX_PATH

# Ensure directory exists
FAISS_INDEX_PATH.mkdir(parents=True, exist_ok=True)

class RetrievalTool(BaseTool):
    """Tool for retrieving documents from vector store"""
    
    name: str = "retrieval_tool"
    description: str = "Retrieve relevant documents from knowledge base"
    retriever: Any = None  # Add retriever as Pydantic field
    last_docs: List[Document] = []  # Store the most recent retrieved documents
    
    def __init__(self, retriever):
        """Initialize retrieval tool"""
        super().__init__(retriever=retriever)  # Pass retriever via parameter
    
    def _run(self, query: str) -> str:
        """Execute retrieval operation"""
        docs = self.retriever.invoke(query)
        self.last_docs = docs  # Save retrieved documents
        
        if not docs:
            return "No relevant documents found."
        
        # Format documents
        formatted_docs = "\n\n".join([f"<doc>\n{doc.page_content}\n</doc>" for doc in docs])
        return formatted_docs
    
    def get_last_docs(self) -> List[Document]:
        """Get the most recently retrieved documents"""
        return self.last_docs

class FAISSConversationalRAGChain:
    """FAISS-based Conversational RAG Chain using Agent implementation"""
    
    def __init__(self, session_id: str = "default"):
        """
        Initialize
        
        Args:
            session_id: Session ID
        """
        self.session_id = session_id
        
        # LLM
        self.llm = get_chat_model()
        
        # Load documents from data/documents directory
        self.document_loader = get_document_loader()
        
        # Get FAISS vector store
        self.faiss_store = get_faiss_vector_store()
        self.retriever = self.faiss_store.get_retriever()
        
        # Memory - use simple list to store conversation history
        self.history = []
        
        # Get prompt
        self.prompt_template = PromptTemplate.template
        
        # Create retrieval tool
        self.retrieval_tool = RetrievalTool(self.retriever)
        
        logger.info(f"Initializing conversation chain for session: {self.session_id}")
        import sqlite3
        
        for file in Path(Config.SHORT_TERM_MEMORY).rglob("*"):
            if file.is_file():  
                file.unlink(missing_ok=True) 
        conn=sqlite3.connect(str(Config.SHORT_TERM_MEMORY/ f"{self.session_id}.db"), check_same_thread=False)
        conn.execute("PRAGMA journal_mode=WAL;")

        from src.memory.long_term_memory import retrieve_similar_history_middleware,save_assistant_response_middleware,save_user_messages_middleware,sanitize_dangling_tool_middleware
        # Create agent with middleware for summarization
        self.agent = create_agent(
            model=self.llm,
            tools=[self.retrieval_tool],
            middleware=[
                sanitize_dangling_tool_middleware,
                SummarizationMiddleware(
                    model=get_chat_model(model="claude-sonnet-4-5"),
                    max_tokens_before_summary=4000,  # Trigger summarization at 4000 tokens
                    messages_to_keep=20,  # Keep last 20 messages after summary
                ),
                # 调整中间件顺序，确保在模型调用前后正确执行
                retrieve_similar_history_middleware,  # 在模型调用前获取相关历史
                save_user_messages_middleware,        # 在模型调用前保存用户消息
                save_assistant_response_middleware    # 在模型调用后保存助手响应
            ],
            
            # Use SqliteSaver instead of AsyncSqliteSaver to avoid event loop issues
            checkpointer = SqliteSaver(conn=conn),
        )
    
    
 
    from streamlit.runtime.uploaded_file_manager import UploadedFile
    def add_documents(self, file_path: UploadedFile):
        """
        Add documents to vector store
        
        Args:
            file_path: File path
        """
        # file_path = self.document_loader.save_uploaded_file(file_path)
        # Convert string path to Path object
        # path = Path(file_path)
        
        # Process file
        chunks = self.document_loader._process_file(file_path=file_path, skip_processed=True)
        
        if not chunks:
            logger.warning(f"⚠️ File {file_path.name} did not generate any document chunks after processing")
            return {"message": f"Skipping already processed file:  {file_path.name} "}
        
        # Use FAISS vector store service to add documents
        self.faiss_store.add_documents(chunks)
        
        # Update retriever
        self.retriever = self.faiss_store.get_retriever()
    
    def  delete_documents(self, doc_id: str):
        """
        Delete document from vector store
        
        Args:
            doc_id: Document ID

        """
        self.document_loader.delete_processed_document(doc_id)
        self.faiss_store.delete_by_source(doc_id)
    
    def clear_documents(self):
        """Clear documents and conversation history"""
        # Clear documents from knowledge base
        self.document_loader.clear_all_processed_documents()
        self.faiss_store.clear()

# Session management
_sessions = {}

def get_conversational_chain(session_id: str) -> FAISSConversationalRAGChain:
    """Get or create conversation Chain"""
    import asyncio
    
    # Ensure we have an event loop
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    if session_id not in _sessions:
        _sessions[session_id] = FAISSConversationalRAGChain(session_id)
    return _sessions[session_id]

def clear_session(session_id: str):
    """Clear session"""
    if session_id in _sessions:
        _sessions[session_id].clear_memory()
        del _sessions[session_id]
