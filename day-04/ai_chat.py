from google import genai

client = genai.Client(api_key="Your API Key")

print("=" * 40)
print("   My First AI Chat! 🤖")
print("   Type 'quit' to exit")
print("=" * 40)

while True:
    user = input("\nYou: ").strip()
    
    if user.lower() == "quit":
        print("AI: Goodbye! Keep learning! 🚀")
        break
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=user
    )
    print(f"AI: {response.text}")
