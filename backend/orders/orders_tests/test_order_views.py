from decimal import Decimal
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from unittest.mock import Mock, patch
from django.urls import reverse

class CreateOrderViewTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('api-order:create-order') 

        self.order_data = {
        'phone_number':'89273388323',
        'first_name':'test',
        'last_name':'test',
        'email': 'test@example.com',
        'total_price': '100.0',
        'city': 'Test City',
        'street': 'Test Street',
        'house': '123',
        'flat': '45',
        'products': {
            1: {'article': 'PROD001', 'quantity': 2},
            2: {'article': 'PROD002', 'quantity': 1},
            },
    }    

    @patch('services.user_service.UserService.get_or_create_user')
    def test_create_order_fail(self, mock_get_or_create_user):
        
        mock_get_or_create_user.return_value = None
        
        response = self.client.post(self.url, self.order_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
