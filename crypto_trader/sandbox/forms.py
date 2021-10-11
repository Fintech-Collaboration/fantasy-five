from django  import forms
from .models import Owner, Portfolio

from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerCreateForm(forms.ModelForm):
    class Meta:
        model  = Owner
        fields = ("__all__")


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

