from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.views.generic import ListView, DetailView

from .models import Client


def details(request: HttpRequest, pk: int):
    """
    TODO
    :param request:
    :param pk:
    :return:
    """

    client = get_object_or_404(
        Client.objects.select_related(
            "job",
            "details",
        ).prefetch_related("services"),
        pk=pk,
    )
    context = {"client": client}
    return render(request, "clients/details.html", context=context)


class ClientListView(ListView):
    queryset = Client.objects.select_related("details").order_by("-id").all()
    template_name = "clients/index.html"
    context_object_name = "clients"


class ClientDetailView(DetailView):
    queryset = Client.objects.select_related(
        "job",
        "details",
    ).prefetch_related("services")
