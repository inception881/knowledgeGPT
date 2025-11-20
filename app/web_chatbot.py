"""
Simplified CHATBOT Web Interface - Supporting single session conversations and document uploads
"""
import os
import sys
import uuid
import time
from pathlib import Path
import streamlit as st
from datetime import datetime

# Add project root directory to Python path
sys.path.append(str(Path(__file__).parent.parent))
import disable_ssl_verification
from src.config import Config
from src.chains.faiss_conversational_chain import get_conversational_chain
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')


# --- Page Configuration ---
st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Modern CSS Styles ---
st.markdown("""
<style>
    /* Global font optimization */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', system-ui, -apple-system, sans-serif;
    }

    /* Sidebar beautification */
    section[data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #e9ecef;
    }
    
    section[data-testid="stSidebar"] .block-container {
        padding-top: 2rem;
    }

    /* Heading styles */
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: 600;
    }
    
    /* Document card styles */
    .doc-card {
        background-color: white;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    
    .doc-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        border-color: #bdc3c7;
    }
    
    .doc-icon {
        margin-right: 10px;
        font-size: 1.2rem;
    }
    
    .doc-name {
        font-size: 0.9rem;
        color: #34495e;
        font-weight: 500;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        max-width: 180px;
    }

    /* Reference sources area */
    .references-box {
        background-color: #f8f9fa;
        border-left: 3px solid #3498db;
        padding: 10px 15px;
        margin-top: 10px;
        border-radius: 0 4px 4px 0;
        font-size: 0.85rem;
        color: #555;
    }

    /* Footer */
    .footer {
        margin-top: 3rem;
        padding-top: 1rem;
        border-top: 1px solid #eee;
        text-align: center;
        font-size: 0.8rem;
        color: #95a5a6;
    }
    
    /* Button fine-tuning */
    .stButton button {
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.2s;
    }
    
    /* Delete button specialization */
    button[kind="secondary"] {
        border-color: #fab1a0;
        color: #d63031;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: transparent; 
    }
    ::-webkit-scrollbar-thumb {
        background: #bdc3c7; 
        border-radius: 3px;
    }
</style>
""", unsafe_allow_html=True)

# --- Logic Functions ---

def generate_session_id():
    """Generate a unique session ID"""
    # return f"session_{int(time.time())}_{uuid.uuid4().hex[:8]}"
    return f"session_123"

def init_session():
    """Initialize session state"""
    if "session_id" not in st.session_state:
        st.session_state.session_id = generate_session_id()
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    if "chatbot" not in st.session_state:
        st.session_state.chatbot = get_conversational_chain(st.session_state.session_id)

def upload_document():
    """Upload document to knowledge base"""
    uploaded_file = st.session_state.uploaded_file
    
    if uploaded_file:
        try:
            with st.spinner("Processing document, please wait..."):
                # Load document and add to vector store
                message = st.session_state.chatbot.add_documents(uploaded_file)
                if message:
                    st.toast(f"{message}", icon="⚠️")
                    return
                # Update session state
                st.toast(f"Document '{uploaded_file.name}' successfully added to knowledge base", icon="✅")
                time.sleep(1) # Let user see the notification
        except Exception as e:
            st.error(f"Upload failed: {str(e)}")

def delete_document(doc_id: str):
    """Delete document from knowledge base"""
    try:
        st.session_state.chatbot.delete_documents(doc_id)
        st.toast(f"Removed {doc_id} from knowledge base", icon="🗑️")
        time.sleep(0.5)
        st.rerun()
    except Exception as e:
        st.error(f"Deletion failed: {str(e)}")

def clear_knowledge_base():
    """Clear all documents from knowledge base and reset chat"""
    try:
        st.session_state.chatbot.clear_documents()
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Knowledge base has been cleared. All documents have been removed. Let's start fresh.",
            "timestamp": datetime.now().isoformat()
        })
        st.toast("Knowledge base completely cleared", icon="✨")
        time.sleep(0.5)
        st.rerun()
    except Exception as e:
        st.error(f"Clearing failed: {str(e)}")

