import timeit
from math import sin
from integrate_threaded import integrate_threaded

print(timeit.timeit(
    "integrate_threaded(sin, 0, 1, n_iter=10**5, n_threads=4)",
    globals=globals(),
    number=1
))

print(timeit.timeit(
    "integrate_threaded(sin, 0, 1, n_iter=10**6, n_threads=4)",
    globals=globals(),
    number=1
))