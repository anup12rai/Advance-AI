import os
import datetime
import requests
from googlesearch import search
from groq import Groq
from json import load, dump, JSONDecodeError

# Load env
Username = os.getenv("Username", "User")
Assistantname = os.getenv("Assistantname", "Jarvis")
GroqAPIKey = os.getenv("GROQ_API_KEY")

if GroqAPIKey is None:
    raise ValueError("GROQ_API_KEY environment variable not found")

client = Groq(api_key=GroqAPIKey)

# Choose a valid Groq model — check available models then pick one.
def get_available_models():
    url = "https://api.groq.com/openai/v1/models"
    resp = requests.get(url, headers={
        "Authorization": f"Bearer {GroqAPIKey}",
        "Content-Type": "application/json"
    })
    resp.raise_for_status()
    data = resp.json()
    return [m["id"] for m in data.get("data", [])]

available = get_available_models()
print("Available models:", available)

# You can choose a default — but make sure it's in available.
DEFAULT_MODEL = None
for m in ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "llama3-70b-8192"]:
    if m in available:
        DEFAULT_MODEL = m
        break

if DEFAULT_MODEL is None:
    raise RuntimeError("None of the default models are available. Please pick a valid model from the printed list.")

print("Using model:", DEFAULT_MODEL)

System = (
    f"Hello, I am {Username}. You are a very accurate and advanced AI chatbot named {Assistantname} "
    "which has real-time up-to-date information from the internet. "
    "Provide answers in a professional way with proper grammar, punctuation, and clarity."
)

if not os.path.exists("Data"):
    os.makedirs("Data")

try:
    with open("Data/ChatLog.json", "r") as f:
        messages = load(f)
except (FileNotFoundError, JSONDecodeError):
    messages = []
    with open("Data/ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

def GoogleSearch(query):
    try:
        results = list(search(query, num_results=5, lang="en"))
        Answer = f"The main points from the search results for '{query}' are:\n[start]\n"
        for i, url in enumerate(results, 1):
            Answer += f"{i}. {url}\n"
        Answer += "[end]\n"
        return Answer
    except Exception as e:
        return f"Google search failed: {e}"

def AnswerModifier(Answer):
    lines = Answer.split("\n")
    non_empty = [line for line in lines if line.strip()]
    return "\n".join(non_empty)

SystemChatBot = [
    {"role": "system", "content": System},
    {"role": "assistant", "content": f"Hello, I am {Assistantname}. How can I help you today?"}
]

def Information():
    now = datetime.datetime.now()
    return (
        "Use the real-time information if needed:\n"
        f"Day: {now.strftime('%A')}\n"
        f"Date: {now.strftime('%d')}\n"
        f"Month: {now.strftime('%B')}\n"
        f"Year: {now.strftime('%Y')}\n"
        f"Time: {now.strftime('%H:%M:%S')}\n"
    )

def RealtimeSearchEngine(prompt):
    global SystemChatBot, messages

    messages.append({"role": "user", "content": prompt})
    SystemChatBot.append({"role": "system", "content": GoogleSearch(prompt)})

    try:
        completion = client.chat.completions.create(
            model=DEFAULT_MODEL,
            messages=SystemChatBot + [{"role": "system", "content": Information()}] + messages,
            temperature=0.7,
            max_tokens=2048,
            top_p=1,
            stream=True
        )
    except Exception as e:
        # print error and return
        return f"Error with Groq API call: {e}"

    Answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            Answer += chunk.choices[0].delta.content

    Answer = Answer.strip().replace("</s>", "")
    messages.append({"role": "assistant", "content": Answer})

    with open("Data/ChatLog.json", "w") as f:
        dump(messages, f, indent=4)

    SystemChatBot.pop()
    return AnswerModifier(Answer)

if __name__ == "__main__":
    print(f"{Assistantname}: Hello! I am your assistant. Type 'exit' to quit.")
    while True:
        prompt = input("You: ")
        if prompt.lower() in ("exit", "quit"):
            break
        response = RealtimeSearchEngine(prompt)
        print(f"{Assistantname}: {response}")
