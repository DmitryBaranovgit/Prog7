import asyncio

async def task1():
    await asyncio.sleep(2)
    return "Result 1"

async def task2():
    await asyncio.sleep(1)
    return "Result 2"

async def process(results):
    for r in results:
        print("Processed:", r)

async def main():
    results = await asyncio.gather(task1(), task2())
    await process(results)

asyncio.run(main())