from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.views import generic

from .models import Product, Category


class ProductListView(generic.ListView):
    """
    TODO
    """

    model = Product
    template_name = "product_list.html"
    ordering = "name"
    context_object_name = "product_list"

    def get_context_data(self, *, product_list=None, **kwargs):
        category_slug = self.kwargs.get("category_slug")
        category = None
        context = super(ProductListView, self).get_context_data(**kwargs)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            if category:
                product_list = Product.objects.filter(available=True, category=category)

        context["category"] = category
        context["categories"] = Category.objects.all()

        if product_list:
            context["product_list"] = product_list

        return context


class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"
