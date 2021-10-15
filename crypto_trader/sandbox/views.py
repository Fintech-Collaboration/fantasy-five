from logging import makeLogRecord
import os
from pickle import MARK

import numpy as np

from datetime          import datetime
from plotly.offline    import plot
from plotly.graph_objs import Scatter
from pathlib           import Path

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
from django.db.models               import Q

from .utils.coin          import icon_path, get_coin_data

from .utils.algo_trading  import (
    dmac,
    ohlc_forecast,
    ml_classifier_apply,
    ml_booster_apply
)

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

    coin_data = list_coin_data()
    coin_icon = icon_path(ticker)

    context = {
        "ticker":    ticker.upper(),
        "coin_name": name,
        "coin_data": coin_data,
        "coin_icon": coin_icon,
    }
    return render(request, "sandbox/home.html", context)


def line_plotter(name: str, ticker: str):
    name  = "".join(name.split(" "))
    short = 50
    long  = 100

    coin_df = dmac(get_coin_data(name, ticker), short=short, long=long)
    x_data  = coin_df.index
    y_data  = coin_df["price_close"]

    y_short_data = coin_df["SMA_short"]
    y_long_data  = coin_df["SMA_long"]

    x_entry_data = coin_df[coin_df["entry_exit"] ==  1.0].index
    y_entry_data = coin_df[coin_df["entry_exit"] ==  1.0]["price_close"]
    x_exit_data  = coin_df[coin_df["entry_exit"] == -1.0].index
    y_exit_data  = coin_df[coin_df["entry_exit"] == -1.0]["price_close"]

    customdata = np.stack((
        coin_df['price_open'],    #0
        coin_df['price_high'],    #1
        coin_df['price_low'],     #2
        coin_df['volume_traded'], #3
        coin_df['trades_count'],  #4

    ), axis=-1)

    hovertemplate = """
    <b>%{x}<br>
    Daily Close:  $%{y:,6.2g}</b><br><br>
    Daily Open:   $%{customdata[0]:,6.2g}<br>
    Daily High:   $%{customdata[1]:,6.2g}<br>
    Daily Low:    $%{customdata[2]:,6.2g}<br>
    Daily Volume:  %{customdata[3]:,.0f}<br>
    Trade Count:   %{customdata[4]:,.0f}
    <extra></extra>
    """

    trace_data = Scatter(
        x=x_data,
        y=y_data,
        mode='lines',
        name=ticker.upper(),
        opacity=0.8,
        marker_color='green',
        customdata=customdata,
        hovertemplate=hovertemplate,
        legendrank=1,
        showlegend=False,
    )

    trace_short = Scatter(
        x=x_data,
        y=y_short_data,
        mode='lines',
        name=f"{short} Day SMA",
        opacity=0.5,
        marker_color='blue',
        customdata=customdata,
        hovertemplate=hovertemplate,
        legendgroup="sma-lines",
        legendgrouptitle_text="Simple Moving Avgs",
        legendrank=2,
    )

    trace_long = Scatter(
        x=x_data,
        y=y_long_data,
        mode='lines',
        name=f"{long} Day SMA",
        opacity=0.5,
        marker_color='orange',
        customdata=customdata,
        hovertemplate=hovertemplate,
        legendgroup="sma-lines",
        legendrank=3,
    )

    trace_entry = Scatter(
        x=x_entry_data,
        y=y_entry_data,
        mode='markers',
        name="Entry Point",
        opacity=0.8,
        marker_color='purple',
        marker_symbol="triangle-up",
        marker_size=10,
        customdata=customdata,
        hovertemplate=hovertemplate,
        legendgroup="entry_exit-point",
        legendgrouptitle_text="SMA Entry/Exit",
        visible="legendonly",
        legendrank=4,
    )

    trace_exit = Scatter(
        x=x_exit_data,
        y=y_exit_data,
        mode='markers',
        name="Exit Point",
        opacity=0.8,
        marker_color='red',
        marker_symbol="triangle-down",
        marker_size=10,
        customdata=customdata,
        hovertemplate=hovertemplate,
        legendgroup="entry_exit-point",
        visible="legendonly",
        legendrank=5,
    )

    plt = plot(
        [trace_data, trace_short, trace_long, trace_entry, trace_exit],
        output_type="div",
    )

    return plt


