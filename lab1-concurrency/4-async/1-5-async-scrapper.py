import asyncio
import aiohttp

class AsyncScrapper:
    def __init__(self, urls):
        self.urls = urls
    
    async def fetch(self, session, url):
        async with session.get(url) as resp:
            text = await resp.text()
            print(url, "->", len(text))
    
    async def run(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session, url) for url in self.urls]
            await asyncio.gather(*tasks)

with open("urls.txt") as f:
    urls = [line.strip() for line in f]

scraper = AsyncScrapper(urls)
asyncio.run(scraper.run())