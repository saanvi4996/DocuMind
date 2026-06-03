# 🧠 DocuMind — AI Research Assistant

A RAG-based tool for querying research papers using Google Gemini and FAISS.
Upload your PDFs and ask questions — answers are grounded in your documents, not general knowledge.

---

## Features

- 📄 Upload and index multiple PDFs at once
- 🔍 Semantic search via FAISS vector database
- 💬 Question answering grounded in document context
- 📝 One-click summarisation of uploaded papers
- ⚖️ Side-by-side comparison across multiple papers
- 📌 Page-level source citations on answers
- 🔑 API key management via `.env`

---

## How it works
Upload PDF(s)
→
Extract text (PyPDF) → Chunk (RecursiveCharacterTextSplitter)
→
Embed chunks (Gemini gemini-embedding-001) → Store in FAISS
→
User query → Retrieve top-k relevant chunks
→
Gemini 2.0 Flash generates a grounded answer with citations

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.11 | Core language |
| LangChain | RAG orchestration |
| Streamlit | Frontend UI |
| FAISS | Vector database |
| Google Gemini API | LLM + Embeddings |
| PyPDF | PDF text extraction |
| python-dotenv | API key management |

---

## Setup

### 1. Clone and create virtual environment

```bash
git clone https://github.com/saanvi4996/DocuMind.git
cd DocuMind
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
pip install langchain-text-splitters
```

### 3. Add your API key

Copy `.env.example` to `.env` and add your key:

```env
GOOGLE_API_KEY=your_key_here
```

Get a free key at [aistudio.google.com](https://aistudio.google.com).

> **Note:** The free tier has rate limits. For regular use, enable billing on your Google AI account.

### 4. Run

```bash
streamlit run app.py
```

---

## Usage

1. Open the app at `http://localhost:8501`
2. Upload one or more PDFs in the sidebar
3. Click **Process PDFs** and wait for indexing to complete
4. Type a question in the chat box
5. Use **Summarise Papers** or **Compare Papers** in the sidebar for bulk analysis

---

## Project Structure
DocuMind/
├── app.py                  # Streamlit UI and orchestration
├── .env                    # API key (never commit this)
├── .env.example            # Template for new users
├── requirements.txt
│
├── rag/
│   ├── loader.py           # PDF loading
│   ├── chunker.py          # Text chunking
│   ├── embeddings.py       # Gemini embeddings
│   ├── retriever.py        # FAISS vector store
│   ├── chain.py            # LLM chain (LCEL)
│   └── prompts.py          # Prompt templates
│
└── utils/
└── helpers.py          # File handling and citation formatting

---

## Known Limitations

- No persistent memory between questions — each answer is independent
- Free tier Gemini API has rate limits (100 requests/minute, daily cap)
- Large PDFs take longer to process and use more quota
- Vector store is in-memory only — reprocessing required on each session

---

## Deployment

1. Push to GitHub (confirm `.env` is in `.gitignore`)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Set main file path to `DocuMind/app.py`
5. Add `GOOGLE_API_KEY` under **Secrets**
6. Click Deploy

---
