from datetime import datetime

from django.db                           import models
from django.db.models.fields             import CharField
from django_userforeignkey.models.fields import UserForeignKey

from polymorphic.models import PolymorphicModel


class Coin(PolymorphicModel):
    start_date    = models.DateTimeField(default=datetime(1970, 1, 1, 0, 0, 0))
    price_open    = models.FloatField(default=0.0)
    price_high    = models.FloatField(default=0.0)
    price_low     = models.FloatField(default=0.0)
    price_close   = models.FloatField(default=0.0)
    volume_traded = models.FloatField(default=0.0)
    trades_count  = models.IntegerField(default=0)
    ticker        = models.CharField(max_length=8)
    name          = models.CharField(max_length=30)
    count         = models.FloatField(default=0.0)

    def __str__(self):
        return self.name


class Portfolio(models.Model):
    nickname = CharField(max_length=20, unique=True)
    balance  = models.FloatField(default=0.0)
    owner    = UserForeignKey(auto_user_add=True)
    coins    = models.ManyToManyField(Coin, through="Transaction")

    def __str__(self):
        return self.nickname
    
    def get_absolute_url(self):
        return '/portfolio/list'


class Transaction(models.Model):
    time_executed = models.DateTimeField()
    coin_count    = models.FloatField(default=0.0)
    coin_cost     = models.FloatField(default=0.0)
    coin          = models.ForeignKey(Coin, on_delete=models.CASCADE)
    portfolio     = models.ForeignKey(Portfolio, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.coin.name} --> {self.portfolio.nickname}"


class Aave(Coin):
    __ticker__ = "AAVE"
    __coinid__ = 1
    
    def __str__(self):
        return self.__ticker__


class Aragon(Coin):
    __ticker__ = "ANT"
    __coinid__ = 2
    
    def __str__(self):
        return self.__ticker__


class Augur(Coin):
    __ticker__ = "REP"
    __coinid__ = 3

    def __str__(self):
        return self.__ticker__


class Balancer(Coin):
    __ticker__ = "BAL"
    __coinid__ = 4

    def __str__(self):
        return self.__ticker__


class Bitcoin(Coin):
    __ticker__ = "BTC"
    __coinid__ = 5

    def __str__(self):
        return self.__ticker__


class Cardano(Coin):
    __ticker__ = "ADA"
    __coinid__ = 6

    def __str__(self):
        return self.__ticker__


class Cosmos(Coin):
    __ticker__ = "ATOM"
    __coinid__ = 7

    def __str__(self):
        return self.__ticker__


class Ethereum(Coin):
    __ticker__ = "ETH"
    __coinid__ = 8

    def __str__(self):
        return self.__ticker__


class EthereumClassic(Coin):
    __ticker__ = "ETC"
    __coinid__ = 9

    def __str__(self):
        return self.__ticker__


class Orchid(Coin):
    __ticker__ = "OXT"
    __coinid__ = 10

    def __str__(self):
        return self.__ticker__


class Tether(Coin):
    __ticker__ = "USDT"
    __coinid__ = 11

    def __str__(self):
        return self.__ticker__


class Tezos(Coin):
    __ticker__ = "XTZ"
    __coinid__ = 12

    def __str__(self):
        return self.__ticker__

