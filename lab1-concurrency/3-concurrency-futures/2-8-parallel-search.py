import os
import threading

found = threading.Event()

def search(files, target):
    for f in files:
        if found.is_set():
            return
        if target in f:
            print("Found:", f)
            found.set()

files = os.listdir(".")
chunks = [files[i::4] for i in range(4)]

for ch in chunks:
    threading.Thread(target=search, args=(ch, "test")).start()