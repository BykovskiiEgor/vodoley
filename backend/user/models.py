from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from .managers import CustomUserManager


class CustomUser(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    phone_number = models.CharField(unique=True)

    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True, help_text="The groups this user belongs to.", verbose_name="groups")
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_set", blank=True, help_text="Specific permissions for this user.", verbose_name="user permissions")

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "phone_number"]

    class Meta:
        verbose_name = "Пользоваетль"
        verbose_name_plural = "Пользователи"


class OneTimePassword(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=50)
    expiration_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.expiration_time
