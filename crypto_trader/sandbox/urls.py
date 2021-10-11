from django.urls         import path, include
from .                   import views
from django.contrib.auth import logout


urlpatterns = [
  path("",                       views.home,                          name="home"),
  path("signup/",                views.SignUp.as_view(),              name="signup"),
  path("logout/",                logout,                              name="logout"),
  path("account/",               include("django.contrib.auth.urls"), name="login"),
  path("owner/list",             views.OwnerList.as_view(),           name="ownerlist"),
  path("portfolio/list",         views.PortfolioList.as_view(),       name="portfoliolist"),
  path("coin/list",              views.CoinList.as_view(),            name="coinlist"),
  path("owner/create",           views.OwnerCreate.as_view(),         name="ownercreate"),
  path("portfolio/create/",      views.PortfolioCreate.as_view(),     name="portfoliocreate"),
  path("owner/update/<pk>/",     views.OwnerUpdate.as_view(),         name="ownerupdate"),
  path("portfolio/update/<pk>/", views.PortfolioUpdate.as_view(),     name="portfolioupdate"),
  path("owner/delete/<pk>/",     views.OwnerDelete.as_view(),         name="ownerdelete"),
  path("portfolio/delete/<pk>/", views.PortfolioDelete.as_view(),     name="portfoliodelete"),

  path("coin/table",             views.coin_table,                    name="cointable"),
  path("coin/<slug:name>/",      views.coin_select,                   name="coinselect")
]

