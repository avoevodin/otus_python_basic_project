from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm


def get_request_cart_data(request, product_pk):
    """
    TODO
    """
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_pk)
    return cart, product


@login_required
@require_POST
def cart_add(request, product_pk):
    """
    TODO
    """
    cart, product = get_request_cart_data(request, product_pk)
    form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product,
            quantity=cd["quantity"],
            update_quantity=cd["update"],
        )

    return redirect("cart:cart_detail")


@login_required
def cart_remove(request, product_pk):
    """
    TODO
    """
    cart, product = get_request_cart_data(request, product_pk)
    cart.remove(product)
    return redirect("cart:cart_detail")


@login_required
def cart_detail(request):
    """
    TODO
    """
    cart = Cart(request)
    return render(request, "cart/cart_detail.html", {"cart": cart})
