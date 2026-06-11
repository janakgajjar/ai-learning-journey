from google import genai
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../.env")
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("=" * 50)

print("\n1: WITHOUT Chain-of-Thought")
print("-" * 50)

without_cot = "A train travels 120km in 2 hours. How long to travel 450km?"

response1 = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=without_cot
)
print(f"Question: {without_cot}")
print(f"Answer: {response1.text.strip()[:200]}")

print("\n1: WITH Chain-of-Thought")
print("-" * 50)

with_cot = """A train travels 120km in 2 hours. 
How long to travel 450km?
Think step by step and show your reasoning."""

response2 = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=with_cot
)
print(f"Question: {with_cot}")
print(f"Answer: {response2.text.strip()[:400]}")

print("\n 2: Few-Shot CoT")
print("-" * 50)

few_shot_cot = """Solve math problems step by step.

Example 1:
Q: If 5 books cost ₹250, what do 8 books cost?
A: Step 1: Cost per book = 250/5 = ₹50
   Step 2: Cost of 8 books = 50 × 8 = ₹400
   Answer: ₹400

Example 2:
Q: A car goes 60km/h. How far in 2.5 hours?
A: Step 1: Distance = Speed × Time
   Step 2: Distance = 60 × 2.5 = 150km
   Answer: 150km

Now solve:
Q: If 12 workers finish in 8 days, 
   how many days for 6 workers?"""

response3 = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=few_shot_cot
)
print(f"Answer: {response3.text.strip()[:400]}")

print("\n 3: ReAct Pattern Simulation")
print("-" * 50)

react_prompt = """You are an AI agent that uses ReAct pattern.
For every question, follow this EXACT format:

THOUGHT: (what you are thinking)
ACTION: (what you will do)
OBSERVATION: (what you found)
THOUGHT: (next thinking based on observation)
FINAL ANSWER: (your answer)

Question: What are the top 3 skills needed 
to become an AI Engineer in 2025?"""

response4 = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=react_prompt
)
print(f"ReAct Response:\n{response4.text.strip()[:500]}")

print("\n4: Self-Reflection")
print("-" * 50)

# Step 1: Get initial answer
initial_prompt = "Explain what is RAG in AI in 3 sentences."
initial_response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=initial_prompt
)
initial_answer = initial_response.text.strip()
print(f"Initial Answer:\n{initial_answer}\n")

# Step 2: Self-reflect and improve
reflection_prompt = f"""Here is an explanation of RAG:
{initial_answer}

Now critique this explanation:
1. Is it clear for a beginner?
2. Is anything missing?
3. Provide an improved version."""

reflection_response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=reflection_prompt
)
print(f"After Self-Reflection:\n{reflection_response.text.strip()[:500]}")