import time
import json
import requests
from bs4 import BeautifulSoup
from loguru import logger

headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

def scrape_page_products_listing(url: str) -> list[str]:
    try:
        s = requests.Session()
        response = s.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        for s in soup.find_all("script"):
            if "landingPageUrl" in str(s.string):
                data = s.string.strip('window.__myx = ')
                json_data = json.loads(data)["searchData"]['results']
                product_urls = []
                for product in json_data['products']:
                    link = product["landingPageUrl"].replace("\u002F", '/')
                    url = "https://myntra.com/" + link
                    product_urls.append(url)

                return product_urls
    except Exception as e:
        logger.error(f"{e} in myntra")
        return []

def scrape_product(url: str):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser') 
        for s in soup.find_all("script"):
            if "pdpData" in str(s.string):
                data = s.string.strip('window.__myx = ')
                json_data = json.loads(data)['pdpData']

                seller_name = json_data["sellers"][0]['sellerName']
                seller_address = json_data["sellers"][0]['sellerAddress']['address']
                size_sellers = json_data['sizes'][0]['sizeSellerData']
                importer = size_sellers[0]['importerInfo']
                manufacturer = size_sellers[0]['manufacturerInfo']
                packer = size_sellers[0]['packerInfo']

                return [seller_name, seller_address, importer, manufacturer, packer]

    except Exception as e:
        logger.error(f"{e} in myntra")
        return None

def scrape_myntra(url: str):
    logger.info("Scraping Myntra")

    seller_data = []
    product_urls = scrape_page_products_listing(url)
    if product_urls:
      for index, product_url in enumerate(product_urls[:10]):
          logger.info(f"Myntra : {index+1}")
          data = scrape_product(product_url)
          if data:
              seller_data.append(data)

          time.sleep(1)

    return seller_data