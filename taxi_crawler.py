import aiohttp
import asyncio

from config_loader import config
from fake_useragent import UserAgent


class CrawlerTaxi:
    api = config.get('config_taxi').get('taxis_api')

    def __init__(self):
        super().__init__()

    async def crawler(self):
        print('mrbilit is crawling')
        ua = UserAgent()
        user_agent = ua.random


        payload = {"from":11320000,
                   "to":31310000,
                   "date":"2026-06-30",
                   "includeClosed":True,
                   "includePromotions":True,
                   "loadFromDbOnUnavailability":True,
                   "includeUnderDevelopment":True
                   }
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
        # try:
        async with aiohttp.ClientSession() as Session:
            async with Session.post(self.api, headers=headers, json=payload) as response:
                json_response = await response.json()
                taxis = json_response.get('buses')
                ticket_list = self.ticket(taxis)
                print(ticket_list)
                print('mrbilit is crawled')
                return ticket_list

        #
        # except Exception as e:
        #     print('this error is related to aiohttp:', e)

    def ticket(self,taxis):
        try:
            ticket_list = list()
            for taxi in taxis:
                price = self.find_price(taxi)
                capacity = self.find_capacity(taxi)

                ticket = {
                    'provider_name': 'mrbilit',
                    'adult_price': price,
                    'capacity': capacity,
                    'origin': taxi.get('fromName'),
                    'destination': taxi.get('toName'),
                    'departure_time': taxi.get('departureTime'),
                    'arrival_time': taxi.get('arrivalTime'),
                    'persian_title': taxi.get('superCorporation'),
                }
                if ticket.get('adult_price') is None:
                    continue
                ticket_list.append(ticket)

            return ticket_list
        except Exception as e:
            print('this error is related to ticket:', e)

    def find_price(self, taxi):
        try:
                adult_price = taxi.get('price')
                return adult_price
        except Exception as e:
            print('this error is related to price:', e)

    def find_capacity(self, taxi):
        try:
                capacity = taxi.get('capacity')
                return capacity
        except Exception as e:
            print('this error is related to find_capacity:', e)

object1 = CrawlerTaxi()
asyncio.run(object1.crawler())
