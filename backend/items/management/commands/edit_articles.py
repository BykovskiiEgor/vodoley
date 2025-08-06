from django.core.management.base import BaseCommand
from items.models import Item


class Command(BaseCommand):
    help = "Edit articles of items"

    def handle(self, **kwargs):
        Item.objects.all().delete()
