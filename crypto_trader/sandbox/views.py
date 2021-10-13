import pickle

import pandas as pd

from datetime          import datetime
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
from django.http                    import Http404, HttpResponse
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

def ml_models(request):        
    if 'gNB' in request.POST:
        gaussian = pickle.load(open('gNB.sav','rb'))
        y_pred = gaussian.predict(test_data_preprocessed)
        output = pd.DataFrame(y_pred)
        output.to_csv('gaussianNB.csv')
        
        filename = 'gaussianNB.csv'
        response = HttpResponse(open(filename, 'rb').read(),    content_type='text/csv')               
        response['Content-Length'] = os.path.getsize(filename)
        response['Content-Disposition'] = 'attachment; filename=%s' % 'gaussianNB.csv'
        return response
    
    if 'multiNB' in request.POST:
        multi = pickle.load(open('classifier_multi_NB.sav','rb'))
        y_pred = multi.predict(test_data_preprocessed)
        output = pd.DataFrame(y_pred)
        output.to_csv('multi_NB.csv')
        
        filename = 'multi_NB.csv'
        response = HttpResponse(open(filename, 'rb').read(), content_type='text/csv')                
        response['Content-Length'] = os.path.getsize(filename)
        response['Content-Disposition'] = 'attachment; filename=%s' % 'multi_NB.csv'
        return response
    
    if 'rf' in request.POST:
        rf = pickle.load(open('random_forest.sav','rb'))
        y_pred = rf.predict(test_data_preprocessed)
        output = pd.DataFrame(y_pred)
        output.to_csv('rf.csv')
        
        filename = 'rf.csv'
        response = HttpResponse(open(filename, 'rb').read(), content_type='text/csv')             
        response['Content-Length'] = os.path.getsize(filename)
        response['Content-Disposition'] = 'attachment; filename=%s' % 'rf.csv'
        return response


""" WALLET METHODS """
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


def coin_page(request, ticker):
    try:
        coin = next(filter(lambda m: m.__ticker__.lower() == ticker.lower(), COIN_MODELS))
    except Coin.DoesNotExist:
        return Http404(f"Coin not found!")
    
    pull_func = lambda col: coin.objects.values_list(col, flat=True).order_by("-start_date")

    context = dict(        
        ticker    = ticker,
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


@login_required(login_url="login")
def transaction_create_view(request, ticker):
    form = TransactionCreateForm(request.POST or None)
    if form.is_valid():
        form.save()

    # Get the latest instance of the current coin
    coin_data_all    = Coin.objects.filter( Q(Coin___ticker = ticker.lower()))
    coin_data_length = len(coin_data_all)-1
    coin_data_now    = coin_data_all[coin_data_length]

    # Get only this user's portfolios
    user_portfolios = [p for p in form.fields["portfolio"]._queryset if p.owner.username == request.user.username]

    context = dict(
        portfolios    = user_portfolios,
        coin_name     = coin_data_now.name,
        start_date    = coin_data_now.start_date.strftime("%Y-%b-%d"),
        price_open    = coin_data_now.price_open,
        price_high    = coin_data_now.price_high,
        price_low     = coin_data_now.price_low,
        price_close   = coin_data_now.price_close,
        volume_traded = coin_data_now.volume_traded,
        trades_count  = coin_data_now.trades_count,
        ticker        = ticker.upper(),
        coin_icon     = icon_path(coin_data_now.ticker.upper()),
    )

    return render(request, "sandbox/transaction_create.html", context)


@login_required(login_url="login")
def transaction_execute(request, ticker):
    if request.method == "POST":
        portfolio_nickname = request.POST["portfolio-buy-select"]
        coin_count         = float(request.POST["coin-buy-input"])
        print(f"{portfolio_nickname} - {coin_count} - {ticker}")

        # Get the latest instance of the current coin
        coin_data_all    = Coin.objects.filter( Q(Coin___ticker = ticker.lower()))
        coin_data_length = len(coin_data_all)-1

        # Set transaction data
        coin_data_now    = coin_data_all[coin_data_length]
        coin_cost        = coin_count * float(coin_data_now.price_close)
        portfolio        = Portfolio.objects.all().filter(nickname = portfolio_nickname)[0]
        time_executed    = datetime.now()

        t = Transaction(
            time_executed=time_executed,
            coin_count=coin_count,
            coin_cost=coin_cost,
            coin=coin_data_now,
            portfolio=portfolio,
        )
        t.save()

    return redirect("transactionlist")
""" -------------- """

""" WALLET CLASSES """
class CoinList(ListView):
    model = Coin


class PortfolioList(LoginRequiredMixin, ListView):
    queryset = Portfolio.objects.order_by("-balance")
    model    = Portfolio
    context_object_name  = "portfolios"


class TransactionList(LoginRequiredMixin, ListView):
    queryset = Transaction.objects.order_by("-time_executed")
    model    = Transaction
    context_object_name  = "transactions"


class PortfolioCreate(LoginRequiredMixin, CreateView):
    model         = Portfolio
    template_name = "sandbox/portfolio_create_form.html"
    form_class    = PortfolioCreateForm


class PortfolioUpdate(LoginRequiredMixin, UpdateView):
  model         = Portfolio
  template_name = "sandbox/portfolio_update_form.html"
  form_class    = PortfolioUpdateForm


class PortfolioDelete(LoginRequiredMixin, DeleteView):
    model         = Portfolio
    template_name = "sandbox/portfolio_delete_form.html"
    success_url   = reverse_lazy("portfoliolist")
""" -------------- """

