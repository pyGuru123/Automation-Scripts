import time
import requests
import json
from bs4 import BeautifulSoup
from loguru import logger

headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Accept-Language" : "en-US"
}

def scrape_page_products_listing(url: str) -> list[str]:
    try:
        response = requests.get(url, headers=headers)
        html = response.content
        soup = BeautifulSoup(html, 'html.parser')
        links = soup.select("[class*='s1Q9rs']")
        product_urls = []
        for link in links:
            url = "https://flipkart.com" + link.get('href')
            product_urls.append(url)

        return product_urls
    except:
        return []

def get_seller_name_and_rating(soup):
    try:
        seller_name = ""
        rating = ""
        name = soup.select_one("[id$='sellerName']").text
        for ch in name:
            if ch.isalpha() or ch==" ":
                seller_name += ch
            else:
                rating += ch
    except:
        seller_name, rating = "", ""

    return seller_name, rating

def get_seller_address(soup):
    try:
        for s in soup.find_all("script"):
            if "callouts" in str(s.string):
                data = str(s.string).strip('window.__INITIAL_STATE__ = ')
                json_data = json.loads(data.strip(';'))
                data = json_data['pageDataV4']['page']['data']['10005']
                for key in data:
                    if key['id'] == 28:
                        seller_info = key['widget']['data']['listingManufacturerInfo']['value']['detailedComponents']
                        manufacturer = seller_info[0]['value']['callouts'][0]
                        if len(seller_info) > 1:
                            packer = seller_info[-1]['value']['callouts'][0]
                        else:
                            packer = ""

                        return manufacturer, packer
    except Exception as e:
        logger.error(f"{e} in Flipkart")
        return "", ""

def scrape_product(url: str):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser') 
        seller_name, rating = get_seller_name_and_rating(soup)
        manufacturer, packer = get_seller_address(soup)

        return [rating, seller_name, manufacturer, packer]

    except Exception as e:
        logger.error(f"{e} in Flipkart @ {url}")
        return None

def scrape_flipkart(url: str):
    logger.info("Scraping Flipkart")

    seller_data = []
    product_urls = scrape_page_products_listing(url)
    if product_urls:
        for index, product_url in enumerate(product_urls[:10]):
            logger.info(f"Flipkart : {index+1}")
            data = scrape_product(product_url)
            if data:
                seller_data.append(data)

            time.sleep(1)

    return seller_data