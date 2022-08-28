from django.shortcuts import get_object_or_404
from django.test import TestCase
from django.urls import reverse

from ..factories.product import ProductFactory, CategoryFactory
from utils import TestUtils
from myauth.tests.factories.my_user import MyUserFactory, USER_PASSWORD
from myauth.models import MyUser

LOGIN_VIEW = "myauth:login"


class ProductListViewTestCase(TestCase):
    """
    TODO
    """

    def setUp(self):
        """
        TODO
        """
        self.PRODUCT_LIST_VIEW = "products:products_list"
        self.PRODUCT_LIST_BY_CATEGORY_VIEW = "products:products_list_by_category"
        self.user = MyUserFactory()

    def test_product_list_without_auth(self):
        """
        TODO
        """
        response = self.client.get(reverse(self.PRODUCT_LIST_VIEW))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, TestUtils.reverse_with_next(LOGIN_VIEW, self.PRODUCT_LIST_VIEW)
        )

    def test_product_list_with_auth_without_products_and_categories(self):
        """
        TODO
        """
        self.client.login(username=self.user.username, password=USER_PASSWORD)
        response = self.client.get(reverse(self.PRODUCT_LIST_VIEW))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["product_list"]), [])
        self.assertEqual(list(response.context["categories"]), [])

    def test_product_list_with_auth_without_products(self):
        """
        TODO
        """
        categories = CategoryFactory.create_batch(5)
        categories.sort(key=lambda x: x.name, reverse=False)
        self.client.login(username=self.user.username, password=USER_PASSWORD)
        response = self.client.get(reverse(self.PRODUCT_LIST_VIEW))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["product_list"]), [])
        self.assertEqual(list(response.context["categories"]), categories)

    def test_product_list_with_auth(self):
        """
        TODO
        """
        categories = CategoryFactory.create_batch(5)
        products = ProductFactory.create_batch(10)
        products_to_compare = [item for item in products if item.available]
        categories.sort(key=lambda x: x.name, reverse=False)
        products_to_compare.sort(key=lambda x: x.name, reverse=False)
        self.client.login(username=self.user.username, password=USER_PASSWORD)
        response = self.client.get(reverse(self.PRODUCT_LIST_VIEW))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["product_list"]), products_to_compare)
        self.assertEqual(list(response.context["categories"]), categories)

    def test_product_list_with_auth_by_category(self):
        """
        TODO
        """
        categories = CategoryFactory.create_batch(5)
        products = ProductFactory.create_batch(10)
        categories.sort(key=lambda x: x.name, reverse=False)
        category = categories[0]
        products_to_compare = [
            item for item in products if item.category == category and item.available
        ]
        products_to_compare.sort(key=lambda x: x.name, reverse=False)
        self.client.login(username=self.user.username, password=USER_PASSWORD)
        response = self.client.get(
            reverse(
                self.PRODUCT_LIST_BY_CATEGORY_VIEW,
                kwargs={"category_slug": category.slug},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context["product_list"]), products_to_compare)
        self.assertEqual(list(response.context["categories"]), categories)
        self.assertEqual(response.context["category"], category)
