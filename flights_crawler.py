import aiohttp
import asyncio
import json

from config_loader import config
from fake_useragent import UserAgent


class CrawlerFlight:
    api = config.get("config_flights").get("flights_api")

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
                    print('mrbilit is crawled')
                    air_lines = self.air_lines(flights)
                    ticket_list = self.ticket(flights)
                    return ticket_list


        except Exception as e:
            print('this error is related to aiohttp:', e)

    def air_lines(self, flights):
        try:
            air_lines = list()
            for flight in flights:
                air_line = {
                    "persian_title": flight.get("Segments")[0].get("Legs")[0].get("Airline").get("PersianTitle"),
                    "english_title": flight.get("Segments")[0].get("Legs")[0].get("Airline").get("EnglishTitle"),
                }
                air_lines.append(air_line)
            with open("air_lines.json", "w", encoding="utf-8") as f:
                json.dump(air_lines, f, ensure_ascii=False, indent=2)
            return air_lines

        except Exception as e:
            print(f"this error is related to airlines: {e}")

    def ticket(self,flights):
        try:
            ticket_list = list()
            index_counter = 0
            for flight in flights:
                leg = flight.get("Segments")[0].get("Legs")[0]
                price = self.find_price(flight)
                capacity = self.find_capacity(flight)
                air_lines = self.air_lines(flights)
                ticket = {
                    'provider_name': 'mrbilit',
                    'adult_price': price,
                    'capacity': capacity,
                    'origin': leg.get('Origin'),
                    'destination': leg.get('Destination'),
                    'departure_time': leg.get('DepartureTime'),
                    'arrival_time': leg.get('ArrivalTime'),
                    'flights_number': leg.get('FlightNumber'),
                    'air_lines': air_lines[index_counter]
                }
                if ticket.get('adult_price') is None:
                    continue
                ticket_list.append(ticket)
                index_counter += 1
            print(ticket_list)
            with open("tickets.json", "w", encoding="utf-8") as f:
                json.dump(ticket_list, f, ensure_ascii=False, indent=4)
            return ticket_list
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
asyncio.run(object1.crawler('THR', 'MHD', '2026-7-13'))
