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

    def get_context_data(self, *, object_list=None, **kwargs):
        category_slug = self.kwargs["category_slug"]
        category = None
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            if category:
                object_list = Product.objects.filter(available=True, category=category)

        context = super(ProductListView, self).get_context_data(
            object_list=object_list, **kwargs
        )
        context["category"] = category
        context["categories"] = Category.objects.all()
        return context
