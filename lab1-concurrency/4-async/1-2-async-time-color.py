import asyncio
from datetime import datetime
from termcolor import colored
from pynput import keyboard

stop = False

def on_press(key):
    global stop
    if key == keyboard.Key.esc:
        stop = True
        return False

async def show_time():
    while not stop:
        now = datetime.now()
        text = (
            colored(now.strftime("%Y-%m-%d"), "green") + " " +
            colored(now.strftime("%H:%M:%S"), "cyan")
        )
        print("\r" + text, end="")
        await asyncio.sleep(1)

listener = keyboard.Listener(on_press=on_press)
listener.start()

asyncio.run(show_time())
print("\nStopped")