## Prog: PDF RAG CHATBOT
## Topic: Retrival Augmented Generation
## Concept: Upload PDF -> Ask Questions -> AI Answers

import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os
import tempfile
import time

load_dotenv()

# Page config

st.set_page_config(
    page_title="PDF RAG Chatbot",
    page_icon="📄",
    layout="centered"
)

st.title("PDF RAG Chtbot")
st.markdown(" **Upload a PDF and ask questions!! **")
st.markdown(" *Built with langchain + gemini + FAISS*")

## Initialize LLM + Embeddings

@st.cache_resource
def init_models():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0.3
    )
    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-001",
        google_api_key=os.getenv("GEMINI_API_KEY")
    )
    return llm, embeddings

llm, embeddings = init_models()

## RAG pipline function

def process_pdf(pdf_file):
    """Load PDF -> Split -> Embed -> Store"""

    #Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(
        delete=False, suffix=".pdf"
    ) as tmp :
        tmp.write(pdf_file.getvalue())
        tmp_path = tmp.name

    #Load PDF
    loader = PyPDFLoader(tmp_path)
    documents = loader.load()

    #Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=200
    )
    chunks = splitter.split_documents(documents)

    #Embed + store
    vectorstore = FAISS.from_documents(chunks, embeddings)

    #Cleanup temp file
    os.unlink(tmp_path)

    batch_size = 5
    all_chunks = []

    for i in range(0, len(chunks), batch_size):
        batch = chunks[i:i+batch_size]
        all_chunks.extend(batch)
        time.sleep(3)

    return vectorstore, len(documents), len(chunks)

def get_answer(vectorstore, question):
    """Retrvie relevant chunks -> Generate answer"""

    retriever = vectorstore.as_retriever(
        search_kwargs={"k": 3}
    )

    #RAG Prompt
    rag_prompt = PromptTemplate(
        input_variables=["context", "question"],
        template="""You are a helpful AI assistant.
Use the context below to answer the question.
If answer is not in context, say " I couldnot find that in the PDF.

Context:
{context}

Question: {question}

Answer clearly and concisely:"""
    )

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
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

## Sidebar - PDF Upload

with st.sidebar:
    st.header("📁 UPlod PDF")

    uploaded_file = st.file_uploader(
        "Choose a PDF File",
        type="pdf"
    )

    if uploaded_file:
        st.success(f" {uploaded_file.name}")

        with st.spinner("Processing PDF..."):
            vectostore, pages, chunks = process_pdf(
                uploaded_file
            )
            st.session_state.vectorstore = vectostore

        st.info(f" Pages : {pages}")
        st.info(f" Chunks: {chunks}")
        st.success("Ready to answer questions!")

    st.divider()
    st.markdown("**How it works:")
    st.markdown("1. Upload PDF")
    st.markdown("2. Ask questions")
    st.markdown("3. AI answers from PDF!")

## Main - chat interface

if "messages" not in st.session_state:
    st.session_state.messages = []

#Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

#Chat Input
if prompt := st.chat_input("Ask a question about your PDF.. "):

    #Check PDF uploaded
    if "vectorstore" not in st.session_state:
        st.warning(" Please upload a PDF first")
    else :
        #show user message

        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        with st.chat_message("user"):
            st.write(prompt)

        #Gen AI answer
        with st.chat_message("assistant"):
            with st.spinner("Thinking.."):
                answer = get_answer(
                    st.session_state.vectorstore,
                    prompt
                )
            st.write(answer)

        #save assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

#Empty state

if "vectorstore" not in st.session_state:
    st.info(" Upload a PDF from the sidebar to start !!")

    