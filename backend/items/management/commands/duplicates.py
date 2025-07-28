from django.core.management.base import BaseCommand
from django.db.models import Count
from django.db.models.functions import Lower
from items.models import Item


class Command(BaseCommand):
    help = "Edit articles of items"

    def handle(self, **kwargs):
        duplicate_articles = Item.objects.annotate(lower_article=Lower("article")).values("lower_article").annotate(article_count=Count("lower_article")).filter(article_count__gt=1)

        duplicate_article_list = [article["lower_article"] for article in duplicate_articles]

        items_with_duplicate_articles = Item.objects.annotate(lower_article=Lower("article")).filter(lower_article__in=duplicate_article_list)

        for item in items_with_duplicate_articles:
            print(f"Дубликаты: Article: {item.article}, Name: {item.name}")

        no_article = Item.objects.filter(article=None)
        for item in no_article:
            print(f"Нет артикула: Name: {item.name}")
