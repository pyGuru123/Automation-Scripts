import tempfile
import pandas as pd
from loguru import logger
from typing import BinaryIO

from app.sellers_scraper.amazon import scrape_amazon
from app.sellers_scraper.flipkart import scrape_flipkart
from app.sellers_scraper.myntra import scrape_myntra

def main(excel_file: BinaryIO, filename: str) -> None:
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        lines = excel_file.readlines()
        temp_file.writelines(lines)
        temp_file.seek(0)

        amazon_sellers = []
        flipkart_sellers = []
        myntra_sellers = []

        df = pd.read_excel(temp_file)
        product_urls = df['URLs'].dropna().to_list()

        for product_url in product_urls:
            if "amazon" in product_url:
                amazon_sellers += scrape_amazon(product_url)
            elif "flipkart" in product_url:
                flipkart_sellers += scrape_flipkart(product_url)
            elif "myntra" in product_url:
                myntra_sellers += scrape_myntra(product_url)
            else:
                logger.error("invalid url")

        amazon_df = pd.DataFrame(
            amazon_sellers, 
            columns = ["Rating", "Seller Name", "Seller Address"],
        )

        flipkart_df = pd.DataFrame(
            flipkart_sellers, 
            columns = ["Rating", "Seller Name", "Manufacturer Address", "Packer Address"],
        )

        myntra_df = pd.DataFrame(
            myntra_sellers, 
            columns = ["Seller Name", "Seller Address", "Importer Address", "Manufacturer Address", "Packer Address"]
        )

        with pd.ExcelWriter(filename) as writer:
            if amazon_sellers:
                amazon_df.to_excel(writer, sheet_name='Amazon', index=None)
            if flipkart_sellers:
                flipkart_df.to_excel(writer, sheet_name='Flipkart', index=None)
            if myntra_sellers:
                myntra_df.to_excel(writer, sheet_name='Myntra', index=None)