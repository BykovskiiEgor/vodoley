from django.urls import path

from .views import CategoryViewSet

app_name = "api"

urlpatterns = [
    path("categories/", CategoryViewSet.as_view({"get": "list"}), name="categories_list"),
]
