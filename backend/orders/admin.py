from django.contrib import admin

from .forms import OrderAdminForm
from .models import Address
from .models import Order
from .models import OrderItem


class AddressInline(admin.TabularInline):
    model = Address

    extra = 0


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

    fields = ["item", "quantity", "price"]


class OrderAdmin(admin.ModelAdmin):

    form = OrderAdminForm

    list_display = [
        "order_date",
        "total_price",
        "customer_info",
        "status",
    ]

    inlines = [OrderItemInline, AddressInline]


admin.site.register(Order, OrderAdmin)
