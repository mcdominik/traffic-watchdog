import logging
import re
from typing import Optional

import requests
import xmltodict

from impediments_tracker.impediment import Impediment


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


class WarsawScrapper:
    def __init__(self):
        self.FEED_URL = 'https://www.wtp.waw.pl/feed/?post_type=impediment'

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
            logging.error(
                f'''Error while parsing: {e}. Probably website structure/API
                response of has changed. If so, {self.__repr__} needs update)''')

    @staticmethod
    def try_find_line_in_title(title: str) -> tuple[Optional[str]]:
        # matches DDD, DD, D, LD, L-D, LDD
        pattern = r"\b(?:[A-Z]-\d|\d{1,3}|[A-Z]\d{1,2})\b"
        matches = re.findall(pattern, title)
        return tuple(matches)

    def get_all_impediments(self) -> list[Optional[Impediment]]:
        raw_impediments = self.__fetch_raw_impediments()
        impediments = []

        for raw_impediment in raw_impediments:
            lines = self.try_find_line_in_title(
                raw_impediment.get('title', ''))
            impediment = Impediment(
                title=raw_impediment.get('title', ''),
                description=raw_impediment.get('description', ''),
                pub_date=raw_impediment.get('pubDate', ''),
                url_with_details=raw_impediment.get('guid', {}).get('#text'),
                lines=lines)
            impediments.append(impediment)

        return impediments

    def get_custom_impediments(self, lines_to_track: tuple[Optional[str]]) -> list[Optional[Impediment]]:
        all_impediments = self.get_all_impediments()
        return [impediment for impediment in all_impediments if set(impediment.lines) & set(lines_to_track)]
