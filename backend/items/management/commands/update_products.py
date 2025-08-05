import pandas as pd
from django.core.management.base import BaseCommand
from items.models import Item
from django.db import transaction


class Command(BaseCommand):
    help = "Update products from Excel file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Путь к Excel файлу")

    def handle(self, **kwargs):
        file_path = kwargs["file_path"]
        df = pd.read_excel(file_path)

        columns = ["Прайс-лист", "Unnamed: 2", "Unnamed: 3", "Unnamed: 4"]
        data = df[columns].values.tolist()

        ignore_until = "Ванна поддоны"
        parsing_started = False

        list_to_delete = []
        list_actual = set()
        rows_to_process = []

        for row in data:
            if all(pd.isna(cell) for cell in row):
                continue

            row_str = str(row[0])

            article = str(row[2]).strip().lower()
            if not parsing_started:
                if article:
                    list_to_delete.append(article)
                if row_str.strip() == ignore_until:
                    parsing_started = True
                continue

            if all(pd.isna(row[i]) for i in range(1, 4)):
                continue

            rows_to_process.append(row)

        all_articles = {str(row[2]).strip().lower() for row in rows_to_process if row[2]}
        existing_items = Item.objects.filter(article__in=all_articles)
        existing_map = {item.article.lower(): item for item in existing_items}

        to_create = []
        to_update = []

        for row in rows_to_process:
            name = row[0]
            quantity = 0 if pd.isna(row[1]) else row[1]
            article = str(row[2]).strip().lower()
            price = row[3]

            if not article:
                print(f"Пропущен товар без артикула: {name}")
                continue

            list_actual.add(article)

            available = quantity > 0
            if not available:
                quantity_status = "Привезем под заказ"
            elif quantity < 2:
                quantity_status = "Скоро закончится"
            else:
                quantity_status = "В наличии"

            if article in existing_map:
                item = existing_map[article]
                updated_fields = []

                if item.name != name:
                    item.name = name
                    updated_fields.append("name")

                if item.price != price:
                    item.price = price
                    updated_fields.append("price")

                if item.quantity != quantity:
                    item.quantity = quantity
                    updated_fields.append("quantity")

                if item.available != available:
                    item.available = available
                    updated_fields.append("available")

                if item.quantity_status != quantity_status:
                    item.quantity_status = quantity_status
                    updated_fields.append("quantity_status")

                if updated_fields:
                    to_update.append(item)
            else:
                to_create.append(
                    Item(
                        name=name,
                        article=article,
                        price=price,
                        available=available,
                        quantity_status=quantity_status,
                        category_id=268,
                        quantity=quantity,
                    )
                )

        with transaction.atomic():
            if to_create:
                Item.objects.bulk_create(to_create, batch_size=500)

            if to_update:
                Item.objects.bulk_update(to_update, ["name", "price", "quantity", "available", "quantity_status"], batch_size=500)

            outdated_articles = set(list_to_delete) - list_actual
            if outdated_articles:
                deleted = Item.objects.filter(article__in=outdated_articles).delete()
                print(f"Удалено устаревших товаров: {deleted[0]}")

        self.stdout.write(self.style.SUCCESS("Successfully updated products"))
