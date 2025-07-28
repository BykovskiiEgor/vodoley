from repositories.user_repository import TemporaryPasswordRepository
from repositories.user_repository import UserRepository
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from services.mail_service import MailService
from services.user_service import UserService
from user.api.v1.serializers import UserRegistrationSerializer

from ...dependencies import get_order_service
from .serializers import OrderAddressSerializer
from .serializers import OrderSerializer


class CreateOrderView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        order_service = get_order_service()
        user_repository = UserRepository()
        temp_password_repository = TemporaryPasswordRepository()
        user_service = UserService(user_repository, temp_password_repository)
        mail_service = MailService()

        all_data = request.data

        try:
            user_data = {
                "email": all_data["email"],
                "first_name": all_data["first_name"],
                "last_name": all_data["last_name"],
                "phone_number": all_data["phone_number"],
            }
            order_data = {
                "total_price": all_data["total_price"],
                "products": all_data["products"],
                "address": all_data["address"],
            }

            user = user_service.get_or_create_user(user_data)
            if user is None:
                raise ValueError("User creation failed")

            user_service.check_user_data(user, user_data)

            order = order_service.create_order(order_data, user)

            mail_service.send_order_email(user_data, order_data)
            response_data = {
                "order": OrderSerializer(order).data,
                "user": UserRegistrationSerializer(user).data,
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error эта ": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class GetUsersOrders(generics.ListAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_service = get_order_service()

        email = request.data.get("email")
        query = request.query_params.get("filter")

        if email:
            order = order_service.get_users_orders(email, query)
            response_data = {
                "orders": OrderSerializer(order, many=True).data,
            }
            return Response(response_data, status=status.HTTP_200_OK)


class AddAddress(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_service = get_order_service()

        email = request.data.get("email")

        if email:
            order = order_service.get_users_orders(email)
            addresses = order_service.get_user_addresses(email)
            response_data = {
                "addresses": OrderAddressSerializer(addresses, many=True).data,
                "orders": OrderSerializer(order, many=True).data,
            }
            return Response(response_data, status=status.HTTP_200_OK)
