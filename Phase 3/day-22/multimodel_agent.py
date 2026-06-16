# ============================================
# Program: Multimodal Agent Demo
# Topic: Vision + Text AI Agent
# Phase: 3 | Day: 22
# Concept: Images + Text → AI Understanding
# ============================================

from google import genai
from google.genai import types
from dotenv import load_dotenv
import os 
import base64
import time
import urllib.request

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

print("-" * 30)
print(" Multimodel Agent ")
print("-" * 30)

## Demo 1: Text + Image understanding
print("\n Demo 1: Image Analysis")
print("-" * 20)

# Download sample image
image_file = r"C:\Users\Dell\Music\Desktop\ai-journey\Phase 3\day-22\icard.jpeg"
print("Downloading sample image...")

#Read image as bytes
with open(image_file, "rb") as f:
    image_bytes = f.read()

#Analyze image
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=[
        types.Part.from_bytes(
            data=image_bytes,
            mime_type="image/png"
        ),
        "Describe what you see in this image in detail."
    ]
)
print(f"Image Analysis:\n{response.text[:300]}")
time.sleep(3)

# Demo 2: Multi-turn vision chart
print("\n Demo 2: Multi-turn Vision Chat")
print("-" * 20)

questions = [
    "What colors are in this image?",
    "What is the main subject?",
    "Describe the background."
]

for q in questions:
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=[
            types.Part.from_bytes(
                data=image_bytes,
                mime_type="image/png"
            ),
            q
        ]
    )
    print(f"\n {q}")
    print(f"{response.text[:150]}")
    time.sleep(4)

## Demo 3: Code Agent Simulation
print("\n Demo 3: Code Agent")
print("-" * 20)

code_agent_prompt = """You are a Python code agent.

when given a programming problem:
1. THINK: Analyze the problem
2. PLAN: Design the solution
3. CODE: Write Python code
4. EXPLAIN: Explain line by line 

Problem: write a function that:
- Takes a list of numbers
- Returns mean, median, mode
- Handles empty list

Format you response as:
THINK: [Your analysis]
PLAN: [Your approach]
CODE:
'''python
[your code]
'''

EXPLAIN: [line by line explanation]"""

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=code_agent_prompt
)
print(f"Code Agent Response:\n{response.text[:600]}")
time.sleep(4)

## Demo 4: Chart Understnding
print("\n Demo 4: Data Analysis from Text")
print("-" * 20)

data_prompt = """Analyze this sales data and provide insights:

Month | Sales | Growth
Jan   | 45000 | -
Feb   | 52000 | +15.5%
Mar   | 48000 | -7.7%
Apr   | 61000 | +27.1%
May   | 73000 | +19.7%
Jun   | 68000 | -6.8%

Provide:
1. Best month and reason
2. Worst month and reason
3. Overall trend
4. Prediction for July
5. Recommendation"""

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=data_prompt
)
print(f"Data Analysis:\n{response.text[:500]}")

# Cleanup
if os.path.exists("sample.png"):
    os.remove("sample.png")

