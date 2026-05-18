from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("-" * 20)
print(" Agent Memory ")
print("-" * 20)

print("\n Demo 1: Without Memory")
print("AI dont remeber previous message")
print("-" * 10)

questions = [
    "My name is janak",
    "I am from gujarat",
    "What is my name ?"
]

for q in questions:
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=q
    )
    print(f"You : {q}")
    print(f"AI : {response.text.strip()[:100]}")
    print()

print("\n Demo 2: Short term Memory")
print("AI conversation history")
print("-" * 10)

short_term_memory = []

conversation = [
    "My name is janak",
    "I am from gujarat",
    "I am studing MCA"
    "What is my name and where am i from ?"
]

for message in conversation:
    short_term_memory.append(f"User: {message}")
    full_context = "\n".join(short_term_memory)
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=full_context
    )

    ai_reply = response.text.strip()
    short_term_memory.append(f"AI : {ai_reply}")

    print(f"You : {message}")
    print(f"AI: {ai_reply[:100]}")
    print()

print("\n Demo 3: Long term Memory")
print("Data stored in file - Available in next session")
print("-" * 10)

memory_file = "long_term_memory.txt"

def save_memory(info):
    with open(memory_file, "a") as f:
        f.write(info + "\n")
    print(f"Saved: {info}")

def load_memory():
    if os.path.exists(memory_file):
        with open(memory_file, "r") as f:
            return f.read()
    return "No memory yet"

save_memory("User name: Janak")
save_memory("User location: Gujarat")
save_memory("User course: MCA - Agentic AI")
save_memory("User goal: Become AI Engineer")

memory = load_memory()
print(f"\n Loaded Memory :\n{memory}")

query = "Based on what you know about me , what career advice would you give?"
full_prompt = f"User Profile:\n{memory}\n\nQuestion: {query}"

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=full_prompt
)

print(f"\nAI Advice: {response.text[:300]}")