def integrate(f, a, b, *, n_iter=1000):
    step = (b-a)/n_iter
    s = 0.0
    x = a
    for _ in range(n_iter):
        s += f(x) * step
        x += step
    return s