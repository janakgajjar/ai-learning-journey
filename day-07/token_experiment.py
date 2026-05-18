from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("-" * 20)
print(" Token Experiment ")
print("-" * 20)

prompts = [
    "Hi",
    "Hello, how are you today?",
    "Explain artificail intelligence in detail with examples"
]

print("Experminet 1 : Token count")
for prompt in prompts:
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    print(f"\nPrompt : '{prompt}")
    print(f"Response length : {len(response.text)} chars")
    print(f"Response : {response.text[:100]} ...") 

print("\n Experiment 2 : Memory test")
short_context = "My name is janak.What is my name ?"
long_context = """
My name is Janak.I am from gujarat.I am studing MCa,I love AI.I want to become an AI engineer.
What is my name and what do i want to become ?
"""

print("\nShort Context Response:")
r1 = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=long_context
)
print(r1.text)

print("\nLong context Response :")
r2 = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=long_context
)
print(r2.text)

print("\n Experiment 3 : Quality Difference")
q1 = "AI?"
q2 = "What is Artificial Intelligence?explain with 3 real life example "

print("/n Vague question:")
r3 = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=q1
)
print(r3.text[:200])

print("\nClear Question:")
r4 = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=q2
)
print(r4.text[:200])