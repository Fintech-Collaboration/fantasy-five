from plotly.offline    import plot
from plotly.graph_objs import Scatter

from django.urls                    import reverse_lazy
from django.shortcuts               import render, redirect
from django.contrib.auth.mixins     import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth            import logout
from django.contrib.auth.forms      import UserCreationForm
from django.views.generic           import ListView
from django.views.generic.edit      import CreateView, DeleteView, UpdateView

from django.http import Http404

from .utils.coin import icon_path, get_coin_data

from .models import (
    Owner,
    Portfolio,
    Coin,
)

from .forms  import (
    OwnerCreateForm,
    PortfolioCreateForm,
    OwnerUpdateForm,
    PortfolioUpdateForm,
)

COIN        = "bitcoin"
COIN_MODELS = Coin.__subclasses__()
USE_MODEL   = next(filter(lambda m: m.__name__.lower() == COIN, COIN_MODELS))

def logout_view(request):
    logout(request)
    return redirect("home")


def home(request):
    ticker = USE_MODEL.__ticker__
    name   = USE_MODEL.__name__

    coin_icon = icon_path(ticker)
    coin_plot = line_plot()

    context = {
        "ticker":    ticker.upper(),
        "coin_name": name,
        "coin_icon": coin_icon,
        "coin_plot": coin_plot,
    }
    return render(request, "sandbox/home.html", context)


def line_plot():
    ticker = USE_MODEL.__ticker__
    name   = USE_MODEL.__name__

    coin_df = get_coin_data(name, ticker)
    x_data  = coin_df.index
    y_data  = coin_df["price_close"]

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


def coin_table(request):
    coin_data = []
    for coin in COIN_MODELS:
        coin_data.append(dict(
            ticker        = coin.objects.last().ticker.upper(),
            name          = coin.objects.last().name.capitalize(),
            price_open    = f"{coin.objects.last().price_open:.2f}",
            price_high    = f"{coin.objects.last().price_high:.2f}",
            price_low     = f"{coin.objects.last().price_low:.2f}",
            price_close   = f"{coin.objects.last().price_close:.2f}",
            volume_traded = f"{coin.objects.last().volume_traded:.2f}",
            trades_count  = coin.objects.last().trades_count,
        ))

        context = {"coin_data": coin_data}
        
    return render(request, "sandbox/coin_list.html", context)


def coin_select(request, name):
    try:
        coin = next(filter(lambda m: m.__name__.lower() == name.lower(), COIN_MODELS))
    except Coin.DoesNotExist:
        return Http404(f"Coin not found!")
    
    pull_func = lambda col: coin.objects.values_list(col, flat=True).order_by("-start_date")

    context = dict(        
        ticker    = coin.objects.last().ticker.upper(),
        name      = coin.objects.last().name.capitalize(),
        count     = coin.objects.count(),
        coin_data = zip(
            pull_func("start_date"),
            pull_func("price_open"),
            pull_func("price_high"),
            pull_func("price_low"),
            pull_func("price_close"),
            pull_func("volume_traded"),
            pull_func("trades_count")),
        coin_icon = icon_path(coin.__ticker__),
    )

    return render(request, f"sandbox/coin_select.html", context)


class SignUp(CreateView):
    form_class    = UserCreationForm
    success_url   = reverse_lazy("login")
    template_name = "registration/signup.html"


class OwnerList(ListView):
    model = Owner


class CoinList(ListView):
    model = Coin


class PortfolioList(ListView):
    model = Portfolio


class OwnerCreate(CreateView):
    model         = Owner
    template_name = "sandbox/owner_create_form.html"
    form_class    = OwnerCreateForm


class PortfolioCreate(LoginRequiredMixin, CreateView):
    model         = Portfolio
    template_name = "sandbox/portfolio_create_form.html"
    form_class    = PortfolioCreateForm


class OwnerUpdate(LoginRequiredMixin, UpdateView):
    model         = Owner
    template_name = "sandbox/owner_update_form.html"
    form_class    = OwnerUpdateForm


class PortfolioUpdate(LoginRequiredMixin, UpdateView):
  model         = Portfolio
  template_name = "sandbox/portfolio_update_form.html"
  form_class    = PortfolioUpdateForm


class OwnerDelete(LoginRequiredMixin, DeleteView):
    model         = Owner
    template_name = "sandbox/owner_delete_form.html"
    success_url   = reverse_lazy("ownerlist")


class PortfolioDelete(LoginRequiredMixin, DeleteView):
    model         = Portfolio
    template_name = "sandbox/portfolio_delete_form.html"
    success_url   = reverse_lazy("portfoliolist")
  