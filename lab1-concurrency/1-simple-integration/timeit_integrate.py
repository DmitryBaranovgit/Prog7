import timeit
from math import sin
from integrate import integrate

print(timeit.timeit(
    "integrate(sin, 0, 1, n_iter=10**4)",
    globals=globals(),
    number=1
))

print(timeit.timeit(
    "integrate(sin, 0, 1, n_iter=10**5)",
    globals=globals(),
    number=1
))

print(timeit.timeit(
    "integrate(sin, 0, 1, n_iter=10**6)",
    globals=globals(),
    number=1
))