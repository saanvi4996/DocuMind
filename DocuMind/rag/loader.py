"""PDF loading module for DocuMind."""

import os
from typing import List

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def load_pdf(file_path: str) -> List[Document]:
    """
    Load a PDF file and return a list of Document objects.

    Args:
        file_path: Absolute path to the PDF file.

    Returns:
        List of Document objects with page_content and metadata.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
        ValueError: If the file is not a PDF.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"PDF not found: {file_path}")

    if not file_path.lower().endswith(".pdf"):
        raise ValueError(f"File must be a PDF: {file_path}")

    loader = PyPDFLoader(file_path)
    documents = loader.load()

    return documents


def load_multiple_pdfs(file_paths: List[str]) -> List[Document]:
    """
    Load multiple PDF files and combine into one document list.

    Args:
        file_paths: List of absolute paths to PDF files.

    Returns:
        Combined list of Document objects from all PDFs.
    """
    all_documents: List[Document] = []

    for path in file_paths:
        docs = load_pdf(path)
        all_documents.extend(docs)

    return all_documents
