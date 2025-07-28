from django.db import models
from category.models import Categories
from user.models import CustomUser


class Item(models.Model):  
    name = models.CharField('Имя', max_length=200)
    article = models.CharField('Артикул', max_length=100, default=1)    
    price = models.DecimalField('Цена', max_digits=10, decimal_places=2)    
    description = models.TextField('Описание товара', null=True, blank=True)
    available = models.BooleanField('Досутпен ли',default=True)
    quantity_status = models.CharField(default=None, null=True, blank=True)
    quantity = models.IntegerField('Количество', null=True, blank=True)
    discount_percent = models.DecimalField('Скидка', max_digits=5, decimal_places=2, default=0.0)
    is_active = models.BooleanField(default=True)
    category = models.ForeignKey(Categories,
        related_name='Item',                        
        on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        indexes = [
        models.Index(fields=['article']),
        models.Index(fields=['name']),
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


    def __str__(self):     
        return self.name
    
    @property
    def discount_price(self):
        if self.discount_percent > 0:
            return self.price - (self.price * self.discount_percent / 100)
        return None


class Attribute(models.Model):
    name = models.CharField('Название атрибута', max_length=200)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Атрибут'
        verbose_name_plural = 'Атрибуты'
    
    
class ItemAttribute(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='attributes')
    attribute = models.ForeignKey('Attribute', on_delete=models.CASCADE)
    value = models.CharField('Значение', max_length=200)
    
    def __str__(self):
        return f"{self.item.name} - {self.attribute.name}: {self.value}"
    
    class Meta:
        verbose_name = 'Атрибут товара'
        verbose_name_plural = 'Атрибуты товаров'
    

class ItemImage(models.Model):
    item = models.ForeignKey(Item, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField('Фото', upload_to='media/imgs', null=True, blank=True)
    
    def __str__(self):
        return f"{self.item.name} Image"
    
    class Meta:
        verbose_name = 'Фото товара'
        verbose_name_plural = 'Фотографии товаров'
    
    
class RecommendItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.item.name
    
    class Meta:
        verbose_name = 'Рекомендуемый товар'
        verbose_name_plural = 'Рекомендуемые товары'
    
    
class ItemStarRating(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    stars = models.IntegerField(default=0)
    
   