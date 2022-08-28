import factory
from django.utils import timezone
from django.contrib.auth.hashers import make_password
from factory.django import DjangoModelFactory
from faker import Faker

fake = Faker()

USER_PASSWORD = "lF$3n9g45m%s"


class MyUserFactory(DjangoModelFactory):
    """
    TODO
    """

    class Meta:
        model = "myauth.MyUser"
        django_get_or_create = (
            "username",
            "email",
        )

    username = fake.user_name()
    first_name = fake.first_name()
    last_name = fake.last_name()
    email = factory.LazyAttribute(
        lambda o: "{name}@{domain}".format(
            name=o.username,
            domain=fake.domain_name(),
        ),
    )
    is_admin = False
    is_active = True
    date_joined = fake.date_time_between(
        start_date="-3M",
        end_date="-1M",
        tzinfo=timezone.utc,
    )
    password = make_password(USER_PASSWORD)
