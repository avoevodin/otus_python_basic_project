from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ["product"]


class OrderAdmin(admin.ModelAdmin):
    list_display = [
        "pk",
        "first_name",
        "last_name",
        "email",
        "address",
        "postal_code",
        "city",
        "paid",
        "created_at",
        "updated_at",
    ]
    list_display_links = ["pk"]
    list_filter = ["paid", "created_at", "updated_at"]
    inlines = [OrderItemInline]


admin.site.register(Order, OrderAdmin)
