# Multi-Source RAG Web Application

A full-stack Retrieval-Augmented Generation (RAG) web application built with **Python Flask**, **LangChain**, **ChromaDB**, and **Groq LLM**. This application allows users to ingest and query content dynamically from three distinct sources: **YouTube Videos** (via transcripts), **PDF Documents**, and **Website URLs** through a modern, responsive HTML/CSS/JavaScript interface.

---

## 🌟 Key Features

* **🎥 YouTube Video RAG:** Extracts transcripts directly using `youtube-transcript-api`, splits text into context-aware chunks, embeds them locally, and answers specific user queries based on video content.
* **📄 PDF Document RAG:** Uses `PyPDFLoader` to parse uploaded PDFs, handles text segmentation, indexes documents into a local vector store, and provides precise answers with document context.
* **🌐 Website Scraping RAG:** Scrapes clean structural text (`h1`, `h2`, `h3`, `h4`, `p`, `li`) from any target website URL using `BeautifulSoup` and `requests` with browser-mimicking headers to bypass restrictions.
* **⚡ Blazing Fast Inference:** Powered by Groq API (`openai/gpt-oss-20b`) for ultra-low latency response generation.
* **🔍 Local Vector Storage:** Utilizes **ChromaDB** with **HuggingFace Embeddings** (`all-MiniLM-L6-v2`) for secure, local, persistent vector storage (`./chroma_db`) without requiring external database servers.
* **💬 Dual-Language Support:** Automatically matches the language of the user's query (English, Hindi, or Hinglish) while keeping answers strictly grounded in the ingested context.

---

## 🏗️ System Architecture & Tech Stack

```text
┌──────────────────────────────────────────────┐
│             HTML / CSS / JS UI               │
│  (Tabbed Dashboard & Real-Time Chat Box)     │
└──────────────────────┬───────────────────────┘
                       │ HTTP Fetch API (JSON / FormData)
                       ▼
┌──────────────────────────────────────────────┐
│           Python Flask Backend               │
│  - /process-youtube                          │
│  - /process-pdf                              │
│  - /process-web                              │
│  - /chat                                     │
└──────────┬───────────┬───────────┬───────────┘
           │           │           │
           ▼           ▼           ▼
     [YouTube API] [PyPDFLoader] [BeautifulSoup]
           │           │           │
           └─────►     ▼     ◄─────┘
               [Text Splitter]
                       │
                       ▼
         [HuggingFace Embeddings]
           (`all-MiniLM-L6-v2`)
                       │
                       ▼
          [ChromaDB Local Vector Store]
                       │
                       ▼
           [Groq LLM (`openai/gpt-oss-20b`)]
                       │
                       ▼
           [Contextual RAG Answer]



multisource_rag_web/
│
├── .env                    # Environment variables (Groq API Key)
├── app.py                  # Main Flask application and API routes
├── requirements.txt        # Project dependencies
│
├── utils/                  # Modular data ingestion loaders
│   ├── youtube_loader.py   # YouTube transcript extractor & chunker
│   ├── pdf_loader.py       # PDF loader and text processor
│   └── web_loader.py       # BeautifulSoup web scraper & cleaner
│
├── static/                 # Frontend assets
│   ├── css/
│   │   └── style.css       # Modern dark/light dashboard styles
│   └── js/
│       └── main.js         # Fetch API communication & chat UI handler
│
├── templates/              # HTML templates
│   └── index.html          # Main dashboard interface
│
├── uploads/                # Temporary storage for uploaded PDF files
└── chroma_db/              # Persistent local vector database storage




