import math

def integrate(f, a, b, *, n_iter=1000):
    step = (b-a) / n_iter
    result = 0.0
    x = a

    for _ in range(n_iter):
        result += f(x) * step
        x += step

    return result

def integrate2(f, a, b, n_iter=1000):
    step = (b-a) / n_iter
    result = 0.0
    x = a

    for _ in range(n_iter):
        result += f(x) * step
        x += step

    return result

if __name__ == "__main__":
    import math
    print(integrate(math.sin, 0, 1, n_iter=100))
    print(integrate2(math.cos, 0, 1, 100))