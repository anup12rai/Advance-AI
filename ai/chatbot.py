from groq import Groq
from dotenv import load_dotenv
import json
import sys
import os
from datetime import datetime

# ---------------------------
# FIX PYTHON IMPORT PATH
# ---------------------------
# Add project root (Advance-AI) to sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT_DIR)

# Now imports work
from core.text_to_speech import TextToSpeech
from ai.emoji_remove import remove_emojis


# ---------------------------
# Load ENV + Groq API
# ---------------------------
load_dotenv()
GroqAPIKey = os.getenv("GroqAPIKey")
client = Groq(api_key=GroqAPIKey)

   # initialize TTS


# ---------------------------
# Save conversation to JSON
# ---------------------------
def save_memory(user_msg, bot_msg):
    data = {
        "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_msg,
        "bot": bot_msg
    }

    # Create memory if missing
    if not os.path.exists("memory.json"):
        with open("memory.json", "w") as f:
            json.dump([], f, indent=4)

    # Load old history
    with open("memory.json", "r") as f:
        history = json.load(f)

    # Add new data
    history.append(data)

    # Save back
    with open("memory.json", "w") as f:
        json.dump(history, f, indent=4)


# ---------------------------
# CHATBOT FUNCTION
# ---------------------------
def ChatBot(user_input):
    try:
        clean_input = remove_emojis(user_input)

        completion = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": clean_input}],
            temperature=1,
            max_completion_tokens=8192,
            top_p=1,
            stream=False
        )

        reply = completion.choices[0].message.content
        reply = remove_emojis(reply)

        # Save chat
        save_memory(user_input, reply)

        # Speak the output
        

        return reply

    except Exception as e:
        return f"Error: {e}"


# ---------------------------
# MAIN LOOP
# ---------------------------
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        bot_reply = ChatBot(user_input)
        print("Bot:", bot_reply)
        TextToSpeech(bot_reply)
