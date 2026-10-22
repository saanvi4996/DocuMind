"""Utility helpers for DocuMind."""

import os
import tempfile
from typing import List, Tuple

import streamlit as st
from langchain_core.documents import Document


def save_uploaded_file(uploaded_file) -> str:
    """
    Save a Streamlit UploadedFile to a temporary path on disk.

    Args:
        uploaded_file: Streamlit UploadedFile object.

    Returns:
        Absolute path to the saved temporary file.
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        return tmp.name


def cleanup_temp_files(paths: List[str]) -> None:
    """
    Remove temporary files from disk.

    Args:
        paths: List of file paths to delete.
    """
    for path in paths:
        try:
            os.remove(path)
        except OSError:
            pass  # Already deleted or never existed


def format_citations(source_docs: List[Document]) -> List[Tuple[str, int]]:
    """
    Extract unique (source filename, page number) pairs from source documents.

    Args:
        source_docs: List of Document objects returned by the retriever.

    Returns:
        Deduplicated list of (source, page) tuples sorted by page number.
    """
    seen = set()
    citations = []

    for doc in source_docs:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page")
        # Convert 0-indexed to 1-indexed; 0 marks a chunk with no page number
        page = page + 1 if isinstance(page, int) else 0

        # Use just the filename, not the full temp path
        filename = os.path.basename(source)
        key = (filename, page)

        if key not in seen:
            seen.add(key)
            citations.append(key)

    citations.sort()
    return citations


def display_citations(source_docs: list) -> None:
    """Render source citations in Streamlit."""
    citations = format_citations(source_docs)

    if citations:
        with st.expander("📚 Sources", expanded=False):
            for filename, page in citations:
                page_label = f" — Page {page}" if page else ""
                st.markdown(f"📄 **{filename}**{page_label}")