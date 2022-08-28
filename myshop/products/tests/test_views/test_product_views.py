from django.test import TestCase
from django.urls import reverse

from ..factories.product import ProductFactory, CategoryFactory
from utils import TestUtils

LOGIN_VIEW = "myauth:login"


class ProductListViewTestCase(TestCase):
    """
    TODO
    """

    def setUp(self):
        self.PRODUCT_LIST_VIEW = "products:products_list"

    def test_product_list_without_auth(self):
        # products = ProductFactory.build_batch(10)
        # categories = CategoryFactory.build_batch(5)
        response = self.client.get(reverse(self.PRODUCT_LIST_VIEW))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, TestUtils.reverse_with_next(LOGIN_VIEW, self.PRODUCT_LIST_VIEW)
        )
