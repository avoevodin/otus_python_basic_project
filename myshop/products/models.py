from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=128, db_index=True)
    slug = models.SlugField(max_length=128, db_index=True, unique=True)
    description = models.CharField(max_length=512)

    class Meta:
        ordering = ("name",)
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
