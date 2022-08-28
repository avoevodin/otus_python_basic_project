from django.urls import path

from .views import (
    MyauthLoginView,
    MyauthRegistrationView,
    MyauthRegistrationDoneView,
    MyauthLogoutView,
    MyauthPasswordChangeView,
    MyauthPasswordChangeDoneView,
    MyauthRegistrationActivateView,
    MyauthRegistrationActivationDoneView,
)

app_name = "myauth"
urlpatterns = [
    path("registration/", MyauthRegistrationView.as_view(), name="registration"),
    path(
        "registration_activate/<str:key>/<str:confirm>/",
        MyauthRegistrationActivateView.as_view(),
        name="registration_activate",
    ),
    path(
        "registration_activation_done/",
        MyauthRegistrationActivationDoneView.as_view(),
        name="registration_activation_done",
    ),
    path(
        "registration_done/",
        MyauthRegistrationDoneView.as_view(),
        name="registration_done",
    ),
    path("login/", MyauthLoginView.as_view(), name="login"),
    path("logout/", MyauthLogoutView.as_view(), name="logout"),
    path(
        "password_change/", MyauthPasswordChangeView.as_view(), name="password_change"
    ),
    path(
        "password_change_done/",
        MyauthPasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
]
