# import pandas as pd
# from django.core.management.base import BaseCommand
# from items.models import Item
# class Command(BaseCommand):
#     help = 'Update products from Excel file'
#     def add_arguments(self, parser):
#         parser.add_argument('file_path', type=str, help='Путь к Excel файлу')
#     def check_actuality(self, list_to_delite, list_actual):
#         actual_data = set(list_to_delite) - set(list_actual)
#         for article in actual_data:
#             try:
#                 item = Item.objects.get(article=article)
#                 print(f"Ненужный товар {item.name}:{item.article}")
#                 item.delete()
#             except Item.DoesNotExist:
#                 pass
#     def handle(self, **kwargs):
#         list_to_delite = []
#         list_actual = []
#         file_path = kwargs['file_path']
#         df = pd.read_excel(file_path)
#         columns = ['Прайс-лист', 'Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4']
#         data = df[columns].values.tolist()
#         ignore_until = "Ванна поддоны"
#         parsing_started = False
#         def filtered_rows(data):
#             nonlocal parsing_started
#             for row in data:
#                 if all(pd.isna(cell) for cell in row):
#                     continue
#                 row_str = str(row[0])
#                 if not parsing_started:
#                     article = str(row[2]).strip().lower()
#                     list_to_delite.append(article)
#                     if row_str.strip() == ignore_until:
#                         parsing_started = True
#                     continue
#                 if all(pd.isna(row[i]) for i in range(1, 4)):
#                     continue
#                 yield row
#         for row in filtered_rows(data):
#             name = row[0]
#             quantity = row[1]
#             article = str(row[2]).strip().lower()
#             price = row[3]
#             try:
#                 list_actual.append(article)
#                 product = Item.objects.get(article__iexact=article)
#                 if product.name != name or product.price != price:
#                     product.name = name
#                     product.price = price
#                     product.save(update_fields=['name', 'price'])
#                 if pd.isna(quantity):
#                     available = False
#                     quantity_status = 'Привезем под заказ'
#                 else:
#                     available = True
#                     quantity_status = 'В наличии'
#                     if quantity < 2:
#                         quantity_status = 'Скоро закончится'
#                 if product.available != available or product.quantity_status != quantity_status:
#                     product.available = available
#                     product.quantity_status = quantity_status
#                     product.save(update_fields=['available', 'quantity_status'])
#             except Item.DoesNotExist:
#                 if pd.isna(quantity):
#                     available = False
#                     quantity_status = 'Привезем под заказ'
#                 else:
#                     available = True
#                     quantity_status = 'В наличии'
#                     if quantity < 2:
#                         quantity_status = 'Скоро закончится'
#                 Item.objects.create(
#                     name=name,
#                     article=article,
#                     price=price,
#                     available=available,
#                     quantity_status=quantity_status,
#                     category_id=1,
#                 )
#         self.check_actuality(list_to_delite, list_actual)
#         self.stdout.write(self.style.SUCCESS('Successfully updated products'))
import pandas as pd
from django.core.management.base import BaseCommand
from items.models import Item


class Command(BaseCommand):
    help = "Update products from Excel file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Путь к Excel файлу")

    def check_actuality(self, list_to_delite, list_actual):
        actual_data = set(list_to_delite) - set(list_actual)

        for article in actual_data:
            try:
                item = Item.objects.get(article=article)
                print(f"Ненужный товар {item.name}:{item.article}")
                item.delete()
            except Item.DoesNotExist:
                pass

    def handle(self, **kwargs):
        list_to_delite = []
        list_actual = []

        file_path = kwargs["file_path"]
        df = pd.read_excel(file_path)

        columns = ["Прайс-лист", "Unnamed: 2", "Unnamed: 3", "Unnamed: 4"]
        data = df[columns].values.tolist()

        ignore_until = "Ванна поддоны"
        parsing_started = False

        def filtered_rows(data):
            nonlocal parsing_started
            for row in data:
                if all(pd.isna(cell) for cell in row):
                    continue

                row_str = str(row[0])

                if not parsing_started:
                    article = str(row[2]).strip().lower()
                    list_to_delite.append(article)
                    if row_str.strip() == ignore_until:
                        parsing_started = True
                    continue

                if all(pd.isna(row[i]) for i in range(1, 4)):
                    continue

                yield row

        for row in filtered_rows(data):

            name = row[0]
            quantity = row[1]
            article = str(row[2]).strip().lower()
            price = row[3]

            try:
                list_actual.append(article)
                product = Item.objects.get(article__iexact=article)
                if pd.isna(quantity):
                    quantity = 0

                if product.name != name or product.price != price or product.quantity != quantity:
                    product.name = name
                    product.price = price
                    product.quantity = quantity
                    product.save(update_fields=["name", "price", "quantity"])

                if pd.isna(quantity) or quantity == 0:
                    available = False
                    quantity_status = "Привезем под заказ"
                else:
                    available = True
                    quantity_status = "В наличии"
                    if quantity < 2:
                        quantity_status = "Скоро закончится"

                if product.available != available or product.quantity_status != quantity_status:
                    product.available = available
                    product.quantity_status = quantity_status
                    product.save(update_fields=["available", "quantity_status"])

            except Item.DoesNotExist:
                if pd.isna(quantity):
                    available = False
                    quantity_status = "Привезем под заказ"
                    quantity = 0
                else:
                    available = True
                    quantity_status = "В наличии"
                    if quantity < 2:
                        quantity_status = "Скоро закончится"

                Item.objects.create(
                    name=name,
                    article=article,
                    price=price,
                    available=available,
                    quantity_status=quantity_status,
                    category_id=268,
                    quantity=quantity,
                )

        self.check_actuality(list_to_delite, list_actual)
        self.stdout.write(self.style.SUCCESS("Successfully updated products"))
