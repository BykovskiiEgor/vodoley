import logging
import os
import subprocess

import requests
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from items.models import Item
from items.models import RecommendItem
from items.pagination import CustomPageNumberPagination
from repositories.category_repository import CategoryRepository
from repositories.items_repository import ItemsRepository
from rest_framework import generics
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from services.category_service import CategoryService
from services.items_service import ItemsService
from user.models import CustomUser

from .serializers import Images
from .serializers import ItemSerializer
from .serializers import RecommendItemSerializer


logger = logging.getLogger(__name__)

EXTERNAL_SERVICE_URL = os.getenv("EXTERNAL_SERVICE_URL")


items_service = ItemsService(ItemsRepository(), CategoryService(CategoryRepository()))


class ItemSearchView(generics.ListAPIView):
    serializer_class = ItemSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        query = self.request.query_params.get("q", "")
        query_params = self.request.query_params
        if query or query_params:
            return items_service.search_by_elactic(query, query_params)
        return Item.objects.none()


class CurrentItemView(generics.RetrieveAPIView):
    serializer_class = ItemSerializer
    pagination_class = None
    permission_classes = [AllowAny]

    queryset = Item.objects.none()

    def get_object(self):
        item_id = self.kwargs.get("id")
        if not item_id:
            raise NotFound("ID parameter is required")
        user = self.request.user if self.request.user.is_authenticated else None
        try:
            item = items_service.get_current_item(item_id, user)
            if item is None:
                raise NotFound("Item not found")
            return item
        except Item.DoesNotExist:
            raise NotFound("Item not found")


class GetByCategory(generics.ListAPIView):
    serializer_class = ItemSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        query = self.request.query_params

        if category_id:
            result = items_service.get_by_category(category_id, query)
            if result:
                items, price_range = result
                self.price_range = price_range
                return items

        self.price_range = {}
        return Item.objects.none()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            items_serializer = self.get_serializer(page, many=True)
            items_for_attributes = queryset
        else:
            items_serializer = self.get_serializer(queryset, many=True)
            items_for_attributes = queryset

        available_attributes = items_service.get_available_attributes(items_for_attributes)

        response_data = {
            "items": items_serializer.data,
            "available_attributes": available_attributes,
            "price_range": self.price_range,
        }

        if page is not None:
            paginated = self.get_paginated_response(items_serializer.data)
            paginated.data["available_attributes"] = available_attributes
            paginated.data["price_range"] = self.price_range
            return paginated

        return Response(response_data)


class UpdateProducts(APIView):
    pagination_class = None

    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        if user.is_superuser is True:
            if "file" not in request.FILES:
                logger.error("File not found in request")
                return Response({"status": "error", "message": "Файл не найден"}, status=400)

            file = request.FILES["file"]
            file_path = default_storage.save("data.xlsx", ContentFile(file.read()))
            abs_file_path = default_storage.path(file_path)
            logger.info(f"File saved to {abs_file_path}")

            manage_py_path = "/app/backend/manage.py"
            logger.info(f"Using manage.py at {manage_py_path}")

            try:
                result = subprocess.run(
                    ["python", manage_py_path, "update_products", abs_file_path],
                    capture_output=True,
                    text=True,
                )
                logger.info(f"Subprocess run completed with returncode {result.returncode}")
                if result.returncode == 0:
                    logger.info(f"Subprocess stdout: {result.stdout}")
                    return Response({"status": "success", "message": result.stdout})
                else:
                    logger.error(f"Subprocess stderr: {result.stderr}")
                    return Response({"status": "error", "message": result.stderr}, status=500)
            except Exception as e:
                logger.error(f"Unhandled exception: {e}")
                return Response({"status": "error", "message": str(e)}, status=500)
            finally:
                if os.path.exists(abs_file_path):
                    os.remove(abs_file_path)
                    logger.info(f"File {abs_file_path} removed after processing")
        else:
            return Response({"status": "error", "message": "Only superuser can update products"})


class RecommendItemsView(generics.ListAPIView):
    serializer_class = RecommendItemSerializer
    queryset = RecommendItem.objects.all()
    permission_classes = [AllowAny]


class ItemsWithDiscounts(generics.ListAPIView):
    serializer_class = ItemSerializer
    pagination_class = CustomPageNumberPagination
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Item.objects.exclude(discount_percent=0.0)


class OrderItem(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            data = request.data
            phone = data.get("phone")
            comment = data.get("comment", "")
            quantity = data.get("quantity", 1)
            product = data.get("product")

            if not phone or not isinstance(phone, str):
                return Response({"error": "Invalid phone number"}, status=status.HTTP_400_BAD_REQUEST)

            send_data = {
                "phone": phone,
                "comment": comment,
                "quantity": quantity,
                "product": product,
            }

            html_message = render_to_string("order_email.html", send_data)

            from_email = settings.EMAIL_HOST_USER
            recipient_list = [from_email]
            email = EmailMessage(
                "Новый заказ",
                html_message,
                from_email,
                recipient_list,
            )
            email.content_subtype = "html"

            email.send()

            return Response({"message": "Order submitted successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class StarRateItems(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            print(request)
            data = request.data
            item_id = data.get("productId")
            rate = data.get("rate")
            user_id = request.user.id

            if not item_id or not rate:
                return Response({"error": "Product ID and rate are required"}, status=status.HTTP_400_BAD_REQUEST)

            if not (1 <= int(rate) <= 5):
                return Response({"error": "Rate must be between 1 and 5"}, status=status.HTTP_400_BAD_REQUEST)

            items_service.rate_star_item(item_id, user_id, rate)

            return Response(status=status.HTTP_201_CREATED)
        except ValueError as ve:
            return Response({"error": str(ve)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "Something went wrong: " + str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAllImages(APIView):
    permission_classes = [AllowAny]
    serializer_class = Images

    def get(self, request):
        images = items_service.get_all_images()
        serializer = self.serializer_class(images, many=True)

        return Response(serializer.data)


class SearchByPhoto(APIView):
    permission_classes = [AllowAny]
    serializer_class = ItemSerializer

    def post(self, request):
        image = request.data.get("image")
        if image:
            response = requests.post(EXTERNAL_SERVICE_URL, json={"image_base64": image}, timeout=10)
            logger.info(response)
            response.raise_for_status()

            similar_ids = response.json()

            if not similar_ids:
                return Response({"message": "No similar items found"}, status=404)
            items = items_service.search_by_photo(similar_ids)
            serializer = self.serializer_class(items, many=True)

            return Response(serializer.data)

        return None
