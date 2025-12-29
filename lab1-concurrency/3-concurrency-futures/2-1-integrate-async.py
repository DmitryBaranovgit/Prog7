import math
import timeit
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from functools import partial
from integrate import integrate

def integrate_async(f, a, b, *, n_jobs=2, n_iter=1000, executor_type="thread"):
    step = (b-a)/n_jobs

    Executor = ThreadPoolExecutor if executor_type == "thread" else ProcessPoolExecutor

    with Executor(max_workers=n_jobs) as executor:
        spawn = partial(executor.submit, integrate, f, n_iter=n_iter // n_jobs)
        futures = [
            spawn(a + i * step, a + (i + 1) * step)
            for i in range(n_jobs)
        ]
        return sum(f.result() for f in as_completed(futures))

if __name__ == "__main__":
    for n_jobs in (2, 4, 6):
        t = timeit.repeat(
            lambda: integrate_async(
                math.atan,
                0,
                math.pi / 2,
                n_iter=10**6,
                n_jobs=n_jobs,
                executor_type="thread"
            ),
            repeat=100,
            number=1
        )
        print(f"Threads {n_jobs}: {sum(t)/len(t)*1000:.2f} ms")

        p = timeit.repeat(
            lambda: integrate_async(
                math.atan,
                0,
                math.pi / 2,
                n_iter=10**6,
                n_jobs=n_jobs,
                executor_type="process"
            ),
            repeat=100,
            number=1
        )
        print(f"Processes {n_jobs}: {sum(p)/len(p)*1000:.2f} ms")