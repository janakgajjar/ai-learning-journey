# Day 11 — LangChain + ReAct Agent

## LangChain Components
| Component | Purpose | Example |
|-----------|---------|---------|
| LLM | AI Model connect | Gemini, GPT |
| PromptTemplate | Reusable prompts | Variables |
| Chain | Steps connect | A→B→C |
| Memory | History store | Chat history |
| Agent | Autonomous AI | ReAct Agent |
| Tools | Capabilities | Calculator |

## ReAct Agent Flow
THOUGHT → ACTION → OBSERVE → THOUGHT → ANSWER

## Prompt Template
input_variables = ["var1", "var2"]
template = "Do {var1} for {var2}"

## Memory Types in LangChain
- ConversationBufferMemory → Full history
- ConversationSummaryMemory → Summarized
- ConversationWindowMemory → Last N messages

## Key Insight
LangChain = LEGO for AI Apps
ReAct = Agent thinking  pattern
Memory = Agent behave as a human