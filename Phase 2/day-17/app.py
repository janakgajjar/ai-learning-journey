# Program: PDF RAG Chatbot — Production
# Topic: RAG + Streamlit Deployment
# Phase: 2 | Day: 17
# Concept: Deploy AI app on Hugging Face

import gradio as gr
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
import os
import tempfile
import time

# Models
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3
)
embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

vectorstore = None

def process_pdf(pdf_file):
    global vectorstore
    
    if pdf_file is None:
        return "⚠️ Please upload a PDF!"
    
    try:
        pdf_path = pdf_file.name \
            if hasattr(pdf_file, 'name') else pdf_file
        
        # Try PyMuPDF first
        loader = PyMuPDFLoader(pdf_path)
        documents = loader.load()
        
        if not documents:
            return "❌ PDF is empty or scanned image — text PDFs only!"
        
        # Check if text exists
        total_text = " ".join([
            doc.page_content for doc in documents
        ]).strip()
        
        if len(total_text) < 50:
            return "❌ PDF has no readable text! Use a text-based PDF."
        
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        chunks = splitter.split_documents(documents)
        
        if not chunks:
            return "❌ Could not process PDF content!"
        
        processed = []
        for i in range(0, len(chunks), 5):
            batch = chunks[i:i+5]
            processed.extend(batch)
            time.sleep(3)
        
        vectorstore = FAISS.from_documents(
            processed, embeddings
        )
        
        return f"✅ Ready! Pages: {len(documents)} | Chunks: {len(chunks)}"
    
    except Exception as e:
        return f"❌ Error: {str(e)}"
        
def answer_question(question, history):
    global vectorstore
    
    if vectorstore is None:
        return "⚠️ Please upload a PDF first!"
    
    if not question.strip():
        return "⚠️ Please ask a question!"
    
    try:
        retriever = vectorstore.as_retriever(
            search_kwargs={"k": 3}
        )
        
        rag_prompt = PromptTemplate(
            input_variables=["context", "question"],
            template="""You are a helpful AI assistant.
Use the context to answer the question.
If not in context, say: 
"I couldn't find that in the PDF."

Context: {context}

Question: {question}

Answer:"""
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
    
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Gradio UI
with gr.Blocks(title="PDF RAG Chatbot") as app:
    gr.Markdown("# 📄 PDF RAG Chatbot")
    gr.Markdown("**Upload PDF → Ask Questions → Get AI Answers!**")
    gr.Markdown("*Built by Janak Gajjar | MCA | Agentic AI*")
    
    with gr.Row():
        with gr.Column(scale=1):
            pdf_input = gr.File(
                label="📁 Upload PDF",
                file_types=[".pdf"]
            )
            upload_btn = gr.Button(
                "Process PDF",
                variant="primary"
            )
            status = gr.Textbox(
                label="Status",
                interactive=False
            )
        
        with gr.Column(scale=2):
            chatbot = gr.ChatInterface(
                fn=answer_question,
                title="Ask Questions",
            )
    
    upload_btn.click(
        fn=process_pdf,
        inputs=[pdf_input],
        outputs=[status]
    )

app.launch()