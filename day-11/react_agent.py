from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=r"C:\Users\Dell\Music\Desktop\ai-journey\day-06\.env")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)

print("=" * 50)
print("   ReAct Agent Simulation — Lab 6")
print("=" * 50)

# Custom Tools
def calculator(expression):
    try:
        return str(eval(expression))
    except:
        return "Calculation error"

def ai_info(topic):
    info = {
        "langchain": "Framework for AI apps",
        "rag": "Retrieval Augmented Generation",
        "agent": "LLM + Memory + Tools + Planning"
    }
    return info.get(topic.lower(), f"No info for {topic}")

# ReAct Prompt
react_template = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI Agent using ReAct pattern.
For the question, follow this format EXACTLY:

THOUGHT: What do I need to do?
ACTION: What action will I take?
OBSERVATION: What did I find?
THOUGHT: What is my conclusion?
FINAL ANSWER: The final response

Question: {question}"""
)

chain = react_template | llm | StrOutputParser()

questions = [
    "What is 25 multiplied by 48?",
    "What is LangChain and why is it useful?",
    "What is an AI Agent?"
]

for q in questions:
    print(f"\n❓ Question: {q}")
    print("-" * 40)
    result = chain.invoke({"question": q})
    print(result[:400])
    print()

print("✅ ReAct Agent Simulation Done!")