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

from .config.coin import coin_references, icon_path, get_coin_data

from .models import (
    Owner,
    Portfolio,
    Coin,
    Aave,
    Aragon,
    Augur,
    Balancer,
    Bitcoin,
    Cardano,
    Cosmos,
    Ethereum,
    EthereumClassic,
    Orchid,
    Tether,
    Tezos,
)

from .forms  import (
    OwnerCreateForm,
    PortfolioCreateForm,
    OwnerUpdateForm,
    PortfolioUpdateForm,
)

TICKER = "BTC"

MODELS = (
    Aave,
    Aragon,
    Augur,
    Balancer,
    Bitcoin,
    Cardano,
    Cosmos,
    Ethereum,
    EthereumClassic,
    Orchid,
    Tether,
    Tezos,
)

def logout_view(request):
    logout(request)
    return redirect("home")


def home(request):
    coin_name = coin_references(TICKER)
    coin_icon = icon_path(TICKER)
    coin_plot = line_plot()

    context = {
        "ticker":    TICKER.upper(),
        "coin_name": coin_name,
        "coin_icon": coin_icon,
        "coin_plot": coin_plot,
    }
    return render(request, "sandbox/home.html", context)


def line_plot():
    coin_df = get_coin_data(TICKER)
    x_data  = coin_df.index
    y_data  = coin_df["price_close"]

    plt = plot([Scatter(
        x=x_data,
        y=y_data,
        mode='lines',
        name=TICKER.upper(),
        opacity=0.8,
        marker_color='green',
    )],
    output_type='div')  

    return plt


def coin_data(request):
    context = {}

    for coin in MODELS:
        key         = f"{coin.objects.all()[0].ticker}_close_price"
        length_vals = coin.objects.count()-1
        price_close = coin.objects.all()[length_vals].price_close
        
        context = {**context, **{key: price_close}}

    return render(request, 'sandbox/coin_list.html', context)


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
  