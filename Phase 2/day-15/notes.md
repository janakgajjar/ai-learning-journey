# Day 15 — Prompt Engineering

## Techniques
| Technique | When to Use | Example |
|-----------|-------------|---------|
| Zero-shot | Simple tasks | "Classify: {text}" |
| Few-shot | Pattern tasks | 3 examples + question |
| CoT | Complex reasoning | "Think step by step" |
| XML Tags | Structured input | <context>...</context> |
| Role Play | Specific persona | "You are expert..." |

## System Prompt Rules
1. Clear role definition
2. Specific constraints
3. Output format
4. Edge case handling
5. Guardrails

## Guardrails = Safety
- Input: Block harmful requests
- Output: Filter wrong content
- Always: Human in the loop

## Output Formats
- JSON → Structured data
- Bullets → Lists
- Table → Comparisons
- Simple → Quick answers

## Prompt Chaining
Step1 Output → Step2 Input → Step3 Input
= Powerful multi-step processing!

## Key Rule
Better Prompt = Better Output
Garbage In = Garbage Out!