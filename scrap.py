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
        ua = UserAgent()
        user_agent = ua.random
        try:
            headers = {
                'User-Agent': user_agent,
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Content-Type': 'application/json-patch+json',
                'Referer': 'https://mrbilit.com/',
                'X-PlayerID': '163fc7ac-d5da-47f5-8b64-0dda1f91c522',
                'SessionId': 'session_35080a0a-bc0e-4bcd-b1b8-5614a839a52b',
                'Origin': 'https://mrbilit.com',
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJidXMiOiI0ZiIsInRybiI6IjE3Iiwic3JjIjoiMiJ9.vvpr9fgASvk7B7I4KQKCz-SaCmoErab_p3csIvULG1w',
            }
        except Exception as e:
            print('this error is related to headers', e)
        payload = {
            'AdultCount': 1,
            'ChildCount': 0,
            'InfantCount': 0,
            'CabinClass': 'All',
            'Routes': [
                {
                    'OriginCode': origin,
                    'DestinationCode': destination,
                    'DepartureDate': date
                }
            ],
            'Baggage': True,
            'IncludeFlightsWithHigherCapacity': False
        }
        try:
            async with aiohttp.ClientSession() as Session:
                async with Session.post('https://flight.atighgasht.com/api/Flights', headers=headers, json=payload) as response:

                    json_response = await response.json()
                    flights = json_response.get('Flights')
                    print(json_response)
                    print('mrbilit is crawled')
        except Exception as e:
            print('this error is related to aiohttp:', e)
        try:
            def price(self):
                price = \
                    {
                    'AdultFare': None,
                    'ChildFare': None,
                    'InfantFare': None,
                    }
                if len(flights[0].get('prices')) > 0:
                    passenger_fares = flights[0].get('Prices')[0].get('PassengerFares')
                    for i in passenger_fares:
                        if i == 0:
                            price.update({'AdultFare': i.get('TotalFare')})
                        elif i == 1:
                            price.update({'ChildFare': i.get('TotalFare')})
                        elif i == 2:
                            price.update({'InfantFare': i.get('TotalFare')})
                print(price)
        except Exception as e:
            print('this error is related to price:', e)
            return 0
object1 = CrawlerFlight()
asyncio.run(object1.crawler('MHD', 'THR', '2026-6-11'))

