import os
import pandas as pd
from django.core.management.base import BaseCommand
from items.models import Item, Attribute, ItemAttribute, ItemImage
from django.core.files import File
from urllib.request import urlopen
from tempfile import NamedTemporaryFile
from django.db.models import Q


class Command(BaseCommand):
    help = 'Get information from flexi and edit items'
    
    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Путь к файлу')
        
    def handle(self, **kwargs):
        updated_count = 0 
        file_path = kwargs['file_path']
        Attribute.objects.get(name='Бренд')
        Attribute.objects.get(name='Страна')
        
        for row in self.read_excel(file_path):
            if all(pd.isna(cell) for cell in row):
                continue
            
            article = str(row[0]).split('.')[0]
            brand = row[1]
            country = row[2]
            img_urls = row[3]
            description = row[4]

            items = self.get_items(article)
            if len(items) != 1:
                self.stdout.write(self.style.WARNING(f'Found {len(items)} items with article {article}, skipping...'))
                continue
            
            item = items[0]
            item_updated = self.update_item(item, brand, country, description)
            if item_updated:
                updated_count += 1
            self.process_images(item, img_urls)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} items from the file.'))

    def read_excel(self, file_path):
        """Генератор для чтения строк из Excel-файла."""
        df = pd.read_excel(file_path)
        columns = ['Код','Бренд','Страна','Адреса изображений','Описание товара']
        data = df[columns].values
        for row in data:
            yield row
    
    def get_items(self, article):
        """Ищет товары по полному артикулу, фильтрует в Python."""
        # Сначала ищем все товары, где артикул содержится в строке
        potential_items = Item.objects.filter(
            Q(article__icontains=article)
        )
        # Затем фильтруем результаты в Python
        return [item for item in potential_items if self.is_exact_match(item.article, article)]
    
    def is_exact_match(self, full_article, article):
        """Проверяет, является ли article точной частью full_article."""
        parts = full_article.split('/')
        return any(part == article for part in parts)
    
    def update_item(self, item, brand, country, description):
        """Обновляет атрибуты и описание товара."""
        
        item_updated = False
        
        if pd.notna(description):            
            item.description = description
            item.save()
            item_updated = True

        if pd.notna(brand):
            ItemAttribute.objects.update_or_create(
                item=item,
                attribute=Attribute.objects.get(name='Бренд'),
                defaults={'value': brand}                
            )
            item_updated = True
        
        if pd.notna(country):
            ItemAttribute.objects.update_or_create(
                item=item,
                attribute=Attribute.objects.get(name='Страна'),
                defaults={'value': country}
            )
            item_updated = True
            
        return item_updated

    def process_images(self, item, img_urls):
        """Обрабатывает изображения и добавляет их к товару, если у товара еще нет изображений."""
        if pd.notna(img_urls):
            # Проверяем, есть ли у товара уже изображения
            if ItemImage.objects.filter(item=item).exists():
                self.stdout.write(self.style.WARNING(f'Item {item.article} already has images, skipping image updates.'))
                return
            
            urls = img_urls.replace('\n', ',').split(',')
            for url in urls:
                self.add_image_to_item(item, url.strip())
    
    def add_image_to_item(self, item, url):
        try:
            img_temp = NamedTemporaryFile(delete=True)
            img_temp.write(urlopen(url).read())
            img_temp.flush()
            item_image = ItemImage(item=item)
            item_image.image.save(os.path.basename(url), File(img_temp), save=True)
            self.stdout.write(self.style.SUCCESS(f'Added image from {url} to item {item.article}.'))
        except Exception as e:
            self.stdout.write(self.style.WARNING(f'Could not add image from {url} to item {item.article}: {e}'))