# Day 21 — AutoGen + DAG

## AutoGen vs Others
| Feature | CrewAI | LangGraph | AutoGen |
|---------|--------|-----------|---------|
| Style | Sequential | Graph | Chat |
| Control | Medium | High | Medium |
| Best For | Content | Logic | Code/Debate |
| Made By | CrewAI | LangChain | Microsoft |

## AutoGen Key Agents
- AssistantAgent → AI powered
- UserProxyAgent → Human proxy
- ConversableAgent → Custom base

## AutoGen Config
config_list = [{
    "model": "model-name",
    "api_key": "key",
    "api_type": "google/openai"
}]

## DAG Rules
- Directed: One direction only
- Acyclic: No loops!
- Dependencies: Clear order

## DAG Pattern
A → B → C → D (Sequential)
A → B           (Parallel possible)
A → C

## Key Insight
AutoGen = Best for conversational tasks
DAG = Best for pipeline workflows
Production systems use both!