from repositories.order_repository import OrderRepository
from repositories.items_repository import ItemsRepository
from services.order_service import OrderService

def get_order_service():
    """di."""
    order_repo = OrderRepository()
    items_repo = ItemsRepository()
    return OrderService(order_repo, items_repo)
