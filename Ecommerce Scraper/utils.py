from amazon import scrape_amazon
from flipkart import scrape_flipkart
from myntra import scrape_myntra
from loguru import logger
import pandas as pd

product_urls = [
	"https://www.amazon.com/s?k=indian+handicrafts&crid=2XDYOLH5NMP2B&sprefix=indian+handicrafts%2Caps%2C728&ref=sr_pg_2",
	"https://www.flipkart.com/search?q=indian+handicraft",
	"https://www.myntra.com/mens-tshirt"
]

sellers = []
for product_url in product_urls:
	if "amazon" in product_url:
		result = scrape_amazon(product_url)
	elif "flipkart" in product_url:
		result = scrape_flipkart(product_url)
	elif "myntra" in product_url:
		result = scrape_myntra(product_url)
	else:
		logger.error("invalid url")
		result = []

	sellers += result

columns = ["Rating", "Seller Name", "Seller Address", "Platform"]
df = pd.DataFrame(sellers, columns=columns)
df.to_excel("scraped_data.xlsx", index=False)