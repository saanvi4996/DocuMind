"""Vector store and retriever module for DocuMind."""

from typing import List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.vectorstores import VectorStoreRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def create_vectorstore(
    chunks: List[Document],
    embeddings: GoogleGenerativeAIEmbeddings,
) -> FAISS:
    """
    Build a FAISS vector store from document chunks.

    Args:
        chunks:     List of chunked Document objects.
        embeddings: Embedding model to vectorise the chunks.

    Returns:
        FAISS vector store populated with embedded chunks.

    Raises:
        ValueError: If chunks list is empty.
    """
    if not chunks:
        raise ValueError("No chunks provided to build vector store.")

    vectorstore = FAISS.from_documents(
        documents=chunks,
        embedding=embeddings,
    )

    return vectorstore


def get_retriever(
    vectorstore: FAISS,
    k: int = 4,
) -> VectorStoreRetriever:
    """
    Create a similarity-based retriever from a FAISS vector store.

    Args:
        vectorstore: Populated FAISS vector store.
        k:           Number of top chunks to retrieve (default 4).

    Returns:
        VectorStoreRetriever configured for similarity search.
    """
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )

    return retriever
