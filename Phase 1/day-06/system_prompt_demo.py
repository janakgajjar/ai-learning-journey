from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

system_prompt = """ You are a helpful AI tutot
for MCA students learning Agenti AI.
Always explain in simple terms .
Always give real life example.
Keep answers short and clear.
Always end with an encouraging message."""

print("-" * 20)
print(" AI tutor - System prompt")
print("-" * 20)

while True:
    user_input = input("\nYou: ").strip()

    if user_input.lower() == "quit":
        break

    full_prompt = f"{system_prompt}\n\nStudent: {user_input}"

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=full_prompt
    )

    print(f"AI tutor: {response.text}")