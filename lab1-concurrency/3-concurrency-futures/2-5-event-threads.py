import threading
import time

event = threading.Event()

def setter():
    time.sleep(3)
    event.set()

def waiter():
    event.wait()
    print("Event occureed")

def watcher():
    while not event.is_set():
        print("Event did not occur")
        time.sleep(1)

threading.Thread(target=setter).start()
threading.Thread(target=waiter).start()
threading.Thread(target=watcher).start()