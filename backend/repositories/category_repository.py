"""CategoryRepository data access logic is encapsulated."""

from abc import ABC
from abc import abstractmethod

from category.models import Categories
from django.db.models import QuerySet


class ICategoryRepository(ABC):
    """Intrface for CategoryRepository."""

    @abstractmethod
    def get_all(self):
        """Abstract get all method."""

    @abstractmethod
    def get_by_category(self, category_id: int):
        """Abstract get items by category method."""

    @abstractmethod
    def get_all_subcategories(self):
        """Abstract get all subcategories method."""


class CategoryRepository(ICategoryRepository):
    """CategoryRepository."""

    def get_all(self) -> QuerySet[Categories]:
        """Return all categories."""
        return Categories.objects.all()

    def get_by_category(self, category_id: int) -> QuerySet[Categories]:
        """Get items by category."""
        return Categories.objects.get(id=category_id)

    def get_all_subcategories(self, category: list) -> set:
        """Get all categories of category."""
        subcategories = set()
        categories_to_check = [category]

        while categories_to_check:
            current_category = categories_to_check.pop()
            subcategories.add(current_category)
            children = current_category.children.all()
            categories_to_check.extend(children)

        return subcategories
