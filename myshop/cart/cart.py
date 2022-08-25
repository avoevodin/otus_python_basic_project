from decimal import Decimal

from django.conf import settings

from products.models import Product


class Cart(object):
    """
    TODO
    """

    def __init__(self, request):
        """
        TODO
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}

        self.cart = cart

    def __iter__(self):
        """
        TODO
        """
        products_pks = self.cart.keys()
        products = Product.objects.filter(id__in=products_pks)

        for product in products:
            self.cart[str(product.pk)]["product"] = product

        for item in self.cart.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["quantity"]
            yield item

    def __len__(self):
        """
        TODO
        """
        return sum(item["quantity"] for item in self.cart.values())

    def add(self, product, quantity=1, update_quantity=False):
        """
        TODO
        """
        product_pk = str(product.pk)
        if product_pk not in self.cart:
            self.cart[product_pk] = {"quantity": 0, "price": str(product.price)}

        if update_quantity:
            self.cart[product_pk]["quantity"] = quantity
        else:
            self.cart[product_pk]["quantity"] += quantity

        self.save()

    def save(self):
        """
        TODO
        """
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True

    def remove(self, product):
        """
        TODO
        """
        product_pk = str(product.pk)
        if product_pk in self.cart:
            del self.cart[product_pk]
            self.save()

    def get_total_price(self):
        """
        TODO
        """
        return sum(
            Decimal(item["price"]) * item["quantity"] for item in self.cart.values()
        )

    def clear(self):
        """
        TODO
        """
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
