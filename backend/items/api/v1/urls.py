from django.urls import path

from . import views
from items.views import run_custom_command

app_name = "api-items"

urlpatterns = [
    path("search/", views.ItemSearchView.as_view(), name="items_search"),
    path("current-items/<int:id>/", views.CurrentItemView.as_view(), name="current_item"),
    path("items/category/<int:category_id>", views.GetByCategory.as_view(), name="get-by-category"),
    path("update-products/", views.UpdateProducts.as_view(), name="update-products"),
    path("recommendations/", views.RecommendItemsView.as_view(), name="recommendations"),
    path("discounts/", views.ItemsWithDiscounts.as_view(), name="discounts"),
    path("preorder/", views.OrderItem.as_view(), name="preorder"),
    path("rate-item/", views.StarRateItems.as_view(), name="star-rating"),
    path("get-images", views.GetAllImages.as_view(), name="all-images"),
    path("search-photo/", views.SearchByPhoto.as_view(), name="serch_by_photo"),
    path("update-flexi/", run_custom_command, name="update-flexi"),
]
