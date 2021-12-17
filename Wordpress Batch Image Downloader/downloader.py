# Wordpress batch post image downloader

# This script downloads all the images of all the pages of any given
# wordpress website.

import os
import time
import requests
from bs4 import BeautifulSoup
import concurrent.futures

def download(file):
	path, url = file
	r = requests.get(url)
	with open(path, 'wb') as file:
		file.write(r.content)

first_page = 1
last_page = 50

for index in range(first_page, last_page+1):
	folder = f'page-{index}'
	os.mkdir(folder)

	url = f'your_website.com/page/{index}/'
	r = requests.get(url)
	html = r.text
	soup = BeautifulSoup(html, 'lxml')

	all_divs = soup.find_all('h2', "entry-title")
	ct = 0
	for div in all_divs:
		ct += 1
		all_hrefs = div.find_all('a', href=True)
		for a in all_hrefs:
			sub_folder = f'{folder}/{ct}'
			print(sub_folder)
			os.mkdir(sub_folder)

			url = a['href']
			r = requests.get(url)
			html = r.text
			soup = BeautifulSoup(html,'lxml')

			count = 0
			all_a = soup.find_all('a', href=True)
			img_urls = list(filter(lambda x : x.endswith('.jpg'), 
							[a['href'] for a in all_a]))

			with concurrent.futures.ThreadPoolExecutor() as executor:
				for url in img_urls:
					count += 1
					path = f'{sub_folder}/{count}.jpg'
					executor.submit(download, (path, url))

			time.sleep(1)
