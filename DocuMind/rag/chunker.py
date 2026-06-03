"""Text chunking module for DocuMind."""

from typing import List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


def split_documents(
    documents: List[Document],
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
) -> List[Document]:
    """
    Split documents into smaller overlapping chunks for retrieval.

    Args:
        documents:     List of Document objects to split.
        chunk_size:    Maximum number of characters per chunk (default 1000).
        chunk_overlap: Number of overlapping characters between chunks (default 200).

    Returns:
        List of chunked Document objects with preserved metadata.

    Raises:
        ValueError: If documents list is empty.
    """
    if not documents:
        raise ValueError("No documents provided for chunking.")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        # Split on paragraphs, sentences, words, then characters
        separators=["\n\n", "\n", ". ", " ", ""],
    )

    chunks = splitter.split_documents(documents)

    return chunks
