# 🧠 DocuMind — AI Research Assistant

A RAG-based tool for querying research papers using Google Gemini and FAISS.
Upload your PDFs and ask questions — answers are grounded in your documents, not general knowledge.

---

## Features

- 📄 Upload multiple PDFs at once
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
