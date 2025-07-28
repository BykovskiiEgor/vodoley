from category.models import Categories
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from items.models import Item
from items.models import RecommendItem
from rest_framework.test import APIClient
from rest_framework.test import APITestCase


class ViewsItemsTest(APITestCase):
    def setUp(self):
        Categories.objects.create(id=1, name="Test")
        Item.objects.create(
            name="Test Item 1",
            article=1,
            price=100,
            description="test",
            available=True,
            quantity_status="В налчии",
            discount_percent=10,
            is_active=True,
            category_id=1,
        )
        Item.objects.create(
            name="Test Item 2",
            article=2,
            price=200,
            description="test",
            available=True,
            quantity_status="В налчии",
            discount_percent="0.00",
            is_active=True,
            category_id=1,
        )

    def test_search_items(self):
        url = reverse("api-items:items_search") + "?q=Test Item 1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["count"], 1)

    def test_get_items_with_discounts(self):
        url = reverse("api-items:discounts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["count"], 1)


class CurrentItemViewTest(APITestCase):
    def setUp(self):
        Categories.objects.create(id=1, name="Test")
        self.item = Item.objects.create(
            name="Test1",
            article=1,
            price=100,
            description="test",
            available=True,
            quantity_status="В налчии",
            discount_percent=10,
            is_active=True,
            category_id=1,
        )

    def test_get_existing_item(self):
        url = reverse("api-items:current_item", kwargs={"id": self.item.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], "Test1")

    def test_get_non_existing_item(self):
        url = reverse("api-items:current_item", kwargs={"id": 999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class UpdateProductsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

    def test_update_products_without_file(self):
        response = self.client.post(reverse("api-items:update-products"))
        self.assertEqual(response.status_code, 401)

    def test_update_products_with_file(self):
        file = SimpleUploadedFile("test.xlsx", b"file_content", content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response = self.client.post(reverse("api-items:update-products"), {"file": file}, format="multipart")
        self.assertEqual(response.status_code, 401)


class RecommendItemsViewTest(APITestCase):
    def setUp(self):
        Categories.objects.create(id=1, name="Test")
        Item.objects.create(
            id=1,
            name="Test Item 1",
            article=1,
            price=100,
            description="test",
            available=True,
            quantity_status="В налчии",
            discount_percent=10,
            is_active=True,
            category_id=1,
        )
        RecommendItem.objects.create(item_id=1)

    def test_get_recommend_items(self):
        url = reverse("api-items:recommendations")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["count"], 1)


class OrderItemTest(APITestCase):
    def test_post_order_item(self):
        data = {"phone": "1234567890", "comment": "Test order", "quantity": 1, "product": "Product 1"}
        response = self.client.post(reverse("api-items:preorder"), data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["message"], "Order submitted successfully")

    def test_invalid_phone(self):
        data = {"phone": "", "comment": "Test order", "quantity": 1, "product": "Product 1"}
        response = self.client.post(reverse("api-items:preorder"), data, format="json")
        self.assertEqual(response.status_code, 400)
