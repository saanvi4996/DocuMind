"""LLM chain module."""

import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from rag.prompts import QA_PROMPT_TEMPLATE


def get_llm(temperature: float = 0.3):
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("GOOGLE_API_KEY is not set.")
    return ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=temperature,
        google_api_key=api_key,
    )


def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


class QAChain:
    def __init__(self, retriever, prompt_template: str = QA_PROMPT_TEMPLATE):
        self.retriever = retriever
        llm = get_llm()
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"],
        )
        self._chain = (
            {
                "context": retriever | format_docs,
                "question": RunnablePassthrough(),
            }
            | prompt
            | llm
            | StrOutputParser()
        )

    def invoke(self, inputs: dict) -> dict:
        query = inputs["query"]
        source_docs = self.retriever.invoke(query)
        result = self._chain.invoke(query)
        return {
            "result": result,
            "source_documents": source_docs,
        }


def create_qa_chain(retriever, prompt_template: str = QA_PROMPT_TEMPLATE) -> QAChain:
    return QAChain(retriever, prompt_template)