# Day 13 — RAG Pipeline

## RAG = Retrieval Augmented Generation

## Why RAG?
- AI knows only training data
- RAG adds YOUR documents
- No hallucination on given docs
- Dynamic updates possible

## RAG Pipeline — 4 Steps
1. LOAD    → Documents load
2. SPLIT   → Chunks create
3. EMBED   → Store in Vector DB
4. RETRIEVE+GENERATE → Answer!

## Key Parameters
- chunk_size: 200-1000 (experiment!)
- chunk_overlap: 10-20% of chunk_size
- k: top-k similar chunks retrieve

## RAG vs Fine-tuning
| | RAG | Fine-tuning |
|--|-----|-------------|
| Cost | Free ✅ | Expensive |
| Speed | Fast ✅ | Slow |
| Update | Easy ✅ | Retrain |
| Use case | Domain docs | Style/behavior |

## Code Pattern