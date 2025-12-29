import asyncio
import aiohttp
import asyncpg
import json

WEB_SERVER_URL = "https://rnacentral.org/api/v1/rna/"
DB_CONNECTION_STRING = (
    "postgres://reader:NWDMCE5xdipIjRrp@hh-pgsql-public.ebi.ac.uk:5432/pfmegrnargs"
)

async def fetch_http():
    async with aiohttp.ClientSession() as session:
        async with session.get(WEB_SERVER_URL) as resp:
            data = await resp.json()
            print(json.dumps(data, indent=2)[:500])

async def fetch_db():
    conn = await asyncpg.connect(DB_CONNECTION_STRING)
    rows = await conn.fetch("SELECT short_name FROM rnc_database LIMIT 5")
    await conn.close()
    print("DB result:", rows)

async def main():
    await asyncio.gather(fetch_http(), fetch_db())

asyncio.run(main())