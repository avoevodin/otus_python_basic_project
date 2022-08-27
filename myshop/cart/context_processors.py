from .cart import Cart


def cart(request):
    """
    TODO
    """
    return {"cart": Cart(request)}
