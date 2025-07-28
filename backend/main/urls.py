from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView


admin.site.site_header = "Водолей Админ Панель"
admin.site.index_title = "Администрирование"


urlpatterns = (
    [
        path(r"vodad!2112/", admin.site.urls),
        path("statistics/", include("statistic.urls"), name="admin-statistics"),
        path("api/", include("items.api.v1.urls", namespace="api-items")),
        path("api/", include("category.api.v1.urls", namespace="api")),
        path("api/", include("orders.api.v1.urls", namespace="api-order")),
        path("api/", include("user.api.v1.urls", namespace="api")),
        path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
        path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    ]
    + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)
