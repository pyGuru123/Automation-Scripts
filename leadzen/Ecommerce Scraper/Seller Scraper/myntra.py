import time
import json
from loguru import logger
from bs4 import BeautifulSoup
from typing import List, Union

from app.sellers_scraper.utils import get_random_time, get_page_content


def scrape_page_products_listing(url: str) -> list[str]:
    try:
        soup = get_page_content(url)
        for s in soup.find_all("script"):
            if "landingPageUrl" in str(s.string):
                data = s.string.strip("window.__myx = ")
                json_data = json.loads(data)["searchData"]["results"]
                product_urls = []
                for product in json_data["products"]:
                    link = product["landingPageUrl"].replace("\u002F", "/")
                    url = "https://myntra.com/" + link
                    product_urls.append(url)

                return product_urls
    except Exception as e:
        logger.error(f"{e} in myntra")
        return []


def scrape_product(url: str) -> Union[List[str], None]:
    try:
        soup = get_page_content(url)
        for s in soup.find_all("script"):
            if "pdpData" in str(s.string):
                data = s.string.strip("window.__myx = ")
                json_data = json.loads(data)["pdpData"]

                seller_name = json_data["sellers"][0]["sellerName"]
                seller_address = json_data["sellers"][0]["sellerAddress"]["address"]
                size_sellers = json_data["sizes"][0]["sizeSellerData"]
                importer = size_sellers[0]["importerInfo"]
                manufacturer = size_sellers[0]["manufacturerInfo"]
                packer = size_sellers[0]["packerInfo"]

                return [seller_name, seller_address, importer, manufacturer, packer]

    except Exception as e:
        logger.error(f"{e} in myntra")
        return None


def scrape_myntra(url: str) -> List[List[str]]:
    logger.info("Scraping Myntra")

    seller_data = []
    product_urls = scrape_page_products_listing(url)
    for index, product_url in enumerate(product_urls[:3]):
        logger.info(f"Myntra : {index+1}")
        data = scrape_product(product_url)
        if data:
            seller_data.append(data)

        time.sleep(get_random_time())

    return seller_data
