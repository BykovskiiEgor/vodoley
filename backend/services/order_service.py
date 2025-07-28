from repositories.order_repository import OrderRepository
from repositories.items_repository import ItemsRepository
from decimal import Decimal
from typing import Any
from user.models import CustomUser
from orders.models import Order
from django.db import transaction


class OrderService:
    """OrderService."""
    
    def __init__(self, order_repository: OrderRepository, item_repository: ItemsRepository) ->  None:
        """Initialize the OrderService with an OrderRepository and ItemsRepository."""   
        self.order_repository = order_repository
        self.item_repository = item_repository

    @transaction.atomic
    def create_order(self, order_data: dict[str, Any] , user: CustomUser) -> Order:   
        """Create new order."""
        order = self.order_repository.create_order(
            user=user,
            total_price=Decimal(order_data['total_price']),            
        )    
        
        self.order_repository.add_order_adress(
            order=order,
            address=order_data['address'],
            user=user,
        )

        for product_id, product_data in order_data['products'].items():
            product = self.item_repository.get_product_by_id(product_data['id'], None)
            self.order_repository.add_order_item(order, product, Decimal(product_data['quantity']))
        
        return order
    
    def get_users_orders(self, email, query_params: dict[str, Any]):
        """Get all orders of user."""
        orders = self.order_repository.get_users_orders(email)         
        orders = self.order_repository.filter_orders(query_params, orders)
        return orders 
    
    def get_user_addresses(self, email):
        """Get all addresses of user."""
        return self.order_repository.get_user_addresses(email)  
