from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import List

from django.db.models import Avg
from django.db.models import Max
from django.db.models import Min
from django.db.models import OuterRef
from django.db.models import Prefetch
from django.db.models import QuerySet
from django.db.models import Subquery
from items.models import Item
from items.models import ItemAttribute
from items.models import ItemImage
from items.models import ItemStarRating


class IItemsRepository(ABC):
    """Intrface for ItemsRepository."""

    @abstractmethod
    def search_items(self) -> None:
        """Abstract search method."""

    @abstractmethod
    def filter_items(self, query_params: dict[str, Any]) -> None:
        """Abstract filter items method."""

    @abstractmethod
    def get_by_category(self, category_id: int) -> None:
        """Abstract get by category method."""

    @abstractmethod
    def rate_item(self, item: Item, user_id: int, rate: int) -> None:
        """Abstract search method."""

    @abstractmethod
    def get_all_images(self) -> List[ItemImage]:
        """Abstract method for all images."""

    @abstractmethod
    def get_items_attributes(self):
        """Abstract method for all attributes."""

    @abstractmethod
    def unique_attributes(self):
        pass


class ItemsRepository(IItemsRepository):
    """ItemsRepository."""

    def search_items(self, query: str) -> QuerySet[Item]:
        """Search for items based on query.

        _Args:
            query (str): search string

        _Returns:
            _type_: _description_
        """
        return Item.objects.filter(name__icontains=query, is_active=True)

    def get_product_by_id(self, id: int, user: object | None = None) -> Item | None:
        """Retrieve the current item by its ID."""
        try:
            queryset = Item.objects.filter(id=id).annotate(
                avg_rating=Avg("itemstarrating__stars"),
            )

            if user and hasattr(user, "id"):
                queryset = queryset.annotate(
                    user_rating=Subquery(
                        ItemStarRating.objects.filter(
                            item=OuterRef("pk"),
                            user=user,
                        ).values(
                            "stars"
                        )[:1],
                    ),
                )

            return queryset.first()
        except Item.DoesNotExist:
            return None

    def filter_items(self, query_params: dict[str, Any], items: QuerySet[Item]) -> tuple[QuerySet[Item], dict[str, Any]]:
        """Filter items based on query parameters."""
        items = items.filter(is_active=True)

        if "filter" in query_params:
            if query_params["filter"] == "exists":
                items = items.filter(available=True)
            elif query_params["filter"] == "not_exists":
                items = items.filter(available=False)

        if "sort" in query_params:
            if query_params["sort"] == "asc":
                items = items.order_by("price")
            elif query_params["sort"] == "desc":
                items = items.order_by("-price")

        attribute_filters = {key: value for key, value in query_params.items() if key.startswith("attributeFilters[") and value}

        if attribute_filters:
            for key, value in query_params.items():
                if key.startswith("attributeFilters[") and value:
                    attr_name = key[len("attributeFilters[") : -1]
                    items = items.filter(
                        attributes__attribute__name=attr_name,
                        attributes__value=value,
                    ).distinct()

        price_min = query_params.get("priceMin")
        price_max = query_params.get("priceMax")

        if price_min:
            items = items.filter(price__gte=float(price_min))
        if price_max and float(price_max) > 0:
            items = items.filter(price__lte=float(price_max))

        price_range = items.aggregate(
            min_price=Min("price"),
            max_price=Max("price"),
        )

        return items, price_range

    def get_by_category(self, category_id: int) -> QuerySet[Item]:
        """Get items by category."""
        return Item.objects.filter(category__in=category_id, is_active=True).annotate(avg_rating=Avg("itemstarrating__stars"))

    def rate_item(self, item: Item, user_id: int, rate: int) -> None:
        """Rate an item by a user."""
        rating, created = ItemStarRating.objects.get_or_create(
            item=item,
            user_id=user_id,
            defaults={"stars": rate},
        )

        if not created:
            raise ValueError(f"User {user_id} has already rated item {item.id}")

    def get_all_images(self):
        return ItemImage.objects.all()

    def search_by_photo(self, similar_product_ids: List[int]):
        items = Item.objects.filter(id__in=similar_product_ids)
        return items

    def get_items_attributes(self, items: list):
        items = items.prefetch_related(
            Prefetch("attributes", queryset=ItemAttribute.objects.select_related("attribute").order_by("value")),
        )

        return items

    def unique_attributes(self, items):
        return ItemAttribute.objects.filter(item__in=items).select_related("attribute")
