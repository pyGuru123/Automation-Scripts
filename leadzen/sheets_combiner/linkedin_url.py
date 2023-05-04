import asyncio
import aiohttp
import csv
import re
import time
import pandas as pd
from aiodecorators import Semaphore
from app.config import API_CONFIG_VALUE_SERP_KEY
import json

count = 0


@Semaphore(100)
async def fetch(session, q):
    global count
    count = count + 1
    print(count)
    if count > 300:
        print("sleeping")
        time.sleep(100)
        count = 0

    print("q coming ", q)
    params = {"api_key": API_CONFIG_VALUE_SERP_KEY, "q": f"{q} linkedin", "gl": "in"}

    try:
        async with session.get(
            "https://api.valueserp.com/search", params=params
        ) as response:
            x = await response.read()
            return json.loads(x.decode("utf8"))
    except Exception as e:
        print("error ", e)
        return "None"

try:
    async def write_result(linkedin_url, q):
        # async with asyncio.Lock():
        #     writer.writerow([q, linkedin_url])
        return [q, linkedin_url]
except Exception as e:
    print("error", e)

try:
    async def validate_page(session, q):
        result = []
        res = await fetch(session, q)
        if "organic_results" in res:
            organic_results = res["organic_results"]
            for organic_result in organic_results:
                if "link" in organic_result:
                    result.append(organic_result["link"])
                break

        linkedin_url = ""
        if result:
            linkedin_list = [url for url in result if "linkedin" in url]
            if linkedin_list:
                linkedin_url = linkedin_list[0]

        return await write_result(linkedin_url, q)
except Exception as e:
    print("error", e)


async def linkedin_url_fast(company_name: list[str]):
    try:
        connector = aiohttp.TCPConnector(limit=100, force_close=True)
        async with aiohttp.ClientSession(connector=connector) as session:
            aws = [validate_page(session, q.strip()) for q in company_name]
            d = await asyncio.gather(*aws)
            return d
            print("!--- finished processing")
    except Exception as e:
        print("error ", e)


loop = asyncio.get_event_loop()