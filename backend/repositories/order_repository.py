from abc import ABC, abstractmethod 
from typing import Any
from orders.models import Order, OrderItem, Address
from decimal import Decimal
from user.models import CustomUser
from items.models import Item
from django.db.models import QuerySet
from django.core.exceptions import ValidationError


class IOrderRepository(ABC):
    """Abstarct order repository."""
    
    @abstractmethod
    def create_order(self, total_price: Decimal, user: CustomUser):
        """Abstract create order method."""
        pass
    
    @abstractmethod
    def add_order_item(self, order: Order, item: OrderItem, quantity: Decimal):
        """Abstract add item to order method."""
        pass
    
class OrderRepository(IOrderRepository):
    """OrderRepository."""

    def create_order(self, total_price: Decimal, user: CustomUser) -> Order:
        """Create new order."""
        return Order.objects.create(total_price=total_price, user=user)
        
        
    def add_order_item(self, order: Order, item: Item, quantity: Decimal) -> OrderItem:
        """Add item to order and update item quantity."""
        if item.quantity is None or item.quantity < quantity:
            raise ValidationError("Недостаточно товара на складе")
        
        if item.quantity == quantity:
            item.quantity_status = 'Привезем под заказ'
            
        item.quantity -= quantity
        item.save(update_fields=["quantity","quantity_status"])

        return OrderItem.objects.create(
            order=order,
            item=item,
            quantity=quantity,
            price=item.price,
        )
        
    def add_order_adress(self, order: Order, address: str, user: CustomUser) -> Address:
        """Add adress to order."""
        return Address.objects.create(
            address = address,
            order = order,
            user = user,
        )
        
        
    def filter_orders(self, query_params: str, orders: QuerySet[Order]) -> QuerySet[Order]:
        if query_params:
            status_map = {
                '1': 'В ожидании',
                '2': 'Обработан',
                '3': 'Собран',
                '4': 'Доставлен',
            }
            
            status = status_map.get(query_params)
            
            if status:
                orders = orders.filter(status=status)
        
        return orders
    
    
    def get_users_orders(self, email: str) -> QuerySet[Order]:
        """Get all orders of user."""
        return Order.objects.filter(user__email=email).order_by('-order_date')
    
    def get_user_addresses(self, email: str) -> QuerySet[Address]:
        return Address.objects.filter(user__email=email)
    