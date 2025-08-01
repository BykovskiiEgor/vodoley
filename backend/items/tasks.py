import logging
import os

from celery import shared_task
from services.telegram_api_service import TelegramService

from django.core.management import call_command

logger = logging.getLogger(__name__)


@shared_task
def send_message_to_telegram():
    """."""
    telegram_service = TelegramService()
    message = "Напоминание об обновлении товаров на сайте"
    chat_id = os.getenv("TELEGRAM_USER_ID")

    try:
        telegram_service.send_notification(chat_id, message)
    except Exception as e:
        logger.error(f"Error sending message to telegram: {e}")
        raise e


@shared_task
def run_flexi_update_command():
    call_command("update_flexi")
