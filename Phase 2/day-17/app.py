# Program: PDF RAG Chatbot — Production
# Topic: RAG + Streamlit Deployment
# Phase: 2 | Day: 17
# Concept: Deploy AI app on Hugging Face


import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
import tempfile
import time

# Page Config
st.set_page_config(
    page_title="PDF RAG Chatbot",
    page_icon="📄",
    layout="centered"
)

st.title("📄 PDF RAG Chatbot")
st.markdown("** Upload a PDF and ask questions! **")
st.markdown("* Built by Janak Gajjar *")
st.divider()

# Initialize Models
@st.cache_resource
def init_models():
    api_key = os.getenv("GEMINI_API_KEY")
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=api_key,
        temperature=0.3
    )
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=api_key
    )
    return llm, embeddings

llm, embeddings = init_models()

# Process PDF
def process_pdf(pdf_file):
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".pdf"
    ) as tmp:
        tmp.write(pdf_file.getvalue())
        tmp_path = tmp.name

    loader = PyPDFLoader(tmp_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(documents)
    os.unlink(tmp_path)

    # Batch embedding
    batch_size = 5
    processed = []
    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        processed.extend(batch)
        time.sleep(2)

    vectorstore = FAISS.from_documents(processed, embeddings)
    return vectorstore, len(documents), len(chunks)

# Get Answer
def get_answer(vectorstore, question):
    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )

    rag_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""You are a helpful AI assistant.
Use the context below to answer the question.
If answer not in context, say: 
"I couldn't find that in the PDF."

Context:
{context}

Question: {question}

Answer clearly and concisely:"""
    )

    def format_docs(docs):
        return "\n\n".join(
            doc.page_content for doc in docs
        )

    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | rag_prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain.invoke(question)

# Sidebar
with st.sidebar:
    st.header("📁 Upload PDF")
    uploaded_file = st.file_uploader(
        "Choose PDF", type="pdf"
    )

    if uploaded_file:
        st.success(f"✅ {uploaded_file.name}")
        with st.spinner("Processing PDF..."):
            vs, pages, chunks = process_pdf(uploaded_file)
            st.session_state.vectorstore = vs
        st.info(f"📄 Pages: {pages}")
        st.info(f"🔢 Chunks: {chunks}")
        st.success("Ready!")

    st.divider()
    st.markdown("**Built with:**")
    st.markdown("🔗 LangChain")
    st.markdown("🤖 Gemini API")
    st.markdown("📊 FAISS")
    st.markdown("🌐 Streamlit")
    st.divider()
    st.markdown("**By:** Janak Gajjar")
    st.markdown("[GitHub](https://github.com/janakgajjar)")

# Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Ask about your PDF..."):
    if "vectorstore" not in st.session_state:
        st.warning("⚠️ Upload a PDF first!")
    else:
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        with st.chat_message("user"):
            st.write(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = get_answer(
                    st.session_state.vectorstore,
                    prompt
                )
            st.write(answer)

        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

if "vectorstore" not in st.session_state:
    st.info("👈 Upload PDF from sidebar!")
    st.markdown("### 💡 Try asking:")
    st.markdown("- What is this document about?")
    st.markdown("- Summarize the main points")
    st.markdown("- What are the key topics?")