import aiohttp
import asyncio

from config_loader import config
from fake_useragent import UserAgent


class CrawlerHotel:
    api = config.get('config_hotel').get('hotels_api')

    def __init__(self):
        super().__init__()

    async def crawler(self):
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

        try:
            async with aiohttp.ClientSession() as Session:
                async with Session.get(self.api, headers=headers) as response:
                    json_response = await response.json()
                    hotels = json_response.get('hotels')
                    ticket_list = self.ticket(hotels)
                    print(ticket_list)
                    print('mrbilit is crawled')
                    return ticket_list


        except Exception as e:
            print('this error is related to aiohttp:', e)

    def ticket(self,hotels):
        try:
            ticket_list = list()
            for hotel in hotels:
                price = self.find_price(hotel)

                ticket = {
                    'provider_name': 'mrbilit',
                    'adult_price': price,
                    'destination': hotel.get('cityName'),
                    'english_title': hotel.get('englishName'),
                    'persian_title': hotel.get('name'),
                    'address': hotel.get('shortAddress'),
                    'hotel_ranking': hotel.get('hotelTypeTitle'),
                }
                ticket_list.append(ticket)

            return ticket_list
        except Exception as e:
            print('this error is related to ticket:', e)

    def find_price(self, hotel):
        try:
                adult_price = hotel.get('totalPrice')
                return adult_price
        except Exception as e:
            print('this error is related to price:', e)

object1 = CrawlerHotel()
asyncio.run(object1.crawler())
