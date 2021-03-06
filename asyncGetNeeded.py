import asyncio
from aiohttp import ClientSession

async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()

async def fetchHead(url, session):
    async with session.head(url) as response:
        return response.status       

async def run(r):
    url = "http://localhost:8080/{}"
    censusLink = "https://census.daybreakgames.com/files/ps2/images/static/" #the urls for each
    psarchivesLink = "https://storage.googleapis.com/planetside/static/"
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for i in range(r):
            task = asyncio.ensure_future(fetch(url.format(i), session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        print(responses)

def print_responses(result):
    print(result)

loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(4    ))
loop.run_until_complete(future)