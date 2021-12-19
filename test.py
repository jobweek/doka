from asyncio import tasks
import random
import time
import aiohttp
import asyncio
from concurrent.futures import FIRST_COMPLETED
from async_class import AsyncObject


async def req(i):

    while True:

        await asyncio.sleep(1)

        if random.randrange(1,10) == 5:
            print(i)
            return True

async def asynchronous():

    tasks = []

    for i in range(10):

        tasks.append(asyncio.create_task(req(i)))

    done, pending = await asyncio.wait(tasks, return_when = FIRST_COMPLETED)

    print(done.pop().result())

    for future in pending:
        future.cancel()

def main():

    ioloop = asyncio.get_event_loop()

    ioloop.run_until_complete(asynchronous())
    ioloop.close()

main()