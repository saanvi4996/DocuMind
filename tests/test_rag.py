"""Offline tests: fake embeddings and a fake LLM, no API key or network needed."""

import pytest
from langchain_core.documents import Document
from langchain_core.embeddings import DeterministicFakeEmbedding
from langchain_core.language_models.fake_chat_models import FakeListChatModel

from rag.chain import create_qa_chain, format_docs
from rag.chunker import split_documents
from rag.loader import load_pdf
from rag.retriever import create_vectorstore, get_retriever
from utils.helpers import format_citations


def make_docs():
    return [
        Document(page_content="Transformers use self-attention. " * 60, metadata={"source": "a.pdf", "page": 0}),
        Document(page_content="FAISS indexes dense vectors. " * 60, metadata={"source": "b.pdf", "page": 2}),
    ]


def test_split_documents_keeps_metadata_and_size():
    chunks = split_documents(make_docs(), chunk_size=200, chunk_overlap=20)
    assert len(chunks) > 2
    assert all(len(c.page_content) <= 200 for c in chunks)
    assert {c.metadata["source"] for c in chunks} == {"a.pdf", "b.pdf"}


def test_split_documents_rejects_empty():
    with pytest.raises(ValueError):
        split_documents([])


def test_load_pdf_validates_path(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_pdf(str(tmp_path / "missing.pdf"))
    txt = tmp_path / "notes.txt"
    txt.write_text("hi")
    with pytest.raises(ValueError):
        load_pdf(str(txt))


def test_format_citations_dedupes_and_handles_missing_page():
    docs = [
        Document(page_content="x", metadata={"source": "/tmp/a.pdf", "page": 1}),
        Document(page_content="y", metadata={"source": "/tmp/a.pdf", "page": 1}),
        Document(page_content="z", metadata={"source": "b.pdf"}),
    ]
    assert format_citations(docs) == [("a.pdf", 2), ("b.pdf", 0)]


def test_format_docs_labels_source_and_page():
    text = format_docs(make_docs())
    assert "[a.pdf, page 1]" in text and "[b.pdf, page 3]" in text


def test_qa_chain_retrieves_once_and_returns_sources():
    chunks = split_documents(make_docs(), chunk_size=200, chunk_overlap=20)
    vectorstore = create_vectorstore(chunks, DeterministicFakeEmbedding(size=32))
    retriever = get_retriever(vectorstore, k=3)

    calls = []
    original = retriever.invoke
    retriever.__dict__["invoke"] = lambda q, *a, **kw: calls.append(q) or original(q, *a, **kw)

    chain = create_qa_chain(retriever, llm=FakeListChatModel(responses=["fake answer"]))
    result = chain.invoke({"query": "What is FAISS?"})

    assert result["result"] == "fake answer"
    assert len(result["source_documents"]) == 3
    assert calls == ["What is FAISS?"]
