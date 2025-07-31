import logging
from typing import Any
from typing import List

from django.db.models import QuerySet
from elasticsearch_dsl import Q
from items.documents import ItemDocument
from items.models import Item
from repositories.items_repository import ItemsRepository
from services.category_service import CategoryService

logger = logging.getLogger(__name__)


class ItemsService:
    """ItemsService."""

    def __init__(self, items_repository: ItemsRepository, category_service: CategoryService) -> None:
        """Initialize the ItemsService with an ItemsRepository."""
        self.items_repository = items_repository
        self.category_service = category_service

    def search_items(self, query: str, query_params: dict[str, Any]) -> QuerySet[Item]:
        """Search for items based on the provided query and query parameters."""
        items = self.items_repository.search_items(query)
        if query_params:
            items = self.items_repository.filter_items(query_params, items)
        return items

    def search_by_elactic(self, query: str, query_params: dict[str, Any]) -> QuerySet[Item]:
        """Search for items based on query and parameters using Elasticsearch."""
        search = ItemDocument.search()

        if query:
            search = search.query(
                "bool",
                should=[
                    Q("match_phrase", name__standard={"query": query, "boost": 10}),
                    Q("match", name__standard={"query": query, "boost": 6}),
                    Q("match_phrase_prefix", name={"query": query, "boost": 3}),
                    Q("match", description={"query": query, "boost": 1}),
                    Q("match", article={"query": query, "boost": 1}),
                    Q("match", category__standard={"query": query, "boost": 3}),
                ],
                minimum_should_match=1,
            )

        search = search[:100]
        return search.to_queryset()

    def get_current_item(self, item_id: int, user: object) -> tuple[Item | None, list[dict]]:
        """Retrieve the current item by its ID along with category breadcrumbs."""
        try:
            item = self.items_repository.get_product_by_id(item_id, user)

            if not item or not item.category:
                return item

            item._breadcrumbs = item.category.get_ancestors(include_self=True)
            return item

        except Exception as e:
            logger.error(f"Error while getting item with breadcrumbs: {e}")
            return None

    def get_by_category(self, category_id: int, query_params: dict[str, Any]) -> tuple[QuerySet[Item], dict[str, Any]] | None:
        """Retrieve items by category and apply additional filters."""
        category = self.category_service.get_items_by_category(category_id)
        if not category:
            return None

        subcategories = self.category_service.get_all_subcategories(category)
        items = self.items_repository.get_by_category(subcategories)
        items = self.items_repository.get_items_attributes(items)
        items, price_range = self.items_repository.filter_items(query_params, items)

        return (items, price_range) if items.exists() else None

    def rate_star_item(self, item_id: int, user_id: int, rate: int) -> None:
        """Rate an item with a star rating."""
        item = self.items_repository.get_product_by_id(item_id, None)
        if item:
            self.items_repository.rate_item(item, user_id, rate)

    def get_all_images(self) -> List[str]:
        return self.items_repository.get_all_images()

    def search_by_photo(self, similar_product_ids: List[int]):
        return self.items_repository.search_by_photo(similar_product_ids)

    def get_available_attributes(self, items: QuerySet[Item]) -> list[dict[str, Any]]:
        attributes = {}

        item_attrs = self.items_repository.unique_attributes(items)

        for attr in item_attrs:
            name = attr.attribute.name
            value = attr.value
            attributes.setdefault(name, set()).add(value)

        return [{"name": name, "values": list(values)} for name, values in attributes.items() if len(values) > 1]
