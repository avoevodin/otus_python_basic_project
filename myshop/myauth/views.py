from uuid import uuid4

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib.auth.views import (
    FormView,
    LoginView,
    TemplateView,
    LogoutView,
    PasswordChangeView,
    PasswordChangeDoneView,
)
from django.contrib.sites.shortcuts import get_current_site
from django.core.cache import cache
from django.urls import reverse_lazy

from .forms import MyauthRegistrationForm, MyauthLoginForm, MyauthPasswordChangeForm
from worker.email.tasks import send_verification_mail, send_onboarding_mail

User = get_user_model()


class MyauthRegistrationView(FormView):
    """Account registration view. If the public group exist it will be
    added to user account by default.

    """

    form_class = MyauthRegistrationForm
    template_name = "registration.html"
    success_url = reverse_lazy("myauth:registration_done")

    def form_valid(self, form):
        response = super(MyauthRegistrationView, self).form_valid(form)
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        key = uuid4().hex
        confirm = uuid4().hex
        data = {
            "confirm": confirm,
            "user_id": user.id,
        }
        cache.set(key, data, settings.EXPIRE_LINK)
        host = get_current_site(self.request).domain
        send_verification_mail.delay(host, user.email, key, confirm)

        return response


class MyauthRegistrationDoneView(TemplateView):
    """Registration view."""

    template_name = "registration_done.html"


class MyauthRegistrationActivateView(TemplateView):
    """View for activate users from link. This link
    is sent to user's email.

    """

    template_name = "registration_activate.html"

    def get_context_data(self, **kwargs):
        context = super(MyauthRegistrationActivateView, self).get_context_data(**kwargs)
        key = kwargs.get("key")
        confirm = kwargs.get("confirm")
        data = cache.get(key)
        if (
            (data is not None)
            and (data.get("confirm"))
            and (data.get("confirm") == confirm)
        ):
            user = User.objects.get(pk=data.get("user_id"))
            user.is_active = True
            user.save()
            context["message"] = "ok"

            host = get_current_site(self.request).domain
            send_onboarding_mail.delay(host, user.email)
        else:
            context["message"] = "error"
        return context


class MyauthRegistrationActivationDoneView(TemplateView):
    """View for activation from email link."""

    template_name = "registration_activation_done.html"


class MyauthLoginView(LoginView):
    """Loging view."""

    form_class = MyauthLoginForm
    template_name = "login.html"
    success_url = settings.LOGIN_REDIRECT_URL


class MyauthLogoutView(LogoutView):
    """Logout view."""

    next_page = settings.LOGIN_URL


class MyauthPasswordChangeView(PasswordChangeView):
    """Password change view."""

    form_class = MyauthPasswordChangeForm
    template_name = "password_change.html"
    success_url = reverse_lazy("myauth:password_change_done")


class MyauthPasswordChangeDoneView(PasswordChangeDoneView):
    """Password change done view."""

    template_name = "password_change_done.html"
