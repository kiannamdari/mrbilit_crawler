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
                async with Session.post(self.api, headers=headers, json=payload) as response:

                    json_response = await response.json()
                    flights = json_response.get('Flights')
                    ticket_list = self.ticket(flights)
                    return ticket_list


        except Exception as e:
            print('this error is related to aiohttp:', e)

    def ticket(self,flights):
        try:
            ticket_list = list()
            for flight in flights:
                price = self.find_price(flight)
                capacity = self.find_capacity(flight)
                leg = flight.get('Segments')[0].get('Legs')[0]
                ticket = {
                    'provider_name': 'mrbilit',
                    'adult_price': price,
                    'capacity': capacity,
                    'origin': leg.get('Origin'),
                    'destination': leg.get('Destination'),
                    'departure_time': leg.get('DepartureTime'),
                    'arrival_time': leg.get('ArrivalTime'),
                    'persian_title': leg.get('Airline').get('PersianTitle'),
                    'english_title': leg.get('Airline').get('EnglishTitle'),
                    'flights_number': leg.get('FlightNumber'),
                }
                if ticket.get('adult_price') is None:
                    continue
                ticket_list.append(ticket)

            print(ticket_list)
            return ticket_list
            print('mrbilit is crawled')
        except Exception as e:
            print('this error is related to ticket:', e)

    def find_price(self, flight):
        try:
            if len(flight.get('Prices')) > 0:
                adult_price = flight.get('Prices')[0].get('PassengerFares')[0].get('TotalFare')
                return adult_price
        except Exception as e:
            print('this error is related to price:', e)

    def find_capacity(self, flight):
        try:
            if len(flight.get('Prices')) > 0:
                capacity = flight.get('Prices')[0].get('Capacity')
                return capacity
        except Exception as e:
            print('this error is related to find_capacity:', e)

object1 = CrawlerFlight()
asyncio.run(object1.crawler('THR', 'MHD', '2026-6-21'))
