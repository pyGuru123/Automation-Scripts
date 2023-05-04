import time
import requests
import pandas as pd
from random import choice
from bs4 import BeautifulSoup

# headers to immitate browser behavior
headers_list = [
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
]

csv_file = "page_listing.csv"
df = pd.read_csv(csv_file)
product_df = df.head(5)

product_dict = {
    'Description' : [],
    'ASIN' : [],
    'Product Description' : [],
    'Manufacturer' : []
}

# Iterating over the previous dataframe
for index, row in df.head(5).iterrows():
    url = row['url']
    headers = ({'User-Agent':choice(headers_list)})
    r = requests.get(url, headers=headers)
    html = r.content
    soup = BeautifulSoup(html, 'lxml')

    # scraping description
    try:
        ul = soup.find("ul", {'class': "a-unordered-list a-vertical a-spacing-mini"}).text
        lists = ul.find_all('li')
        desc = ""
        for li in ul:
            desc += li.text.replace(",". " ")
        product_dict['Description'].append(desc)
    except:
        product_dict['Description'].append("No Information Available")

    # scraping manufacturer
    try:
        table1 = soup.find('table', {'id':'productDetails_techSpec_section_1'})
        trows = table1.find_all('tr')
        for row in trows:
            if row.find('th').text.strip() == "Manufacturer":
                product_dict['Manufacturer'].append(row.find('td').text.strip())
                break
    except:
        product_dict['Manufacturer'].append("No Information Available")

    # scraping ASIN
    try:
        asin = url.split('dp/')[1].split('/')[0]
        product_dict['ASIN'].append(asin)
    except:
        product_dict['ASIN'].append("No Information Available")

    # scraping product description
    try:
        product_description = soup.find('div', {'id':'productDescription'}).text
        product_dict['Product Description'].append(product_description)
    except:
        product_dict['Product Description'].append("No Information Available")

    print(f"product {index} done")
    time.sleep(1)

product_df['Description'] = product_dict['Description']
product_df['ASIN'] = product_dict['ASIN']
product_df['Product Description'] = product_dict['Product Description']
product_df['Manufacturer'] = product_dict['Manufacturer']

product_df.to_csv("product_details.csv")