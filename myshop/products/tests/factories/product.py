import factory
from django.utils import timezone
from django.utils.text import slugify
from factory.django import DjangoModelFactory


class CategoryFactory(DjangoModelFactory):
    """
    TODO
    """

    class Meta:
        model = "products.Category"
        django_get_or_create = ("name",)

    name = factory.Iterator(["Smartphone", "TV", "Headphone", "Laptop", "Tablet"])
    slug = slugify(name)
    description = factory.Faker("text", max_nb_chars=512)


class ProductFactory(DjangoModelFactory):
    """
    TODO
    """

    class Meta:
        model = "products.Product"
        django_get_or_create = ("name",)

    name = factory.Faker("sentence", nb_words=3)
    slug = factory.LazyAttribute(lambda o: slugify(o.name))
    category = factory.SubFactory(CategoryFactory)
    description = factory.Faker("text", max_nb_chars=512)
    price = factory.Faker("pydecimal", left_digits=8, right_digits=2, positive=True)
    stock = factory.Faker("pyint")
    available = factory.Faker("pybool")
    created = factory.Faker(
        "date_time_between",
        start_date="-3M",
        end_date="-1M",
        tzinfo=timezone.utc,
    )
    updated = factory.Faker(
        "date_time_between",
        start_date="-20d",
        tzinfo=timezone.utc,
    )
