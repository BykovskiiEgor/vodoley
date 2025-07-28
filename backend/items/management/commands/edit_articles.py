from django.core.management.base import BaseCommand
from django.db.models import Count
from items.models import Item


class Command(BaseCommand):
    help = "Edit articles of items"

    def handle(self, **kwargs):
        # Item.objects.all().delete()
        duplicate_articles = Item.objects.values("article").annotate(article_count=Count("article")).filter(article_count__gt=1)

        items_with_duplicate_articles = Item.objects.filter(article__in=[article["article"] for article in duplicate_articles])

        for item in items_with_duplicate_articles:
            print(f"Article: {item.article}, Name: {item.name}")
