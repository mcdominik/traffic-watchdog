from utils.city import City
from utils.warsaw_scrapper import WarsawScrapper


class ImpedimentsFetcher:
    def __init__(self, city: City = City.WARSAW):
        if city == 'Warsaw':
            self.scrapper = WarsawScrapper()
        else:
            raise Exception('Unsupported City')

    def get_all_impediments(self):
        return self.scrapper.get_all_impediments()

    def get_metro_impediments(self):
        return self.scrapper.get_metro_impediments()

    def are_any_impediments(self):
        return bool(self.get_all_impediments())
