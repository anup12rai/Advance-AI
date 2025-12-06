import os
import subprocess
import asyncio
from difflib import get_close_matches
from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import keyboard
import requests

# ----------------------------
# Environment & Groq Client
# ----------------------------
env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")
if not GroqAPIKey:
    raise ValueError("GroqAPIKey not found in .env")
client = Groq(api_key=GroqAPIKey)

# System messages for AI
SystemChatBot = [
    {"role": "system", "content": "Hello, I am your AI assistant. Write content like professional letters, guides, or applications."}
]
messages = []

# User agent for scraping
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36'

# ----------------------------
# Known apps for fuzzy matching
# ----------------------------
KNOWN_APPS = ["facebook", "chrome", "notepad", "spotify", "whatsapp", "calculator", "excel", "word"]
CONTENT_KEYWORDS = ["letter", "content", "application", "rules", "document"]

# ----------------------------
# Helper Functions
# ----------------------------
def GoogleSearch(topic: str):
    search(topic)
    print(f"[green]Google search done for: {topic}[/green]")
    return True

def OpenNotepad(file_path: str):
    subprocess.Popen(['notepad.exe', file_path])

def ContentWritterAI(prompt: str):
    messages.append({"role": "user", "content": f"{prompt} in a professional format."})
    completion = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=SystemChatBot + messages,
        max_tokens=2048,
        temperature=0.7,
        top_p=1,
        stream=True
    )
    answer = ""
    for chunk in completion:
        if chunk.choices[0].delta.content:
            answer += chunk.choices[0].delta.content
    answer = answer.replace("</s>", "")
    messages.append({"role": "assistant", "content": answer})
    return answer

def Content(topic: str):
    topic_clean = topic.replace("content ", "")
    ai_content = ContentWritterAI(topic_clean)
    file_path = os.path.join("Data", f"{topic_clean.lower().replace(' ', '')}.txt")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(ai_content)
    OpenNotepad(file_path)
    print(f"[green]Content generated and opened for: {topic_clean}[/green]")
    return True

def YouTubeSearch(topic: str):
    url = f"https://www.youtube.com/results?search_query={topic}"
    webopen(url)
    print(f"[green]YouTube search done for: {topic}[/green]")
    return True

def PlayYoutube(query: str):
    playonyt(query)
    print(f"[green]Playing YouTube video: {query}[/green]")
    return True

def extract_link(html):
    if not html:
        return []
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.find_all('a', {'jsname': 'UWckNb'})
    return [link.get('href') for link in links]

def search_google(query, sess=requests.session()):
    url = f'https://www.google.com/search?q={query}'
    headers = {"User-Agent": useragent}
    response = sess.get(url, headers=headers)
    return response.text if response.status_code == 200 else None

def OpenApp(app: str):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        print(f"[green]Opened {app} successfully[/green]")
        return True
    except Exception:
        html = search_google(app)
        links = extract_link(html)
        if links:
            webopen(links[0])
            print(f"[yellow]Opened {app} in browser as fallback[/yellow]")
        else:
            print(f"[red]No web link found for {app}[/red]")
        return True

def CloseApp(app: str):
    if "chrome" in app.lower():
        print("[yellow]Skipping Chrome close[/yellow]")
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True)
            print(f"[green]Closed {app} successfully[/green]")
            return True
        except Exception as e:
            print(f"[red]Failed to close {app}: {e}[/red]")
            return False

def System(command: str):
    mapping = {
        "mute": 'volume mute',
        "unmute": 'volume mute',
        "volume up": 'volume up',
        "volume down": 'volume down'
    }
    key = mapping.get(command)
    if key:
        keyboard.press_and_release(key)
        print(f"[green]Executed system command: {command}[/green]")
    else:
        print(f"[yellow]Unknown system command: {command}[/yellow]")
    return True

# ----------------------------
# Async Command Executor with fuzzy matching
# ----------------------------
async def TranslateAndExecute(commands: list[str]):
    funcs = []

    for command in commands:
        command_clean = command.strip().lower()

        # Check for known apps (exact or fuzzy match)
        if command_clean in KNOWN_APPS:
            funcs.append(asyncio.to_thread(OpenApp, command_clean))
            continue
        match = get_close_matches(command_clean, KNOWN_APPS, n=1, cutoff=0.7)
        if match:
            funcs.append(asyncio.to_thread(OpenApp, match[0]))
            continue

        # Keyword-based commands
        if command_clean.startswith("open "):
            funcs.append(asyncio.to_thread(OpenApp, command_clean.removeprefix("open ")))
        elif command_clean.startswith("close "):
            funcs.append(asyncio.to_thread(CloseApp, command_clean.removeprefix("close ")))
        elif command_clean.startswith("play "):
            funcs.append(asyncio.to_thread(PlayYoutube, command_clean.removeprefix("play ")))
        elif command_clean.startswith("google search "):
            funcs.append(asyncio.to_thread(GoogleSearch, command_clean.removeprefix("google search ")))
        elif command_clean.startswith("youtube search "):
            funcs.append(asyncio.to_thread(YouTubeSearch, command_clean.removeprefix("youtube search ")))
        elif command_clean.startswith("system "):
            funcs.append(asyncio.to_thread(System, command_clean.removeprefix("system ")))
        elif any(keyword in command_clean for keyword in CONTENT_KEYWORDS):
            # Generate AI content
            async def content_and_notify():
                Content(command_clean)
                print(f"[cyan]Sir, here is your text for '{command_clean}'[/cyan]")
            funcs.append(content_and_notify())
        else:
            print(f"[yellow]No function found for command: {command_clean}[/yellow]")

    results = await asyncio.gather(*funcs)
    return results

# ----------------------------
# Main loop
# ----------------------------
async def main():
    
    print("[cyan]Welcome to your AI assistant! Type 'exit' to quit.[/cyan]")
    while True:
        user_input = input("[bold green]Command > [/bold green]").strip()
        if user_input.lower() in ["exit", "quit"]:
            print("[cyan]Goodbye![/cyan]")
            break
        await TranslateAndExecute([user_input])

if __name__ == "__main__":
    asyncio.run(main())
