from django import forms
from .models import Order


class OrderModelForm(forms.ModelForm):
    """
    TODO
    """

    class Meta:
        model = Order
        fields = [
            "first_name",
            "last_name",
            "email",
            "address",
            "postal_code",
            "city",
        ]
        widgets = {
            "first_name": forms.TextInput(
                attrs={"class": "form-control mb-2", "placeholder": "first name"}
            ),
            "last_name": forms.TextInput(
                attrs={"class": "form-control mb-2", "placeholder": "last name"}
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "form-control mb-2",
                    "placeholder": "Email",
                }
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control mb-2", "placeholder": "address"}
            ),
            "postal_code": forms.TextInput(
                attrs={"class": "form-control mb-2", "placeholder": "postal code"}
            ),
            "city": forms.TextInput(
                attrs={"class": "form-control mb-2", "placeholder": "city"}
            ),
        }
