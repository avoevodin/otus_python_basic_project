from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views import generic

from cart.forms import CartAddProductForm
from .models import Product, Category


class ProductListView(LoginRequiredMixin, generic.ListView):
    """
    TODO
    """

    model = Product
    template_name = "product_list.html"
    ordering = ("name",)
    context_object_name = "product_list"

    def get_queryset(self):
        """
        TODO
        """
        return Product.objects.filter(available=True)

    def get_context_data(self, **kwargs):
        """
        TODO
        """
        category_slug = self.kwargs.get("category_slug")
        category = None
        context = super(ProductListView, self).get_context_data(**kwargs)

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            if category:
                product_list = Product.objects.filter(available=True, category=category)
                context["product_list"] = product_list

        context["category"] = category
        context["categories"] = Category.objects.all()

        return context


class ProductDetailView(LoginRequiredMixin, generic.DetailView):
    """
    TODO
    """

    model = Product
    template_name = "products/product_detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        """
        TODO
        """
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        cart_form = CartAddProductForm()
        context["cart_product_form"] = cart_form
        return context
