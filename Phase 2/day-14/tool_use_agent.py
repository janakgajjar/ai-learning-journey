from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os
import json
import math
import datetime

load_dotenv()

print("-" * 30)
print(" Tool Use + function Calling")
print("-" * 30)

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0
)


##Step 1: Define tools
print("\n Step 1: Defineing Tools")
print("-" * 20)

#Tool 1: Calculator
def calculator(expression: str) -> str:
    """Mathemetical calculations"""
    try:
        allowed = {
            'abs': abs, 'round': round,
            'math': math, 'sqrt': math.sqrt,
            'pow': pow
        }
        result = eval(expression, {"__builtins__": {}}, allowed)
        return f"Result: {result}"
    except Exception as e:
        return f"Error: {str(e)}"
    
#Tool 2 : word counter
def word_counter(text: str) -> str:
    """Count words and characters"""
    words = len(text.split())
    chars = len(text)
    sentences = text.count('.') + text.count('!') + text.count('?')
    return f"Words: {words} | Characters: {chars} | Sentencses: {sentences}"

#Tool 3: Text formatter
def text_formatter(text: str, format_type: str) -> str:
    """Format text in different ways"""
    if format_type == "upper":
        return text.upper()
    elif format_type == "lower":
        return text.lower()
    elif format_type == "title":
        return text.title()
    elif format_type == "reverse":
        return text[::-1]
    else:
        return f"Unknow format: {format_type}"\
        
#Tool 4: Date/time 
def get_datetime(query: str) -> str:
    """Get current date and time info"""
    now = datetime.datetime.now()
    if "date" in query.lower():
        return f"Today: {now.strftime('%y-%m-%d')}"
    elif "time" in query.lower():
        return f"Time: {now.strftime('%H:%M:%S')}"
    elif "day" in query.lower():
        return f"Day: {now.strftime('%A')}"
    else:
        return f"DateTime: {now.strftime('%y-%m-%d %H:%M:%S')}"
    
#Tool 5: AI knowledge 
def ai_knowledge(topic: str) -> str:
    """Get AI-related information"""
    knowledge = {
        "langchain": "Framework for building AI applications with LLMs",
        "rag": "Retrieval Augmented Generation - combines search with AI",
        "agent": "Autonomous AI system with memory, tools, and planning",
        "llm": "Large Language Model - AI trained on massive text data",
        "crewai": "Multi-agent framework for collaborative AI systems",
        "langgraph": "Graph-based framework for stateful AI workflows",
        "embedding": "Converting text to numerical vectors",
        "faiss": "Facebook's fast similarity search library",
        "chroma": "Open-source vector database for AI applications"
    }
    result = knowledge.get(topic.lower(), f"No info found for: {topic}")
    return result

#Tools Registry
TOOLS = {
    "calculator": {
        "function": calculator,
        "description": "Math calculations. Input: expression like '25 * 48'"
    },
    "word_counter": {
        "function": word_counter,
        "description": "Count words/chars. Input: any text string"
    },
    "text_formatter": {
        "function": lambda x: text_formatter(*x.split("|")),
        "description" : "Format text. Input: 'text|format' (upper/lower/title/reverse)"
    },
    "get_datetime": {
        "function": get_datetime,
        "description": "Get date/time. Input: 'date' or 'time' or 'day'"
    },
    "ai_knowledge": {
        "function": ai_knowledge,
        "description": "AI topic info. Input: topic like 'langchain', 'rag', 'agent'"
    }
}

print("Tools Defined:")
for name, tool in TOOLS.items():
    print(f" { name}: {tool['description'][:50]}")

##Step 2: Tool selector agent
print("\n Step 2: Tool selector agent")
print("-" * 30)

tools_description = "\n".join([
    f"- {name}: {info['description']}"
    for name, info in TOOLS.items()
])

selector_template = PromptTemplate(
    input_variables=["tools", "questions"],
    template="""You are a tool selector AI agent.
    
Avilable Tools:
{tools}

User Question: {question}

Select the Best tool and provide input.
Respond in this EXACT format:
TOOL: [tool_name]
INPUT: [input_for_tool]
REASON: [why this tool]

Only use tools from the list above."""
)

selector_chain = selector_template | llm | StrOutputParser()


##Step 3: Execute tool Calls
print("\n Step 3: Testing tool calls")
print("-" * 40)

def run_agent(question: str):
    print(f"\n question: {question}")

    #select tool
    selection = selector_chain.invoke({
        "tools": tools_description,
        "question": question
    })

    #parse selection
    lines = selection.strip().split('\n')
    tool_name = "" 
    tool_input = ""

    for line in lines:
        if line.startswith("TOOL:"):
            tool_name = line.replace("TOOL:", "").strip()
        elif line.startswith("INPUT:"):
            tool_input = line.replace("INPUT:", "").strip()

    print(f"Selected Tool: {tool_name}")
    print(f"Input: {tool_input}")

    #Execute tool
    if tool_name in TOOLS:
        result = TOOLS[tool_name]["function"](tool_input)
        print(f"Tool Result: {result}")
    else:
        result = "Tool not found"
        print(f"{result}")

    #Generate final answer
    answer_template = PromptTemplate(
        input_variables=["question", "tool_result"],
        template="""Question: {question}
        
Give a clear, helpful final answer based on the tool result:"""
    )
    answer_chain = answer_template | llm | StrOutputParser()
    final_answer = answer_chain.invoke({
        "question": question,
        "tool_result": result
    })

    print(f"Final answer: {final_answer[:200]}")
    print("-" * 20)

#Test different tools
test_questions = [
    "What is 15% of 8500?",
    "Count words in: I am learning Agentic AI at MCA Gujarat",
    "What is today's date?",
    "What is LangChain?",
    "Convert to uppercase: agentic ai is the future"
]

for question in test_questions:
    run_agent(question)


##Step 4: Tool chaining 
print("\n step 4: Tool chaining demo")
print("-" * 20)
print("Task : Get AI info about RAG, count its words, format to uppercase")

step1 = ai_knowledge("rag")
print(f"\nStep 1 (AI Knowledge): {step1}")

step2 = word_counter(step1)
print(f"Step 2 (Word Count): {step2}")

step3 = text_formatter(step1, "upper")
print(f"step 3 (Formatted): {step3}")

print("\nTool Chaining Complete!")
print(" Output of Tool 1 = Input of Tool 2")
print(" Output of Tool 2 = Input of Tool 3")