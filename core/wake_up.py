WAKE_WORD = "jarvis"  # choose your wake-up word

user_input = input("You: ").lower()

if WAKE_WORD in user_input:
    print("Bot: Hello! How can I help you?")
else:
    print("Bot: Say 'Jarvis' to start talking to me.")
