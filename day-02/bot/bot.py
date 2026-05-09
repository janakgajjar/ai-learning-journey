print("=" * 40)
print("   Welcome to AIBot v1.0")
print("=" * 40)

while True:
    user_input = input("\nYou: ").lower().strip()

    if user_input == "quit":
        print("AIBot: Goodbye! Keep learning! ")
        break
    elif "hello" in user_input or "hi" in user_input:
        print("AIBot: Hello! Great to meet you!")
    elif "name" in user_input:
        print("AIBot: I am AIBot - built by an MCA student!")
    elif "joke" in user_input:
        print("AIBot: Why do programmers prefer dark mode?")
        print("       Because light attracts bugs! ")
    elif "fact" in user_input:
        print("AIBot: Python was named after Monty Python!")
    else:
        print(f"AIBot: I heard '{user_input}' - still learning!")