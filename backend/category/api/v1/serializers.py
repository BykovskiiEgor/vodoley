from category.models import Categories
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Categories
        fields = ("id", "name", "children", "image")

    def get_children(self, obj):
        children = obj.get_children()
        if children:
            return CategorySerializer(children, many=True).data
        return []
