# Day 20 — LangGraph Stateful Agents

## LangGraph vs CrewAI
| Feature | CrewAI | LangGraph |
|---------|--------|-----------|
| Complexity | Simple | Advanced |
| Control | Limited | Full |
| Loops | No | Yes |
| State | Basic | TypedDict |
| Best For | Simple tasks | Complex flows |

## Key Components
- StateGraph: Graph container
- TypedDict: State structure
- Nodes: Processing functions
- Edges: Connections
- Conditional Edges: Smart routing
- END: Terminal node

## State Flow
Node 1 reads state → updates → 
Node 2 reads updated state → updates →
Node 3 reads → Final output

## Routing Pattern
def should_continue(state):
    if condition: return "path_a"
    else: return "path_b"

## Key Insight
LangGraph = Most powerful agent framework!
Production AI systems use LangGraph!