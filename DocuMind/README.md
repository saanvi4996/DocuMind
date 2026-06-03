# 🧠 DocuMind — AI Research Assistant

Chat with your research papers using Retrieval-Augmented Generation (RAG), powered by Google Gemini and FAISS.

---

## Features

- 📄 Upload multiple PDFs simultaneously
- 💬 Conversational chat with document context
- 🔍 Semantic search via FAISS vector database
- 📝 One-click paper summarisation
- ⚖️ Multi-paper comparison
- 📌 Page-level citations on every answer
- 🧠 Session-based chat history
- 🔑 Secure API key management via `.env`

---

## Architecture

```
Upload PDF(s)
     ↓
Extract Text (PyPDF)
     ↓
Chunk Text (RecursiveCharacterTextSplitter)
     ↓
Generate Embeddings (Gemini embedding-001)
     ↓
Store in FAISS Vector DB
     ↓
User Query → Semantic Retrieval (top-k chunks)
     ↓
LLM Receives Context + Prompt (Gemini 1.5 Flash)
     ↓
Grounded Answer + Page Citations
```

---

## Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.9+ | Core language |
| LangChain | RAG orchestration |
| Streamlit | Frontend UI |
| FAISS | Vector database |
| Google Gemini API | LLM + Embeddings |
| PyPDF | PDF text extraction |
| python-dotenv | API key security |

---

## Setup

### 1. Clone & create virtual environment

```bash
git clone <repo-url>
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
```

### 3. Add your API key

```bash
cp .env .env.local  # optional, or just edit .env directly
```

Edit `.env`:

```env
GOOGLE_API_KEY=your_google_api_key_here
```

Get your key at [Google AI Studio](https://aistudio.google.com).

### 4. Run the app

```bash
streamlit run app.py
```

---

## Project Structure

```
DocuMind/
├── app.py                  # Streamlit frontend & orchestration
├── .env                    # API keys (never commit this)
├── requirements.txt
├── README.md
│
├── rag/
│   ├── loader.py           # PDF loading
│   ├── chunker.py          # Text chunking
│   ├── embeddings.py       # Embedding model
│   ├── retriever.py        # FAISS vector store & retriever
│   ├── chain.py            # LLM + RetrievalQA chain
│   └── prompts.py          # Prompt templates
│
├── utils/
│   └── helpers.py          # File handling, citation formatting
│
├── data/                   # (optional) store PDFs locally
└── vectorstore/            # (optional) persist FAISS index
```

---

## Deployment

### Streamlit Community Cloud (free)

1. Push to GitHub (ensure `.env` is in `.gitignore`)
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your repo
4. Add `GOOGLE_API_KEY` under **Secrets**
5. Deploy

---

