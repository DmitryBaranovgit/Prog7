import threading

def worker():
    print(f"Выполняется поток: {threading.current_thread().name}")


threads = []

for i in range(5):
    t = threading.Thread(target=worker, name=f"Thread-{i}")
    threads.append(t)
    t.start()

for t in threads:
    t.join()