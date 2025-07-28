from django.core.management.base import BaseCommand
from items.models import Item
from category.models import Categories


class Command(BaseCommand):
    help = 'Get information from flexi and edit items'    
        
    def handle(self, **kwargs):        
       
        keyword_category_map = {
            '55*110': '55*110',          
        }
        
        items = Item.objects.filter(category = 268)
        
        categories = {category.name: category for category in Categories.objects.all()}
       
        for item in items:
            category_assigned = False  
            for keyword, category_name in keyword_category_map.items():
                if keyword.lower() in item.name.lower():
                    item.category = categories.get(category_name)
                    if item.category:  
                        item.save()
                        print(f'Updated item {item.name} with category {category_name}')
                    else:
                        print(f'Category {category_name} not found for item {item.name}')
                    category_assigned = True
                    break  
            if not category_assigned:
                print(f'No category assigned for item {item.name}')