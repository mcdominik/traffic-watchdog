from typing import Optional
import requests

import xmltodict

from utils.impediment import Impediment
from utils.vehicle import Vehicle


class WarsawScrapper:
    def __init__(self):
        self.FEED_URL = 'https://www.wtp.waw.pl/feed/?post_type=impediment'
        self.known_metro_lines = ['M1', 'M2']

    def __repr__(self):
        return 'Warsaw Scrapper'

    def __fetch_raw_impediments(self) -> list[dict]:
        response = requests.get(self.FEED_URL)
        response.raise_for_status()
        try:
            feed_data = xmltodict.parse(response.content)
            items = feed_data['rss']['channel'].get('item', [])
            return items if isinstance(items, list) else [
                items]
        except Exception as e:
            print(
                f'''Error while parsing: {e}. Probably website structure/API
                response of has changed. If so, {self.__repr__} needs update)''')

    def __get_line_from_title(self, title) -> str:
        return title.rsplit(' ', 1)[-1]

    def __map_line_to_vehicle(self, line: str) -> Vehicle:
        if line in self.known_metro_lines:
            return Vehicle.METRO.value
        else:
            raise ValueError(f"Unknown line: {line}")

    def get_all_impediments(self) -> list[Optional[Impediment]]:
        raw_impediments = self.__fetch_raw_impediments()
        impediments = []
        for raw_impediment in raw_impediments:
            line = self.__get_line_from_title(
                raw_impediment.get('title', ''),)
            try:
                vehicle = self.__map_line_to_vehicle(line)
            except:
                impediment = Impediment(
                    title=raw_impediment.get('title', ''),
                    description=raw_impediment.get('description', ''),
                    pub_date=raw_impediment.get('pubDate', ''),
                    url_with_details=raw_impediment.get(
                        'guid', {}).get('#text'),
                    vehicle='',
                    line='')
                impediments.append(impediment)
                continue

            impediment = Impediment(
                title=raw_impediment.get('title', ''),
                description=raw_impediment.get('description', ''),
                pub_date=raw_impediment.get('pubDate', ''),
                url_with_details=raw_impediment.get('guid', {}).get('#text'),
                vehicle=vehicle,
                line=line)
            impediments.append(impediment)
        return impediments

    def get_metro_impediments(self):
        all_impediments = self.get_all_impediments()
        return [impediment for impediment in all_impediments if impediment.vehicle == Vehicle.METRO.value]
