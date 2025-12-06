from googlesearch import search
from groq import Groq
from json import load, dump, JSONDecodeError
import datetime
from dotenv import dotenv_values
import os

# Load environment variables
env_vars = dotenv_values(".env")
Username = env_vars.get("Username", "User")
Assistantname = env_vars.get("Assistantname", "Jarvis")
GroqAPIKey = env_vars.get("GroqAPIKey")

# Initialize Groq API client
client = Groq(api_key=GroqAPIKey)

# Define system message template
System = f"""Hello, I am {Username}. You are a very accurate and advanced AI chatbot named {Assistantname} which has real-time up-to-date information from the internet.
Provide answers in a professional way with proper grammar, punctuation, and clarity."""

# Ensure Data folder exists
if not os.path.exists("Data"):
    os.makedirs("Data")

# Initialize chat log
try:
    with open("Data/ChatLog.json", "r") as f:
        messages = load(f)
except (FileNotFoundError, JSONDecodeError):
    messages = []
    with open("Data/ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

# Function for Google search
def GoogleSearch(query):
    try:
        results = list(search(query, num_results=5, lang='en'))
        Answer = f"The main points from the search results for '{query}' are:\n[start]\n"
        for i, url in enumerate(results, 1):
            Answer += f"{i}. {url}\n"
        Answer += "[end]\n"
        return Answer
    except Exception as e:
        return f"Google search failed: {e}"

# Function to clean and modify the answer
def AnswerModifier(Answer):
    lines = Answer.split('\n')
    non_empty_lines = [line for line in lines if line.strip()]
    return "\n".join(non_empty_lines)

# Initialize system messages
SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "assistant", "content": f"Hello, I am {Assistantname}. How can I help you today?"}
]

# Function to generate real-time information
def Information():
    now = datetime.datetime.now()
    data = (
        "Use the real-time information if needed:\n"
        f"Day: {now.strftime('%A')}\n"
        f"Date: {now.strftime('%d')}\n"
        f"Month: {now.strftime('%B')}\n"
        f"Year: {now.strftime('%Y')}\n"
        f"Time: {now.strftime('%H:%M:%S')}\n"
    )
    return data

# Main function for real-time search engine and chatbot interaction
def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    # Append user message to chat log
    messages.append({"role": "user", "content": prompt})

    # Add search results to system messages
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    # Send to Groq AI (updated model)
    completion = client.chat.completions.create(
        model="llama3-70b",  # fixed model
        messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
        temperature=0.7,
        max_tokens=2048,
        top_p=1,
        stream=True  # can be True or False
    )

    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.strip().replace("</s>", "")

    # Append assistant response to chat log
    messages.append({"role": "assistant", "content": Answer})

    # Save chat log
    with open("Data/ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    # Remove last search system message to avoid duplication
    SystemChatBot.pop()

    return AnswerModifier(Answer)

# Main loop for user input
if __name__ == "__main__":
    print(f"{Assistantname}: Hello! I am your assistant. Type 'exit' to quit.")
    while True:
        prompt = input("You: ")
        if prompt.lower() in ["exit", "quit"]:
            break
        response = RealtimeSearchEngine(prompt)
        print(f"{Assistantname}: {response}")
