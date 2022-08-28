from django.test import TestCase
from django.urls import reverse

from ..factories.product import ProductFactory


class ProductModelTestCase(TestCase):
    """
    TODO
    """

    def setUp(self):
        """
        TODO
        """
        self.product = ProductFactory()

    def test_product_str(self):
        """
        TODO
        """
        self.assertEqual(str(self.product), self.product.name)

    def test_product_abs_url(self):
        """
        TODO
        """
        self.assertEqual(
            self.product.get_absolute_url(),
            reverse(
                "products:product_detail",
                args=[self.product.pk, self.product.slug],
            ),
        )
