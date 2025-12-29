import asyncio
import json

async def main():
    reader, writer = await asyncio.open_connection("127.0.0.1", 8888)
    while True:
        text = input(">> ")
        writer.write(json.dumps({"msg": text}).encode() + b"\n")
        await writer.drain()
        data = await reader.readline()
        print("Echo:", data.decode())
    
asyncio.run(main())