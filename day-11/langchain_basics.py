from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
import os
load_dotenv()

print("-" * 40)
print("   LangChain Basics")
print("-" * 40)

# LLM Setup
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.7
)
print("\n✅ LLM Connected!")

# ─────────────────────────────
# DEMO 1: Prompt Templates
# ─────────────────────────────
print("\n🔹 DEMO 1: Prompt Templates")
print("-" * 40)

template = PromptTemplate(
    input_variables=["topic", "level"],
    template="Explain {topic} for a {level} student. Keep it under 100 words with one example."
)

chain1 = template | llm | StrOutputParser()

response1 = chain1.invoke({
    "topic": "Artificial Intelligence",
    "level": "MCA"
})
response2 = chain1.invoke({
    "topic": "RAG Systems",
    "level": "beginner"
})

print(f"AI Explanation:\n{response1[:200]}")
print(f"\nRAG Explanation:\n{response2[:200]}")

# ─────────────────────────────
# DEMO 2: Simple Chain
# ─────────────────────────────
print("\n🔹 DEMO 2: Simple Chain")
print("-" * 40)

chain_template = PromptTemplate(
    input_variables=["concept"],
    template="""For the AI concept: {concept}
Provide:
1. Simple definition (1 line)
2. Real world example
3. Why MCA students should learn this
Be concise."""
)

chain2 = chain_template | llm | StrOutputParser()

concepts = ["LangChain", "Vector Database", "AI Agent"]

for concept in concepts:
    result = chain2.invoke({"concept": concept})
    print(f"\n📌 {concept}:")
    print(result[:200])

# ─────────────────────────────
# DEMO 3: Memory Chain
# ─────────────────────────────
# DEMO 3: Memory
print("\n🔹 DEMO 3: Conversation Memory")
print("-" * 40)

history = ChatMessageHistory()

def get_history(session_id):
    return history

chain_with_memory = RunnableWithMessageHistory(
    llm,
    get_history,
)

messages = [
    "My name is Janak and I am learning LangChain",
    "I am an MCA student from Gujarat", 
    "What is my name and what am I learning?"
]

for msg in messages:
    response = chain_with_memory.invoke(
        msg,
        config={"configurable": {"session_id": "janak"}}
    )
    print(f"\nYou: {msg}")
    print(f"AI:  {response.content[:150]}")

print("\n✅ Memory Working!")