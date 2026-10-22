import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Override with GEMINI_EMBEDDING_MODEL in .env. Changing it requires re-processing the PDFs.
DEFAULT_EMBEDDING_MODEL = "models/gemini-embedding-001"


def get_embeddings() -> GoogleGenerativeAIEmbeddings:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "GOOGLE_API_KEY is not set. "
            "Add it to your .env file: GOOGLE_API_KEY=your_key_here"
        )

    embeddings = GoogleGenerativeAIEmbeddings(
        model=os.getenv("GEMINI_EMBEDDING_MODEL", DEFAULT_EMBEDDING_MODEL),
        google_api_key=api_key,
    )

    return embeddings
