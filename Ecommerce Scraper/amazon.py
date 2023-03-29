import time
import requests
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
		links = soup.select("[class*='a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal']")
		product_urls = []
		for link in links:
			url = "https://amazon.com" + link.get('href')
			if 'sspa' not in url:
				product_urls.append(url)

		return product_urls
	except:
		return []

def get_product_rating(soup):
	try:
		rating = soup.select_one("[class*='a-icon-alt']").text.split()[0]
	except:
		rating = ""

	return rating

def get_business_name_and_address(soup):
	try:
		seller_name = soup.select_one("[id$='seller-name']").text
	except:
		seller_name = ""

	try:
		seller_address = ""
		address_lines = soup.select("[class*='a-row a-spacing-none indent-left']")
		for line in address_lines:
			seller_address += (line.text + '\n')
	except:
		seller_address = ""

	return seller_name, seller_address

def scrape_product(url: str):
	try:
		response = requests.get(url, headers=headers)
		soup = BeautifulSoup(response.content, 'html.parser')
		seller_profile = soup.find('a', attrs={'id':'sellerProfileTriggerId'})
		if not seller_profile:
			return None

		rating = get_product_rating(soup)

		seller_profile_url = "https://www.amazon.com" + seller_profile['href']
		response = requests.get(seller_profile_url, headers=headers)
		soup = BeautifulSoup(response.content, 'html.parser')
		seller_name, seller_address = get_business_name_and_address(soup)

		return [rating, seller_name, seller_address, "Amazon"]

	except:
		return None

def scrape_amazon(url: str):
	logger.info("Scraping Amazon")

	seller_data = []
	product_urls = scrape_page_products_listing(url)
	if product_urls:
		for index, product_url in enumerate(product_urls[:10]):
			logger.info(f"Amazon : {index+1}")
			data = scrape_product(product_url)
			if data:
				seller_data.append(data)

			time.sleep(1)

	return seller_data