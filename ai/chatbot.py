from groq import Groq
from dotenv import load_dotenv
import os

# Load .env
load_dotenv()
GroqAPIKey = os.getenv("GroqAPIKey")  # Make sure .env has GroqAPIKey=YOUR_KEY

# Initialize client
client = Groq(api_key=GroqAPIKey)

def ChatBot(user_input):
    try:
        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "user", "content": user_input}
            ],
            temperature=1,
            max_completion_tokens=8192,
            top_p=1,
            stream=True,
            stop=None
        )

        # Stream output
        Answer = ""
        for chunk in completion:
            Answer += chunk.choices[0].delta.content or ""
            print(chunk.choices[0].delta.content or "", end="")

        print()  # newline
        return Answer

    except Exception as e:
        return f"Error: {e}"

# Run chatbot
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        print("Bot:", ChatBot(user_input))
