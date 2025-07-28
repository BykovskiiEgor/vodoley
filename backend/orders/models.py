from django.core.exceptions import ValidationError
from django.db import models
from user.models import CustomUser


class Order(models.Model):
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=100, decimal_places=2)

    STATUS_CHOICES = (
        ("В ожидании", "В ожидании"),
        ("Обработан", "Обработан"),
        ("Собран", "Собран"),
        ("Доставлен", "Доставлен"),
    )

    STATUS_ORDER = {
        "В ожидании": 0,
        "Обработан": 1,
        "Собран": 2,
        "Доставлен": 3,
    }

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="В ожидании")
    user = models.ForeignKey(CustomUser, default=None, on_delete=models.CASCADE)

    def customer_info(self):
        user = self.user
        return f"Name: {user.first_name} {user.last_name}, " f"Email: {user.email}, " f"Phone: {user.phone_number}, "

    customer_info.short_description = "Customer Info"

    def save(self, *args, **kwargs):
        if self.pk:
            previous = Order.objects.get(pk=self.pk)
            if self.STATUS_ORDER[self.status] < self.STATUS_ORDER[previous.status]:
                raise ValidationError(f"Нельзя изменить статус с '{previous.status}' на '{self.status}'")
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey("items.Item", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField("Quantity")
    price = models.DecimalField(max_digits=100, decimal_places=2)

    class Meta:
        verbose_name = "Заказанный товар"
        verbose_name_plural = "Заказынные товары"


class Address(models.Model):
    address = models.CharField("Адрес", max_length=255)
    order = models.ForeignKey(Order, related_name="address", on_delete=models.CASCADE, null=True, blank=True)
    user = models.ForeignKey(CustomUser, default=None, on_delete=models.CASCADE, related_name="addresses")

    class Meta:
        verbose_name = "Адрес"
        verbose_name_plural = "Адреса"
