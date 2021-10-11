from django                     import forms
from django.contrib.auth.forms  import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Owner, Portfolio


class OwnerCreateForm(forms.ModelForm):
    class Meta:
        model  = Owner
        fields = ("__all__")


class UserCreateForm(UserCreationForm):
    class Meta:
        model  = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]


class PortfolioCreateForm(LoginRequiredMixin, forms.ModelForm):
    class Meta:
        model  = Portfolio
        fields = ("__all__")


class OwnerUpdateForm(forms.ModelForm):
    class Meta:
        model  = Owner
        fields = ("__all__")


class PortfolioUpdateForm(forms.ModelForm):
    class Meta:
        model  = Portfolio
        fields = (
            "coin_list",
            "investment",
        )

