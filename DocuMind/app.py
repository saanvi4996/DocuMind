import os
import streamlit as st
from dotenv import load_dotenv
from rag.loader import load_pdf
from rag.chunker import split_documents
from rag.embeddings import get_embeddings
from rag.retriever import create_vectorstore, get_retriever
from rag.chain import create_qa_chain
from rag.prompts import SUMMARY_PROMPT_TEMPLATE, COMPARISON_PROMPT_TEMPLATE
from utils.helpers import save_uploaded_file, cleanup_temp_files, display_citations

load_dotenv()

st.set_page_config(page_title="DocuMind", page_icon="🧠", layout="wide")
st.title("🧠 DocuMind")
st.caption("Chat with research papers using Retrieval-Augmented Generation (RAG)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None
if "retriever" not in st.session_state:
    st.session_state.retriever = None
if "docs_loaded" not in st.session_state:
    st.session_state.docs_loaded = False
if "temp_paths" not in st.session_state:
    st.session_state.temp_paths = []

with st.sidebar:
    st.header("📂 Upload Papers")
    uploaded_files = st.file_uploader(
        "Choose PDF files",
        type="pdf",
        accept_multiple_files=True,
    )
    process_btn = st.button("⚙️ Process PDFs", use_container_width=True)
    st.divider()
    st.header("🛠️ Tools")
    summarise_btn = st.button("📝 Summarise Papers", use_container_width=True)
    compare_btn = st.button("⚖️ Compare Papers", use_container_width=True)
    st.divider()
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.chat_history = []
        st.rerun()

if process_btn and uploaded_files:
    temp_paths = []
    with st.spinner("Reading and processing PDFs…"):
        try:
            all_documents = []
            for uf in uploaded_files:
                path = save_uploaded_file(uf)
                temp_paths.append(path)
                docs = load_pdf(path)
                for doc in docs:
                    doc.metadata["source"] = uf.name
                all_documents.extend(docs)
            st.session_state.temp_paths = temp_paths

            chunks = split_documents(all_documents)
            embeddings = get_embeddings()
            vectorstore = create_vectorstore(chunks, embeddings)
            retriever = get_retriever(vectorstore)
            qa_chain = create_qa_chain(retriever)

            st.session_state.retriever = retriever
            st.session_state.qa_chain = qa_chain
            st.session_state.docs_loaded = True
            st.session_state.chat_history = []

            st.success(f"✅ Processed {len(uploaded_files)} PDF(s) → {len(all_documents)} pages → {len(chunks)} chunks.")

        except EnvironmentError as e:
            st.error(f"🔑 API Key Error: {e}")
        except Exception as e:
            st.error(f"❌ Error: {e}")
        finally:
            cleanup_temp_files(temp_paths)

for role, message in st.session_state.chat_history:
    st.chat_message(role).write(message)

if st.session_state.docs_loaded:
    user_question = st.chat_input("Ask a question about your papers…")
else:
    user_question = st.chat_input("Upload and process PDFs first…", disabled=True)

if user_question and st.session_state.qa_chain:
    st.chat_message("user").write(user_question)
    st.session_state.chat_history.append(("user", user_question))

    with st.spinner("Thinking…"):
        try:
            result = st.session_state.qa_chain.invoke({"query": user_question})
            answer = result.get("result", "No answer generated.")
            source_docs = result.get("source_documents", [])
        except Exception as e:
            answer = f"An error occurred: {e}"
            source_docs = []

    st.chat_message("assistant").write(answer)
    st.session_state.chat_history.append(("assistant", answer))
    if source_docs:
        display_citations(source_docs)

if summarise_btn:
    if not st.session_state.docs_loaded:
        st.warning("Please upload and process PDFs first.")
    else:
        with st.spinner("Generating summary…"):
            try:
                chain = create_qa_chain(st.session_state.retriever, prompt_template=SUMMARY_PROMPT_TEMPLATE)
                result = chain.invoke({"query": "Provide a detailed structured summary of all uploaded research papers."})
                summary = result.get("result", "No summary generated.")
                source_docs = result.get("source_documents", [])
                with st.expander("📝 Paper Summary", expanded=True):
                    st.write(summary)
                    if source_docs:
                        display_citations(source_docs)
            except Exception as e:
                st.error(f"❌ Summarisation error: {e}")

if compare_btn:
    if not st.session_state.docs_loaded:
        st.warning("Please upload and process PDFs first.")
    else:
        with st.spinner("Comparing papers…"):
            try:
                chain = create_qa_chain(st.session_state.retriever, prompt_template=COMPARISON_PROMPT_TEMPLATE)
                result = chain.invoke({"query": "Compare all uploaded research papers across objectives, methodology, datasets, results, and conclusions."})
                comparison = result.get("result", "No comparison generated.")
                source_docs = result.get("source_documents", [])
                with st.expander("⚖️ Paper Comparison", expanded=True):
                    st.write(comparison)
                    if source_docs:
                        display_citations(source_docs)
            except Exception as e:
                st.error(f"❌ Comparison error: {e}")