import os
import asyncio
from dataclasses import dataclass
from defusedxml.ElementTree import fromstring
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
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
    help = "Fast update items from Flexi with optimized routines"

    def parse_xml(self, text: str) -> dict[str, ItemParse]:
        root = fromstring(text)
        res = {}

        for offer in root.findall(".//offer"):
            article = offer.get("id")
            if not article:
                continue

            pictures = [p.text for p in offer.findall("picture") if p.text]
            if not pictures:
                continue

            description = offer.findtext("description") or None
            features_raw = offer.findtext("features")

            features = {}
            if features_raw:
                for f in features_raw.split(";"):
                    if ":" in f:
                        k, v = f.split(":", 1)
                        features[k.strip()] = v.strip()

            res[article] = ItemParse(article=article, pictures=pictures, description=description, features=features or None)

        return res

    async def download_xml(self) -> str | None:
        if not flexi_url:
            self.stdout.write(self.style.ERROR("FLEXI_URL missing"))
            return None

        async with httpx.AsyncClient() as client:
            try:
                r = await client.get(flexi_url, timeout=30)
                if r.status_code == 200:
                    return r.text
                self.stdout.write(self.style.ERROR(f"Bad status: {r.status_code}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(str(e)))

        return None

    async def download_images(self, parsed: dict, existing_items: dict):
        semaphore = asyncio.Semaphore(10)
        tasks = []
        images = []

        async with httpx.AsyncClient(http2=True) as client:

            async def fetch(url, item):
                async with semaphore:
                    try:
                        r = await client.get(url)
                        if r.status_code == 200:
                            images.append((item, os.path.basename(url), r.content))
                    except:
                        pass

            for article, item in existing_items.items():
                if item.images.exists():
                    continue

                p = parsed.get(article)
                if not p:
                    continue

                for url in p.pictures:
                    tasks.append(asyncio.create_task(fetch(url, item)))

            if tasks:
                await asyncio.gather(*tasks)

        return images

    def process_items_and_attributes(self, parsed):
        items = {it.article: it for it in Item.objects.all().prefetch_related("images")}
        self.stdout.write(self.style.SUCCESS(f"Loaded {len(items)} items"))

        to_update_desc = []
        for article, item in items.items():
            p = parsed.get(article)
            if p and p.description and item.description != p.description:
                item.description = p.description
                to_update_desc.append(item)

        if to_update_desc:
            Item.objects.bulk_update(to_update_desc, ["description"])
            self.stdout.write(self.style.SUCCESS(f"Updated descriptions: {len(to_update_desc)}"))

        attr_names = set()
        for p in parsed.values():
            if p.features:
                attr_names.update(p.features.keys())

        attr_map = {a.name: a for a in Attribute.objects.filter(name__in=attr_names)}

        missing = [Attribute(name=a) for a in attr_names if a not in attr_map]
        if missing:
            Attribute.objects.bulk_create(missing)
            for a in missing:
                attr_map[a.name] = a

            self.stdout.write(self.style.SUCCESS(f"Created attributes: {len(missing)}"))

        existing_ia = {(ia.item_id, ia.attribute_id): ia for ia in ItemAttribute.objects.all()}

        to_create = []
        to_update = []

        for article, item in items.items():
            p = parsed.get(article)
            if not p or not p.features:
                continue

            for k, v in p.features.items():
                attr = attr_map[k]
                key = (item.id, attr.id)

                existing = existing_ia.get(key)
                if existing:
                    if existing.value != v:
                        existing.value = v
                        to_update.append(existing)
                else:
                    to_create.append(ItemAttribute(item_id=item.id, attribute_id=attr.id, value=v))

        if to_create:
            ItemAttribute.objects.bulk_create(to_create)

        if to_update:
            ItemAttribute.objects.bulk_update(to_update, ["value"])

        self.stdout.write(self.style.SUCCESS(f"Attributes added: {len(to_create)}, updated: {len(to_update)}"))

        return items

    def save_images_sync(self, images_to_create):
        for item, filename, data in images_to_create:
            img = ItemImage(item=item)
            img.image.save(filename, ContentFile(data), save=True)

        self.stdout.write(self.style.SUCCESS(f"Images saved: {len(images_to_create)}"))

    def handle(self, *args, **options):
        xml = asyncio.run(self.download_xml())
        if not xml:
            return

        parsed = self.parse_xml(xml)

        items = self.process_items_and_attributes(parsed)

        images_to_create = asyncio.run(self.download_images(parsed, items))

        self.save_images_sync(images_to_create)
