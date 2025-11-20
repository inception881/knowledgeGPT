<div align="center">
  <img src="https://i.imgur.com/XR70Ysm.png" alt="KnowledgeGPT Logo" width="220">
  <h1>✨ KnowledgeGPT ✨</h1>
  <p><strong>Your AI-powered knowledge assistant that brings documents to life</strong></p>
  
  <p>
    <a href="#-features"><img src="https://img.shields.io/badge/RAG-Powered-blueviolet?style=for-the-badge" alt="RAG"></a>
    <a href="#-quick-start"><img src="https://img.shields.io/badge/Easy-Setup-success?style=for-the-badge" alt="Setup"></a>
    <a href="#-technology-stack"><img src="https://img.shields.io/badge/Claude-AI-ff69b4?style=for-the-badge" alt="Claude"></a>
    <a href="https://streamlit.io/"><img src="https://img.shields.io/badge/Built_with-Streamlit-FF4B4B?style=for-the-badge" alt="Streamlit"></a>
  </p>
  
  <p>
    <img src="https://img.shields.io/badge/LangChain-0.1.4-blue" alt="LangChain">
    <img src="https://img.shields.io/badge/Python-3.9+-green" alt="Python">
    <img src="https://img.shields.io/badge/License-MIT-yellow" alt="License">
    <img src="https://img.shields.io/badge/Streamlit-1.31.0-red" alt="Streamlit">
  </p>
</div>

<hr>

<p align="center">
  <img src="https://i.imgur.com/XR70Ysm.png" alt="KnowledgeGPT Demo" width="80%">
</p>

## 🚀 Introduction

**KnowledgeGPT** transforms how you interact with your documents. Using cutting-edge Retrieval-Augmented Generation (RAG) technology, it allows you to have natural conversations with your PDFs, Word documents, and text files. Simply upload your documents and start asking questions in plain language to receive accurate, context-aware responses based on your content.

> 💡 **Perfect for researchers, students, professionals, and knowledge workers who need to quickly extract insights from large documents.**

<details>
<summary>💫 Why KnowledgeGPT?</summary>

- **Save Hours of Reading**: Extract key information without reading entire documents
- **Discover Hidden Insights**: Uncover connections across multiple documents
- **Enhance Learning**: Interact with complex material through natural conversation
- **Boost Productivity**: Get answers to specific questions instantly
- **Privacy First**: Your documents never leave your machine - no data harvesting

</details>

## ✨ Features

<table>
  <tr>
    <td width="50%">
      <h3>📄 Universal Document Support</h3>
      <p>Seamlessly process PDFs, Word documents, TXT files, and Markdown with intelligent text extraction that preserves document structure.</p>
    </td>
    <td width="50%">
      <h3>🧠 Advanced RAG Architecture</h3>
      <p>Utilizes state-of-the-art retrieval techniques with FAISS vector search for lightning-fast, highly relevant document retrieval.</p>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>💬 Conversational Memory</h3>
      <p>Maintains context across your conversation with both short-term session memory and long-term persistent memory for more natural interactions.</p>
    </td>
    <td width="50%">
      <h3>🔍 Source Attribution</h3>
      <p>Every answer includes references to the specific documents and sections used, ensuring transparency and verifiability.</p>
    </td>
  </tr>
  <tr>
    <td width="50%">
      <h3>⚡ Real-time Responses</h3>
      <p>Streaming response generation provides immediate feedback with token-by-token display for a fluid chat experience.</p>
    </td>
    <td width="50%">
      <h3>🛠️ Customizable Experience</h3>
      <p>Fine-tune retrieval parameters, model behavior, and interface settings to match your specific use case and preferences.</p>
    </td>
  </tr>
</table>

## 🎬 Live Demo

<div align="center">
  <p><i>Upload documents and chat with them instantly</i></p>
  <img src="https://i.imgur.com/XR70Ysm.png" alt="KnowledgeGPT Demo" width="80%">
</div>

## 🛠️ Technology Stack

<table>
  <tr>
    <td align="center" width="20%">
      <img src="https://anthropic.com/images/icons/claude-icon.svg" width="60" height="60"/><br>
      <strong>Claude AI</strong><br>
      <small>Advanced reasoning</small>
    </td>
    <td align="center" width="20%">
      <img src="https://python.langchain.com/img/langchain_icon.svg" width="60" height="60"/><br>
      <strong>LangChain</strong><br>
      <small>RAG framework</small>
    </td>
    <td align="center" width="20%">
      <img src="https://raw.githubusercontent.com/facebookresearch/faiss/main/faiss-logo.svg" width="60" height="60"/><br>
      <strong>FAISS</strong><br>
      <small>Vector search</small>
    </td>
    <td align="center" width="20%">
      <img src="https://streamlit.io/images/brand/streamlit-mark-color.svg" width="60" height="60"/><br>
      <strong>Streamlit</strong><br>
      <small>Web interface</small>
    </td>
    <td align="center" width="20%">
      <img src="https://www.svgrepo.com/show/374144/typescript.svg" width="60" height="60"/><br>
      <strong>Qwen</strong><br>
      <small>Embeddings</small>
    </td>
  </tr>
</table>

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- API keys for Claude and OpenAI/Qwen Embeddings

### Installation

<details>
<summary>📋 Step-by-step instructions</summary>

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/knowledgegpt.git
cd knowledgegpt
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set up environment variables**

Create a `.env` file in the root directory:

```
ANTHROPIC_LLM_API_KEY=your_anthropic_api_key
OPENAI_EMBEDDING_API_KEY=your_openai_api_key
```

4. **Run the application**

```bash
streamlit run app/web_chatbot.py
```

5. **Access the web interface**

Open your browser and go to `http://localhost:8501`

</details>

