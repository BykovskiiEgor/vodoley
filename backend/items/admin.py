# admin.py
from category.models import Categories
from django import forms
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from mptt.forms import TreeNodeChoiceField

from .models import Attribute
from .models import Item
from .models import ItemAttribute
from .models import ItemImage
from .models import RecommendItem


class ItemAttributeInline(admin.TabularInline):
    model = ItemAttribute
    extra = 1
    autocomplete_fields = ["attribute"]


class ItemImageInline(admin.TabularInline):
    model = ItemImage
    extra = 1


class CategoryFilter(admin.SimpleListFilter):
    title = _("category")
    parameter_name = "category"

    def lookups(self, request, model_admin):
        categories = Categories.objects.all()

        SPECIAL_CATEGORY_NAME = "Новинки"
        special_category = Categories.objects.filter(name=SPECIAL_CATEGORY_NAME).first()

        lookups = []
        if special_category:
            lookups.append((special_category.id, f"{'--' * special_category.level} {special_category.name}"))

        for category in categories.exclude(id=special_category.id if special_category else None):
            level_indicator = "--" * category.level
            lookups.append((category.id, f"{level_indicator} {category.name}"))

        return lookups

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(category__id=self.value())
        return queryset


class ItemAdminForm(forms.ModelForm):
    category = TreeNodeChoiceField(queryset=Categories.objects.all())

    class Meta:
        model = Item
        fields = "__all__"


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    form = ItemAdminForm
    list_display = (
        "name",
        "article",
        "price",
        "available",
        "category",
        "discount_percent",
    )
    search_fields = ("name", "article", "category__name")
    list_filter = (CategoryFilter,)
    inlines = [ItemAttributeInline, ItemImageInline]


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ["name"]


@admin.register(ItemAttribute)
class ItemAttributeAdmin(admin.ModelAdmin):
    list_display = ("item", "attribute", "value")
    search_fields = ("item__name", "attribute__name", "value")


@admin.register(ItemImage)
class ItemImageAdmin(admin.ModelAdmin):
    list_display = ("item", "image")
    search_fields = ("item__name",)


@admin.register(RecommendItem)
class RecommendItemAdmin(admin.ModelAdmin):
    list_display = ("item",)
    search_fields = ("item__name",)
