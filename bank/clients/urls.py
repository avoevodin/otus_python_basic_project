from django.urls import path

from .views import ClientListView, ClientDetailView

app_name = "clients"

urlpatterns = [
    path("", ClientListView.as_view(), name="list"),
    path("<int:pk>/", ClientDetailView.as_view(), name="details"),
]
