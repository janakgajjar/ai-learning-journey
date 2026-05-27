# Day 14 — Tool Use + Function Calling

## What is Tool Use?
Agent + Tools = Can act in real world!

## Tool Definition
Every tool needs:
1. Name        → Unique identifier
2. Description → When to use
3. Function    → Actual code
4. Input type  → What to pass

## Tool Execution Flow
Question → Select Tool → Execute → Result → Answer

## Tool Chaining
Tool1 Output → Tool2 Input → Tool3 Input → Final

## Our Tools Built
| Tool | Purpose |
|------|---------|
| Calculator | Math operations |
| Word Counter | Text analysis |
| Text Formatter | Text transformation |
| DateTime | Current time/date |
| AI Knowledge | Domain info |

## JSON Schema Pattern
{
  "name": "tool_name",
  "description": "what it does",
  "parameters": {input definition}
}

## Key Insight
Tools = Agent Superpowers!
More tools = More capable agent!