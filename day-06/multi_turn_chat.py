from google import genai
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

conversation_history = []

print("=" * 40)
print("   Multi-Turn AI Chat!")
print("   AI previous messages યાદ રાખે!")
print("=" * 40)

while True:
    user_input = input("\nYou: ").strip()
    
    if user_input.lower() == "quit":
        print("AI: Goodbye!")
        break
    
    conversation_history.append(f"User: {user_input}")
    full_context = "\n".join(conversation_history)
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=full_context
    )
    
    ai_response = response.text
    conversation_history.append(f"AI: {ai_response}")
    print(f"AI: {ai_response}")