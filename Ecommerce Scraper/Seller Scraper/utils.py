import random
import requests
from bs4 import BeautifulSoup


headers = {'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'}


def get_random_time() -> float:
    return random.randrange(1, 3)


def get_page_content(url: str) -> BeautifulSoup:
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    return soup