from django.urls import path

from .views import OrderCreateView, OrderDetailView

app_name = "order"

urlpatterns = [
    path("create/", OrderCreateView.as_view(), name="order_create"),
    path("<int:pk>", OrderDetailView.as_view(), name="order_detail"),
]
