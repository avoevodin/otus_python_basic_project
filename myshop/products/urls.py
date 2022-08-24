from django.urls import re_path

from .views import ProductListView, ProductDetailView

app_name = "products"

urlpatterns = [
    re_path(r"^$", ProductListView.as_view(), name="products_list"),
    re_path(
        r"^(?P<category_slug>[-\w]+)/$",
        ProductListView.as_view(),
        name="products_list_by_category",
    ),
    re_path(
        r"^(?P<pk>\d+)/(?P<slug>[-\w]+)$",
        ProductDetailView.as_view(),
        name="product_detail",
    ),
]
