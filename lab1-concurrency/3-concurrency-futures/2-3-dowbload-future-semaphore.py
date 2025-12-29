import requests
from concurrent.futures import ThreadPoolExecutor
from threading import Semaphore

urls = [
    "https://via.placeholder.com/150",
    "https://via.placeholder.com/200",
    "https://via.placeholder.com/250"
]

sem = Semaphore(2)

def download(url, i):
    with sem:
        r = requests.get(url)
        with open(f"img_{i}.png", "wb") as f:
            f.write(r.content)

with ThreadPoolExecutor() as ex:
    futures = [ex.submit(download, u, i) for i, u, in enumerate(urls)]