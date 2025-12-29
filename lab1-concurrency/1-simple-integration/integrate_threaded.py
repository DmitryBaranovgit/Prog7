import threading

def integrate_threaded(f, a, b, *, n_iter=1000, n_threads=4):
    step = (b-a) / n_iter
    total = 0.0
    lock = threading.Lock()

    def worker(start_iter, end_iter):
        nonlocal total
        local_sum = 0.0
        x = a + start_iter * step

        for _ in range(start_iter, end_iter):
            local_sum += f(x) * step
            x += step

        with lock:
            total += local_sum
    
    threads = []
    chunk = n_iter // n_threads

    for i in range(n_threads):
        start = i * chunk
        end = n_iter if i == n_threads - 1 else (i+1) * chunk
        t = threading.Thread(target=worker, args=(start, end))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    return total