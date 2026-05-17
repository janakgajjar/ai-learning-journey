from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

question = "Write a creative tagline for an AI startup"

print("=" * 40)
print("   Temperature Demo!")
print("=" * 40)

# Low Temperature = Predictable
print("\n🥶 Low Temperature (0.1) — Predictable:")
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=question,
    config={"temperature": 0.1}
)
print(response.text)

# High Temperature = Creative
print("\n🔥 High Temperature (1.5) — Creative:")
response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents=question,
    config={"temperature": 1.5}
)
print(response.text)

print("\n" + "=" * 40)
print("Notice the difference? 🤔")