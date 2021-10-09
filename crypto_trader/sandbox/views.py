import pandas as pd

from .config.coin import coin_references, icon_path

from django.urls                    import reverse_lazy
from django.shortcuts               import render
from django.views.generic           import ListView
from django.views.generic.edit      import CreateView, DeleteView, UpdateView

from .models import Owner, Portfolio

from pathlib           import Path
from plotly.offline    import plot
from plotly.graph_objs import Scatter


TEST_DATA = r"C:\Users\JasonGarcia24\FINTECH\workspace\fantasy-five\data\latest-quotes_data_ALL.csv"


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
        Path(TEST_DATA),
        index_col="last_updated",
        parse_dates=True,
        infer_datetime_format=True,
    )

    df_btc = df.loc[df["symbol"]==ticker]
    x_data = df_btc.index
    y_data = df_btc["quote.USD.price"]

    plt = plot([Scatter(
        x=x_data,
        y=y_data,
        mode='lines',
        name='BTC',
        opacity=0.8,
        marker_color='green',
    )],
    output_type='div')  

    return plt


class OwnerList(ListView):
  model = Owner


class PortfolioList(ListView):
  model = Portfolio


class OwnerCreate(CreateView):
  model         = Owner
  template_name = "sandbox/owner_create_form.html"
  fields        = ["username", "first_name", "last_name", "email"]
  success_url   = reverse_lazy("ownerlist")

class PortfolioCreate(CreateView):
  model         = Portfolio
  template_name = "sandbox/portfolio_create_form.html"
  fields        = ["coin_list", "investment", "balance", "owner"]
  success_url   = reverse_lazy("portfoliolist")


class OwnerUpdate(UpdateView):
  model         = Owner
  template_name = "sandbox/owner_update_form.html"
  fields        = ["username", "first_name", "last_name", "email"]


class PortfolioUpdate(UpdateView):
  model         = Portfolio
  template_name = "sandbox/portfolio_update_form.html"
  fields        = ["coin_list", "investment", "balance", "owner"]


class OwnerDelete(DeleteView):
  model         = Owner
  template_name = "sandbox/owner_delete_form.html"
  success_url   = reverse_lazy("ownerlist")


class PortfolioDelete(DeleteView):
  model         = Portfolio
  template_name = "sandbox/portfolio_delete_form.html"
  success_url   = reverse_lazy("portfoliolist")
  