from dataclasses import dataclass
from typing import Optional
import requests
import xmltodict
# from json import dump
from enum import Enum


class Vehicle(Enum):
    METRO = 'METRO',
    BUS = 'BUS'
    TRAM = 'TRAM',
    TRAIN = 'TRAIN',
    WKD = 'WKD'


@dataclass
class Impediment:
    title: str
    description: str
    pub_date: str
    url_with_details: Optional[str]
    vehicle: Optional[Vehicle]
    line: Optional[str]


known_metro_lines = ['M1', 'M2']
known_tram_lines = ['1', '2', '3', '4', '5',
                    '6', '7', '8', '9', '10', '11', '13', '15', '17', '18', '20', '22', '23', '24', '25', '26', '27', '28', '31', '33', '35' 'C1', 'C4', 'C6']
known_train_lines = ['S1', 'S2', 'S3', 'S4', 'S40']
known_bus_lines = [
    '102', '103', '104', '105', '106', '107', '108', '109', '110', '111',
    '112', '114', '115', '116', '117', '118',
    '119', '120', '121', '122', '123', '124', '125', '126', '127', '128', '129', '131', '132', '133', '134',
    '135', '136', '138', '139', '140', '141', '142', '143', '145', '146', '147', '148', '149', '150', '151',
    '152', '153', '154', '156', '158', '159', '160', '161', '162', '163', '164', '165', '166', '167',
    '168', '169', '170', '171', '173', '174', '175', '176', '178', '179',
    '180', '181', '183', '184', '185', '186', '187', '188', '189', '190', '191', '192', '193', '194', '196', '197', '198',
    '199', '200', '201', '202', '203', '204', '207', '208', '209', '210', '211', '212', '213', '217', '218',
    '219', '220', '221', '225', '226', '228', '234', '239', '240', '245', '249', '250', '251', '256', '262',
    '263', '264',
    '300', '303', '305', '308', '311', '314', '317', '319', '320', '326', '331', '332', '338', '339', '340',
    '349', '356', '379',
    '401', '402', '409', '411', '414',
    '500', '502', '503', '504', '507', '509', '511', '512', '514', '516', '517', '518', '519', '520', '521',
    '522', '523', '525', '527',
    '702', '703', '704', '705', '706', '707', '709', '710', '711', '712', '713', '714', '715', '716', '717',
    '719', '720', '721', '722', '723', '724', '727', '728', '729', '730', '731', '733', '735', '736', '737',
    '738', '739', '742', '743', '750',
    '800', '809', '815', '817', '850', '900', 'E-1', 'E-2', 'ZS2', 'Z12', 'Z20', 'C09', 'C40', 'N01', 'N02', 'N03', 'N11',
    'N12', 'N13', 'N14', 'N16',
    'N21', 'N22', 'N24', 'N25', 'N31', 'N32', 'N33', 'N34',
    'N35', 'N36', 'N37', 'N38', 'N41', 'N42', 'N43', 'N44',
    'N45', 'N46', 'N50', 'N56', 'N58', 'N61', 'N62', 'N63',
    'N64', 'N71', 'N72', 'N81', 'N83', 'N85', 'N86', 'N88',
    'N91', 'N95', 'L-1', 'L-2', 'L-3', 'L-4', 'L-5', 'L-6', 'L-7', 'L-8', 'L-9', 'L10', 'L11', 'L12', 'L13', 'L14', 'L15',
    'L16', 'L17', 'L18', 'L19', 'L20', 'L21', 'L22', 'L23', 'L24', 'L25', 'L26', 'L27', 'L28', 'L29', 'L30',
    'L31', 'L32', 'L33', 'L34', 'L35', 'L36', 'L37', 'L38', 'L39', 'L40', 'L41', 'L42', 'L43', 'L45', 'L46',
    'L47', 'L48', 'L49', 'L50', 'L51', 'L52']


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
            print(
                f'''Error while parsing: {e}. Probably website structure/API
                response of has changed. If so, {self.__repr__} needs update)''')

    def __get_line_from_title(self, title) -> str:
        return title.rsplit(' ', 1)[-1]

    def __map_line_to_vehicle(self, line: str) -> Vehicle:
        if line in known_metro_lines:
            return Vehicle.METRO.value
        elif line in known_tram_lines:
            return Vehicle.TRAM.value
        elif line in known_bus_lines:
            return Vehicle.BUS.value
        elif line in known_train_lines:
            return Vehicle.TRAIN.value
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
                print('unknown line')
                impediment = Impediment(
                    title=raw_impediment.get('title', ''),
                    description=raw_impediment.get('description', ''),
                    pub_date=raw_impediment.get('pubDate', ''),
                    url_with_details=raw_impediment.get(
                        'guid', {}).get('#text'),
                    vehicle='',
                    line='')
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

    def is_any_metro_impedimented(self):
        return bool(self.get_metro_impediments())

    def get_tram_impediments(self):
        all_impediments = self.get_all_impediments()
        return [impediment for impediment in all_impediments if impediment.vehicle == Vehicle.TRAM.value]

    def is_any_tram_impedimented(self):
        return bool(self.get_tram_impediments())

    def get_train_impediments(self):
        all_impediments = self.get_all_impediments()
        return [impediment for impediment in all_impediments if impediment.vehicle == Vehicle.TRAIN.value]

    def is_any_train_impedimented(self):
        return bool(self.get_train_impediments())

    def get_bus_impediments(self):
        all_impediments = self.get_all_impediments()
        return [impediment for impediment in all_impediments if impediment.vehicle == Vehicle.BUS.value]

    def is_any_bus_impedimented(self):
        return bool(self.get_bus_impediments())

    def are_any_impediments(self):
        return bool(self.get_all_impediments())

    def is_impedimented(self, line: str) -> bool:
        if not any(line in lines for lines in [known_bus_lines, known_metro_lines, known_train_lines, known_tram_lines]):
            raise ValueError('Unknown Line')
        return any(impediment.line == line for impediment in self.get_all_impediments())


class CracowScrapper:
    pass


class Manager:
    def __init__(self, city: str):
        if city == 'Warsaw':
            self.scrapper = WarsawScrapper()
        elif city == 'Cracow':
            self.scrapper = CracowScrapper()
        else:
            raise Exception('Unsupported City')

    def is_impedimented(self, line: str):
        return self.scrapper.is_impedimented(line)

    def get_all_impediments(self):
        return self.scrapper.get_all_impediments()

    def get_bus_impediments(self):
        return self.scrapper.get_bus_impediments()

    def get_metro_impediments(self):
        return self.scrapper.get_metro_impediments()

    def are_any_impediments(self):
        return bool(self.get_all_impediments())


if __name__ == "__main__":
    manager = Manager('Warsaw')
    imp = manager.are_any_impediments()
