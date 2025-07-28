from rest_framework import viewsets
from category.models import Categories
from .serializers import CategorySerializer
from rest_framework.permissions import AllowAny


class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [AllowAny]
    pagination_class = None
    queryset = Categories.objects.filter(level=0)  
    serializer_class = CategorySerializer

