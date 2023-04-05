import time
from loguru import logger
from bs4 import BeautifulSoup
from typing import List, Union

from app.sellers_scraper.utils import get_random_time, get_page_content


def scrape_page_products_listing(url: str) -> list[str]:
    try:
        soup = get_page_content(url)
        logger.info(soup.title)
        links = soup.select(
            "[class*='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']"
        )
        product_urls = []
        for link in links:
            url = "https://amazon.com" + link.get("href")
            if "sspa" not in url:
                product_urls.append(url)

        return product_urls
    except Exception as e:
        logger.error(e)
        return []


def get_business_rating(soup: BeautifulSoup) -> str:
    try:
        rating = soup.find(
            "span", attrs={"id": "effective-timeperiod-rating-year-description"}
        ).text
    except:
        rating = ""

    return rating


def get_business_name(soup: BeautifulSoup) -> str:
    try:
        seller_name = soup.find("h1", attrs={"id": "seller-name"}).text
    except:
        seller_name = ""

    return seller_name


def get_business_address(soup: BeautifulSoup) -> str:
    try:
        seller_address = ""
        address_lines = soup.select("[class*='a-row a-spacing-none indent-left']")
        for line in address_lines:
            seller_address += line.text + "\n"
    except:
        seller_address = ""

    return seller_address


def scrape_product(url: str) -> Union[List[str], None]:
    try:
        soup = get_page_content(url)
        seller_id = soup.find("input", attrs={"id": "deliveryBlockSelectMerchant"})
        if not seller_id:
            return None

        seller_profile_url = (
            f"https://www.amazon.com/sp?ie=UTF8&seller={seller_id['value']}"
        )
        soup = get_page_content(seller_profile_url)
        rating = get_business_rating(soup)
        seller_name = get_business_name(soup)
        seller_address = get_business_address(soup)

        return [rating, seller_name, seller_address]

    except:
        return None


def scrape_amazon(url: str) -> List[List[str]]:
    logger.info("Scraping Amazon")

    seller_data = []
    product_urls = scrape_page_products_listing(url)
    for index, product_url in enumerate(product_urls[:3]):
        logger.info(f"Amazon : {index+1}")
        data = scrape_product(product_url)
        if data:
            seller_data.append(data)

        time.sleep(get_random_time())

    return seller_data
