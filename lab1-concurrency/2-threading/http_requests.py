import threading
import requests

urls = [
    "https://httpbin.org/get",
    "https://httpbin.org/delay/1",
    "https://httpbin.org/uuid"
]

def fetch(url):
    response = requests.get(url)
    print(f"{url} -> статус {response.status_code}")

threads = []

for url in urls:
    t = threading.Thread(target=fetch, args=(url,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()