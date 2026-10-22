"""LLM chain module."""

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from rag.prompts import QA_PROMPT_TEMPLATE

# Override with GEMINI_MODEL in .env when Google retires a model version.
DEFAULT_LLM_MODEL = "gemini-3.8-flash"


def get_llm(temperature: float = 0.3):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_API_KEY is not set.")
    return ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_MODEL", DEFAULT_LLM_MODEL),
        temperature=temperature,
        google_api_key=api_key,
    )


def format_docs(docs) -> str:
    """Join chunks, tagging each with its source file and page so the LLM can cite them."""
    parts = []
    for doc in docs:
        source = os.path.basename(doc.metadata.get("source", "Unknown"))
        page = doc.metadata.get("page")
        label = f"{source}, page {page + 1}" if isinstance(page, int) else source
        parts.append(f"[{label}]\n{doc.page_content}")
    return "\n\n".join(parts)


class QAChain:
    def __init__(self, retriever, prompt_template: str = QA_PROMPT_TEMPLATE, llm=None):
        self.retriever = retriever
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"],
        )
        self._chain = prompt | (llm or get_llm()) | StrOutputParser()

    def invoke(self, inputs: dict) -> dict:
        query = inputs["query"]
        # Retrieve once and reuse the same chunks for the prompt and the citations.
        source_docs = self.retriever.invoke(query)
        result = self._chain.invoke({
            "context": format_docs(source_docs),
            "question": query,
        })
        return {
            "result": result,
            "source_documents": source_docs,
        }


def create_qa_chain(retriever, prompt_template: str = QA_PROMPT_TEMPLATE, llm=None) -> QAChain:
    return QAChain(retriever, prompt_template, llm)
