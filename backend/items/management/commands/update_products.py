import pandas as pd
from django.core.management.base import BaseCommand
from items.models import Item


class Command(BaseCommand):
    help = "Update products from Excel file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Путь к Excel файлу")

    def check_actuality(self, list_to_delete, list_actual):
        actual_data = set(list_to_delete) - set(list_actual)
        for article in actual_data:
            try:
                item = Item.objects.get(article=article)
                print(f"Ненужный товар {item.name}:{item.article}")
                item.delete()
            except Item.DoesNotExist:
                pass

    def handle(self, **kwargs):
        file_path = kwargs["file_path"]
        df = pd.read_excel(file_path)

        columns = ["Прайс-лист", "Unnamed: 2", "Unnamed: 3", "Unnamed: 4"]
        data = df[columns].values.tolist()

        ignore_until = "Ванна поддоны"
        parsing_started = False

        list_to_delete = []
        list_actual = []

        rows_to_process = []
        articles_in_file = set()

        for row in data:
            if all(pd.isna(cell) for cell in row):
                continue

            row_str = str(row[0])
            article = str(row[2]).strip()

            if not parsing_started:
                if article:
                    list_to_delete.append(article)
                if row_str.strip() == ignore_until:
                    parsing_started = True
                continue

            if all(pd.isna(row[i]) for i in range(1, 4)):
                continue

            rows_to_process.append(row)
            if article:
                articles_in_file.add(article.lower())

        existing_items = Item.objects.filter(article__iexact__in=articles_in_file)
        existing_map = {item.article.lower(): item for item in existing_items}

        items_to_create = []
        items_to_update = []

        for row in rows_to_process:
            name = row[0]
            quantity = row[1]
            article = str(row[2]).strip()
            article_key = article.lower()
            price = row[3]

            if not article:
                print(f"Пропущен товар без артикула: {name}")
                continue

            list_actual.append(article)

            if pd.isna(quantity):
                quantity = 0
            available = quantity > 0
            if not available:
                quantity_status = "Привезем под заказ"
            elif quantity < 2:
                quantity_status = "Скоро закончится"
            else:
                quantity_status = "В наличии"

            existing_item = existing_map.get(article_key)

            if existing_item:
                changed = False

                if existing_item.name != name:
                    existing_item.name = name
                    changed = True

                if existing_item.price != price:
                    existing_item.price = price
                    changed = True

                if existing_item.quantity != quantity:
                    existing_item.quantity = quantity
                    changed = True

                if existing_item.available != available:
                    existing_item.available = available
                    changed = True

                if existing_item.quantity_status != quantity_status:
                    existing_item.quantity_status = quantity_status
                    changed = True

                if changed:
                    items_to_update.append(existing_item)

            else:
                item = Item(
                    name=name,
                    article=article,
                    price=price,
                    available=available,
                    quantity_status=quantity_status,
                    category_id=268,
                    quantity=quantity,
                )
                items_to_create.append(item)

        if items_to_create:
            Item.objects.bulk_create(items_to_create, batch_size=500)

        if items_to_update:
            Item.objects.bulk_update(
                items_to_update,
                ["name", "price", "quantity", "available", "quantity_status"],
                batch_size=500,
            )

        self.check_actuality(list_to_delete, list_actual)

        self.stdout.write(self.style.SUCCESS("Successfully updated products"))
