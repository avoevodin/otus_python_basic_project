from django.urls import path

from .views import cart_remove, cart_add, cart_detail

app_name = "cart"

urlpatterns = [
    path("", cart_detail, name="cart_detail"),
    path(
        "add/<int:product_pk>",
        cart_add,
        name="cart_add",
    ),
    path(
        "remove/<int:product_pk>",
        cart_remove,
        name="cart_remove",
    ),
]
