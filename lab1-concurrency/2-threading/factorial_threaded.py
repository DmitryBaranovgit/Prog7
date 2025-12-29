import threading

def factorial_threaded(n, n_threads=4):
    result = 1
    lock = threading.Lock()

    def worker(start, end):
        nonlocal result
        local = 1
        for i in range(start, end + 1):
            local *= i
        with lock:
            result *= local
    
    step = n // n_threads
    threads = []

    for i in range(n_threads):
        start = i * step + 1
        end = n if i == n_threads - 1 else (i + 1) * step
        t = threading.Thread(target=worker, args=(start, end))
        threads.append(t)
        t.start()
    
    for t in threads:
        t.join()

    return result

print(factorial_threaded(10))