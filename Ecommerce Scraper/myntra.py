import time
import json
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
}

def scrape_page(url: str) -> list[str]:
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
        print(e)
        return []

def scrape_page_products_listing(url: str):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser') 
        for s in soup.find_all("script"):
            if "pdpData" in str(s.string):
                data = s.string.strip('window.__myx = ')
                json_data = json.loads(data)['pdpData']

                rating = float("{:.2f}".json_data['ratings']['averageRating'])
                seller_name = json_data["sellers"][0]['sellerName']
                seller_address = json_data["sellers"][0]['sellerAddress']['address']

                return [rating, seller_name, seller_address]

    except:
        return None

def scrape_myntra(url: str):
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
    url = "https://www.myntra.com/mens-tshirt"
    seller_data = scrape_myntra(url)
    print(seller_data)