import pandas as pd
from django.core.management.base import BaseCommand
from items.models import Item


class Command(BaseCommand):
    help = "Update products from Excel file"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Путь к Excel файлу")

    def check_actuality(self, list_to_delete, list_actual):
        unused_articles = set(list_to_delete) - set(list_actual)
        for article in unused_articles:
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
        rows_to_create = []
        items_to_update = []

        article_set = set()

        def filtered_rows(data):
            nonlocal parsing_started
            for row in data:
                if all(pd.isna(cell) for cell in row):
                    continue

                name = row[0]
                quantity = row[1]
                raw_article = row[2]
                price = row[3]

                if not parsing_started:
                    article = str(raw_article).strip().lower() if pd.notna(raw_article) else ""
                    if article:
                        list_to_delete.append(article)
                    if str(name).strip() == ignore_until:
                        parsing_started = True
                    continue

                if all(pd.isna(row[i]) for i in range(1, 4)):
                    continue

                if pd.isna(raw_article):
                    continue

                article = str(raw_article).strip().lower()
                if not article or article == "nan":
                    continue

                article_set.add(article)
                yield name, quantity, article, price

        existing_items = Item.objects.filter(article__in=article_set)
        existing_map = {item.article.lower(): item for item in existing_items}

        for name, quantity, article, price in filtered_rows(data):
            list_actual.append(article)

            quantity = int(quantity) if pd.notna(quantity) else 0
            available = quantity > 0
            if not available:
                quantity_status = "Привезем под заказ"
            elif quantity < 2:
                quantity_status = "Скоро закончится"
            else:
                quantity_status = "В наличии"

            item = existing_map.get(article)

            if item:
                changed_fields = []

                if item.name != name:
                    item.name = name
                    changed_fields.append("name")

                if item.price != price:
                    item.price = price
                    changed_fields.append("price")

                if item.quantity != quantity:
                    item.quantity = quantity
                    changed_fields.append("quantity")

                if item.available != available:
                    item.available = available
                    changed_fields.append("available")

                if item.quantity_status != quantity_status:
                    item.quantity_status = quantity_status
                    changed_fields.append("quantity_status")

                if changed_fields:
                    items_to_update.append(item)
            else:
                rows_to_create.append(
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

        if rows_to_create:
            Item.objects.bulk_create(rows_to_create, batch_size=500)

        if items_to_update:
            Item.objects.bulk_update(items_to_update, ["name", "price", "quantity", "available", "quantity_status"], batch_size=500)

        self.check_actuality(list_to_delete, list_actual)
        self.stdout.write(self.style.SUCCESS("Successfully updated products"))
