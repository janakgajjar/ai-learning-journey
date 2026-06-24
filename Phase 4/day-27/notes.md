# Day 27 — Fine-tuning + LoRA + Governance

## Fine-tuning vs RAG
| | Fine-tuning | RAG |
|--|------------|-----|
| Cost | High | Low |
| Update | Retrain | Add docs |
| Best For | Style change | Knowledge |
| Speed | Slow setup | Fast |

## LoRA Key Points
- Original model = Frozen (unchanged)
- Small adapters = Added on top
- Only adapters train = 10x cheaper!
- Formula: W + (A × B)
- r (rank) = Lower = Fewer params

## EU AI Act Risk Levels
🔴 Unacceptable = BANNED
🟠 High Risk = Heavy regulation
🟡 Limited Risk = Transparency needed
🟢 Minimal Risk = Free to use

## NIST RMF 4 Functions
1. GOVERN = Policies
2. MAP = Context understand
3. MEASURE = Metrics
4. MANAGE = Risk treat

## Observability 3 Pillars
- Logs = What happened
- Metrics = How well (numbers)
- Traces = How it happened

## Our Project Risk Level
PDF RAG Chatbot = 🟡 Limited Risk
→ Must tell users it's AI chatbot
→ No heavy regulation needed