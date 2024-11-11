import os
import asyncio
import logging

from dotenv import load_dotenv

from utils.telegram_wrapper import TelegramWrapper
from utils.impediments_fetcher import ImpedimentsFetcher
from utils.impediment import Impediment

load_dotenv()

LINES_TO_TRACK = os.getenv('LINES_TO_TRACK', '*').split(",")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class App:
    def __init__(self) -> None:
        self.manager = ImpedimentsFetcher('Warsaw')
        self.telegram = TelegramWrapper()
        self.known_impediments: set[Impediment] = set()

    async def run(self, lines_to_track: tuple[str]) -> None:
        logging.info(f'Started tracking: {lines_to_track}')
        await self.telegram.send_message(f'Started tracking: {lines_to_track}')

        while True:
            if lines_to_track == ['*']:
                new_impediments = self.manager.get_all_impediments()
            else:
                new_impediments = self.manager.get_custom_impediments(lines_to_track)
            logger.info('Warsaw Impediments Fetched')
            if new_impediments:
                for new_impediment in new_impediments:
                    if new_impediment not in self.known_impediments:
                        self.known_impediments.add(new_impediment)
                        message = f"{new_impediment.title} {new_impediment.description} {new_impediment.url_with_details}"
                        await self.telegram.send_message(message)
                        logging.info(f'New impediment sent: {new_impediment.title}')

            await asyncio.sleep(120)


watchdog = App()
asyncio.run(watchdog.run(LINES_TO_TRACK))