<details>
<summary>🐳 Docker installation (alternative)</summary>

```bash
# Build the Docker image
docker build -t knowledgegpt .

# Run the container
docker run -p 8501:8501 --env-file .env knowledgegpt
```

</details>

## 📚 Usage Guide

<table>
  <tr>
    <td width="33%">
      <h3>1️⃣ Upload Documents</h3>
      <p>Click "Upload New Document" in the sidebar and select your files (PDF, DOCX, TXT, MD).</p>
      <img src="https://i.imgur.com/XR70Ysm.png" width="100%" alt="Upload Documents">
    </td>
    <td width="33%">
      <h3>2️⃣ Ask Questions</h3>
      <p>Type your questions in natural language in the chat input field at the bottom.</p>
      <img src="https://i.imgur.com/XR70Ysm.png" width="100%" alt="Ask Questions">
    </td>
    <td width="33%">
      <h3>3️⃣ Get Insights</h3>
      <p>Receive detailed answers with reference sources from your documents.</p>
      <img src="https://i.imgur.com/XR70Ysm.png" width="100%" alt="Get Insights">
    </td>
  </tr>
</table>

### 💡 Example Questions

- "What are the key points in the executive summary?"
- "Summarize the methodology section in bullet points"
- "Compare the financial results from 2023 to 2024"
- "What did the author say about climate change impacts?"
- "Extract all tables from the document and format them nicely"

## 🧩 Project Architecture

```
knowledgegpt/
├── app/                          # Application layer
│   └── web_chatbot.py            # Streamlit web interface
├── src/                          # Core source code
│   ├── chains/                   # LangChain chains
│   │   └── faiss_conversational_chain.py  # Main RAG chain
│   ├── chat_model/               # LLM integration
│   ├── embedding/                # Vector embeddings
│   ├── loaders/                  # Document loaders
│   ├── memory/                   # Conversation memory
│   │   └── long_term_memory.py   # Persistent memory
│   ├── prompts/                  # Prompt templates
│   ├── utils/                    # Utility functions
│   ├── vectorstores/             # Vector store implementations
│   └── config.py                 # Configuration
├── data/                         # Data directory
│   ├── documents/                # Document storage
│   ├── faiss_index/              # FAISS vector indices
│   └── long_term_memory/         # Persistent memory storage
├── requirements.txt              # Dependencies
└── README.md                     # Documentation
```

## ⚙️ Advanced Configuration

Fine-tune KnowledgeGPT by adjusting parameters in `src/config.py`:

<details>
<summary>🔧 Available Configuration Options</summary>

```python
# LLM configuration
ANTHROPIC_MODEL_NAME = "claude-3-7-sonnet"  # Model selection
TEMPERATURE = 0.7                           # Response creativity (0.0-1.0)
MAX_TOKENS = 2000                           # Maximum response length

# Retrieval parameters
TOP_K = 5                                   # Number of chunks to retrieve
SIMILARITY_THRESHOLD = 0.7                  # Minimum relevance score

# Chunking parameters
CHUNK_SIZE = 1000                           # Text chunk size
CHUNK_OVERLAP = 200                         # Overlap between chunks

# Memory configuration
MAX_HISTORY_LENGTH = 20                     # Conversation turns to remember
```

</details>

## 🔮 Roadmap

<table>
  <tr>
    <td>✅ Multi-document support</td>
    <td>✅ Source attribution</td>
    <td>✅ Conversational memory</td>
  </tr>
  <tr>
    <td>🔜 Multi-language support</td>
    <td>🔜 Document comparison</td>
    <td>🔜 Custom knowledge bases</td>
  </tr>
  <tr>
    <td>🔜 Image/chart analysis</td>
    <td>🔜 Data visualization</td>
    <td>🔜 Mobile app</td>
  </tr>
</table>

## ❓ FAQ

<details>
<summary><b>What types of documents can I use?</b></summary>
KnowledgeGPT supports PDF, Word documents (.docx), plain text files (.txt), and Markdown (.md) files.
</details>

<details>
<summary><b>Is my data secure?</b></summary>
Yes! Your documents are processed locally on your machine. Only the necessary chunks are sent to the LLM API for generating responses, and no data is stored on external servers.
</details>

<details>
<summary><b>How accurate are the responses?</b></summary>
KnowledgeGPT uses advanced RAG techniques to retrieve the most relevant information from your documents. The accuracy depends on the quality of your documents and the specificity of your questions. The system always provides source references so you can verify the information.
</details>

<details>
<summary><b>Can I use a different LLM?</b></summary>
Yes, the system is designed to be model-agnostic. You can modify the configuration to use other LLMs like GPT-4, Llama, or Mistral by adjusting the settings in the config file.
</details>

<details>
<summary><b>How many documents can I upload?</b></summary>
There's no hard limit on the number of documents, but performance may decrease with very large document collections. For optimal performance, we recommend keeping your knowledge base under 1,000 pages total.
</details>

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

- [LangChain](https://python.langchain.com/) for the amazing RAG framework
- [Anthropic Claude](https://www.anthropic.com/claude) for the powerful LLM
- [FAISS](https://github.com/facebookresearch/faiss) for efficient vector search
- [Streamlit](https://streamlit.io/) for the easy-to-use web framework
- [Qwen](https://github.com/QwenLM/Qwen) for high-quality embeddings

---

<div align="center">
  <p>Built with 💙 for the knowledge seekers of the world</p>
  <p>
    <a href="https://github.com/yourusername/knowledgegpt/issues">Report Bug</a> •
    <a href="https://github.com/yourusername/knowledgegpt/issues">Request Feature</a> •
    <a href="https://github.com/yourusername/knowledgegpt/stargazers">Star Us</a>
  </p>
</div>
