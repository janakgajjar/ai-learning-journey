# ============================================
# Program: AutoGen Multi-Agent Demo
# Topic: Conversational Multi-Agent System
# Phase: 3 | Day: 21
# Concept: AutoGen Agents + DAG Workflow
# ============================================

import autogen
from dotenv import load_dotenv
import os

load_dotenv()

print("-" * 30)
print(" Autogen + DAG Demo")
print("-" * 30)

## LLM Config for AutoGen
config_list = [
    {
        "model": "gemini-2.5-flash-lite",
        "api_key": os.getenv("GEMINI_API_KEY"),
        "api_type": "google"
    }
]

llm_config = {
    "config_list": config_list,
    "temperature": 0.3,
    "timeout": 120
}

# Demo 1: Simple 2 Agent Chat
print("\n Demo 1: Assistant + UserProxy")
print("-" * 20)

# Assistant Agent
assistant = autogen.AssistantAgent(
    name="AI_Assistant",
    llm_config=llm_config,
    system_message="""You are a helpful AI assistant for MCA students
    learning Agentic AI.
    Explain concepts clearly with examples.
    Keep response concise."""
)

# UserProxy Agent
user_proxy = autogen.UserProxyAgent(
    name="Student",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    is_termination_msg=lambda x: x.get(
        "content", ""
    ).rstrip().endswith("DONE"),
    code_execution_config=False
)

print("\n Starting Agent Conversation..")
print("-" * 20)

user_proxy.initiate_chat(
    assistant,
    message="""Explain these 3 concepts briefly:
    1. What is Langchain?
    2. What is Langgraph?
    3. What is Multi-Agent AI?
    End your response with 'DONE'"""
)

# Demo 2: Debate Pattern
print("\n Demo 2: Debte Pattern")
print("-" * 20)

agent_for = autogen.AssistantAgent(
    name="Agent_For",
    llm_config=llm_config,
    system_message="""You argue FOR the given topic.
    Give 3 strong points.
    Be consie and persuasive."""
)

agent_against = autogen.AssistantAgent(
    name="Agent_Against",
    llm_config=llm_config,
    system_message="""You argue AGAINST the given topic.
    Give 3 counter points.
    Be concise and persuasive."""
)

moderator = autogen.UserProxyAgent(
    name="Moderator",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=2,
    is_termination_msg=lambda x: x.get(
        "content", ""
    ).rstrip().endswith("DEBATE_END"),
    code_execution_config=False
)

print("\n Debate: 'AI will replace programmers'")
print("-" * 20)

moderator.initiate_chat(
    agent_for,
    message="""Topic: 'AI will replace programmers'
    Give your FOR argument in 3 points.
    Then end with 'DEBATE_END'"""
)

print("\n" + "-" * 20)
moderator.initiate_chat(
    agent_against,
    message="""Topic: 'AI will replace programmers'
    Give your AGAINST argument in 3 points.
    Then end with 'DEBATE_END'"""
)

## DAG Workflow Simulation

print("\n Demo 3: DAG Workflow")
print("-" * 20)
print("Task: Research -> Summarize -> Format -> Save")

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY"),
    temperature=0.3
)
parser = StrOutputParser()

# DAG Node Functions
def task_research(topic: str) -> str:
    """Node A: Research topic"""
    print(f"\n Node A: Researching '{topic}'...")
    prompt = PromptTemplate(
        input_variables=["topic"],
        template="Provide 5 key facts about: {topic}"
    )
    return (prompt | llm | parser).invoke(
        {"topic": topic}
    )

def task_summarize(content: str) -> str:
    """NOde B: Summarize content"""
    print(" Node B: summarizing...")
    prompt =PromptTemplate(
        input_variables=["content"],
        template="Summarize in 3 sentences: {content}"
    )
    return (prompt | llm | parser).invoke(
        {"content":content}
    )

def task_format(summary: str) -> str:
    """Node C: Format as report"""
    print("Node C: Formatting report...")
    prompt = PromptTemplate(
        input_variables=["summary"],
        template="""Format as a mini report:
Title, Key Points, conclusion
Content: {summary}"""
    )
    return (prompt | llm | parser).invoke(
        {"summary": summary}
    )

def task_save(report: str, filename: str) -> str:
    """Node D: Save to file"""
    print(f" Node D: Saving to {filename}...")
    with open(filename, "w") as f:
        f.write(report)
    return f" Saved to {filename}"

# Execute DAG
print("\n Executing DAG Pipeline...")
print("A -> B -> C -> D")
print("-" * 20)

topic = "Agentic AI in 2026"

# A -> B -> C -> D(sequential DAG)
research_output = task_research(topic)
summary_output = task_summarize(research_output)
report_output = task_format(summary_output)
save_output = task_save(report_output, "dag_report.txt")

print(f"\n Final Report preview:")
print(report_output[:300])
print(f"\n{save_output}")