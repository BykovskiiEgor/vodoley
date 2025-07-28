from rest_framework import serializers
from orders.models import Order, OrderItem, Address

         
class OrderItemSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    class Meta:
        model = OrderItem
        fields = ['name', 
                  'quantity']
        
    def get_name(self, obj):
        return obj.item.name 
    
class OrderAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['address']
        
class OrderSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True)
    address = OrderAddressSerializer(many=True)

    class Meta:
        model = Order
        fields = ['total_price',
                  'order_date',
                  'orderitem_set',
                  'status',
                  'id', 
                  'address',                          
        ]
