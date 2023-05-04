import httpx
import asyncio
import numpy as np
import pandas as pd
from loguru import logger
from aiodecorators import Semaphore
from aiolimiter import AsyncLimiter

from app.config import (
    API_CONFIG_VALUE_SERP_KEY,
    API_CONFIG_HTTP_CALL_TIMEOUT_IN_SECONDS,
    API_CONFIG_SERP_RATE_LIMIT_MAX_CALL_COUNT,
    API_CONFIG_SERP_RATE_LIMIT_DURATION_IN_SECONDS,
)
from app.valueserp import search_value_serp_api_with_limiter

def get_company_names(df):
    df.replace(['None.com'], np.nan, inplace=True)
    company_name_df = df.loc[df["Company"].notnull() & df["Website"].isnull()]
    return company_name_df["Company"].tolist()

async def company_website(query_list: list[str]):
    rate_limiter = AsyncLimiter(
        API_CONFIG_SERP_RATE_LIMIT_MAX_CALL_COUNT,
        API_CONFIG_SERP_RATE_LIMIT_DURATION_IN_SECONDS,
    )
    async with httpx.AsyncClient() as client:
        coroutines = [
            coroutine_company_website(
                client=client,
                limiter=rate_limiter,
                query=query,
                i=index,
            )
            for index, query in enumerate(query_list)
        ]

        return await asyncio.gather(*coroutines)


async def coroutine_company_website(
    i, query, client: httpx.AsyncClient, limiter: AsyncLimiter
):
    try:
        if i != 0 and i % 50 == 0:
            logger.info(f"index no: {i}")
        return await get_company_website(query, client, limiter)
    except Exception as e:
        logger.critical(f"Error {i} {e}")

@Semaphore(100)
async def get_company_website(query: str, client, limiter):
    logger.debug(f"searching for {query}")
    my_try = 0

    while my_try < 5:  # trying 5 times because sometimes valueserp failes
        try:
            async with limiter:
                result = []
                results = await search_value_serp_api_with_limiter(
                    query=f"website for {query}", client=client, limiter=limiter
                )
                if "organic_results" in results:
                    organic_results = results["organic_results"]

                    for organic_result in organic_results:
                        if "link" in organic_result:
                            result.append(organic_result["link"])
                    break
                my_try += 1
        except Exception as e:
            result = None
            my_try += 1
            logger.warning(f"value serp failed {e} trying again for {my_try} time(s)")

    return [query] + result


def get_companies_with_no_company_linkedin(df):
    company_df = df.loc[df["Company"].notnull() & df["Company Linkedin Url"].isnull()]
    return company_df["Company"].tolist()

def fill_companies_with_company_linkedin(df, linkedin_ids):
    logger.info(linkedin_ids)
    count = 0
    for ids in linkedin_ids:
        if len(ids) > 1:
            try:
                df.loc[df['Company'] == ids[0], ["Company Linkedin Url"]] = [ids[1]]
                count += 1
            except:
                logger.info(f"{ids[0]}")

    logger.info(f"{count} rows affected")
    return df

def fill_company_website(df, company_websites):
    for website in company_websites:
        if len(website) > 1:
            df.loc[df['Company'] == website[0], ["Website"]] = [website[1]]

    return df