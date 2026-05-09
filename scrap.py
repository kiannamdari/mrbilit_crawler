import re

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests

class Scrap:
    def __init__(self, url, vehicle, your_city, end_city, date):
        self.url = url
        self.vehicle = vehicle
        self.your_city = your_city
        self.end_city = end_city
        self.date = date

    def scrap(self):
        ua = UserAgent()
        user_agent = ua.random
        headers = {"User-Agent": user_agent}
        self.url = f'https://mrbilit.com/{self.vehicle}/{self.your_city}-{self.end_city}?departureDate={self.date}'
        response = requests.get(self.url, headers=headers)

