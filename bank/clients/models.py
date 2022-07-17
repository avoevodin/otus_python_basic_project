from django.db import models


class ClientJob(models.Model):
    """
    TODO
    """

    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name})"


class Client(models.Model):
    """
    TODO
    """

    first_name = models.CharField(max_length=128)
    middle_name = models.CharField(max_length=128, blank=True, null=True)
    last_name = models.CharField(max_length=128)
    birthday = models.DateField()
    job = models.ForeignKey(ClientJob, on_delete=models.PROTECT, null=True)

    services = models.ManyToManyField("clients.ClientService", related_name="clients")

    def __str__(self):
        middle_name = self.middle_name or ""
        required_len = len(middle_name) + 1
        return f"{self.first_name}{middle_name.rjust(required_len) if middle_name else ''} {self.last_name}"

    def __repr__(self):
        return (
            f"{self.__class__.__name__}(first_name={self.first_name}"
            f", middle_name={self.middle_name}"
            f", last_name={self.last_name})"
        )


class ClientDetail(models.Model):
    """
    TODO
    """

    client = models.OneToOneField(
        Client,
        primary_key=True,
        on_delete=models.PROTECT,
        related_name="details",
    )
    bio = models.TextField(blank=True)
    income = models.IntegerField(null=True)

    def __str__(self):
        return f"{self.client}: {self.bio}"


class ClientService(models.Model):
    """
    TODO
    """

    name = models.CharField(max_length=128, unique=True)
    price = models.IntegerField()
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"name={self.name!r}, "
            f"price={self.price}, "
            f"description={self.description})"
        )
