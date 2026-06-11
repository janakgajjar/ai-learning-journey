# Program: Multi-Agent System 
# Topic: CrewAI Multi-Agent Framework
# Phase: 3 | Day: 19
# Concept: Multiple AI Agents collaborate

from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
import os

load_dotenv()

print("-" * 30)
print(" Multi-Agent System")
print("-" * 30)

os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

llm = "gemini/gemini-2.5-flash-lite"

## Demo 1: Simple 2 Agent System

print("\n Demo 1: Researcher + Writer Agents")
print("-" * 20)

#Agent 1: Researcher
researcher = Agent(
    role="AI Research Analyst",
    goal="Research and gather accurate information about AI topics",
    backstory="""You are an expert AI researcher with 10 years
    of experience. You always provide accurate,
    well-sturctured information about AI concepts.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

#Agent 2: Writer
writer = Agent(
    role="Technical Content Writer",
    goal="Write clear, engaging content for MCA students",
    backstory="""You are a skilled technical writer who specializes in making complex AI concepts easy to understand for students. You write in simple,
    clear language with practical examples.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

# Task 1: Research
research_task = Task(
    description="""Research the topic: 'What is Agentic AI?'
    
    Find and organize:
    1.Clear defination
    2.Key charchteristics
    3.Real world applications
    4.Why it matters in 2026""",
    expected_output="""A structured research report with:
    - Defination of Agentic AI
    - 3-4 key charcteristics
    - 2-3 real world examples
    - Importance in current tech landscape""",
    agent=researcher
)

# Task 2: Write Article
write_task = Task(
    description="""Using the research provided, write a beginner-frienldy article about agentic AI for MCA students.
    
    Requirements:
    - Simple language
    - Real world examples
    - under 300 words
    - Engaging and information""",
    expected_output="""A well-written article that:
    - Examples Agentic Ai simply
    - Uses student-friendly examplse
    - Is under 300 words
    - Has clear sections""",
    agent=writer,
    content=[research_task]
)

#Create Crew

crew1 = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_task],
    process=Process.sequential,
    verbose=True
)

print("\n Starting Crew1...")
result1 = crew1.kickoff()
print(f"\n Final Article:\n {result1}")
