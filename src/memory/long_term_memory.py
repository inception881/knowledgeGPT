from langchain_chroma import Chroma
from src.embedding import get_embeddings
from src.config import Config
# Ensure correct v1.0 components are imported
from langchain.agents.middleware import before_model, after_model
from datetime import datetime
import hashlib
from src.utils.logging_config import get_logger

# Initialize logger
logger = get_logger(__name__)

# Initialize Chroma
chroma_store = Chroma(
    collection_name="conversation_history",
    embedding_function=get_embeddings(),
    persist_directory=Config.LONG_TERM_MEMORY
)

def generate_msg_id(content: str, role: str) -> str:
    """Generate content-based unique ID to prevent duplicate storage"""
    raw = f"{role}:{content}"
    return hashlib.md5(raw.encode('utf-8')).hexdigest()

# 1. Retrieval middleware
@before_model
def retrieve_similar_history_middleware(state, runtime):
    """
    Retrieves similar history before calling the model and temporarily injects it into the System Prompt.
    Fixes the issue of unlimited growth of state.system.
    """
    messages = getattr(state, "messages", [])
    if not messages:
        return state

    # 1. Get the latest user message
    last_msg = messages[-1]
    current_query = ""
    
    # Compatibility check: Confirm it's a HumanMessage
    if hasattr(last_msg, "type") and last_msg.type == "human":
         current_query = last_msg.content
    elif hasattr(last_msg, "content") and not hasattr(last_msg, "tool_calls"):
         current_query = last_msg.content

    if not current_query:
        return state
    
    # 2. Execute vector retrieval
    # print("Retrieving relevant conversation history...") # for debugging
    results = chroma_store.similarity_search(current_query, k=3)
    
    if results:
        history_context = "\n".join([f"- {r.page_content}" for r in results])
        
        # Construct the prompt to be injected
        additional_prompt = f"\n\n## Reference Conversation History (Memory):\n{history_context}\n"
        
        # --- 🔥 Core modification begins ---
        
        # Get the current system prompt (prioritize from runtime parameters, otherwise from state)
        # Note: getattr(state, "system", "") prevents errors if state has no system field
        original_system = runtime.kwargs.get("system") or getattr(state, "system", "") or ""
        
        # Concatenate original prompt + history records
        # Only modify runtime.kwargs, which are "temporary parameters" that won't be saved to the database by Checkpointer
        runtime.kwargs["system"] = f"{original_system}{additional_prompt}"
        
        # --- 🔥 Core modification ends ---

    return state
# 2. Save user messages middleware (fixed duplication issue)
@before_model
def save_user_messages_middleware(state, runtime):
    messages = getattr(state, "messages", [])
    if not messages:
        return state
        
    # ✅ Key change: only process the last message in the list
    # Since before_model is triggered before the model call, the last message must be newly sent by the user
    last_msg = messages[-1]
    
    # Determine if it's a valid user text message
    is_human = (hasattr(last_msg, "type") and last_msg.type == "human") or \
               (hasattr(last_msg, "role") and last_msg.role == "user")
               
    if is_human and hasattr(last_msg, "content"):
        content = last_msg.content
        # Handle List[content] (like multimodal input)
        if isinstance(content, list):
            text_parts = [item["text"] for item in content if isinstance(item, dict) and "text" in item]
            content = " ".join(text_parts)
            
        if content and isinstance(content, str) and content.strip():
            try:
                # ✅ Use ID to prevent duplication
                msg_id = generate_msg_id(content, "user")
                chroma_store.add_texts(
                    texts=[content],
                    metadatas=[{"role": "user", "timestamp": datetime.now().isoformat()}],
                    ids=[msg_id] # Explicit deduplication: if ID already exists, will typically update or skip
                )
                logger.info(f"User message saved to long-term memory with ID: {msg_id[:8]}...")
            except Exception as e:
                logger.error(f"Failed to save user message: {e}")
    
    return state

# 3. Save AI response middleware (fixed tool call filtering)
@after_model
def save_assistant_response_middleware(state, runtime):
    # state.response is a ModelResponse object
    if not hasattr(state, "response"):
        return state
        
    response = state.response
    
    # ✅ Key change: check if it contains tool calls
    # If the model decides to call a tool, content is usually empty or tool parameters, should not be stored in conversation history
    if hasattr(response, "tool_calls") and response.tool_calls:
        return state # Skip saving tool call steps
        
    content = getattr(response, "content", "")
    
    # Handle List content
    if isinstance(content, list):
        text_parts = [item["text"] for item in content if isinstance(item, dict) and "text" in item]
        content = " ".join(text_parts)
        
    if content and isinstance(content, str) and content.strip():
        try:
            msg_id = generate_msg_id(content, "assistant")
            chroma_store.add_texts(
                texts=[content],
                metadatas=[{"role": "assistant", "timestamp": datetime.now().isoformat()}],
                ids=[msg_id]
            )
            logger.info(f"Assistant response saved to long-term memory with ID: {msg_id[:8]}...")
        except Exception as e:
            logger.error(f"Failed to save model response: {e}")
            
    return state

from langchain_core.messages import AIMessage, ToolMessage
from langchain.agents.middleware import before_model

@before_model
def sanitize_dangling_tool_middleware(state, runtime):
    """
    [Gatekeeper Middleware]
    Detect and fix dangling tool calls at the end of conversation history.
    
    Scenario:
    In the previous run, the model issued a tool_use request, but before the tool execution result
    was written to the database, the program crashed or was interrupted. This causes the history
    to end with a tool_use, and requesting Claude again will result in a 400 Error.
    
    Processing logic:
    Directly remove the last unfinished tool_use message, allowing the model to face
    the user's previous question again.
    """
    # 1. Get message list (compatible with attribute access and dictionary access)
    messages = getattr(state, "messages", [])
    if not messages:
        return state

    # 2. Check the last message
    last_msg = messages[-1]
    
    # Determine if it's an AI message and contains tool calls
    # Note: Different versions of LangChain/Core may have slightly different attributes, compatibility is provided here
    is_ai_msg = isinstance(last_msg, AIMessage)
    has_tool_calls = hasattr(last_msg, "tool_calls") and last_msg.tool_calls
    
    if is_ai_msg and has_tool_calls:
        logger.warning(f"🚨 [Auto-fix] Detected dangling tool call (ID: {last_msg.id}), removing...")
        
        # 3. Execute removal operation
        # This operation depends on whether state is a Pydantic object or Dict, usually direct slicing works
        # We remove the last message, so the conversation will revert to the User input state
        try:
            # Try to modify state object
            if hasattr(state, "messages"):
                # Note: Must assign a new list, cannot modify in place, otherwise may not trigger state update
                state.messages = messages[:-1]
            elif isinstance(state, dict) and "messages" in state:
                state["messages"] = messages[:-1]
                
            logger.info("✅ [Auto-fix] Fix complete, state reset to previous step.")
            
        except Exception as e:
            logger.error(f"❌ [Auto-fix] Failed to remove message: {e}")

    return state
