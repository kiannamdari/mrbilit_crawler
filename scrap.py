# import re
# import requests
#
# from bs4 import BeautifulSoup
# from fake_useragent import UserAgent
#
#
# class ScrapFlights:
#     def __init__(self,base_url):
#         self.base_url = base_url
#
#     def crawl(self, your_city, end_city, date):
#         ua = UserAgent()
#         user_agent = ua.random
#         headers = {"User-Agent": user_agent}
#         url = f'https://mrbilit.com/flights/{your_city}-{end_city}?departureDate={date}'
#         response = requests.get(url, headers=headers)
#         soup = BeautifulSoup(response.text, "html.parser")
#         bilits = soup.select('div.lazy-mount')
#         print(response.text)
#         print(response.status_code)
#         for i in bilits:
#             print(i)
#
#
# s1 = ScrapFlights('https://mrbilit.com')
# s1.crawl('THR', 'MHD', '1405-02-31')
#
import aiohttp

from .conf import MrBilitConfig
from .base_crawler import BaseCrawler
from utils.utils import find_same_flights

class MrBilit(BaseCrawler):
    api = MrBilitConfig.mrbilit_api
    provider_name = "mrbilit"

    def __init__(self):
        super().__init__()

    async def crawl_flights(self, origin: str, destination: str, date: str, is_foreign_flight: bool) -> list:
        print("Crawling mrbilit ...")
        headers = {
            "User-Agent": self.ua.random,
            "Content-Type": "application/json",
        }

        payload = {
            "AdultCount": 1,
            "ChildCount": 0,
            "InfantCount": 0,
            "CabinClass": "All",
            "Routes": [
                {
                    "OriginCode": origin,
                    "DestinationCode": destination,
                    "DepartureDate": date
                }
            ],
            "Baggage": True
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.api, headers=headers, json=payload, ssl=self.ssl_context) as response:
                json_response = await response.json()
                flight_list = json_response.get("Flights", [])

                if len(flight_list) > 0:
                    flight_list = self.output_wrapper(flight_list)
                    flight_list = self.transform_flight_data(flight_list, is_foreign_flight)
                    flight_list = find_same_flights(flight_list)
                else:
                    print(f"There were no flights for following date & endpoints in {self.provider_name}: origin: {origin}, "
                        f"destination: {destination}, date: {date}.")

                print("mrbilit crawled.")
                return flight_list

    def transform_flight_data(self, flight_list: list, is_foreign_flight: bool) -> list:
        transformed_flight_list = list()
        origin, destination = self.find_flight_endpoints(flight_list[0])

        for flight in flight_list:
            try:
                price = self.find_price(flight)
                new_flight = {
                    "provider_name": self.provider_name,
                    "origin": origin,
                    "destination": destination,
                    "departure_date_time": flight.get("segments")[0].get("legs")[0].get("departure_time"),
                    "arrival_date_time": flight.get("segments")[0].get("legs")[0].get("arrival_time"),
                    "adult_price": price,
                    "airline_name_fa": flight.get("segments")[0].get("legs")[0].get("airline").get("persian_title"),
                    "airline_name_en": flight.get("segments")[0].get("legs")[0].get("airline").get("english_title"),
                    "flight_number": flight.get("segments")[0].get("legs")[0].get("flight_number"),
                    "capacity": 0 if price == 0 else flight.get("prices")[0].get("capacity", -1),
                    "is_foreign_flight": is_foreign_flight,
                    "rules": "" if price == 0 else str(flight.get("prices")[0].get("fare_rules")),
                }
                transformed_flight_list.append(new_flight)
            except Exception as e:
                print(f"There is something wrong in this flight: {flight}. The error was: {e}")
                continue

        return transformed_flight_list

    @classmethod
    def find_price(cls, flight: dict) -> int:
        try:
            if len(flight.get("prices", [])) > 0:
                return int(flight.get("prices", [{}])[0].get("passenger_fares", [{}])[0].get("total_fare", 0))
            else:
                return 0
        except Exception as e:
            print(f"Error getting price from flight data: {e}\nFlight: {flight}")
            return 0

    @classmethod
    def find_flight_endpoints(cls, flight: dict) -> tuple:
        origin = flight.get("segments")[0].get("legs")[0].get("origin_code")
        destination = flight.get("segments")[0].get("legs")[-1].get("destination_code")
        return origin, destination
