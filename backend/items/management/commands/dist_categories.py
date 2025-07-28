from django.core.management.base import BaseCommand
from django.db.models import Count
from django.db.models.functions import Lower
from items.models import Item

class Command(BaseCommand):
    help = 'Edit articles of items'

    def handle(self, **kwargs):
        # Приведение артикула к нижнему регистру для поиска дубликатов
        duplicate_articles = Item.objects.annotate(
            lower_article=Lower('article')
        ).values('lower_article').annotate(
            article_count=Count('lower_article')
        ).filter(article_count__gt=1)
        
        # Создание списка дублирующихся артикулов
        duplicate_article_list = [article['lower_article'] for article in duplicate_articles]

        # Получение товаров с дублирующимися артикулами
        items_with_duplicate_articles = Item.objects.annotate(
            lower_article=Lower('article')
        ).filter(lower_article__in=duplicate_article_list)
        
        # Вывод всех товаров с дублирующимися артикулами
        for item in items_with_duplicate_articles:
            print(f'Дубликаты: Article: {item.article}, Name: {item.name}')
            
        no_article = Item.objects.filter(article__isnull=True) | Item.objects.filter(article='')
        for item in no_article:
            print(f'Нет артикула: Name: {item.name}')