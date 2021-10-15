from django.urls import path, include
from .           import views


urlpatterns = [
  path("",        views.home,                          name="home"),
  path("about/",  views.home,                          name="about"),
  path("signup/", views.signup_view,                   name="signup"),
  path("login/",  views.login_view,                    name="login"),
  path("logout/", views.logout_view,                   name="logout"),
  path("login/",  include("django.contrib.auth.urls"), name="login"),

  path("coin/table/",                       views.coin_table,              name="cointable"),
  path("coin/<slug:ticker>/",               views.coin_page,               name="coinpage"),
  path("transaction/create/<slug:ticker>/", views.transaction_create_view, name="transactioncreate"),
  path("<slug:ticker>",                     views.transaction_execute,     name="transactionexecute"),

  path("coin/list/",             views.CoinList.as_view(),        name="coinlist"),
  path("portfolio/list/",        views.PortfolioList.as_view(),   name="portfoliolist"),
  path("transaction/list/",      views.TransactionList.as_view(), name="transactionlist"),
  path("portfolio/create/",      views.PortfolioCreate.as_view(), name="portfoliocreate"),
  path("portfolio/update/<pk>/", views.PortfolioUpdate.as_view(), name="portfolioupdate"),
  path("portfolio/delete/<pk>/", views.PortfolioDelete.as_view(), name="portfoliodelete"),
]

