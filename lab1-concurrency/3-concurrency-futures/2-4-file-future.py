from concurrent.futures import ThreadPoolExecutor

def write_file():
    with open("data.txt", "w") as f:
        f.write("Hello")

def read_file():
    with open("data.txt") as f:
        return f.read()

with ThreadPoolExecutor() as ex:
    f1 = ex.submit(write_file)
    f1.result()
    f2 = ex.submit(read_file)
    print(f2.result())