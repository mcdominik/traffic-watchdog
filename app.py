import asyncio
import logging

from utils.telegram_wrapper import TelegramWrapper
from utils.impediments_fetcher import ImpedimentsFetcher
from utils.impediment import Impediment


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

    async def run(self) -> None:
        while True:
            new_impediments = self.manager.get_all_impediments()
            logger.info('Warsaw Impediments Fetched')
            if new_impediments:
                for new_impediment in new_impediments:
                    if new_impediment not in self.known_impediments:
                        self.known_impediments.add(new_impediment)
                        message = f"{new_impediment.title} {new_impediment.description} {new_impediment.url_with_details}"
                        await self.telegram.send_message(message)

            await asyncio.sleep(120)


watchdog = App()
asyncio.run(watchdog.run())
