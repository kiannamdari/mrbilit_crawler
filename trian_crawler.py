import aiohttp
import asyncio

from fake_useragent import UserAgent
from config_loader import config

class CrawlerTrains:
    api = config.get('config_trains').get('trains_api')

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
                async with Session.get(self.api, headers=headers, json=payload) as response:

                    json_response = await response.json()
                    trains = json_response.get('trains')
                    ticket_list = self.ticket(trains)
                    print(ticket_list)
                    print('mrbilit is crawled')
                    return ticket_list


        except Exception as e:
            print('this error is related to aiohttp:', e)

    def ticket(self,trains):
        try:
            ticket_list = list()
            for train in trains:
                price = self.find_price(train)
                capacity = self.find_capacity(train)
                ticket = {
                    'provider_name': 'mrbilit',
                    'adult_price': price,
                    'capacity': capacity,
                    'from_name': train.get('fromName'),
                    'to_name': train.get('toName'),
                    'departure_time': train.get('departureTime'),
                    'arrival_time': train.get('arrivalTime'),
                    'corporation_name': train.get('corporationName'),
                    'train_number': train.get('trainNumber')
                }
                if ticket.get('adult_price') is None:
                    continue
                ticket_list.append(ticket)

            return ticket_list

        except Exception as e:
            print('this error is related to ticket:', e)

    def find_price(self, train):
        try:
            if len(train.get('prices')) > 0:
                adult_price = train.get('prices')[0].get('classes')[0].get('price')
                return adult_price
        except Exception as e:
            print('this error is related to price:', e)

    def find_capacity(self, train):
        try:
            if len(train.get('prices')) > 0:
                capacity = train.get('prices')[0].get('classes')[0].get('capacity')
                return capacity
        except Exception as e:
            print('this error is related to find_capacity:', e)

object1 = CrawlerTrains()
asyncio.run(object1.crawler('THR', 'MHD', '2026-6-24'))
