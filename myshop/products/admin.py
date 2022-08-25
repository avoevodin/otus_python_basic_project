from django.contrib import admin

from .models import Product, Category


class CategoryAdmin(admin.ModelAdmin):
    """
    TODO
    """

    list_display = ["id", "name", "slug"]
    list_display_links = ["id", "name"]
    prepopulated_fields = {"slug": ("name",)}


class ProductAdmin(admin.ModelAdmin):
    """
    TODO
    """

    list_display = [
        "id",
        "name",
        "slug",
        "price",
        "stock",
        "available",
        "created",
        "updated",
    ]
    list_display_links = ["id", "name"]
    list_filter = ["available", "created", "updated"]
    list_editable = ["price", "stock", "available"]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
