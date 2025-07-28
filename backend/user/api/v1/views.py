from drf_spectacular.utils import extend_schema
from repositories.user_repository import TemporaryPasswordRepository
from repositories.user_repository import UserRepository
from rest_framework import status
from rest_framework import views
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from services.user_service import UserService

from .serializers import EditEmailSerializer
from .serializers import UserRegistrationSerializer


class RegisterUserView(views.APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        user_service = UserService()
        if serializer.is_valid() and request.method == "POST":
            try:
                data = request.data
                user = user_service.create_user(data)
                refresh = RefreshToken.for_user(user)
                refresh.payload.update({"user_id": user.id})
                return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(views.APIView):
    permission_classes = [AllowAny]

    user_repository = UserRepository()
    temp_password_repository = TemporaryPasswordRepository()
    user_service = UserService(user_repository, temp_password_repository)

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = self.user_service.authenticate_user(email, password)

        if not user:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        user_data = UserRegistrationSerializer(user).data

        return Response(
            {
                "user": user_data,
                "tokens": {
                    "access": access_token,
                    "refresh": str(refresh),
                },
            },
            status=status.HTTP_200_OK,
        )


class SendTPForLogIn(views.APIView):
    permission_classes = [AllowAny]
    user_repository = UserRepository()
    temp_password_repository = TemporaryPasswordRepository()
    user_service = UserService(user_repository, temp_password_repository)

    def post(self, request):
        email = request.data.get("email")
        if email:
            user = self.user_service.login_user(email)
            if user:
                return Response({"message": "Temporary password sent to your email"}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid email"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    request=EditEmailSerializer,
    responses={200: EditEmailSerializer},
    description="Update user email",
)
class EditUserEmail(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer = EditEmailSerializer()
    user_repository = UserRepository()
    temp_password_repository = TemporaryPasswordRepository()
    user_service = UserService(user_repository, temp_password_repository)

    def patch(self, request):
        user = request.user
        new_email = request.data.get("email")
        if not new_email:
            return Response(
                {"error": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        is_free = self.user_service.is_email_free(new_email)
        if is_free:
            user.email = new_email
            user.save()

            return Response(
                {
                    "message": "Email updated successfully",
                    "email": new_email,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Email is already taken"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class EditUserPhone(views.APIView):
    permission_classes = [IsAuthenticated]
    serializer = EditEmailSerializer
    user_repository = UserRepository()
    temp_password_repository = TemporaryPasswordRepository()
    user_service = UserService(user_repository, temp_password_repository)

    def patch(self, request):
        user = request.user
        new_phone = request.data.get("phone_number")
        if not new_phone:
            return Response(
                {"error": "Phone number is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        is_phone_free = self.user_service.is_phone_free(new_phone)
        if is_phone_free:
            user.phone_number = new_phone
            user.save()

            return Response(
                {
                    "message": "Phone number updated successfully",
                    "number": new_phone,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Phone number is already taken"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class AddAddress(views.APIView):
    permission_classes = [IsAuthenticated]
