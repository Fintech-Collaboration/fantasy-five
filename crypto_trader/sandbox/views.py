import os
from django.http.response import HttpResponse

import pandas as pd

from .config.coin import coin_references, icon_path

from django.urls                    import reverse_lazy
from django.shortcuts               import render, redirect
from django.contrib.auth.mixins     import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth            import authenticate, login, logout
from django.views.generic           import ListView
from django.views.generic.edit      import CreateView, DeleteView, UpdateView

from .models import Owner, Portfolio

from pathlib           import Path
from plotly.offline    import plot
from plotly.graph_objs import Scatter


DATA_PATH = "../data/archive"
TEST_DATA = lambda t: os.path.join(DATA_PATH, f"{coin_references(t)}_5_year.csv")


def login_view(request):
    context = {
        "login_view": "active",
    }

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user     = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            render(request, "registration/login.html", context)

    return render(request, "registration/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("home")


def home(request):
    ticker    = "BTC"
    coin_name = coin_references(ticker)
    coin_icon = icon_path(ticker)
    coin_plot = line_plot(ticker)

    context = {
        "ticker":    ticker.upper(),
        "coin_name": coin_name,
        "coin_icon": coin_icon,
        "coin_plot": coin_plot,
    }
    return render(request, "sandbox/home.html", context)


def line_plot(ticker):
    df = pd.read_csv(
        Path(TEST_DATA(ticker)),
        index_col=f"{ticker.lower()}_start_date",
        parse_dates=True,
        infer_datetime_format=True,
    )

    x_data = df.index
    y_data = df["price_close"]

    plt = plot([Scatter(
        x=x_data,
        y=y_data,
        mode='lines',
        name=ticker.upper(),
        opacity=0.8,
        marker_color='green',
    )],
    output_type='div')  

    return plt


class OwnerList(ListView):
    model = Owner


class PortfolioList(ListView):
    model = Portfolio


class OwnerCreate(LoginRequiredMixin, CreateView):
    model         = Owner
    template_name = "sandbox/owner_create_form.html"
    fields        = ["username", "first_name", "last_name", "email"]
    success_url   = reverse_lazy("ownerlist")

class PortfolioCreate(LoginRequiredMixin, CreateView):
    model         = Portfolio
    template_name = "sandbox/portfolio_create_form.html"
    fields        = ["coin_list", "investment", "balance", "owner"]
    success_url   = reverse_lazy("portfoliolist")


class OwnerUpdate(LoginRequiredMixin, UpdateView):
    model         = Owner
    template_name = "sandbox/owner_update_form.html"
fields        = ["username", "first_name", "last_name", "email"]


class PortfolioUpdate(LoginRequiredMixin, UpdateView):
  model         = Portfolio
  template_name = "sandbox/portfolio_update_form.html"
  fields        = ["coin_list", "investment", "balance", "owner"]


class OwnerDelete(LoginRequiredMixin, DeleteView):
    model         = Owner
    template_name = "sandbox/owner_delete_form.html"
    success_url   = reverse_lazy("ownerlist")


class PortfolioDelete(LoginRequiredMixin, DeleteView):
    model         = Portfolio
    template_name = "sandbox/portfolio_delete_form.html"
    success_url   = reverse_lazy("portfoliolist")
  