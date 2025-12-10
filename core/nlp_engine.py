import time

text = "Hello World"

for char in text:
    print(char, end="", flush=True)
    time.sleep(0.1)   # delay 0.1 sec between letters

print()  # for new line
