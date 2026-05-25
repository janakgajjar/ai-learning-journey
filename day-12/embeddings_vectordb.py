from dotenv import load_dotenv
import os

load_dotenv()

print("-" * 30)
print("Embeddings + VectorDB")
print("-" * 30)

# part 1: Embeddings

print("\n Part 1: Text Embeddings")
print("-" * 20)

from google import genai

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

texts = [
    "Aritifcial intelligence is the future."
    "Machine Learning uses data to learn",
    "python is a programming language",
    "AI and ML are related fields",
    "I love eating pizza"
]

print("Generating embeddings...")
embeddings = []
for text in texts:
    result = client.models.embed_content(
        model="models/gemini-embedding-001",
        contents=text
    )
    embeddings.append(result.embeddings[0].values)
    print(f"'{text[:40]}' -> {len(result.embeddings[0].values)} dimensions")


##Part 2 : Similarity search with FAISS

print("\n Part 2: FAISS Similarity Search")
print("-" * 20)

import faiss
import numpy as np

#convet to numpy array
embedding_matrix = np.array(embeddings).astype('float32')

#create FAISS index
dimension = len(embeddings[0])
index = faiss.IndexFlatL2(dimension)
index.add(embedding_matrix)

print(f"FAISS Index Created!!")
print(f"Stored: {index.ntotal} embeddings")
print(f"Dimensions : {dimension}")

#search similar texts

query = "Deep Learning and AI technologies"
print(f"\n Query: '{query}'")

query_result = client.models.embed_content(
    model="models/gemini-embedding-001",
    contents=query
)

query_embedding = np.array(
    [query_result.embeddings[0].values]
).astype('float32')

#find top 3 similar
distances, indices = index.search(query_embedding, 3)

print("\n Top 3 similar results:")
for i, (dist, idx) in enumerate(
    zip(distances[0], indices[0]), 1
):
    print(f"{i}. '{texts[idx]}' (distance: {dist:.4f})")

##Part 3: Chroma Vector DB

print("\n Part 3: ChromaDB")
print("-" * 20)

import chromadb

chroma_client = chromadb.Client()
collection = chroma_client.create_collection(
    name="ai_knowledge"
)

#add documents
documents = [
    "Langchain is a framework for building AI apps",
    "RAG combines retrieval with generation",
    "Agents use tools to complete tasks",
    "Vector databse store embeddings",
    "Python is used for AI development"
]

collection.add(
    documents=documents,
    ids=[f"doc{i}" for i in range(len(documents))]
)

print(f'Added {len(documents)} docs to ChromaDB')

#query ChromaDB

queries = [
    "How to build AI applications?",
    "What are AI agents?"
]

for q in queries:
    results = collection.query(
        query_texts=[q],
        n_results=2
    )
    print(f"\n Query: '{q}'")
    for doc in results['documents'][0]:
        print(f"   → {doc}")

print("\n Embeddings + Vector DB Lab Complete!")
print("\nKey Learnings:")
print("→ Embeddings convert text to numbers")
print("→ FAISS does fast similarity search")
print("→ ChromaDB stores and queries documents")
print("→ Similar texts have similar embeddings!")