from django.contrib import admin

from .models import (
    Client,
    ClientDetail,
    ClientJob,
    ClientService,
)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    """
    TODO
    """

    list_display = (
        "first_name",
        "middle_name",
        "last_name",
        "birthday",
        "job",
    )

    list_display_links = (
        "first_name",
        "middle_name",
        "last_name",
    )


@admin.register(ClientDetail)
class ClientDetailAdmin(admin.ModelAdmin):
    """
    TODO
    """

    list_display = (
        "client",
        "income",
        "bio_short",
    )

    list_display_links = ("client",)

    def bio_short(self, obj: ClientDetail):
        if len(obj.bio) < 50:
            return obj.bio
        return obj.bio[:50] + "..."


admin.site.register(ClientJob)
admin.site.register(ClientService)
