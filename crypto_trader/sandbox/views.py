from plotly.offline    import plot
from plotly.graph_objs import Scatter

from django.urls                    import reverse_lazy
from django.shortcuts               import render, redirect
from django.contrib.auth.mixins     import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth            import authenticate
from django.contrib.auth            import logout, login
from django.views.generic           import ListView
from django.views.generic.edit      import CreateView, DeleteView, UpdateView
from django.contrib                 import messages
from django.http                    import Http404
from django.template.defaultfilters import slugify
from django.db.models               import Q

from .utils.coin import icon_path, get_coin_data

from .models import (
    Portfolio,
    Coin,
    Transaction,
)

from .forms  import (
    UserCreateForm,
    PortfolioCreateForm,
    TransactionCreateForm,
    PortfolioUpdateForm,
)

COIN        = "bitcoin"
COIN_MODELS = Coin.__subclasses__()
USE_MODEL   = next(filter(lambda m: m.__name__.lower() == COIN, COIN_MODELS))


def signup_view(request):
    if request.user.is_authenticated:
        messages.info(request, f"Logged out of {request.user}")
        logout(request)
        
    form = UserCreateForm()
    context = {"form": form}

    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()

            user = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {user}!")

            return redirect("login")

    return render(request, "registration/signup.html", context)


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user     = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Username OR password is incorrect")
    
    context = {}
    return render(request, "registration/login.html", context)


@login_required(login_url="login")
def logout_view(request):
    logout(request)
    return redirect("login")


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


def coin_page(request, name):
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

    return render(request, f"sandbox/coin_page.html", context)


# portfolio_select coin_id coin_count
def transaction_create_view(request, coin_name):
    form = TransactionCreateForm(request.POST or None)
    if form.is_valid():
        form.save()

    # Get the latest instance of the current coin
    coin_data_all    = Coin.objects.filter( Q(Coin___name = coin_name))
    coin_data_length = len(coin_data_all)-1
    coin_data_now    = coin_data_all[coin_data_length]

    # Get only this user's portfolios
    user_portfolios = [p for p in form.fields["portfolio"]._queryset if p.owner.username == request.user.username]
    print(user_portfolios)

    context = dict(
        form          = form,
        portfolio     = user_portfolios,
        coin_name     = coin_name,
        start_date    = coin_data_now.start_date,
        price_open    = coin_data_now.price_open,
        price_high    = coin_data_now.price_high,
        price_low     = coin_data_now.price_low,
        price_close   = coin_data_now.price_close,
        volume_traded = coin_data_now.volume_traded,
        trades_count  = coin_data_now.trades_count,
        ticker        = coin_data_now.ticker.upper(),
        coin_icon     = icon_path(coin_data_now.ticker.upper()),
    )

    return render(request, f"sandbox/transaction_create.html", context)


def coin_buy(request, name):
    try:
        coin = next(filter(lambda m: m.__name__.lower() == name.lower(), COIN_MODELS))
    except Coin.DoesNotExist:
        return Http404(f"Coin not found!")
    
    username = request.user.username

    if request.method == "POST":
        selected  = request.POST["coin-buy-select"]
        count     = request.POST["coin-buy-count"]
        portfolio = [p for p in Portfolio.objects.all() if p.nickname == selected][0]


        portfolio.coin_list = f"{portfolio.coin_list}, {coin.__coinid__}" if portfolio.coin_list else f"{coin.__coinid__}"
    else:
        portfolio = None    

    context = dict(        
        ticker        = coin.objects.last().ticker.upper(),
        name          = coin.objects.last().name.capitalize(),
        coin_id       = coin.__coinid__,
        start_date    = coin.objects.last().start_date.strftime("%Y-%b-%d"),
        price_open    = f"{coin.objects.last().price_open:,.2f}",
        price_high    = f"{coin.objects.last().price_high:,.2f}",
        price_low     = f"{coin.objects.last().price_low:,.2f}",
        price_close   = f"{coin.objects.last().price_close:,.2f}",
        volume_traded = f"{coin.objects.last().volume_traded:,.0f}",
        trades_count  = f"{coin.objects.last().trades_count:,.0f}",
        portfolio     = portfolio,
        coin_icon     = icon_path(coin.__ticker__),
    )

    return render(request, f"sandbox/coin_buy.html", context)


class CoinList(ListView):
    model = Coin


class PortfolioList(LoginRequiredMixin, ListView):
    model = Portfolio


class PortfolioCreate(LoginRequiredMixin, CreateView):
    model         = Portfolio
    template_name = "sandbox/portfolio_create_form.html"
    form_class    = PortfolioCreateForm


# class TransactionCreate(LoginRequiredMixin, CreateView):
#     model         = Transaction
#     template_name = "sandbox/transaction_create.html"
#     form_class    = TransactionCreateForm


class PortfolioUpdate(LoginRequiredMixin, UpdateView):
  model         = Portfolio
  template_name = "sandbox/portfolio_update_form.html"
  form_class    = PortfolioUpdateForm


class PortfolioDelete(LoginRequiredMixin, DeleteView):
    model         = Portfolio
    template_name = "sandbox/portfolio_delete_form.html"
    success_url   = reverse_lazy("portfoliolist")

