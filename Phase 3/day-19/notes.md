# Day 19 — Multi-Agent Systems

## Why Multi-Agent?
- Complex tasks need specialists
- Parallel processing
- Better quality output
- Real world = Teams, not solo!

## Design Patterns
| Pattern | How | Best For |
|---------|-----|---------|
| Orchestrator | Boss + Workers | Large tasks |
| Peer-to-Peer | Equal agents | Collaboration |
| Critic | Generate + Review | Quality |
| Debate | For + Against | Decisions |

## CrewAI Components
- Agent = Role + Goal + Backstory + LLM
- Task = Description + Expected Output + Agent
- Crew = Agents + Tasks + Process
- Process = Sequential or Hierarchical

## Context Flow
Task 1 Output → Task 2 Input (via context=[task1])

## Key Insight
Single Agent = Solo developer
Multi-Agent = Development Team
= Better, Faster, Higher Quality!