def forecast_plotter(name: str, ticker: str, col: str):
    name  = "".join(name.split(" "))
    df_forecast, df = ohlc_forecast(name, ticker, col)

    trace_name = " ".join([s.capitalize() for s in f"{col}".split("_")])

    x_data            = df_forecast["ds"]
    y_data_y          = df["y"]
    y_data_yhat       = df_forecast["yhat"]
    y_data_upper_band = df_forecast['yhat_upper']
    y_data_lower_band = df_forecast['yhat_lower']


    trace_y = Scatter(
        x=x_data,
        y=y_data_y,
        mode='markers',
        name=trace_name,
        marker_color='#FFBAD2',
        marker=dict(
            line=dict(width=1)
        ),
        legendrank=1,
    )

    trace_yhat = Scatter(
    x=x_data,
    y=y_data_yhat,
    mode='lines',
    name='Trend',
    marker_color="red",
    marker=dict(
        line=dict(width=1)
    ),
    legendrank=2,
    )

    trace_upper_band = Scatter(
        x=x_data,
        y=y_data_upper_band,
        mode='lines',
        name='Upper Band',
        marker_color='#57b88f',
        fill='tonexty',
        legendrank=3,
    )

    trace_lower_band = Scatter(
        x=x_data,
        y=y_data_lower_band,
        name='Lower Band',
        mode='lines',
        marker_color='#1705ff',
        legendrank=4,
    )

    # trace_actual = Scatter(
    #     name='Actual price',
    #     mode='markers',
    #     x=list(df0['ds']),
    #     y=list(df0['y']),
    #     marker=dict(
    #         color='black',
    #         line=dict(width=2)
    #     )
    # )

    plt = plot(
        [trace_lower_band, trace_upper_band, trace_y, trace_yhat],
        output_type="div",
    )

    return plt


def ml_plotter(model_func, name: str, ticker: str):
    name       = "".join(name.split(" "))
    market_cap = {
        "lowcap":  {"type": "Low-Cap",  "color": "red"},
        "midcap":  {"type": "Mid-Cap",  "color": "orange"},
        "highcap": {"type": "High-Cap", "color": "blue"},
    }

    pred_df = {}
    traces  = []
    for key, val in market_cap.items():
        pred_df[key] = model_func(
            model=model_func.__str__(),
            name=name,
            ticker=ticker,
            market_cap="".join(val["type"].split("-"))
        )

        # Plot the actual returns versus the strategy returns
        x_data_cum_prod          = pred_df[key].index
        y_data_cum_prod_actual   = (1 + pred_df[key]['Actual Returns'  ]).cumprod() - 1
        y_data_cum_prod_strategy = (1 + pred_df[key]['Strategy Returns']).cumprod() - 1

        traces.append(Scatter(
            x=x_data_cum_prod,
            y=y_data_cum_prod_strategy,
            name=f"Strategy Returns<br>{val['type']}",
            mode="lines",
            marker_color=val["color"],
            legendrank=1,
        ))

    traces.append(Scatter(
        x=x_data_cum_prod,
        y=y_data_cum_prod_actual,
        name="Actual Returns",
        mode="lines",
        marker_color="green",
        legendrank=0,
    ))

    plt = plot(
        traces,
        output_type="div",
    )

    return plt


def list_coin_data():
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

    return coin_data


""" WALLET METHODS """
def coin_table(request):
    coin_data = list_coin_data()
    context   = {"coin_data": coin_data}
        
    return render(request, "sandbox/coin_list.html", context)


def coin_page(request, ticker: str):
    try:
        coin = next(filter(lambda m: m.__ticker__.lower() == ticker.lower(), COIN_MODELS))
    except Coin.DoesNotExist:
        return Http404(f"Coin not found!")
    
    pull_func = lambda col: coin.objects.values_list(col, flat=True).order_by("-start_date")

    name = coin.objects.last().name.capitalize()
    coin_plot     = line_plotter(name, ticker)
    # forecast_plot = forecast_plotter(name, ticker, "price_close")
    ml_svc_plot   = ml_plotter(ml_classifier_apply, name, ticker)
    ml_boost_plot = ml_plotter(ml_booster_apply, name, ticker)

    context = dict(        
        ticker    = ticker,
        name      = name,
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
        coin_plot     = coin_plot,
        # forecast_plot = forecast_plot,
        ml_svc_plot   = ml_svc_plot,
        ml_boost_plot = ml_boost_plot,
    )

    return render(request, f"sandbox/coin_page.html", context)


@login_required(login_url="login")
def transaction_create_view(request, ticker: str):
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
def transaction_execute(request, ticker: str):
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

