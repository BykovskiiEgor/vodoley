import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "shop.settings")

app = Celery("shop")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "send-daily-telegram-message": {
        "task": "items.tasks.send_message_to_telegram",
        "schedule": crontab(hour=19, minute=0),
    },
}
