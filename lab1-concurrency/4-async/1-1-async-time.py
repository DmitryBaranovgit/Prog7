import asyncio
from datetime import datetime

async def show_time():
    while True:
        print(datetime.now().strftime("%H:%M:%S"))
        await asyncio.sleep(1)

asyncio.run(show_time())