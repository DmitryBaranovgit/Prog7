import asyncio
import aiohttp

class AsyncScraper:
    def __init__(self, urls):
        self.urls = urls
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()
    
    async def fetch(self, url):
        async with self.session.get(url) as resp:
            print(url, resp.status)

async def main():
    with open("urls.txt") as f:
        urls = [u.strip() for u in f]

    async with AsyncScraper(urls) as scraper:
        await asyncio.gather(*(scraper.fetch(u) for u in urls))

asyncio.run(main())