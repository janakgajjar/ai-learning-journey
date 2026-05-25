# Day 12 — Plan-Execute + Reflexion + Embeddings

## Plan-Execute Pattern
- Plan FIRST → Execute THEN
- Better for complex, multi-step tasks
- Clear path vs reactive path
- Steps: Plan → Execute Step 1 → Step 2...

## Reflexion Pattern  
- Answer → Critique → Improve → Better Answer
- Iterative self-improvement
- Like: Draft → Review → Final
- Best for: Writing, Analysis, Code

## Embeddings
- Text → Numbers (Vectors)
- Similar words = Similar vectors
- King - Man + Woman = Queen
- Dimension: 768, 1536, 3072 (model dependent)

## Vector Databases
| DB | Type | Best For |
|----|------|---------|
| FAISS | Local | Fast search |
| Chroma | Local | Easy setup |
| Pinecone | Cloud | Production |

## Similarity Search
1. Store: Text → Embed → Save in DB
2. Query: Question → Embed → Compare
3. Return: Most similar documents

## Key Insight
Embeddings + Vector DB = RAG System Foundation!
Tomorrow: Full RAG Pipeline!