import aiohttp
import asyncio

from config import ConfigFlight
from fake_useragent import UserAgent


class CrawlerFlight:
    api = ConfigFlight.flights_api

    def __init__(self):
        super().__init__()

    async def crawler(self, origin: str, destination: str, date: str):
        print('mrbilit is crawling')
        user_agent = UserAgent.random
        headers = {
           'User-Agent': user_agent
        }
        payload = {
            'AdultCount': 1,
            'ChildCount': 0,
            'InfantCount': 0,
            'CabinClass': 'All',
            'routes': [{
                'OriginIataCode': origin,
                'DestinationIataCode': destination,
                'DepartureDate': date
            }]
        }
        async with aiohttp.ClientSession() as Session:
            async with Session.post(self.api, headers=headers, json=payload) as response:
                json_response = await response.json()
                flight_list = json_response.get('Flights')
                print(flight_list)


object1 = CrawlerFlight()
asyncio.run(object1.crawler('THR', 'MHD', '2026/05/31'))

