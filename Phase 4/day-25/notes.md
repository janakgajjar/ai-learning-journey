# Day 25 — LLMOps + Monitoring

## LLMOps = LLM + Operations
- Monitor AI calls
- Track costs
- Optimize performance
- Version prompts

## Key Metrics
| Metric | What | Target |
|--------|------|--------|
| Latency | Response speed | < 3 sec |
| Token Use | API cost | Minimize |
| Error Rate | Failures | < 1% |
| Cache Hit | Repeat calls | Maximize |

## Caching Strategy
- Same question → Cache check first
- Cache HIT = 0ms, $0 cost
- Cache MISS = API call

## Prompt Versioning
v1 → Basic (fast, less quality)
v2 → Structured (balanced)
v3 → Optimized (best quality)
→ Test all → Pick best!

## Monitoring Log Fields
- timestamp: When called
- user_id: Who called
- latency: How fast
- status: success/error
- error: What went wrong

## Fine-tuning vs RAG
| | Fine-tuning | RAG |
|--|------------|-----|
| Cost | High | Low |
| Speed | Slow to setup | Fast |
| Update | Retrain needed | Just add docs |
| Best For | Behavior change | Knowledge update |

## Key Insight
"Monitor everything in production!"
LangSmith = Best free monitoring tool