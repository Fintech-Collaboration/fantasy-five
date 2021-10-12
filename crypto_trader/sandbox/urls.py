from django.urls         import path, include
from .                   import views
from django.contrib.auth import login, logout


urlpatterns = [
  path("",                       views.home,                          name="home"),
  path("signup/",                views.signup_view,                   name="signup"),
  path("login/",                 views.login_view,                    name="login"),
  path("logout/",                views.logout_view,                   name="logout"),
  path("login/",                 include("django.contrib.auth.urls"), name="login"),
  path("portfolio/list",         views.PortfolioList.as_view(),       name="portfoliolist"),
  path("coin/list",              views.CoinList.as_view(),            name="coinlist"),
  path("portfolio/create/",      views.PortfolioCreate.as_view(),     name="portfoliocreate"),
  path("portfolio/update/<pk>/", views.PortfolioUpdate.as_view(),     name="portfolioupdate"),
  path("portfolio/delete/<pk>/", views.PortfolioDelete.as_view(),     name="portfoliodelete"),

  path("coin/table",             views.coin_table,                    name="cointable"),
  path("coin/<slug:name>/",      views.coin_select,                   name="coinselect")
]

