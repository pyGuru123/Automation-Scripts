# Amazon Scraper

[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/check-it-out.svg)](https://forthebadge.com)


This is an automated script to scrape multiple amazon pages using beautifulsoup.

## How to Download

Download this project from here [Download Amazon Scraper](https://minhaskamal.github.io/DownGit/#/home?url=https://github.com/pyGuru123/Amazon-Scraper)

## Requirements

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install following packages :-
* lxml
* pandas
* Requests
* BeautifulSoup

```bash
pip install -r requirements.txt
```

## Usage

These scripts work in two steps:
1. Run page_scraper.py, change url to scrape products other than bags.
	Running above script will generate a page_listing.csv file.
2. Run product_scraper.py file, this will scrape additional information about the products listed in the page_listing.csv, creating another product_details.csv file.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.