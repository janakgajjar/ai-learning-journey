from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
import os

load_dotenv()

print("-" * 30)
print(" RAG Pipline")
print("-" * 30)

##setup

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/gemini-embedding-001",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

## Step 1: Load Document

print("\n Step 1: Loading Documents..")
print("-" * 20)

loader = TextLoader("sample.txt")
documents = loader.load()
print(f"Loaded: {len(documents)} documents(s)")
print(f" Content preview: {documents[0].page_content[:100]}...")

##Step 2: Split into chunks

print("\n Step 2: Splitting into chunks...")
print("-" * 20)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=200,
    chunk_overlap=50
)

chunks = splitter.split_documents(documents)
print(f"Created : {len(chunks)} chunks")
for i, chunk in enumerate(chunks):
    print(f" chunk {i+1}: {chunk.page_content[:80]}...")

##Step 3: Embed + Store

print("\n Step 3: Embedding + Storing...")
print("-" * 20)

vectorstore = FAISS.from_documents(chunks, embeddings)
print(f" Stored in FAISS vector DB!")
print(f"Total chunks embedded: {len(chunks)}")

##Step 4: Retrieve + Generate

print("\n Step 4: Retrieval + Generation...")
print("-" * 20)

retriever = vectorstore.as_retriever(
    search_kwargs={"k": 2}
)

#RAG Prompt
rag_prompt = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are a helpful AI assistant.
Use the following context to answer the question.
If you don;t know,say "I don;t have that information."

Context:
{context}

Question: {question}

Answer clearly and concisely:"""
)


##RAG chain

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


##Test Questions
questions =[
    "What is agentic AI?",
    "What is Langchain used for?",
    "What is RAG?",
    "What is CrewAI?",
    "What are vector databaeses?"
]

print("\n Testing RAG Q&A System:")
print("-" * 20)

for q in questions:
    print(f"\n Question: {q}")

    #reteieved context
    retrieved = retriever.invoke(q)
    print(f"Retrieved: {retrieved[0].page_content[:80]}...")

    #get answer
    answer = rag_chain.invoke(q)
    print(f"Answer: {answer[:200]}")
    print("-" * 20)


##step 5: save vector store

print("\n Step 5: Saving Vector Store...")
vectorstore.save_local("faiss_index")
print("Vector store saved!")
print("   Load later with: FAISS.load_local('faiss_index', embeddings)")
