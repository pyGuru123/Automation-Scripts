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

# pandas empty dataframe
columns = ['page', 'name', 'price', 'url', 'rating', 'reviews']
df = pd.DataFrame(columns=columns)

# scraping 20 amazon pages
for page in range(1):
    url = f"https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page}"
    headers = ({'User-Agent':choice(headers_list)})

    r = requests.get(url, headers=headers)
    html = r.content
    soup = BeautifulSoup(html, 'lxml')

    divs = soup.find_all('div', {'class':'s-result-item'})
    for index, div in enumerate(divs[:30]):
        name = div.find('span', {'class':'a-size-medium a-color-base a-text-normal'})
        if name:
            try:
                row = []
                price = div.find('span', {'class': 'a-price-whole'}).text
                url = div.find('a', {'class':'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})['href']
                url = "https://amazon.com" + url
                rating = div.find('span', {'class':'a-icon-alt'}).text.split()[0]
                reviews = div.find('span', {'class':'a-size-base s-underline-text'}).text
                
                if 'sspa' in url:
                    continue
                    
                row.append(1)
                row.append(name.text)
                row.append(price)
                row.append(url)
                row.append(rating)
                row.append(reviews)
                df.loc[len(df)] = row

                if index > 30:
                    break
            except:
                pass

    print(f"Page {page} done.")
    time.sleep(1)

df.to_csv('page_listing.csv')