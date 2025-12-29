import threading
import requests

urls = [
    "https://via.placeholder.com/150",
    "https://via.placeholder.com/200",
    "https://via.placeholder.com/250"
]

def download(url, index):
    response = requests.get(url)
    with open(f"image_{index}.png", "wb") as f:
        f.write(response.content)
    print(f"Файл image_{index}.png загружен")

threads = []

for i, url in enumerate(urls):
    t = threading.Thread(target=download, args=(url, i))
    threads.append(t)
    t.start()

for t in threads:
    t.join()