import re
import requests

from bs4 import BeautifulSoup
from fake_useragent import UserAgent


class ScrapFlights:
    def __init__(self,base_url):
        self.base_url = base_url

    def crawl(self, your_city, end_city, date):
        ua = UserAgent()
        user_agent = ua.random
        headers = {"User-Agent": user_agent}
        url = f'https://mrbilit.com/flights/{your_city}-{end_city}?departureDate={date}'
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, "html.parser")
        bilits = soup.find_all('div', class_="lazy-mount")
        print(response.text)
        print(response.status_code)
        print(bilits)


s1 = ScrapFlights('https://mrbilit.com')
s1.crawl('THR', 'MHD', '1405-02-31')
