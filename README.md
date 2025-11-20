# ✨ KnowledgeGPT ✨

**Your AI-powered knowledge assistant that brings documents to life**

![RAG](https://img.shields.io/badge/RAG-Powered-blueviolet?style=for-the-badge)
![Setup](https://img.shields.io/badge/Easy-Setup-success?style=for-the-badge)
![Claude](https://img.shields.io/badge/Claude-AI-ff69b4?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Built_with-Streamlit-FF4B4B?style=for-the-badge)

![LangChain](https://img.shields.io/badge/LangChain-0.1.4-blue)
![Python](https://img.shields.io/badge/Python-3.9+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31.0-red)

---

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

### 📄 Universal Document Support
Seamlessly process PDFs, Word documents, TXT files, and Markdown with intelligent text extraction that preserves document structure.

### 🧠 Advanced RAG Architecture
Utilizes state-of-the-art retrieval techniques with FAISS vector search for lightning-fast, highly relevant document retrieval.

### 💬 Conversational Memory
Maintains context across your conversation with both short-term session memory and long-term persistent memory for more natural interactions.

### 🔍 Source Attribution
Every answer includes references to the specific documents and sections used, ensuring transparency and verifiability.

### ⚡ Real-time Responses
Streaming response generation provides immediate feedback with token-by-token display for a fluid chat experience.

### 🛠️ Customizable Experience
Fine-tune retrieval parameters, model behavior, and interface settings to match your specific use case and preferences.

## 🛠️ Technology Stack

| 🤖 Claude AI | 🔗 LangChain | 🔎 FAISS | 🌐 Streamlit | 📊 Qwen |
|:---:|:---:|:---:|:---:|:---:|
| Advanced reasoning | RAG framework | Vector search | Web interface | Embeddings |

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- API keys for Claude and OpenAI/Qwen Embeddings

### Installation

<details>
<summary>📋 Step-by-step instructions</summary>

**1. Clone the repository**

```bash
git clone https://github.com/yourusername/knowledgegpt.git
cd knowledgegpt
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Set up environment variables**

Create a `.env` file in the root directory:

```
ANTHROPIC_LLM_API_KEY=your_anthropic_api_key
OPENAI_EMBEDDING_API_KEY=your_openai_api_key
```

**4. Run the application**

```bash
streamlit run app/web_chatbot.py
```

**5. Access the web interface**

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

### 1️⃣ Upload Documents
Click "Upload New Document" in the sidebar and select your files (PDF, DOCX, TXT, MD).

### 2️⃣ Ask Questions
Type your questions in natural language in the chat input field at the bottom.

### 3️⃣ Get Insights
Receive detailed answers with reference sources from your documents.

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

| Current Features | Coming Soon | Future Plans |
|:---|:---|:---|
| ✅ Multi-document support | 🔜 Multi-language support | 🔜 Image/chart analysis |
| ✅ Source attribution | 🔜 Document comparison | 🔜 Data visualization |
| ✅ Conversational memory | 🔜 Custom knowledge bases | 🔜 Mobile app |

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

**Built with 💙 for the knowledge seekers of the world**

[Report Bug](https://github.com/yourusername/knowledgegpt/issues) • [Request Feature](https://github.com/yourusername/knowledgegpt/issues) • [Star Us](https://github.com/yourusername/knowledgegpt/stargazers)
