from rest_framework import serializers
from items.models import Item, Attribute, ItemImage, ItemAttribute, RecommendItem

class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Attribute
        fields = ['name']  
        
        
class ItemAttributeSerializer(serializers.ModelSerializer):
    attribute = AttributeSerializer(read_only=True)
    class Meta:
        model=ItemAttribute
        fields = ['attribute', 'value']
        
        
class ItemImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ItemImage
        fields = ['image']
        

class AttributeValueSerializer(serializers.Serializer):
    name = serializers.CharField()
    values = serializers.ListField(child=serializers.CharField())
    
    
class ItemSerializer(serializers.ModelSerializer):
    attributes = ItemAttributeSerializer(many=True, read_only=True)
    images = ItemImageSerializer(many=True, read_only=True)
    avg_rating = serializers.DecimalField(max_digits=5, decimal_places=2, read_only=True)  
    user_rating = serializers.IntegerField(read_only=True, allow_null=True)

    class Meta:
        model= Item
        fields = [
            'id',
            'name', 
            'article', 
            'price',                
            'description',
            'available',
            'category',
            'attributes',
            'images',  
            'discount_percent', 
            'discount_price',  
            'quantity_status',   
            'is_active',   
            'avg_rating', 
            'user_rating',
            'quantity',
            ]
   
   
class ItemListWithAttributesSerializer(serializers.Serializer):
    items = ItemSerializer(many=True)
    available_attributes = AttributeValueSerializer(many=True)        
        

class RecommendItemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    
    class Meta:
        model = RecommendItem
        fields = ['item']
        
        
class OrdertemSerializer(serializers.ModelSerializer):
    item = ItemSerializer(read_only=True)
    
    class Meta:
        model = RecommendItem
        fields = ['item']
        
class Images(serializers.ModelSerializer):
    item_id = serializers.PrimaryKeyRelatedField(source='item.id', read_only=True)
    image = ItemImageSerializer
    
    class Meta:
        model = ItemImage
        fields = ['item_id', 'image']