from django.db import models
from mptt.models import MPTTModel
from mptt.models import TreeForeignKey


class Categories(MPTTModel):
    name = models.CharField(max_length=200)
    parent = TreeForeignKey("category.Categories", on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    image = models.ImageField("Фото", upload_to="media/imgs", null=True, blank=True)

    class MPTTMeta:
        order_insertion_by = ["name"]
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
