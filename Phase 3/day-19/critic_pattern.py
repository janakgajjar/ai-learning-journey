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

# Demo : Critic Pattern

print("\n\n Demo 1: Generator + Critic Pattern")
print("-" * 30)

# Agent 1: Generator

generator = Agent(
    role="Content Generator",
    goal="Generate high quality explanations",
    backstory="""Expert at creating clear explanations of techinal concepts.""",
    llm=llm,
    verbose=True,
    allow_delegation=False
)

#Agent 2: Critic
critic = Agent(
    role="Quality Reviewer",
    goal="Review and improve content quality",
    backstory="""Expert reviewer who ensures content is accurate, clear, and comprehensive.
    Always provide constructive feedback.""",
    llm=llm,
    verboce=False,
    allow_delegation=False
)

# Tasks
generate_task = Task(
    description="Explain RAG(Retrieval Augmented Generation) in 5 sentences for beginners.",
    expected_output="A 5-sentences explanation of RAG that is clear and beginner-friendly.",
    agent=generator
)

critique_task = Task(
    description="""Review the explanation of RAG provided.
    Check for:
    1. clarity
    2. Accuracy
    3. Completeness
    Then provide an improved version.""",
    expected_output="""Your review with:
    - what was good
    - what was missing
    - Improved explanation""",
    agent=critic,
    context=[generate_task]
)

crew1 = Crew(
    agents=[generator, critic],
    tasks=[generate_task, critique_task],
    process=Process.sequential,
    verbose=False
)

print("\n Starting Crew ....")
result = crew1.kickoff()
print(f"\n Reviewed Output: \n {result}")
