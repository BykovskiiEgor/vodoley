from orders.models import Address
from rest_framework import serializers
from user.models import CustomUser


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "address"]


class UserRegistrationSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ["email", "first_name", "last_name", "phone_number", "addresses"]


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EditEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()


class EditPhoneSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
