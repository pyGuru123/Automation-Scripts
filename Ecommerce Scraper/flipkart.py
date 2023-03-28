import time
import requests
import json
from bs4 import BeautifulSoup

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

def get_product_rating(soup):
    try:
        rating = soup.select_one("[class*='_3LWZlK']").text
    except:
        rating = ""

    return rating

def get_seller_name(soup):
    try:
        seller_name = ""
        name = soup.select_one("[id$='sellerName']").text
        for ch in name:
            if ch.isalpha() or ch==" ":
                seller_name += ch
    except:
        seller_name = ""

    return seller_name

def get_seller_address(soup):
    try:
        for s in soup.find_all("script"):
            if "callouts" in str(s.string):
                data = str(s.string).strip('window.__INITIAL_STATE__ = ')
                json_data = json.loads(data.strip(';'))
                data = json_data['pageDataV4']['page']['data']['10005']
                for key in data:
                    if key['id'] == 28:
                        seller_info = key['widget']['data']['listingManufacturerInfo']['value'] 
                        return seller_info['detailedComponents'][0]['value']['callouts'][0]
    except Exception as e:
        print(e)
        return ""

def scrape_product(url: str):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser') 
        rating = get_product_rating(soup)
        seller_name = get_seller_name(soup)
        seller_address = get_seller_address(soup)

        return [rating, seller_name, seller_address]

    except:
        return None

def scrape_flipkart(url: str):
    seller_data = []
    product_urls = scrape_page_products_listing(url)
    print(len(product_urls))
    if product_urls[:5]:
        for index, product_url in enumerate(product_urls[:5]):
            print(f"Product {index}")
            data = scrape_product(product_url)
            if data:
                seller_data.append(data)

            time.sleep(1)

    return seller_data


if __name__ == '__main__':
    url = "https://www.flipkart.com/search?q=indian+handicraft"
    seller_data = scrape_flipkart(url)
    print(seller_data)