from groq import Groq
from dotenv import load_dotenv
import os
from emoji_remove import remove_emojis  # Emoji cleaner
import time

# Optional COLORS
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

load_dotenv()
GroqAPIKey = os.getenv("GroqAPIKey") 
client = Groq(api_key=GroqAPIKey)
os.system("cls" if os.name == "nt" else "clear")

def print_header():
    print("\n" + BLUE + "-------------------- CHATBOT --------------------" + RESET)
    print(GREEN + "                Powered by Groq AI                " + RESET)
    print(BLUE + "--------------------------------------------------\n" + RESET)

def ChatBot(user_input):
    try:
        clean_input = remove_emojis(user_input)

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": clean_input}],
            temperature=1,
            max_completion_tokens=8192,
            top_p=1,
            stream=True,
            stop=None
        )

        print(YELLOW + "Bot:" + RESET, end=" ")

        Answer = ""
        for chunk in completion:
            content = chunk.choices[0].delta.content or ""
            clean_output = remove_emojis(content)

            # typing effect here 👇
            for ch in clean_output:
                print(ch, end="", flush=True)
                time.sleep(0.03)   

            Answer += clean_output

        print()
        return Answer

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    print_header()

    while True:
        user_input = input(GREEN + "You: " + RESET)
        if user_input.lower() in ["exit","quit","bye"]:
            print("\n" + BLUE + "------------------ Chat Ended ------------------" + RESET)
            break

        ChatBot(user_input)
