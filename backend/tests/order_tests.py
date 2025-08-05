import pytest
from unittest.mock import Mock, MagicMock
from decimal import Decimal

from services.order_service import OrderService
from user.models import CustomUser


@pytest.fixture
def order_repo():
    return Mock()


@pytest.fixture
def item_repo():
    return Mock()


@pytest.fixture
def service(order_repo, item_repo):
    return OrderService(order_repo, item_repo)


@pytest.fixture
def user():
    return MagicMock(spec=CustomUser, email="test@example.com")


@pytest.mark.django_db
def test_create_order_success(service, order_repo, item_repo, user):
    order_mock = MagicMock()
    product_mock = MagicMock()
    order_repo.create_order.return_value = order_mock
    item_repo.get_product_by_id.return_value = product_mock

    order_data = {"total_price": "100.50", "address": "ул. Ленина, 1", "products": {"1": {"id": 1, "quantity": "2"}, "2": {"id": 2, "quantity": "3"}}}

    result = service.create_order(order_data, user)

    order_repo.create_order.assert_called_once_with(user=user, total_price=Decimal("100.50"))
    order_repo.add_order_adress.assert_called_once_with(order=order_mock, address="ул. Ленина, 1", user=user)
    assert item_repo.get_product_by_id.call_count == 2
    assert order_repo.add_order_item.call_count == 2
    assert result == order_mock


@pytest.mark.django_db
def test_create_order_with_empty_products(service, order_repo, item_repo, user):
    order_mock = MagicMock()
    order_repo.create_order.return_value = order_mock

    order_data = {"total_price": "0.00", "address": "ул. Пустая, 0", "products": {}}

    result = service.create_order(order_data, user)

    order_repo.create_order.assert_called_once()
    order_repo.add_order_adress.assert_called_once()
    item_repo.get_product_by_id.assert_not_called()
    order_repo.add_order_item.assert_not_called()
    assert result == order_mock


@pytest.mark.django_db
def test_create_order_raises_when_product_not_found(service, order_repo, item_repo, user):
    order_mock = MagicMock()
    order_repo.create_order.return_value = order_mock

    order_data = {"total_price": "10.00", "address": "ул. Ошибочная, 404", "products": {"1": {"id": 999, "quantity": "1"}}}

    item_repo.get_product_by_id.side_effect = Exception("Product not found")

    with pytest.raises(Exception) as exc_info:
        service.create_order(order_data, user)

    assert "Product not found" in str(exc_info.value)


def test_get_users_orders_applies_filter(service, order_repo):
    raw_orders = [MagicMock()]
    filtered_orders = [MagicMock()]
    order_repo.get_users_orders.return_value = raw_orders
    order_repo.filter_orders.return_value = filtered_orders

    query_params = {"status": "pending"}
    result = service.get_users_orders("test@example.com", query_params)

    order_repo.get_users_orders.assert_called_once_with("test@example.com")
    order_repo.filter_orders.assert_called_once_with(query_params, raw_orders)
    assert result == filtered_orders


def test_get_user_addresses_returns_value(service, order_repo):
    addresses = ["ул. Пушкина", "ул. Лермонтова"]
    order_repo.get_user_addresses.return_value = addresses

    result = service.get_user_addresses("test@example.com")

    order_repo.get_user_addresses.assert_called_once_with("test@example.com")
    assert result == addresses
