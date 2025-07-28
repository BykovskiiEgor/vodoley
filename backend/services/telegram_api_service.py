import logging
import os

import requests
import telegram

logger = logging.getLogger(__name__)


class TelegramService:
    """."""

    def __init__(self) -> None:
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))

    def send_notification(self, chat_id: int, message: str) -> None:
        """."""
        # try:
        #     self.bot.send_message(chat_id=int(chat_id), text=message)
        #     logger.info(f"Message sent to Telegram user {chat_id}")
        # except Exception as e:
        #     logger.error(f"Failed to send message to {chat_id}: {e}")
        #     raise e
        try:
            url = "https://api.telegram.org/bot" + self.token + "/sendMessage"
            data = {
                "chat_id": 1595124705,
                "text": "Hello",
            }
            response = requests.post(url, json=data)
            print("Status Code", response.status_code)
            print("JSON Response ", response.json())
        except Exception as e:
            raise e
