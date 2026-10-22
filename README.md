# 🧠 DocuMind — AI Research Assistant

A RAG (Retrieval-Augmented Generation) app for querying research papers with Google Gemini and FAISS.
Upload PDFs and ask questions. Answers are generated only from the retrieved passages of your documents and come with page-level citations.

---

## Features

- 📄 Upload multiple PDFs at once
- 🔍 Semantic search over chunks with a FAISS vector index (in memory, rebuilt per session)
- 💬 Question answering grounded in the retrieved context, with an explicit "not found" answer when the papers don't cover the question
- 📝 One-click structured summary (objective, method, findings, datasets, conclusions)
- ⚖️ Comparison across papers under fixed headings
- 📌 Source file and page citations under every answer
- 🔑 API key and model names configured through `.env`

---

## How it works

```
PDF(s) ──► PyPDF text extraction ──► RecursiveCharacterTextSplitter (1000 chars, 200 overlap)
       ──► Gemini embeddings (gemini-embedding-001) ──► FAISS index

Question ──► top-k similar chunks (k=4 for chat, k=12 for summary/compare)
         ──► prompt with chunks labelled [file, page] ──► Gemini Flash ──► answer + citations
```

Each question triggers one retrieval. The same chunks go into the prompt and the citation list, so the sources shown are exactly what the model saw.

---

## Tech stack

| Technology | Purpose |
|---|---|
| Python 3.11+ | Core language |
| LangChain (core, community, text-splitters) | Prompting, chunking, vector-store wrapper |
| Google Gemini API (`langchain-google-genai`) | LLM and embeddings |
| FAISS (`faiss-cpu`) | Vector similarity search |
| PyPDF | PDF text extraction |
| Streamlit | Web UI |
| pytest | Offline tests |

---

## Project structure

```
DocuMind/
├── app.py               # Streamlit UI: upload, chat, summarise, compare
├── rag/
│   ├── loader.py        # PDF → LangChain Documents (one per page)
│   ├── chunker.py       # overlapping text chunks
│   ├── embeddings.py    # Gemini embedding model
│   ├── retriever.py     # FAISS index + top-k retriever
│   ├── chain.py         # prompt → Gemini → answer, with source documents
│   └── prompts.py       # QA, summary and comparison prompts
├── utils/helpers.py     # temp-file handling, citation formatting
├── tests/               # offline tests (fake embeddings / fake LLM)
├── requirements.txt
└── .env.example
```

---

## Setup

### 1. Clone and create a virtual environment

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
```

### 3. Add your API key

Copy `.env.example` to `.env` and set your key:

```env
GOOGLE_API_KEY=your_key_here
```

Get a free key at [aistudio.google.com](https://aistudio.google.com). The free tier is rate-limited, so very large PDFs may take a while to embed.

Optional: `GEMINI_MODEL` (default `gemini-3.8-flash`) and `GEMINI_EMBEDDING_MODEL` (default `models/gemini-embedding-001`). Google retires model versions regularly, so check the [deprecations page](https://ai.google.dev/gemini-api/docs/deprecations) if requests start failing with "model not found".

### 4. Run

```bash
streamlit run app.py
```

---

## Usage

1. Open the app at `http://localhost:8501`
2. Upload one or more PDFs in the sidebar
3. Click **Process PDFs** and wait for indexing to finish
4. Type a question in the chat box
5. Use **Summarise Papers** or **Compare Papers** in the sidebar for bulk analysis

---

## Tests

```bash
pip install pytest
pytest
```

The tests run offline. They use LangChain's fake embeddings and fake chat model to check chunking, citation formatting, the single retrieval per query, and that the Streamlit app starts. They do not test Gemini's answer quality.

---

## Deployment (Streamlit Community Cloud)

1. Push the repository to GitHub.
2. At [share.streamlit.io](https://share.streamlit.io) choose **New app**, pick this repository and set the main file to `app.py`.
3. Under **Advanced settings → Secrets**, add:
   ```toml
   GOOGLE_API_KEY = "your_key_here"
   ```
   Streamlit exposes top-level secrets as environment variables, which is where the app reads the key from.

---

## Limitations

- The index lives in memory and is lost when the session ends. PDFs are re-embedded on every upload.
- Summarise and Compare see the 12 most relevant chunks, not every page, so very long papers are summarised partially.
- Scanned PDFs without a text layer produce no text (there is no OCR).
- `langchain-community`, used for the FAISS wrapper and the PDF loader, is being sunset upstream. It is pinned below 0.5 here.
