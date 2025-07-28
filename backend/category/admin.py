from category.models import Categories
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin

# Register your models here.


admin.site.register(
    Categories,
    DraggableMPTTAdmin,
    list_display=(
        "tree_actions",
        "indented_title",
        # ...more fields if you feel like it...
    ),
    list_display_links=("indented_title",),
)
