from django.db import models
from django.urls import reverse


class Category(models.Model):
    """
    TODO
    """

    name = models.CharField(max_length=128, db_index=True)
    slug = models.SlugField(max_length=128, db_index=True, unique=True)
    description = models.CharField(max_length=512, blank=True)

    class Meta:
        ordering = ("name",)
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "products:products_list_by_category",
            args=[self.slug],
        )


class Product(models.Model):
    """
    TODO
    """

    name = models.CharField(max_length=128, db_index=True)
    slug = models.SlugField(max_length=128, db_index=True)
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.PROTECT
    )
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True)
    description = models.CharField(max_length=512, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        index_together = (("id", "slug"),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            "products:product_detail",
            args=[self.pk, self.slug],
        )