def init_session_state():
    """Initialize all session state variables"""
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = "user_123"

    if "session_id" not in st.session_state:
        st.session_state.session_id = generate_session_id()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "chatbot" not in st.session_state:
        try:
            st.session_state.chatbot = get_conversational_chain(st.session_state.session_id)
        except Exception as e:
            st.error(f"Failed to initialize chatbot: {e}")
            import traceback
            st.error(traceback.format_exc())

# Call the initialization function
init_session_state()

def main():
    """Main function"""
    init_session_state()
    from src.loaders.document_loader import get_document_loader
    document_loader = get_document_loader()
    
    # --- Sidebar Design ---
    with st.sidebar:
        st.markdown("## Personal Knowledge Assistant")
        st.caption("Intelligent Q&A system built with RAG technology")
        st.markdown("---")
        
        # 1. Document Upload Area
        st.markdown("### Upload New Document")
        uploaded_file = st.file_uploader(
            "Supports PDF, TXT, DOCX, MD",
            type=["pdf", "txt", "docx", "md"],
            key="uploaded_file",
            on_change=upload_document,
            label_visibility="collapsed"
        )
        
        st.markdown("---")
        
        # 2. Document List Area
        st.markdown("### Knowledge Base Documents")
        
        processed_docs = document_loader.list_all_processed_documents()
        
        if processed_docs:
            # Using container to limit height, although Streamlit sidebar has scrolling, this helps with visual layering
            with st.container():
                for doc_id in processed_docs:
                    # Filename extraction logic
                    if "UploadedFile" in doc_id:
                        import re
                        match = re.search(r"name='([^']+)'", doc_id)
                        filename = match.group(1) if match else doc_id
                    else:
                        filename = doc_id.split('/')[-1] if '/' in doc_id else doc_id
                    
                    # Custom HTML card layout
                    col_doc, col_del = st.columns([0.85, 0.15])
                    with col_doc:
                        st.markdown(
                            f"""
                            <div class="doc-card">
                                <div style="display:flex; align-items:center;">
                                    <span class="doc-icon">📄</span>
                                    <span class="doc-name" title="{filename}">{filename}</span>
                                </div>
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
                    with col_del:
                        # Vertically center delete button
                        st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
                        if st.button("×", key=f"del_{doc_id}", help=f"Delete {filename}", type="secondary"):
                            delete_document(doc_id)
        else:
            st.info("Knowledge base is empty. Please upload documents.")
        
        st.markdown("---")
        
        # # 3. Settings and Management
        # with st.expander("Settings and Management"):
        if "confirm_clear" not in st.session_state:
            st.session_state.confirm_clear = False
        
        if st.session_state.confirm_clear:
            st.warning("Are you sure you want to clear all documents?")
            c1, c2 = st.columns(2)
            if c1.button("Confirm Clear", type="primary", use_container_width=True):
                clear_knowledge_base()
                st.session_state.confirm_clear = False
            if c2.button("Cancel", use_container_width=True):
                st.session_state.confirm_clear = False
                st.rerun()
        else:
            if st.button("Clear Knowledge Base", use_container_width=True):
                st.session_state.confirm_clear = True
                st.rerun()
            
    
    # --- Main Chat Interface ---
    st.title("Intelligent Conversation Assistant")
    st.caption("You can ask any questions about your uploaded documents")
    
    # If no messages, show welcome message
    if not st.session_state.messages:
        st.markdown("""
        <div style="background-color: #e8f4f8; padding: 20px; border-radius: 10px; margin-bottom: 20px; border: 1px solid #d1eaed;">
            <h4>Welcome!</h4>
            <p>Please upload your documents (PDF, Word, TXT, etc.) in the sidebar, then ask questions here.</p>
            <p>For example:</p>
            <ul>
                <li>"What are the key points in this document?"</li>
                <li>"Summarize the chapter about XXX"</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

    # Display message history
    for message in st.session_state.messages:
        role = message.get("role", "")
        content = message.get("content", "")
        
        if role == "user":
            with st.chat_message("user"):
                st.markdown(content)
        
        elif role == "assistant":
            with st.chat_message("assistant"):
                st.markdown(content)
                
                # Display reference sources
                metadata = message.get("metadata", {})
                if "reference_files" in metadata and metadata["reference_files"]:
                    files = metadata["reference_files"]
                    if files:
                        st.markdown(
                            f"""
                            <div class="references-box">
                                <b>References:</b><br>
                                {"<br>".join([f"• {f}" for f in files])}
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )
    
    
    # Chat input processing
    if prompt := st.chat_input("Enter your question..."):
        # 1. Display user input
        with st.chat_message("user"):
            st.markdown(prompt)
        
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "timestamp": datetime.now().isoformat()
        })
        
        if "chatbot" not in st.session_state or st.session_state.chatbot is None:
            st.error("System not initialized. Please refresh the page.")
            return
        
        # 2. Generate response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response_buffer = ""
            
            try:
                # Progress indicator
                # with st.spinner("Analyzing documents and generating response..."):
                
                # Stream generation
                print(f"prompt: {prompt}")
                stream_config = {"configurable": {"thread_id": st.session_state.thread_id}}
                
                for chunk in st.session_state.chatbot.agent.stream(
                    {"messages": [{"role": "user", "content": prompt}]},
                    config=stream_config,
                    stream_mode="updates"
                ):
                    # Process model messages
                    if "model" in chunk and "messages" in chunk["model"]:
                        messages = chunk["model"]["messages"]
                        if messages:
                            last = messages[0]
                            
                            # Text content
                            if hasattr(last, "content"):
                                if isinstance(last.content, list):
                                    for item in last.content:
                                        if item.get("type") == "text":
                                            full_response_buffer += item.get("text", "")
                                            message_placeholder.markdown(full_response_buffer + "▌")
                                elif isinstance(last.content, str):
                                    full_response_buffer += last.content
                                    message_placeholder.markdown(full_response_buffer + "▌")
                            
                            # Tool call hints (optional, not as final reply)
                            if hasattr(last, "tool_calls") and last.tool_calls:
                                names = [tc.get("name", "") for tc in last.tool_calls]
                                # Here you can choose whether to display the tool call process
                                # For a cleaner interface, you can choose to only print in the backend or display temporary status
                                # message_placeholder.markdown(full_response_buffer + f"\n\n*Searching knowledge base: {', '.join(names)}...*")

                    # Process tools messages
                    elif "tools" in chunk and "messages" in chunk["tools"]:
                        messages = chunk["tools"]["messages"]
                        if messages:
                            last = messages[0]
                            if hasattr(last, "content") and last.content:
                                # Tool return content is usually for the model to see, direct display may not look good, decide whether to append based on needs
                                full_response_buffer += last.content
                                message_placeholder.markdown(full_response_buffer + "▌")
                
                # Remove cursor
                message_placeholder.markdown(full_response_buffer)
                
                # Get reference sources
                retrieved_docs = st.session_state.chatbot.retrieval_tool.get_last_docs()
                reference_files = []
                
                if retrieved_docs:
                    displayed_files = set()
                    for doc in retrieved_docs:
                        file_name = doc.metadata.get("file_name", "Unknown document")
                        if file_name not in displayed_files:
                            displayed_files.add(file_name)
                            reference_files.append(file_name)
                    
                    if reference_files:
                        st.markdown(
                            f"""
                            <div class="references-box">
                                <b>References:</b><br>
                                {"<br>".join([f"• {f}" for f in reference_files])}
                            </div>
                            """, 
                            unsafe_allow_html=True
                        )

                # Save to history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": full_response_buffer,
                    "timestamp": datetime.now().isoformat(),
                    "metadata": {"reference_files": reference_files}
                })
                
            except Exception as e:
                st.error(f"Error generating response: {e}")
                import traceback
                st.error(traceback.format_exc())

    # --- Footer ---
    st.markdown("""
    <div class="footer">
        AI Knowledge Base Assistant © 2025 | Powered by LangChain & Streamlit
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
