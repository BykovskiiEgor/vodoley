import os
import asyncio
from dataclasses import dataclass
from collections.abc import Generator
from defusedxml.ElementTree import fromstring
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from asgiref.sync import sync_to_async
from aiohttp import ClientSession
import httpx

from items.models import Item, ItemImage, ItemAttribute, Attribute

flexi_url = os.getenv("FLEXI_URL")


@dataclass
class ItemParse:
    article: str
    pictures: list
    description: str | None
    features: dict | None


class Command(BaseCommand):
    help = "Update all items from flexi"

    def process_features(self, features: str) -> dict:
        parsed_features = {}
        if features:
            for feature in features.split(";"):
                if ":" in feature:
                    key, value = feature.split(":", 1)
                    parsed_features[key.strip()] = value.strip()
        return parsed_features

    def process_file(self, text: str) -> Generator[ItemParse, None, None]:
        try:
            root = fromstring(text)
            offers = root.findall(".//offer")

            for offer in offers:
                article = offer.get("id")
                description = offer.findtext("description") or None
                features = offer.findtext("features") or None
                pictures = [pic.text for pic in offer.findall("picture")]
                parsed_features = self.process_features(features)
                if article and pictures:
                    yield ItemParse(
                        article,
                        pictures,
                        description,
                        parsed_features,
                    )
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error parsing XML: {e}"))

    async def download_data(self) -> str | None:
        """Загрузка XML с Flexi."""
        if not flexi_url:
            self.stdout.write(self.style.ERROR("FLEXI_URL is not defined."))
            return None

        try:
            async with ClientSession() as session:
                async with session.get(flexi_url, timeout=30) as response:
                    if response.status == 200:
                        return await response.text()
                    else:
                        self.stdout.write(self.style.ERROR(f"Failed to fetch data. HTTP Status: {response.status}"))
        except Exception as ex:
            self.stdout.write(self.style.ERROR(f"Error downloading data: {ex}"))
        return None

    async def download_image(self, url: str, product):
        """Асинхронная загрузка изображения."""
        if not url.startswith(("http", "https")):
            self.stdout.write(self.style.ERROR("URL must start with 'http:' or 'https:'"))
            return

        try:
            async with httpx.AsyncClient(http2=True) as client:
                response = await client.get(url)
                if response.status_code == 200:
                    img_data = response.content
                    item_image = ItemImage(item=product)
                    await sync_to_async(item_image.image.save, thread_sensitive=True)(
                        os.path.basename(url),
                        ContentFile(img_data),
                        save=True,
                    )
                    self.stdout.write(self.style.SUCCESS(f"Added image from {url}."))
                else:
                    self.stdout.write(self.style.ERROR(f"Error downloading image from {url}. HTTP Status: {response.status_code}"))
        except httpx.RequestError as ex:
            self.stdout.write(self.style.ERROR(f"Error downloading image from {url}: {ex}"))

    async def save_attributes(self, product, **attributes):
        """Сохранение атрибутов товара."""
        self.stdout.write(self.style.NOTICE(f"Обработка атрибутов: {product.article}"))

        for attr_name, attr_data in attributes.items():
            if not attr_data:
                continue
            attr_label, attr_value = attr_data
            if attr_value is None:
                continue

            attribute_obj, created = await sync_to_async(Attribute.objects.get_or_create, thread_sensitive=True)(name=attr_label)

            if created:
                self.stdout.write(self.style.SUCCESS(f"Создан новый атрибут: {attr_label}"))

            try:
                item_attr = await sync_to_async(ItemAttribute.objects.get, thread_sensitive=True)(item=product, attribute=attribute_obj)

                if item_attr.value != attr_value:
                    item_attr.value = attr_value
                    await sync_to_async(item_attr.save, thread_sensitive=True)()
                    self.stdout.write(self.style.SUCCESS(f"Атрибут {attr_label} обновлён для {product.article}"))
            except ItemAttribute.DoesNotExist:
                await sync_to_async(ItemAttribute.objects.create, thread_sensitive=True)(
                    item=product,
                    attribute=attribute_obj,
                    value=attr_value,
                )
                self.stdout.write(self.style.SUCCESS(f"Атрибут {attr_label} добавлен для {product.article}"))

    async def add_description(self, article, description):
        """Обновление описания товара."""
        if description is None:
            return
        try:
            item = await sync_to_async(Item.objects.get, thread_sensitive=True)(article=article)
            if item.description != description:
                item.description = description
                await sync_to_async(item.save, thread_sensitive=True)()
                self.stdout.write(self.style.SUCCESS(f"Описание для {article} обновлено"))
        except Item.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Товар {article} не найден"))

    async def handle_async(self, data: str, items_articles: list):
        """Обработка данных асинхронно."""
        parsed_items = {item.article: item for item in self.process_file(data)}
        tasks = []
        semaphore = asyncio.Semaphore(10)

        async def limited_download(url, product):
            async with semaphore:
                await self.download_image(url, product)

        for product in items_articles:
            item = parsed_items.get(product.article)
            if not item:
                article_parts = set(product.article.split("/"))
                matched_key = next(
                    (key for key in parsed_items if set(key.split("/")) & article_parts),
                    None,
                )
                if matched_key:
                    item = parsed_items[matched_key]

            if item:
                await self.add_description(product.article, item.description)
                await self.save_attributes(
                    product=product,
                    **{k: (k, v) for k, v in (item.features or {}).items()},
                )

                has_images = await sync_to_async(product.images.exists, thread_sensitive=True)()
                if has_images:
                    self.stdout.write(self.style.WARNING(f"Product {product.article} already has images, skipping download."))
                    continue

                for url in item.pictures:
                    tasks.append(asyncio.create_task(limited_download(url, product)))

        results = await asyncio.gather(*tasks, return_exceptions=True)
        for idx, result in enumerate(results):
            if isinstance(result, Exception):
                self.stderr.write(f"Task {idx} failed with error: {result}")

    def handle(self, *args, **options):
        asyncio.run(self.main_async())

    async def main_async(self):
        data = await self.download_data()
        if not data:
            return
        items_articles = await sync_to_async(list)(Item.objects.all())
        self.stdout.write(self.style.SUCCESS(f"Processing {len(items_articles)} items"))
        await self.handle_async(data, items_articles)
