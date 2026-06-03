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
        page = doc.metadata.get("page", 0) + 1  # Convert 0-indexed to 1-indexed

        # Use just the filename, not the full temp path
        filename = os.path.basename(source)
        key = (filename, page)

        if key not in seen:
            seen.add(key)
            citations.append(key)

    citations.sort(key=lambda x: x[1])
    return citations


def display_citations(source_docs: list) -> None:
    """Render source citations in Streamlit."""
    import streamlit as st
    import os

    seen = set()
    lines = []
    for doc in source_docs:
        source = doc.metadata.get("source", "Unknown")
        page = doc.metadata.get("page", "?")
        filename = os.path.basename(source)
        key = (filename, page)
        if key not in seen:
            seen.add(key)
            lines.append(f"📄 **{filename}** — Page {int(page) + 1}")

    if lines:
        with st.expander("📚 Sources", expanded=False):
            for line in lines:
                st.markdown(line)