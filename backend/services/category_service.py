"""CategoryService is used to receive and process data."""

from typing import List
from category.models import Categories
from django.db.models import QuerySet
from repositories.category_repository import CategoryRepository


class CategoryService:
    """CategoryService."""

    def __init__(self, category_repository: CategoryRepository) -> None:
        """Initialize the CategoryService with an CategoryRepository."""
        self.category_repository = category_repository

    def get_all_categories(self) -> QuerySet[Categories]:
        """Return all categories."""
        return self.category_repository.get_all()

    def get_items_by_category(self, category_id: int) -> QuerySet[Categories]:
        """Get items by category."""
        return self.category_repository.get_by_category(category_id)

    def get_all_subcategories(self, category: list) -> set:
        """Get all subcategories."""
        return self.category_repository.get_all_subcategories(category)

    def get_all_subcategories_ids(self, category_id: int) -> List[int]:
        """Get all subcategory IDs including the main category using MPTT."""
        try:
            category = Categories.objects.get(id=category_id)
            descendants = category.get_descendants(include_self=True)
            return list(descendants.values_list("id", flat=True))
        except Categories.DoesNotExist:
            return []
