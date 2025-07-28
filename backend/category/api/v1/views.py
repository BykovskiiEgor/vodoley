from category.models import Categories
from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from .serializers import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    pagination_class = None
    queryset = Categories.objects.filter(level=0)
    serializer_class = CategorySerializer
