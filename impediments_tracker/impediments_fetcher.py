from typing import Optional

from impediments_tracker.city import City
from impediments_tracker.impediment import Impediment
from impediments_tracker.warsaw_scrapper import WarsawScrapper


class ImpedimentsFetcher:
    def __init__(self, city: City = City.WARSAW) -> None:
        if city == 'Warsaw':
            self.scrapper = WarsawScrapper()
        else:
            raise Exception('Unsupported City')

    def get_all_impediments(self) -> list[Optional[Impediment]]:
        return self.scrapper.get_all_impediments()

    def get_custom_impediments(self, lines_to_track: tuple[Optional[str]]) -> list[Optional[Impediment]]:
        return self.scrapper.get_custom_impediments(lines_to_track)

    def are_any_impediments(self) -> bool:
        return bool(self.get_all_impediments())
