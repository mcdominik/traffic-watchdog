import os

from dotenv import load_dotenv
from telegram import Bot

load_dotenv()

CHAT_ID = os.getenv('CHAT_ID', '')
BOT_TOKEN = os.getenv('BOT_TOKEN', '')


class TelegramWrapper():
    def __init__(self) -> None:
        self.chat_id = CHAT_ID
        self.bot_token = BOT_TOKEN
        self.bot = Bot(token=self.bot_token)

    async def send_message(self, message: str) -> None:
        await self.bot.send_message(chat_id=self.chat_id, text=message)
