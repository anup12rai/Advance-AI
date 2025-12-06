from groq import Groq
from dotenv import load_dotenv
import os
from utils.emoji_remover import remove_emojis

load_dotenv()
GroqAPIKey = os.getenv("GroqAPIKey") 
client = Groq(api_key=GroqAPIKey)

def ChatBot(user_input):
    try:
        # Remove emojis from user input
        clean_input = remove_emojis(user_input)

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[
                {"role": "user", "content": clean_input}
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
            content = chunk.choices[0].delta.content or ""
            content_no_emoji = remove_emojis(content)  # Remove emojis from output
            Answer += content_no_emoji
            print(content_no_emoji, end="")

        print()  # newline
        return Answer

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        print("Bot:", ChatBot(user_input))
