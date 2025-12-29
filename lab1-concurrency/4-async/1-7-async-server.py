import asyncio
import json

async def handle(reader, writer):
    while True:
        data = await reader.readline()
        if not data:
            break
        msg = json.loads(data.decode())
        writer.write(json.dumps(msg).encode() + b"\n")
        await writer.drain()

async def main():
    server = await asyncio.start_server(handle, "127.0.0.1", 8888)
    async with server:
        await server.serve_forever()

asyncio.run(main())