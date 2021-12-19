import requests
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import logging
import aiohttp
import asyncio
from http.client import HTTPConnection
requests.packages.urllib3.disable_warnings()
from multiprocessing import Process, Pipe, freeze_support
from concurrent.futures import FIRST_COMPLETED
from aiohttp_socks import ProxyType, ProxyConnector, ChainProxyConnector

def rand_user_agent():

    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value] 
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

    rand_user_agent = {'User-Agent':user_agent_rotator.get_random_user_agent()}

    return rand_user_agent

url = 'https://ru.dotabuff.com'
proxy = {'https':'socks4://77.71.168.9:4145'}
prox = 'socks5://72.217.216.239:4145'
user_agent = rand_user_agent()

def req():

    HTTPConnection.debuglevel = 1
    logging.basicConfig()
    logging.getLogger().setLevel(logging.DEBUG)
    requests_log = logging.getLogger("urllib3")
    requests_log.setLevel(logging.DEBUG)
    requests_log.propagate = True

    r = requests.get(url = url, proxies = proxy, headers = user_agent, verify = False, cert = False, timeout = 6)

    return r

async def async_req():
    print('start')
    conn = ProxyConnector.from_url(prox)
    session_timeout = aiohttp.ClientTimeout(total=6,sock_connect=None,sock_read=None)

    async with aiohttp.ClientSession(connector = conn, headers = user_agent, timeout = session_timeout) as session:

        async with session.get(url, ssl = False) as r:
            
            await r.release()

            return r
                
async def abc():

    i = 0

    while True:

        await asyncio.sleep(0.2)

        print(i)
        i += 1

async def tasks():

    tasks = []

    tasks.append(asyncio.create_task(async_req()))

    done, pending = await asyncio.wait(tasks, timeout = 7, return_when = FIRST_COMPLETED)

    for future in pending:
        future.cancel()

    return done.pop().result()

#print(req().status_code)

if __name__ == '__main__':

    freeze_support()
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(tasks())
