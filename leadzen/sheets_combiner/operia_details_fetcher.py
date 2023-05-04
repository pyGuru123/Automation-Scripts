import asyncio
import pandas as pd
from loguru import logger

from app.config import API_CONFIG_OPERIA_FETCHER_API
from app.third_party.company.operia import search_company_details_with_operia_api_server
from app.third_party.profile.operia import search_person_details_with_operia_api_server

async def get_company_info(urls):
    results = await search_company_details_with_operia_api_server(urls)
    results_with_company_details = []

    for result in results:
        linkedin_id = result["linkedin_url"]
        data = result.get("data", {})
        if data is not None and "company_name" in data:
            company_info = {}
            company_info["id"] = linkedin_id
            company_info["Company Linkedin Url"] = data.get("social_url", "")
            company_info["Company"] = data.get("company_name", "")
            company_info["Website"] = str(data.get("website", "")).split(".com")[0] + ".com"
            company_info["location"] = data.get("locations", [])
            company_info["Industry"] = data.get("industry", "")
            company_info["# Employees"] = data.get("employees_num", 0)
            results_with_company_details.append(company_info)
            
    return results_with_company_details

def get_linkedin_urls_with_no_company(df):
    company_linkedin_df = df.loc[df["Company Linkedin Url"].notnull() & df["# Employees"].isnull() & df["Industry"].isnull()]
    company_linkedin_urls = company_linkedin_df["Company Linkedin Url"].tolist()
    company_linkedin_urls = list(filter(lambda x: x != "No Company Page", company_linkedin_urls))

    return company_linkedin_urls

async def fetch_company_details(df):
    company_linkedin_urls = get_linkedin_urls_with_no_company(df)
    return await get_company_info(company_linkedin_urls)