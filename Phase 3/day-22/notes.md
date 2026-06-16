# Day 22 — Multimodal + Evaluation

## Multimodal AI
- Text + Image + Audio = Multimodal
- Gemini supports vision natively
- Code: types.Part.from_bytes(data, mime_type)

## Code Agents
- Think → Plan → Code → Execute → Fix
- Agent writes + runs code autonomously
- Used in: Data analysis, debugging, automation

## Evaluation Metrics
| Metric | What | How |
|--------|------|-----|
| Keyword Score | Keywords found? | Count/Total |
| AI Score | Quality 1-10 | AI evaluator |
| Latency | Speed | Time in seconds |
| Token Use | Efficiency | Token count |

## Benchmarks
- MMLU: General knowledge
- HumanEval: Code generation
- AgentBench: Agent task completion

## Evaluation Flow
Generate Answer → Check Keywords 
→ AI Evaluate → Measure Latency 
→ Calculate Score → Report

## Key Insight
"You can't improve what you don't measure!"
Always evaluate before production deploy!